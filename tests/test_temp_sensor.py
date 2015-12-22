from plugins.check_cumulus_sw_temp import check_temp
import mock
from nose.tools import assert_equals, assert_raises


@mock.patch('plugins.check_cumulus_sw_temp.subprocess.check_output')
def test_temp_sensor_warning(mock_subproc):
    """
    Changed ASIC Networking Sensor to 53C. Max is set at 54
    See tests/smonctl_warning.txt. This stubs the smonctl -j output
    """
    smonctl_out = open('tests/smonctl_warning.txt').read()
    mock_subproc.return_value = smonctl_out
    with assert_raises(SystemExit) as cm:
        check_temp()
    assert_equals(cm.exception.code, 1)


@mock.patch('plugins.check_cumulus_sw_temp.subprocess.check_output')
def test_temp_sensor_critical(mock_subproc):
    """
    Test Critical Warning. Changed ASIC Network Sensor to 84C. Crit is 85
    See tests/smonctl_critical.txt. This stubs the smonctl -j output
    """
    smonctl_out = open('tests/smonctl_critical.txt').read()
    mock_subproc.return_value = smonctl_out
    with assert_raises(SystemExit) as cm:
        check_temp()
    assert_equals(cm.exception.code, 2)
