[RIOC's court reservation system](https://rioc.civicpermits.com/) sucks! With this project, you can (1) check court availability, (2) and make reservation for a court in a time slot.

### Check RIOC Policy before booking!

- Reservations are required and can only be made two days in advance.
- Reservations can be submitted Monday through Friday between 8AM and 4PM, and requests submitted outside of these times will be canceled, according to [RIOC website](https://rioc.ny.gov/399/Tennis-Information).
- Check their website for the latest policy update:  https://rioc.ny.gov/399/Tennis-Information

# How to use
### 1. Install required packages

Install python 3.10 or higher, then run:
```
pip install -r requirements.txt
```

### 2. Check court availability

- Make sure you created [RIOC website](https://rioc.civicpermits.com/Account/Login) account.

Commandline usage example:
```bash
(base) ➜  octagon_tennis_booker git:(main) ✗ python -m check_avail
=== Check RIOC's Octagon Tennis courts availability. ===
Email (default is ferrarijm9@gmail.com): 
Password: 
Login successful.
(Optional) Date to check in YYYY-MM-DD fmt (Defaults to 2 days after today): 2025-09-14
(Optional) Time window to check in HH HH fmt (Ex. "08 22". Defaults to 17 22): 08 22
Checking court1's availability...
Checking court2's availability...
Checking court3's availability...
Checking court4's availability...
Checking court5's availability...
Checking court6's availability...
=== Available court slots found. Check the following list! ===
court: court4, slot: ('2025-09-14T08:00:00', '2025-09-14T09:00:00')
```

### 3. Issue permit request

Commandline usage example:
```bash
(base) ➜  octagon_tennis_booker git:(main) ✗ python -m request_permit
=== Send Octagon Tennis permit request. ===
Email (default is ferrarijm9@gmail.com): ferrarijm@naver.com
Password: 
Login successful.
(Optional) Date to check in YYYY-MM-DD fmt (Defaults to 2 days after today):
Start time of 1h time slot to request in HH fmt (e.g. "17" for 5 PM): 11
Court number(1-6) to request (ex. "1"): 6
Successfully sent permit request!
Check your permits at: https://rioc.civicpermits.com/
```