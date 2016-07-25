"""Parsel Command Line Interface."""
import sys

from .cli import main


if __name__ == "__main__":
    sys.exit(main(progname='python -m parsel_cli'))
