import os

from py.path import local
from pytest import fixture, skip


def pytest_addoption(parser):
    if os.environ.get('CI'):
        parser.addoption('--skip-slow', action='store_true',
                         help='Skip slow tests')
    else:
        parser.addoption('--run-slow', action='store_true',
                         help='Run slow tests')


def pytest_runtest_setup(item):
    if 'slow' in item.keywords:
        if os.environ.get('CI'):
            if item.config.getoption('--skip-slow'):
                skip('skipped; --skip-slow option is used')
        else:
            if not item.config.getoption('--run-slow'):
                skip('need --run-slow option to run')


@fixture
def fx_asset():
    """The fixture that provides :class:`py.path.local` instance that
    points the :file:`assets` directory.  You can use this in test
    functions::

        def test_something(fx_asset):
            monalisa = str(fx_asset.join('mona-lisa.jpg'))
            with open(monalisa) as f:
                assert f.tell() == 0

    """
    return local(__file__).dirpath('assets')
