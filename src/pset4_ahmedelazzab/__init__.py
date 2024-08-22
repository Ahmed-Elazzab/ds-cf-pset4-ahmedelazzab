"""Main package for pset4_AhmedElazzab.

Code in this module takes care of your package versioning.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    # Read version from PKG metadata
    __version__ = version("pg-ds-cf-pset4-ahmedelazzab")
except PackageNotFoundError:
    __version__ = "0.0.0"  # fall-back version
