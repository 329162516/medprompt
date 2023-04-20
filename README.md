# MEDPrompt

## Collection of healthcare-inspired prompts for Large Language Models (LLMs)

![Prompt Engineering](images/medprompt.jpg)

## About
Prompt engineering is the process of designing and constructing effective prompts for LLMs. The goal of prompt engineering is to provide the LLM with the necessary information and context to generate accurate and relevant responses. **MEDPrompt** is a user contributed collection of prompts for medical applications.

## Design
MEDPrompt's philosophy is that application logic shouldn’t make the prompt engineer's job difficult. We use [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) as a template engine.

## Usage

### Install

```
pip install git+https://github.com/dermatologist/medprompt.git
```

### Import

```
from medprompt import MedPrompter
prompt = MedPrompter()
prompt.set_template(
    template_name="fhir-search-openai-chat.json")

print(prompt.get_template_variables())

messages = prompt.generate_prompt(
    {"question": "Find Conditions for patient with first name John?"})
```

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
