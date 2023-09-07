# List of prompts

### Usage
```
from medprompt import MedPrompter
prompt = MedPrompter()
prompt.set_template(
    template_name="<name from list below>")
messages = prompt.generate_prompt()
```

## fhir_rails_v1.xml

[Guardrails](https://docs.getguardrails.ai/) string for mapping text to FHIR search query

## observation_v1.jinja

Mapping [FHIR Observation]() to free form text