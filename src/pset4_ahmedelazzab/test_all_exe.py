"""Module with universal executables test."""

import subprocess
from pathlib import Path


def test_executables(monkeypatch):
    """Test executables setup.

    It iterates through all modules that should be added as executables to your package,
    tests them via a command line executable call with `--help` flag and checks if `--help`
    flag provides any information on how to use the module.

    **This test will fail if we don't install the package with dependencies.
    You should install your package using a new clean virtual environment or test via
    run_pytest_cov.py script.**
    """
    for exe in Path.cwd().glob("src/**/exe/*.py"):
        exe = Path(exe).relative_to(Path.cwd())
        if exe.name == "__init__.py":
            continue
        final_exe = (
            "-".join(x.replace("_", "-") for x in exe.parent.parent.parts[1:]) + "-" + exe.stem.replace("_", "-")
        )
        print(f"testing executable {final_exe}")  # noqa
        output = subprocess.check_output([final_exe, "--help"], stderr=subprocess.STDOUT)
        output = output.decode("utf-8").split("\n")
        has_usage = False
        for o in output:
            if f"usage: {final_exe}" in o:
                has_usage = True
                break
        assert has_usage, f"no usage information provided while running `{final_exe} --help`"
