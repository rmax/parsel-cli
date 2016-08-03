import mock
import pytest

from parsel_cli.utils import file_opener, open_url, urlopen


@pytest.fixture()
def tmpfile(request, tmpdir):
    fp = tmpdir.join("testfile")
    fp.write("test")
    request.addfinalizer(fp.remove)
    return fp.strpath


def test_file_opener(tmpfile):
    assert file_opener(tmpfile).read() == 'test'
    assert file_opener('file://' + tmpfile).read() == 'test'
    with pytest.raises(ValueError):
        file_opener('test://foo')


def test_open_url(tmpfile):
    assert open_url(tmpfile).read() == 'test'
    assert open_url('file://' + tmpfile).read() == 'test'

    def _open(uri, *args):
        return open(uri.rpartition('://')[2])

    url_opener = mock.Mock()
    url_opener.open.side_effect = _open

    with mock.patch.dict(urlopen.__globals__, _opener=url_opener):
        assert open_url('http://' + tmpfile).read() == 'test'
        url_opener.open.assert_called_with('http://' + tmpfile, None, mock.ANY)
        assert open_url('https://' + tmpfile).read() == 'test'
        url_opener.open.assert_called_with('https://' + tmpfile, None, mock.ANY)

    with pytest.raises(ValueError):
        open_url('unknown://uri')
