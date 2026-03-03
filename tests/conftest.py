import copy
import os
import sys

# ensure the application module is importable
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

import app  # noqa: E402
import pytest

# keep an untouched copy of the initial activities state
_original_activities = copy.deepcopy(app.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset the in‑memory activities dictionary before each test.

    This fixture is autouse, so it's applied automatically to every
    test in the suite.
    """
    app.activities = copy.deepcopy(_original_activities)
