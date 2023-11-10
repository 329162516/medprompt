from datetime import datetime, timedelta, timezone


def get_time_diff_from_today(timestamp, datetime_format="%Y-%m-%dT%H:%M:%S%z"):
    """Return the difference between the given timestamp and today's date."""
    if len(timestamp) < 12:
        timestamp += "T01:01:01+01:00"  #"2013-04-02T09:30:10+01:00"
    datetime_object = datetime.strptime(timestamp, datetime_format)
    datetime_object = datetime_object.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - datetime_object).days
