
import json
from src.medprompt import *

def test_fhir_procedure_v1(f):
    fhir_obs = '''
{
    "resourceType": "Procedure",
    "id": "example",
    "status": "completed",
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "80146002",
                "display": "Appendectomy (Procedure)"
            }
        ],
        "text": "Appendectomy"
    },
    "subject": {
        "reference": "Patient/example"
    },
    "performedDateTime": "2013-04-02T09:30:10+01:00",
    "recorder": {
        "reference": "Practitioner/example",
        "display": "Dr Cecil Surgeon"
    },
    "asserter": {
        "reference": "Practitioner/example",
        "display": "Dr Cecil Surgeon"
    },
    "performer": [
        {
            "actor": {
                "reference": "Practitioner/example",
                "display": "Dr Cecil Surgeon"
            }
        }
    ],
    "reasonCode": [
        {
            "text": "Generalized abdominal pain 24 hours. Localized in RIF with rebound and guarding"
        }
    ],
    "followUp": [
        {
            "text": "ROS 5 days  - 2013-04-10"
        }
    ],
    "note": [
        {
            "text": "Routine Appendectomy. Appendix was inflamed and in retro-caecal position"
        }
    ]
}
'''
    f.set_template(
        template_name="procedure_v1.jinja")
    input_object = json.loads(fhir_obs)
    input_object["time_diff"] = get_time_diff_from_today
    prompt = f.generate_prompt(input_object)
    print (prompt)
    assert prompt is not None