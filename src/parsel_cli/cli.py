"""Parsel Command Line Interface."""
from __future__ import print_function, unicode_literals

import argparse
import pprint
import re
import sys

import six

from parsel import Selector, __version__ as parsel_version

from . import __version__
from .utils import open_url, fix_parsel_parser


PARSER_TYPE = fix_parsel_parser()


def main(argv=None, progname=None):
    parser = argparse.ArgumentParser(prog=progname, description=__doc__)
    parser.add_argument('expr', metavar='EXPRESSION',
                        help="A CSS expression, or a XPath expression if --xpath is given.")
    parser.add_argument('file', metavar='FILE_OR_URL', nargs='?',
                        help="If missing, it reads the HTML content from the standard input.")
    parser.add_argument('--base-url', help="Base URL for links. Default: input URL")
    parser.add_argument('--absolute-links', action='store_true',
                        help="Make links absolute.")
    parser.add_argument('--xpath', action='store_true',
                        help="Given expression is a XPath expression.")
    parser.add_argument('--re', metavar='PATTERN',
                        help="Apply given regular expression.")
    parser.add_argument('--encoding', metavar='ENCODING', default='utf-8',
                        help="Input encoding. Default: utf-8.")
    parser.add_argument('--repr', action='store_true',
                        help="Output result object representation instead of as text.")
    parser.add_argument('--version', action='version',
                        version='parsel-cli %s, parsel %s' % (__version__, parsel_version))

    args = parser.parse_args(argv)

    if args.file:
        try:
            text = open_url(args.file).read()
        except ValueError as e:
            parser.error(str(e))
    else:
        text = sys.stdin.read()

    if isinstance(text, six.binary_type):
        try:
            text = text.decode(args.encoding)
        except UnicodeDecodeError:
            parser.error("Failed to decode input using encoding: %s" % args.encoding)

    sel = Selector(text=text, type=PARSER_TYPE)

    base_url = args.base_url or args.file
    if args.absolute_links:
        if not base_url:
            parser.error("--base-url is required")
        sel.root.make_links_absolute(base_url)

    if args.xpath:
        result = sel.xpath(args.expr)
    else:
        result = sel.css(args.expr)

    if args.re:
        regex = args.re.encode(args.encoding)
        regex = regex.decode('string_escape' if six.PY2 else 'unicode_escape')
        out = result.re(re.compile(regex, re.IGNORECASE | re.UNICODE))
    else:
        out = result.extract()

    if args.repr:
        pprint.pprint(out)
    else:
        print("\n".join(out))

    return 0
