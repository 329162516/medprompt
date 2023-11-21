
import json
from src.medprompt import *

def test_fhir_medicationrequest_v1(f):
    fhir_obs = '''
{
    "resourceType": "MedicationRequest",
    "id": "medrx002",
    "identifier": [
        {
            "use": "official",
            "system": "http://www.bmc.nl/portal/prescriptions",
            "value": "12345"
        }
    ],
    "status": "active",
    "intent": "order",
    "medicationReference": {
        "reference": "Medication/med0316",
        "display": "prescribed medication"
    },
    "subject": {
        "reference": "Patient/pat1",
        "display": "Donald Duck"
    },
    "encounter": {
        "reference": "Encounter/f001",
        "display": "encounter that leads to this prescription"
    },
    "authoredOn": "2015-03-01",
    "requester": {
        "reference": "Practitioner/f007",
        "display": "Patrick Pump"
    },
    "medicationCodeableConcept": {
    "coding": [
      {
        "code": "12345",
        "display": "aspirin 81 mg chewable tablet",
        "system": "http://hl7.org/fhir/sid/ndc"
      }
    ],
    "text": "aspirin 81 mg chewable tablet"
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "59621000",
                    "display": "Essential hypertension (disorder)"
                }
            ]
        }
    ],
    "dosageInstruction": [
        {
            "sequence": 1,
            "text": "Take one tablet daily as directed"
        }
    ]
}
'''
    f.set_template(
        template_name="medicationrequest_v1.jinja")
    input_object = json.loads(fhir_obs)
    prompt = f.generate_prompt(input_object)
    print (prompt)
    assert prompt is not None