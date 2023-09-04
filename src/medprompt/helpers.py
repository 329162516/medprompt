from datetime import datetime, timedelta, timezone


def get_time_diff_from_today(timestamp):
    """Return the difference between the given timestamp and today's date."""
    datetime_format = "%Y-%m-%dT%H:%M:%S%z"
    datetime_object = datetime.strptime(timestamp, datetime_format)
    return (datetime.now(timezone.utc) - datetime_object).days
