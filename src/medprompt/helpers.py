"""
 Copyright 2023 Bell Eapen

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


import base64
import logging
from datetime import datetime, timezone
from typing import List

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

def process_document_reference(content: List) -> str:
    """Process document reference.

    Args:
        content (List): List of document references

    Returns:
        str: Processed document content
    """
    _data = ""
    try:
        for _item in content:
            item = _item["attachment"]
            _decoded_data = base64.b64decode(
                item["data"]).decode('utf-8', errors='ignore')

            if item["contentType"] == "application/rtf":
                try:
                    _text = rtf_to_text(_decoded_data, errors='ignore')
                    _data = ""
                    for line in str(_text).split("\n"):
                        if (line.strip()):
                            line = line.replace('|', " ")
                            _data = _data + line + "\n"
                except:
                    logging.debug("Error in parsing RTF file.")

            # content may have both types. Parse pdf last
            if item["contentType"] == "application/pdf" and _data == "":
                try:
                    _pdf_file = open(_decoded_data, 'rb')
                    _pdfReader = pypdf.PdfReader(_pdf_file)
                    for _page in _pdfReader.pages:
                        _text += _page.extract_text()
                    for _line in str(_text).split("\n"):
                        if (_line.strip()):
                            _line = _line.replace('|', " ")
                            _data = _data + _line + "\n"
                except:
                    logging.debug("Error in parsing PDF file.")
    except:
        logging.debug("Error in parsing document reference.")
    return _data
