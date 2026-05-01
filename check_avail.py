import logging
import os

import aiohttp
import asyncio

from dotenv import load_dotenv
from configs.config import *
from login import login
from utils import setup_logging, get_date_from_input, get_time_window, get_hourly_slots_ts

logger = logging.getLogger(__name__)

async def check_avail(session: aiohttp.ClientSession, court_id: str, start_ts: str, end_ts: str) -> bool:
    body = {
        "FacilityNames": ["Tennis Courts"],
        "FacilityIds": [court_id],
        "Dates": [
            {
                "Start": start_ts,
                "Stop": end_ts,
            }
        ],
    }

    async with session.post(CHECK_AVAIL_URL, json=body) as resp:
        resp_body = await resp.text()

        if resp_body == "[]":
            return True
        elif resp_body == "[0]":
            return False
        else:
            logger.error("Unknown response: status=[%s], body=%s", resp.status, resp_body)
            raise RuntimeError(f"Unknown response: status=[{resp.status}], body={resp_body}")

async def main():
    setup_logging()
    logger.info("=== Check RIOC's Octagon Tennis courts availability. ===")

    async with aiohttp.ClientSession() as session:
        load_dotenv()
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

        await login(session, LOGIN_URL, email, password)

        dt = CHECK_AVAIL_DATE if CHECK_AVAIL_DATE else get_date_from_input()
        t1, t2 = CHECK_AVAIL_WINDOW if CHECK_AVAIL_WINDOW else get_time_window()

        # build tasks for all courts and slots
        tasks = []
        available_court_slots = {}
        for court_name, court_id in COURTS.items():
            logger.info("Checking %s's availability...", court_name)
            slots = get_hourly_slots_ts(dt, t1, t2)
            for start_ts, end_ts in slots:
                tasks.append(
                    (court_name, start_ts, end_ts,
                     asyncio.create_task(check_avail(session, court_id, start_ts, end_ts)))
                )
            for court_name, start_ts, end_ts, task in tasks:
                try:
                    is_avail = await task
                    if is_avail:
                        logger.info("[%s] Available: %s to %s", court_name, start_ts, end_ts)
                        if not available_court_slots.get(court_name):
                            available_court_slots[court_name] = []
                        available_court_slots[court_name].append((start_ts, end_ts))
                    else:
                        logger.info("[%s] Not available: %s to %s", court_name, start_ts, end_ts)
                except RuntimeError as e:
                    logger.error("[%s] Error for slot %s-%s: %s", court_name, start_ts, end_ts, e)
            tasks.clear()

        # gather results
        if not available_court_slots:
            logger.info("No available courts found.")
        else:
            logger.info("=== Available court slots found. Check the following list! ===")
            for court, slots in available_court_slots.items():
                for slot in slots:
                    logger.info("court: %s, slot: %s", court, slot)

if __name__ == "__main__":
    asyncio.run(main())
