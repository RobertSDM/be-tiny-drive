import subprocess as sp
import pytest

def test_database_connection():
    pross = sp.run(["alembic", "current"], capture_output=True, text=True)
    if pross.returncode != 0:
        pytest.fail()
