from datetime import datetime, timedelta, timezone


def get_time_diff_from_today(timestamp, datetime_format="%Y-%m-%dT%H:%M:%S%z", return_type="auto"):
    """Return the difference between the given timestamp and today's date."""
    if len(timestamp) < 12:
        timestamp += "T01:01:01+01:00"  #"2013-04-02T09:30:10+01:00"
    datetime_object = datetime.strptime(timestamp, datetime_format)
    datetime_object = datetime_object.replace(tzinfo=timezone.utc)
    if return_type == "seconds":
        _return = (datetime.now(timezone.utc) - datetime_object).seconds
        _return_type = "seconds"
    elif return_type == "minutes":
        _return = (datetime.now(timezone.utc) - datetime_object).seconds / 60
        _return_type = "minutes"
    elif return_type == "hours":
        _return = (datetime.now(timezone.utc) - datetime_object).seconds / 3600
        _return_type = "hours"
    elif return_type == "days":
        _return = (datetime.now(timezone.utc) - datetime_object).days
        _return_type = "days"
    elif return_type == "weeks":
        _return = (datetime.now(timezone.utc) - datetime_object).days / 7
        _return_type = "weeks"
    elif return_type == "months":
        _return = (datetime.now(timezone.utc) - datetime_object).days / 30
        _return_type = "months"
    elif return_type == "years":
        _return = (datetime.now(timezone.utc) - datetime_object).days / 365
        _return_type = "years"
    elif return_type == "auto":
        _return = (datetime.now(timezone.utc) - datetime_object).days
        _return_type = "days"
        if _return_type == "days" and _return > 14:
            _return = _return / 7
            _return_type = "weeks"
        if _return_type == "weeks" and _return > 4:
            _return = _return / 4
            _return_type = "months"
        if _return_type == "months" and _return > 12:
            _return = _return / 12
            _return_type = "years"
    else:
        _return = (datetime.now(timezone.utc) - datetime_object).days
        _return_type = "days"

    return str(int(_return)) + " " + _return_type
