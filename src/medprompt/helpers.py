from datetime import datetime, timedelta, timezone
from typing import List
import base64
import pypdf
from striprtf.striprtf import rtf_to_text

def get_time_diff_from_today(timestamp, datetime_format="%Y-%m-%dT%H:%M:%S%z", return_type="auto"):
    """Return the difference between the given timestamp and today's date."""
    try:
        datetime_object = datetime.strptime(timestamp, datetime_format)
    except:
        return "some time ago"
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

def process_document_reference(content: List):
    _data = ""
    for _item in content:
        item = _item["attachment"]
        _decoded_data = base64.b64decode(
            item["data"]).decode('utf-8', errors='ignore')
        if item["contentType"] == "application/pdf":
            _pdf_file = open(_decoded_data, 'rb')
            _pdfReader = pypdf.PdfReader(_pdf_file)
            for _page in _pdfReader.pages:
                _text += _page.extract_text()
            for _line in str(_text).split("\n"):
                if (_line.strip()):
                    _line = _line.replace('|', " ")
                    _data = _data + _line + "\n"
        #* TODO: handle other formats
        if item["contentType"] == "application/rtf":
            _text = rtf_to_text(_decoded_data, errors='ignore')
            _data = ""
            for line in str(_text).split("\n"):
                if (line.strip()):
                    line = line.replace('|', " ")
                    _data = _data + line + "\n"
    return _data
