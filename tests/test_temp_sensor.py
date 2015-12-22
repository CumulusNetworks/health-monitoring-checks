from plugins.check_cumulus_sw_temp import check_temp
import mock
from nose.tools import assert_equals, assert_raises


@mock.patch('plugins.check_cumulus_sw_temp.subprocess.check_output')
def test_temp_sensor_warning(mock_subproc):
    smonctl_out = open('tests/smonctl_warning.txt').read()
    mock_subproc.return_value = smonctl_out
    with assert_raises(SystemExit) as cm:
        check_temp()
    assert_equals(cm.exception.code, 1)


@mock.patch('plugins.check_cumulus_sw_temp.subprocess.check_output')
def test_temp_sensor_warning(mock_subproc):
    smonctl_out = open('tests/smonctl_critical.txt').read()
    mock_subproc.return_value = smonctl_out
    with assert_raises(SystemExit) as cm:
        check_temp()
    assert_equals(cm.exception.code, 2)
