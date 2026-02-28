import subprocess as sp
import pytest


def test_database_connection():
    """
    Test the connection to the database
    """

    proc = sp.run(".\\venv\\Scripts\\python.exe -m alembic current".split(" "))

    if proc.returncode != 0:
        pytest.fail(proc.stdout)
