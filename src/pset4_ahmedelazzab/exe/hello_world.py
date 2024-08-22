"""Sample Hello World executable module."""

import argparse

from pset4_ahmedelazzab.helloworld import hello_world


def main():
    """Run sample program.

    This is a sample executable module that prints quote of the day.
    To get more details about this program, run it with the `--help` flag.
    """
    parser = argparse.ArgumentParser(description="Prints a quote of the day.")
    parser.add_argument("--times", default=1, type=int, help="print QOTD that many times")
    parser.add_argument("--web", action="store_true", help="get quote from the web")
    args = parser.parse_args()

    for _ in range(args.times):
        hello_world(args.web)


if __name__ == "__main__":  # pragma: no cover
    main()
