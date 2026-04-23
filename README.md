[RIOC's court reservation system](https://rioc.civicpermits.com/) sucks! With this project, you can (1) check court availability across all six Octagon courts, and (2) auto-issue permit requests against a configured set of preferred courts and time slots.

### Check RIOC Policy before booking!

- Reservations are required and can only be made two days in advance.
- Reservations can be submitted Monday through Friday between 8AM and 4PM, and requests submitted outside of these times will be canceled, according to [RIOC website](https://rioc.ny.gov/399/Tennis-Information).
- Check their website for the latest policy update: https://rioc.ny.gov/399/Tennis-Information

# Setup

### 1. Install required packages

Python 3.10 or higher.

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file

Make sure you have an account at [the RIOC website](https://rioc.civicpermits.com/Account/Login), then put your credentials in a `.env` file at the repo root (gitignored):

```
EMAIL=you@example.com
PASSWORD=your-password
```

### 3. Configure booking behavior in [config.py](config.py)

Both scripts are config-driven, not interactive. Edit [config.py](config.py) before running:

| Constant | Used by | Purpose |
|---|---|---|
| `CHECK_AVAIL_DATE` | `check_avail` | Pin the availability check to `"YYYY-MM-DD"`, or `None` to be prompted. |
| `CHECK_AVAIL_WINDOW` | `check_avail` | `(start_hour, end_hour)` window to scan, e.g. `(16, 22)`. |
| `PERMIT_REQUEST_DATE` | `request_permit` | Pin the request date, or `None` to default to two days from today. |
| `PERMIT_REQUEST_HOURS` | `request_permit` | Per-weekday tuple of preferred start hours, e.g. `FRI: (9, 10, 17, 18, 19)`. |
| `PERMIT_REQUEST_COURTS` | `request_permit` | Ordered list of court names to try, e.g. `["court1", "court2", ...]`. |

# Usage

### Check court availability

```bash
python -m check_avail
```

Logs each court × slot as available or not, then prints a summary of every available slot found.

### Issue a permit request

```bash
python -m request_permit                  # date defaults to 2 days from today (or PERMIT_REQUEST_DATE)
python -m request_permit --dt 2026-04-30  # override the date
```

For the resolved date, iterates `PERMIT_REQUEST_COURTS × PERMIT_REQUEST_HOURS[<weekday>]` and exits on the first successful request. Confirm the result at https://rioc.civicpermits.com/.

# Reference

[request_capture.md](request_capture.md) documents the captured RIOC API requests and responses (`/Permits/ConflictCheck`, `/Permits`) that this client is built against.
