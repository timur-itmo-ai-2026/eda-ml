import sys


def test_python_version() -> None:
    assert sys.version_info >= (3, 13)


def test_package_importable() -> None:
    import eda_ml

    assert eda_ml is not None
