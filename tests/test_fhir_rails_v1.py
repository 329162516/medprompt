def test_default(f):
    f.set_template(
    template_name="fhir_rails_v1.xml")
    assert(f.generate_prompt()) is not None