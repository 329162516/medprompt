"""
    Dummy conftest.py for medprompt.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest


@pytest.fixture
def f():
    from src.medprompt import MedPrompter
    _m = MedPrompter()
    return _m
