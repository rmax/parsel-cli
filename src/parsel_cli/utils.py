from lxml import html as lxml_html
from parsel import selector
from six.moves.urllib.request import urlopen


def fix_parsel_parser(new_type='html_html', base_type='html'):
    """Fix a custom parser for parsel using lxml.html.HTMLParser.

    The main reason is to have handy helpers as make_links_absolute method.
    """
    selector._ctgroup[new_type] = selector._ctgroup[base_type].copy()
    selector._ctgroup[new_type]['_parser'] = lxml_html.HTMLParser
    return new_type


def file_opener(uri, sep='://'):
    scheme, _, filename = uri.rpartition(sep)
    if scheme and scheme != 'file':
        raise ValueError("Invalid scheme: %s" % scheme)
    return open(filename)


SCHEME_OPENERS = {
    'http': urlopen,
    'https': urlopen,
    'file': file_opener,
    '': file_opener,
}


def open_url(url, sep='://', openers=SCHEME_OPENERS):
    scheme = url.rpartition(sep)[0]
    opener = openers.get(scheme)
    if not opener:
        raise ValueError("Unknown scheme: %s" % scheme)
    return opener(url)
