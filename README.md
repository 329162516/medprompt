# MEDPrompt
## Medical prompts for Large Language Models (LLMs) ✍️
![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/medprompt)
[![PyPI download total](https://img.shields.io/pypi/dm/medprompt.svg)](https://pypi.python.org/pypi/medprompt/)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/dermatologist/medprompt)

## About
Prompt engineering is the process of designing and constructing effective prompts for LLMs. The goal of prompt engineering is to provide the LLM with the necessary information and context to generate accurate and relevant responses. **MEDPrompt** is a user-contributed collection of prompts and [Guardrails](https://docs.getguardrails.ai/) for medical applications. MEDPrompt also includes a collection of templates for using FHIR in LLM prompts (see below). WIP, User contributions are highly appreciated!

### FHIR2Text -> Convert FHIR resources to plain text
This repository includes templates for converting **FHIR resources into a text representation** that can be injected into an LLM prompt. Only relevant information is extracted from the resource with simple transformations using helper functions. You can create **joint embeddings from structured and unstructured data** from FHIR resources!  🚒[**See this example usage**](/tests/test_fhir_observation_v1.py).

### FHIR2Calculator -> Calculate clinical scores from a FHIR Bundle (*Work in progress*)
Clinical calculators are tools that help healthcare professionals make medical decisions by providing them with quick and easy access to various medical formulas, scores, and algorithms. Calculations performed by LLMs are not reliable. FHIR2Calculator performs calculations on data fields extracted from a FHIR bundle and outputs the results as plain text that can be injected into LLM prompts.

### Below is the logical architecture for an end-to-end system using these templates (*Work in progress*).

[![FHIR Engine](https://github.com/dermatologist/medprompt/blob/develop/notes/fhirqa.drawio.svg)](https://github.com/dermatologist/medprompt/blob/develop/notes/fhirqa.drawio.svg)

:sparkles: Checkout [FHIRy](https://github.com/dermatologist/fhiry) for FHIR -> pandas df mapping!

## [LIST OF TEMPLATES](/info/index.md)

## Design
MEDPrompt's philosophy is that application logic shouldn’t make the prompt engineer's job difficult. We use [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) as a template engine.

## Usage

## See [Examples folder](/examples)
1. [Observation](/examples/fhirToText.ipynb)
2. [FHIR Bundle](/examples/fhirBundle.ipynb)

### Install

```
pip install medprompt
```

### Install Develop branch

```
pip install git+https://github.com/dermatologist/medprompt.git
```

### Import

```
from medprompt import MedPrompter
prompt = MedPrompter()
prompt.set_template(
    template_name="fhir_search_oai_chat_v1.json")

print(prompt.get_template_variables())

messages = prompt.generate_prompt(
    {"question": "Find Conditions for patient with first name John?"})

print(messages)
```

## [Documentation](https://dermatologist.github.io/medprompt/)

## Give us a star ⭐️
If you find this project useful, give us a star. It helps others discover the project.

## Contributing
* PR welcome
* Add templates in [this folder](src/medprompt/templates/) as [jinja2](https://jinja.palletsprojects.com/en/3.1.x/) or JSON.
* Follow the naming conventions in the folder.
* Add documentations [here](info/) as a markdown file with the same name.
* Add a link in the [index.md file](info/index.md).
* Please see [CONTRIBUTING.md](/CONTRIBUTING.md)

## Contributers
* [Bell Eapen](https://nuchange.ca) | [![Twitter Follow](https://img.shields.io/twitter/follow/beapen?style=social)](https://twitter.com/beapen)
