
import json
from src.medprompt import *

def test_fhir_documentreference_v1(f):
    fhir_obs = '''
{
  "author": [
    {
      "display": "PROVIDER, TEST",
      "identifier": {
        "system": "http://somesite.com/systemid/epic/perid",
        "value": "12345678"
      },
      "type": "Practitioner"
    }
  ],
  "category": [
    {
      "coding": [
        {
          "code": "clinical-note",
          "display": "Clinical Note",
          "system": "http://hl7.org/fhir/us/core/CodeSystem/us-core-documentreference-category"
        }
      ],
      "text": "Clinical Note"
    }
  ],
  "content": [
    {
      "attachment": {
        "contentType": "application/rtf",
        "data": ""
      }
    }
    ],
    "context": {
    "encounter": [
      {
        "identifier": {
          "system": "http://somesite.com/systemid/epic/csn",
          "value": "2000002094411"
        },
        "type": "Encounter"
      }
    ],
    "practiceSetting": {
      "coding": [
        {
          "code": "NEU",
          "display": "NEU (Neurology)",
          "system": "http://somesite.com/codesystem/EPIC_CLINICAL_SVC_CODE"
        }
      ],
      "text": "NEU (Neurology)"
    }
  },
  "date": "2022-04-12T15:00:00.000+00:00",
  "description": "NEU (Neurology) H&P",
  "docStatus": "final",
  "id": "98f946df-c600-432d-8827-12893546dc16",
  "identifier": [
    {
      "system": "http://somesite.com/systemid/epic/document_id",
      "type": {
        "coding": [
          {
            "code": "documentReference",
            "display": "DocumentReference",
            "system": "http://somesite.com/systemid/gdr/assigned_identifier"
          }
        ],
        "text": "DocumentReference"
      },
      "use": "usual",
      "value": "20012383"
    }
  ],
  "meta": {
    "lastUpdated": "2022-05-17T06:54:21.306721-05:00",
    "source": "http://somesite.com/systemid/gdr/datasource/epic",
    "versionId": "MTY1Mjc4ODQ2MTMwNjcyMTAwMA"
  },
  "resourceType": "DocumentReference",
  "status": "current",
  "subject": {
    "reference": "Patient/11324ddd-7212-45b6-a98c-0a75cb472f59"
  },
  "type": {
    "coding": [
      {
        "code": "H&P",
        "display": "H&P",
        "system": "http://somesite.com/codesystem/EPIC_NOTE_TYPE_CODE"
      }
    ],
    "text": "H&P"
  }
}

'''
    f.set_template(
        template_name="documentreference_v1.jinja")
    input_object = json.loads(fhir_obs)
    input_object["time_diff"] = get_time_diff_from_today
    input_object["process_document"] = process_document_reference
    prompt = f.generate_prompt(input_object)
    print (prompt)
    assert prompt is not None