import subprocess
from time import sleep

import pytest


def test_app_init():
    try:
        pross = subprocess.run(["python", "main.py"], capture_output=True, text=True, timeout=5)

        if pross.returncode != 0:
            pytest.fail(pross.stderr)
            
        pross.terminate()
    except subprocess.TimeoutExpired:
        pass
    return
