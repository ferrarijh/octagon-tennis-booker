import argparse
import logging
import os
from datetime import datetime, timedelta

import aiohttp
from login import login
from utils import setup_logging, get_hourly_slots_ts
from configs.config import *
import asyncio
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

async def send_request(
        session: aiohttp.ClientSession,
        url: str, court_id: str, ts1: str, ts2: str) -> bool:

    body = PERMIT_REQUEST_BODY_TEMPLATE.copy()
    body["Events"][0]["FacilityIds"] = [court_id]
    body["Events"][0]["Dates"] = [
        {
            "Start": ts1,
            "Stop": ts2,
        }
    ]
    async with session.post(url, json=body) as resp:
        if resp.status == 200:
            return True
        else:
            logger.error("Request failed: status=[%s], body=%s", resp.status, await resp.text())
            return False
        
def get_date_strs(args: argparse.Namespace) -> list[str]|None:
    dt_arg = args.dt.strip()
    if dt_arg:
        try:
            return [datetime.strptime(dt_arg, "%Y-%m-%d").strftime("%Y-%m-%d")]
        except ValueError:
            logger.error("Invalid dt argument. Please use YYYY-MM-DD format.")
            return None
    if PERMIT_REQUEST_DATE:
        return [PERMIT_REQUEST_DATE]

    today = datetime.now()
    # Requests are normally sent 2 days ahead, but on Fridays we also cover
    # Sat/Sun when this script doesn't run, so request Sun/Mon/Tue as well.
    days_ahead = (2, 3, 4) if today.strftime("%a").upper() == FRI else (2,)
    return [(today + timedelta(days=d)).strftime("%Y-%m-%d") for d in days_ahead]


async def book_date(session: aiohttp.ClientSession, dt_str: str, court_names: list[str]) -> None:
    day = datetime.strptime(dt_str, "%Y-%m-%d").strftime("%a").upper()
    hh_starts = [hh for hh in PERMIT_REQUEST_HOURS[day]]

    for court_name in court_names:
        court_id = COURTS[court_name]
        for hh in hh_starts:
            ts_start = f"{dt_str}T{hh:02d}:00:00"
            ts_end = f"{dt_str}T{hh+1:02d}:00:00"
            logger.info("Sending request with court=%s, ts1=%s, ts2=%s...", court_name, ts_start, ts_end)
            permit_res = await send_request(session, PERMIT_REQUEST_URL, court_id, ts_start, ts_end)
            if permit_res:
                logger.info("Permit request sent for %s from %s to %s. Check: https://rioc.civicpermits.com/", court_name, ts_start, ts_end)
                return


async def main():
    setup_logging()
    logger.info("=== Send Octagon Tennis permit request. ===")
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--dt", dest="dt", default="")
    parser.add_argument("--phase", choices=["dev", "prod"], default="dev")
    args = parser.parse_args()

    dt_strs = get_date_strs(args)
    if not dt_strs:
        raise ValueError("No valid date provided.")

    async with aiohttp.ClientSession() as session:
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        await login(session, LOGIN_URL, email, password)

        court_names = PERMIT_REQUEST_COURTS if PERMIT_REQUEST_COURTS else None
        if not court_names:
            logger.error("No courts specified for permit request. Please check config file. Exiting...")
            return

        await asyncio.gather(*(book_date(session, dt_str, court_names) for dt_str in dt_strs))

if __name__ == '__main__':
    asyncio.run(main())
