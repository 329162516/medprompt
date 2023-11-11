from datetime import datetime, timedelta, timezone


def get_time_diff_from_today(timestamp, datetime_format="%Y-%m-%dT%H:%M:%S%z", return_type="days"):
    """Return the difference between the given timestamp and today's date."""
    if len(timestamp) < 12:
        timestamp += "T01:01:01+01:00"  #"2013-04-02T09:30:10+01:00"
    datetime_object = datetime.strptime(timestamp, datetime_format)
    datetime_object = datetime_object.replace(tzinfo=timezone.utc)
    if return_type == "seconds":
        return (datetime.now(timezone.utc) - datetime_object).seconds
    elif return_type == "minutes":
        return (datetime.now(timezone.utc) - datetime_object).seconds / 60
    elif return_type == "hours":
        return (datetime.now(timezone.utc) - datetime_object).seconds / 3600
    elif return_type == "days":
        return (datetime.now(timezone.utc) - datetime_object).days
    elif return_type == "weeks":
        return (datetime.now(timezone.utc) - datetime_object).days / 7
    elif return_type == "months":
        return (datetime.now(timezone.utc) - datetime_object).days / 30
    elif return_type == "years":
        return (datetime.now(timezone.utc) - datetime_object).days / 365
    else:
        return (datetime.now(timezone.utc) - datetime_object).days
