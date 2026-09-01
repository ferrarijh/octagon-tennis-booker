import argparse
import unittest
from datetime import datetime
from unittest.mock import patch

import request_permit


def _args(dt: str = "") -> argparse.Namespace:
    return argparse.Namespace(dt=dt)


class FixedDatetime(datetime):
    """datetime subclass whose now() is pinned, used to control "today" in tests."""

    _fixed_now: datetime

    @classmethod
    def now(cls, tz=None):
        return cls._fixed_now


def fixed_datetime(fixed_now: datetime) -> type[FixedDatetime]:
    return type("FixedDatetime", (FixedDatetime,), {"_fixed_now": fixed_now})


class GetDateStrsTest(unittest.TestCase):
    def test_explicit_dt_arg_returns_single_date(self):
        result = request_permit.get_date_strs(_args("2026-09-15"))
        self.assertEqual(result, ["2026-09-15"])

    def test_invalid_dt_arg_returns_none(self):
        result = request_permit.get_date_strs(_args("not-a-date"))
        self.assertIsNone(result)

    def test_dt_arg_takes_priority_over_permit_request_date(self):
        with patch.object(request_permit, "PERMIT_REQUEST_DATE", "2026-01-01"):
            result = request_permit.get_date_strs(_args("2026-09-15"))
        self.assertEqual(result, ["2026-09-15"])

    def test_permit_request_date_override_returns_single_date(self):
        with patch.object(request_permit, "PERMIT_REQUEST_DATE", "2026-01-01"):
            result = request_permit.get_date_strs(_args(""))
        self.assertEqual(result, ["2026-01-01"])

    def test_friday_returns_sunday_monday_tuesday(self):
        friday = datetime(2026, 9, 4)  # a Friday
        with patch.object(request_permit, "PERMIT_REQUEST_DATE", None), \
             patch.object(request_permit, "datetime", fixed_datetime(friday)):
            result = request_permit.get_date_strs(_args(""))
        self.assertEqual(result, ["2026-09-06", "2026-09-07", "2026-09-08"])

    def test_non_friday_returns_single_date_two_days_ahead(self):
        monday = datetime(2026, 9, 7)  # a Monday
        with patch.object(request_permit, "PERMIT_REQUEST_DATE", None), \
             patch.object(request_permit, "datetime", fixed_datetime(monday)):
            result = request_permit.get_date_strs(_args(""))
        self.assertEqual(result, ["2026-09-09"])


if __name__ == "__main__":
    unittest.main()
