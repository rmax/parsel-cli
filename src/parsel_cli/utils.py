from six.moves.urllib.request import urlopen


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
