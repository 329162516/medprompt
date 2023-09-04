
import json
from src.medprompt import *

def test_fhir_observation_v1(f):
    fhir_obs = '''
{
    "resourceType": "Observation",
    "id": "f001",
    "identifier": [
        {
            "use": "official",
            "system": "http://www.bmc.nl/zorgportal/identifiers/observations",
            "value": "6323"
        }
    ],
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "15074-8",
                "display": "Glucose [Moles/volume] in Blood"
            }
        ]
    },
    "subject": {
        "reference": "Patient/f001",
        "display": "P. van de Heuvel"
    },
    "effectiveDateTime": "2013-04-02T09:30:10+01:00",
    "issued": "2013-04-03T15:30:10+01:00",
    "performer": [
        {
            "reference": "Practitioner/f005",
            "display": "A. Langeveld"
        }
    ],
    "valueQuantity": {
        "value": 6.3,
        "unit": "mmol/l",
        "system": "http://unitsofmeasure.org",
        "code": "mmol/L"
    },
    "interpretation": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                    "code": "H",
                    "display": "High"
                }
            ]
        }
    ],
    "referenceRange": [
        {
            "low": {
                "value": 3.1,
                "unit": "mmol/l",
                "system": "http://unitsofmeasure.org",
                "code": "mmol/L"
            },
            "high": {
                "value": 6.2,
                "unit": "mmol/l",
                "system": "http://unitsofmeasure.org",
                "code": "mmol/L"
            }
        }
    ]
}
'''
    f.set_template(
        template_name="observation_v1.jinja")
    input_object = json.loads(fhir_obs)
    input_object["time_diff"] = get_time_diff_from_today
    prompt = f.generate_prompt(input_object)
    print (prompt)
    assert prompt is not None