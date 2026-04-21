import os

import aiohttp
from login import login
from utils import *
from config import *
import asyncio
from dotenv import load_dotenv

async def send_request(session: aiohttp.ClientSession, url, court_id, ts1, ts2) -> bool:
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
        
async def main():
    print("=== Send Octagon Tennis permit request. ===")
    load_dotenv()
    
    async with aiohttp.ClientSession() as session:
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        await login(session, LOGIN_URL, email, password)

        dt_str = PERMIT_REQUEST_DATE if PERMIT_REQUEST_DATE else get_date().strftime("%Y-%m-%d")
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