from plugins.check_cumulus_sw_fans import check_fans
import mock
from nose.tools import assert_equals, assert_raises


class TestArgs(object):
    """
    Mock the argparse.parser_args return value
    returns an object with warning and critical
    settings
    """
    def __init__(self, warning, critical):
        self.warning = warning
        self.critical = critical


@mock.patch('plugins.check_cumulus_sw_fans.subprocess.check_output')
def test_fan_sensor_warning(mock_subproc):
    """
    Set fan2 reading to 18000. Confirm that a warning is issued (exit code 1)
    when warning is set to 90% and critical is set to 99%
    See tests/smonctl_warning.txt. This stubs the smonctl -j output
    """
    newargs = TestArgs(90, 99)
    smonctl_out = open('tests/smonctl_warning.txt').read()
    mock_subproc.return_value = smonctl_out
    with assert_raises(SystemExit) as cm:
        check_fans(newargs)
    assert_equals(cm.exception.code, 1)


@mock.patch('plugins.check_cumulus_sw_fans.subprocess.check_output')
def test_fan_sensor_critical(mock_subproc):
    """
    Set fan2 reading to 18500. Confirm that a critical exit code is issued (exit code 2)
    when warning is set to 90% and critical is set to 95%
    See tests/smonctl_warning.txt. This stubs the smonctl -j output
    """
    newargs = TestArgs(90, 95)
    smonctl_out = open('tests/smonctl_critical.txt').read()
    mock_subproc.return_value = smonctl_out
    with assert_raises(SystemExit) as cm:
        check_fans(newargs)
    assert_equals(cm.exception.code, 2)
