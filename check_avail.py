import aiohttp
import asyncio
from constants import *
from login import login
from utils import *

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
            print(f"Unknown response: status=[{resp.status}], body={resp_body}")
            raise RuntimeError(f"Unknown response: status=[{resp.status}], body={resp_body}")

async def main():
    print("=== Check RIOC's Octagon Tennis courts availability. ===")

    async with aiohttp.ClientSession() as session:

        await login(session, LOGIN_URL)

        dt = get_date()
        t1, t2 = get_time_window()

        # build tasks for all courts and slots
        tasks = []
        available_court_slots = {}
        for court_name, court_id in COURTS.items():
            print(f"Checking {court_name}'s availability...")
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
                        # print(f"[{court_name}] Available: {start_ts} to {end_ts}")
                        if not available_court_slots.get(court_name):
                            available_court_slots[court_name] = []
                        available_court_slots[court_name].append((start_ts, end_ts))
                    # else:
                    #     print(f"[{court_name}] Not available: {start_ts} to {end_ts}")
                except RuntimeError as e:
                    print(f"[{court_name}] Error for slot {start_ts}-{end_ts}: {e}")
            tasks.clear()

        # gather results

        if not available_court_slots:
            print("No available courts found.")
        else:
            print("=== Available court slots found. Check the following list! ===")
            for court, slots in available_court_slots.items():
                for slot in slots:
                    print(f"court: {court}, slot: {slot}")

if __name__ == "__main__":
    asyncio.run(main())
