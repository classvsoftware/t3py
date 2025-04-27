# tests/test_imports.py
import t3py


def test_import_root():
    assert hasattr(t3py, "__version__") or hasattr(t3py, "__doc__")


def test_import_module():
    from t3py import cli

    assert callable(cli.main)
