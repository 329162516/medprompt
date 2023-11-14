# Clinical note summarization

## Template variables

clinical_note: Clinical note in text format   - Required
word_count: Size of summary. default is  250 - Optional

## Usage

```
f.set_template(
        template_name="summary_v1.jinja")
f.generate_prompt({"clinical_note": "This patient is a diabetic and hypertensive."})

```