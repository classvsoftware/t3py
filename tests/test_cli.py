# tests/test_cli.py
import subprocess


def test_cli_basic_output():
    result = subprocess.run(["t3py"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Welcome" in result.stdout  # or whatever your CLI prints
