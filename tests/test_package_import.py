import parsel_cli


def test_package_metadata():
    assert parsel_cli.__author__
    assert parsel_cli.__email__
    assert parsel_cli.__version__
