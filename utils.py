import asyncio
import logging
import sys
from datetime import date, timedelta, datetime
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

import aiohttp

logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )


def get_hourly_slots_ts(dt: date, h_start: int, h_end: int) -> list[tuple[str, str]]:
    formatted = dt.strftime("%Y-%m-%d")
    slots = []
    for hour in range(h_start, h_end):
        h_start = f"{formatted}T{hour:02d}:00:00"
        h_end = f"{formatted}T{hour+1:02d}:00:00"
        slots.append((h_start, h_end))
    return slots

async def get_server_datetime(session: aiohttp.ClientSession, url: str, tz: str = "America/New_York") -> datetime:
    async with session.head(url) as resp:
        date_header = resp.headers.get("Date")
    if not date_header:
        raise RuntimeError(f"Server response from {url} has no Date header.")
    return parsedate_to_datetime(date_header).astimezone(ZoneInfo(tz))


async def wait_for_reservation_window(
    session: aiohttp.ClientSession,
    url: str,
    window_start_hour: int = 8,
    window_end_hour: int = 16,
    poll_interval: float = 1.0,
    max_wait: float = 180.0,
    tz: str = "America/New_York",
) -> bool:
    """Poll the server's Date header until its local time falls within
    [window_start_hour, window_end_hour) on a weekday, to avoid submitting
    a request a few seconds early/late due to clock skew with the Mac."""
    wait_started_at = None
    elapsed = 0.0
    while True:
        now = await get_server_datetime(session, url, tz=tz)
        now_str = now.strftime("%Y-%m-%d %H:%M:%S %Z")

        if now.weekday() < 5 and window_start_hour <= now.hour < window_end_hour:
            if wait_started_at is not None:
                logger.info(
                    "Reservation window opened. Waited %.0fs (started waiting at %s, server time now %s).",
                    elapsed, wait_started_at.strftime("%Y-%m-%d %H:%M:%S %Z"), now_str,
                )
            return True

        if now.weekday() >= 5 or now.hour >= window_end_hour:
            logger.error(
                "Server time %s is outside the reservation window (%02d:00-%02d:00, Mon-Fri). Aborting.",
                now_str, window_start_hour, window_end_hour,
            )
            return False

        if elapsed >= max_wait:
            logger.error(
                "Timed out after %.0fs waiting for reservation window to open (started waiting at %s, server time now %s). Aborting.",
                max_wait, wait_started_at.strftime("%Y-%m-%d %H:%M:%S %Z"), now_str,
            )
            return False

        if wait_started_at is None:
            wait_started_at = now

        await asyncio.sleep(poll_interval)
        elapsed += poll_interval


def get_date_from_input() -> date:
    while True:
        date_str = input("(Optional) Date in YYYY-MM-DD fmt (Defaults to 2 days after today): ").strip()
        if not date_str:
            return date.today() + timedelta(days=2)
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").date()
            if dt < date.today():
                logger.warning("Date cannot be in the past! Please try again.")
                continue
            return dt
        except ValueError:
            logger.warning("Invalid date! Please try again.")

def get_time_window() -> tuple[int, int]:
    while True:
        input_str = input("(Optional) Time window to check in HH HH fmt (Ex. \"08 22\". Defaults to 17 22): ").strip()
        if not input_str:
            return 17, 22
        try:
            parts = input_str.split()
            if len(parts) != 2:
                logger.warning("Invalid format! Please use HH HH format.")
                continue
            t1, t2 = (int(parts[0]), int(parts[1]))
            if 0 <= t1 < 24 and 0 <= t2 < 24 and t1 < t2:
                return t1, t2
            else:
                logger.warning("Invalid time range! Please try again.")
        except ValueError:
            logger.warning("Invalid format! Please use HH HH format.")
