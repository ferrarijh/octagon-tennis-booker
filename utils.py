from datetime import date, timedelta, datetime

def get_hourly_slots_ts(dt: date, h_start: int, h_end: int) -> list[tuple[str, str]]:
    formatted = dt.strftime("%Y-%m-%d")
    slots = []
    for hour in range(h_start, h_end):
        h_start = f"{formatted}T{hour:02d}:00:00"
        h_end = f"{formatted}T{hour+1:02d}:00:00"
        slots.append((h_start, h_end))
    return slots

def get_date() -> date:
    while True:
        date_str = input("(Optional) Date to check in YYYY-MM-DD fmt (Defaults to 2 days after today): ").strip()
        if not date_str:
            return date.today() + timedelta(days=2)
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").date()
            if dt < date.today():
                print("Date cannot be in the past! Please try again.")
                continue
            return dt
        except ValueError:
            print("Invalid date! Please try again.")

def get_time_window() -> tuple[int, int]:
    while True:
        input_str = input("(Optional) Time window to check in HH HH fmt (Ex. \"08 22\". Defaults to 17 22): ").strip()
        if not input_str:
            return 17, 22
        try:
            parts = input_str.split()
            if len(parts) != 2:
                print("Invalid format! Please use HH HH format.")
                continue
            t1, t2 = (int(parts[0]), int(parts[1]))
            if 0 <= t1 < 24 and 0 <= t2 < 24 and t1 < t2:
                return t1, t2
            else:
                print("Invalid time range! Please try again.")
        except ValueError:
            print("Invalid format! Please use HH HH format.")

def get_time(msg: str) -> int:
    while True:
        time_str = input(msg).strip()
        try:
            t = int(time_str)
            if 0 <= t < 24:
                return t
            else:
                print("Invalid hour! Please try again.")
        except ValueError:
            print("Invalid format! Please enter an integer hour.")