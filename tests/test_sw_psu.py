from plugins.check_cumulus_sw_psu import check_psu
import mock
from nose.tools import assert_equals, assert_raises


class FakeArgs(object):
    def __init__(self, psu_count):
        self.min_psu = psu_count


@mock.patch('plugins.check_cumulus_sw_psu.subprocess.check_output')
def test_psu_count(mock_subproc):
    """
    in smonctl_psu_count test file set one PSU to a failed status
    min-psu is set to 2
    """
    smonctl_out = open('tests/smonctl_psu_count.txt').read()
    mock_subproc.return_value = smonctl_out
    with assert_raises(SystemExit) as cm:
        check_psu(FakeArgs(2))
    assert_equals(cm.exception.code, 2)
