"""Module with tests for hello_world.py module."""

from unittest.mock import Mock, patch

import pytest

from pset4_ahmedelazzab.exe.hello_world import main
from pset4_ahmedelazzab.helloworld import hello_world


class _MockRequestResponse:
    @staticmethod
    def json():
        return {"contents": {"quotes": [{"quote": "This is a test quote"}]}}


@pytest.mark.ipa
def test_hello_world_ipa():
    """Dummy Test for IPA marker."""
    assert 1 == 1


def test_hello_world():
    """Test Hello World.

    It calls the `hello_world` package code with different flags for full test coverage.
    """
    with patch(
        "pset4_ahmedelazzab.helloworld.get",
        Mock(return_value=_MockRequestResponse()),
    ) as mock_get:
        rv = hello_world(remote=True)
        mock_get.assert_called_once_with("https://quotes.rest/qod")
        assert rv == "This is a test quote"

    rv = hello_world(remote=False)
    assert rv == "Père Noël ne sois pas triste si tu tombes si tu glisses"

    with patch("sys.argv", ["executable_name", "--times=2"]):
        with patch("pset4_ahmedelazzab.exe.hello_world.hello_world") as mock_hw:
            main()
            assert mock_hw.call_count == 2


@pytest.mark.slow
def test_hello_world_heavy():
    """Example of a long-running test with slow and/or heavy workload.

    Test decorated with @pytest.mark.slow will be excluded from the run by default.
    To include slow tests execute `pytest --include-slow`
    """
    from time import sleep

    sleep(5)
