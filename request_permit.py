import argparse
import os
from datetime import datetime

import aiohttp
from login import login
from utils import *
from config import *
import asyncio
from dotenv import load_dotenv

async def send_request(session: aiohttp.ClientSession, url, court_id, ts1, ts2) -> bool:
    print("debug: sending request with court_id=", court_id, "ts1=", ts1, "ts2=", ts2)

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
    dt_str = None
    if dt_arg:
        try:
            dt_str = datetime.strptime(dt_arg, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid dt argument. Please use YYYY-MM-DD format.")
            return
    else:
        dt_str = PERMIT_REQUEST_DATE if PERMIT_REQUEST_DATE else get_date_from_input().strftime("%Y-%m-%d")
    return dt_str

        
async def main():
    print("=== Send Octagon Tennis permit request. ===")
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--dt", dest="dt", default="")
    args = parser.parse_args()

    dt_str=get_date_str(args)
    if not dt_str:
        print("No valid date provided. Exiting...")
        return
    
    async with aiohttp.ClientSession() as session:
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        await login(session, LOGIN_URL, email, password)

        h_start, h_end = PERMIT_REQUEST_WINDOW if PERMIT_REQUEST_WINDOW else get_time_window()
        court_names = PERMIT_REQUEST_COURTS if PERMIT_REQUEST_COURTS else None
        if not court_names:
            print("No courts specified for permit request. Please check config file. Exiting...")
            return

        for court_name in court_names:
            court_id = COURTS[court_name]
            for hh in range(h_start, h_end):
                permit_res = await send_request(session, PERMIT_REQUEST_URL, court_id, f"{dt_str}T{hh}:00:00", f"{dt_str}T{hh+1}:00:00")
                if permit_res:
                    print(f"Request sent successfully for {court_name} from {hh}:00 to {hh+1}:00.")
                    return

if __name__ == '__main__':
    asyncio.run(main())
