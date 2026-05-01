import logging
import sys
from datetime import date, timedelta, datetime

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
