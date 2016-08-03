import contextlib
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest

import six

from parsel_cli import __version__
from parsel_cli.cli import main


HTML = u"""
    <div><a href="foo">bar</a></div>
""".encode('utf-8')


@contextlib.contextmanager
def capture(stdin=None, encoding='utf-8', redir_stderr=False):
    orig_stdin, orig_stdout, orig_stderr = sys.stdin, sys.stdout, sys.stderr
    if six.PY2:
        sys.stdin = stdin or six.StringIO()
        sys.stdout = six.StringIO()
    else:
        sys.stdin = io.TextIOWrapper(stdin or io.BytesIO(), encoding=encoding)
        sys.stdout = io.TextIOWrapper(io.BytesIO(), encoding=encoding)
    if redir_stderr:
        sys.stderr = sys.stdout
    try:
        yield sys.stdout
    finally:
        sys.stdin = orig_stdin
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr


class MainTestCase(unittest.TestCase):

    def test_invalid_scheme(self):
        argv = ['a', 'unknown://test']
        with capture(redir_stderr=True) as stdout:
            try:
                main(argv)
            except SystemExit:
                pass

        stdout.seek(0)
        assert 'scheme: unknown' in stdout.read()

    def test_default_arguments(self):
        argv = ['a::attr(href)']
        with capture(stdin=io.BytesIO(HTML)) as stdout:
            main(argv)

        stdout.seek(0)
        self.assertEqual(stdout.read(), u'foo\n')

    def test_make_links_absolute_requires_base_url(self):
        argv = ['--absolute-links', 'a']
        with capture(stdin=io.BytesIO(HTML), redir_stderr=True) as stdout:
            # FIXME: Avoid to catch SystemError for arguments errors.
            try:
                main(argv)
            except SystemExit:
                pass

        stdout.seek(0)
        self.assertIn('--base-url is required', stdout.read())

    def test_make_links_absolute_with_base_url(self):
        argv = ['--absolute-links', '--base-url', '/base/', 'a::attr(href)']
        with capture(stdin=io.BytesIO(HTML)) as stdout:
            main(argv)

        stdout.seek(0)
        self.assertEqual(stdout.read(), u'/base/foo\n')

    def test_default_arguments_from_file(self, prefix=''):
        argv = ['a::attr(href)']
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            fp.write(HTML)
            fp.flush()
            argv.append(prefix + fp.name)
            with capture() as stdout:
                main(argv)

            stdout.seek(0)
            self.assertEqual(stdout.read(), u'foo\n')

    def test_make_links_absolute_from_arg(self):
        argv = ['--absolute-links', 'a::attr(href)']
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            fp.write(HTML)
            fp.flush()
            argv.append(fp.name)
            with capture() as stdout:
                main(argv)

            stdout.seek(0)
            self.assertEqual(stdout.read(), u'%s/foo\n' % os.path.dirname(fp.name))

    def test_default_arguments_from_file_with_scheme(self):
        self.test_default_arguments_from_file('file://')

    def test_with_all_arguments(self):
        argv = [
            '--re',
            '(foo|bar)',
            '--xpath',
            '//a[@href]',
            '--encoding',
            'latin1',
            '--repr',
        ]
        with capture(stdin=io.BytesIO(HTML)) as stdout:
            main(argv)

        stdout.seek(0)
        self.assertEqual(eval(stdout.read()), ['foo', 'bar'])


def test_command():
    output = subprocess.check_output(['parsel-cli', '--version'],
                                     stderr=subprocess.STDOUT)
    if isinstance(output, six.binary_type):
        output = output.decode('utf-8')
    assert re.search(r'\b%s\b' % __version__, output) is not None
