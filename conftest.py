"""This file is read by pytest at initialization."""

import pytest


def pytest_addoption(parser):
    """Add command line option to skip selected tests.

    Args:
        parser : passed by pytest
    """
    parser.addoption("--include-slow", action="store_true", default=False, help="include long-running tests")


def pytest_configure(config):
    """Add custom markers, to avoid a ton of warnings.

    Args:
        config : passed by pytest
    """
    config.addinivalue_line("markers", "slow: mark long-running test")


def pytest_collection_modifyitems(config, items):
    """Use command line option to skip tagged tests.

    Args:
        config : passed by pytest
        items : passed by pytest
    """
    if config.getoption("--include-slow"):
        # Run all tests, skip filtering
        return

    skip_slow = pytest.mark.skip(reason="need --include-slow option to run")
    for item in items:
        if "slow" in item.keywords and not config.getoption("--include-slow"):
            item.add_marker(skip_slow)
