import argparse
import os
from datetime import datetime

import aiohttp
from login import login
from utils import *
from configs.config import *
import asyncio
from dotenv import load_dotenv

async def send_request(
        session: aiohttp.ClientSession, 
        url: str, court_id: str, ts1: str, ts2: str) -> bool:
    print(f"Sending request with court_id={court_id}, ts1={ts1}, ts2={ts2}...")

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
            print(f"Successfully sent permit request!")
            print(f"Check your permits at: https://rioc.civicpermits.com/")
            return True
        else:
            print(f"Request failed: status=[{resp.status}], body={await resp.text()}")
            return False
        
def get_date_str(args: argparse.Namespace) -> str|None:
    dt_arg = args.dt.strip()
    if dt_arg:
        try:
            return datetime.strptime(dt_arg, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid dt argument. Please use YYYY-MM-DD format.")
            return None
    else:
        date_p2d_str = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d") 
        return date_p2d_str if not PERMIT_REQUEST_DATE else PERMIT_REQUEST_DATE
        
async def main():
    print("=== Send Octagon Tennis permit request. ===")
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--dt", dest="dt", default="")
    parser.add_argument("--phase", choices=["dev", "prod"], default="dev")
    args = parser.parse_args()

    dt_str=get_date_str(args)
    if not dt_str:
        raise ValueError("No valid date provided.")
    
    async with aiohttp.ClientSession() as session:
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        await login(session, LOGIN_URL, email, password)

        court_names = PERMIT_REQUEST_COURTS if PERMIT_REQUEST_COURTS else None
        if not court_names:
            print("No courts specified for permit request. Please check config file. Exiting...")
            return

        day = datetime.strptime(dt_str, "%Y-%m-%d").strftime("%a").upper()
        hh_starts = [hh for hh in PERMIT_REQUEST_HOURS[day]]

        for court_name in court_names:
            court_id = COURTS[court_name]
            for hh in hh_starts:
                ts_start = f"{dt_str}T{hh:02d}:00:00"
                ts_end = f"{dt_str}T{hh+1:02d}:00:00"
                permit_res = await send_request(session, PERMIT_REQUEST_URL, court_id, ts_start, ts_end)
                if permit_res:
                    print(f"Request sent successfully for {court_name} from {ts_start} to {ts_end}.")
                    return

if __name__ == '__main__':
    asyncio.run(main())
