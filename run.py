from pathlib import Path

import pytest


if __name__ == "__main__":
    project_root = Path(__file__).parent
    pytest_ini = project_root / "pytest.ini"
    pytest.main(["-c", str(pytest_ini)])
