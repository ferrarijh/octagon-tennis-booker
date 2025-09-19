import aiohttp
import constants
from login import login
from utils import *
import asyncio

async def send_request(session: aiohttp.ClientSession, url, court_id, ts1, ts2) -> bool:
    body = constants.PERMIT_REQUEST_BODY_TEMPLATE.copy()
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
        
def get_court_name() -> str:
    while True:
        court_number = input(f"Court number(1-6) to request (ex. \"1\"): ").strip()
        court_name = f"court{court_number}"
        if court_name in constants.COURTS:
            return court_name
        else:
            print("Invalid court number! Please try again.")
        
async def main():
    print("=== Send Octagon Tennis permit request. ===")
    async with aiohttp.ClientSession() as session:
        await login(session, constants.LOGIN_URL)

        dt_str = get_date().strftime("%Y-%m-%d")
        t_start = get_time("Start time to request in HH fmt (e.g. \"17\" for 5 PM): ")
        court_id = constants.COURTS[get_court_name()]

        await send_request(session, constants.PERMIT_REQUEST_URL, court_id, f"{dt_str}T{t_start}:00:00", f"{dt_str}T{t_start+1}:00:00")

if __name__ == '__main__':
    asyncio.run(main())