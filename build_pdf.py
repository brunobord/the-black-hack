"""
The Black Hack OGL content Python builder.

This script is Public Domain.
"""
import argparse
from toolbox.pdf import PDFBuilder


if __name__ == '__main__':
    builder = PDFBuilder()

    directories = builder.dir_list
    targets = ('all', 'none') + directories

    parser = argparse.ArgumentParser("PDF Building")
    parser.add_argument("target", choices=targets)
    parser.add_argument(
        "--do-not-sync", action="store_true", default=False,
        help="Do not sync static pdf directory with the build"
    )

    options = parser.parse_args()
    builder.build(options.target, not options.do_not_sync)
