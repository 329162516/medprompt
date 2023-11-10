
import json
from src.medprompt import *

def test_fhir_condition_v1(f):
    fhir_obs = '''
{
    "resourceType": "Condition",
    "id": "f202",
    "meta": {
        "security": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "TBOO",
                "display": "taboo"
            }
        ]
    },
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved"
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed"
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis"
                }
            ]
        }
    ],
    "severity": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "24484000",
                "display": "Severe"
            }
        ]
    },
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "363346000",
                "display": "Malignant neoplastic disease"
            }
        ]
    },
    "bodySite": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "361355005",
                    "display": "Entire head and neck"
                }
            ]
        }
    ],
    "subject": {
        "reference": "Patient/f201",
        "display": "Roel"
    },
    "onsetAge": {
        "value": 52,
        "unit": "years",
        "system": "http://unitsofmeasure.org",
        "code": "a"
    },
    "abatementAge": {
        "value": 54,
        "unit": "years",
        "system": "http://unitsofmeasure.org",
        "code": "a"
    },
    "recordedDate": "2013-04-02T09:30:10+01:00",
    "evidence": [
        {
            "reference": {
                "reference": "DiagnosticReport/f201",
                "display": "Erasmus' diagnostic report of Roel's tumor"
            }
        }
    ]
}
'''
    f.set_template(
        template_name="condition_v1.jinja")
    input_object = json.loads(fhir_obs)
    input_object["time_diff"] = get_time_diff_from_today
    input_object["datetime_format"] = "%Y-%m-%dT%H:%M:%S%z"
    prompt = f.generate_prompt(input_object)
    print (prompt)
    assert prompt is not None