from plugins.check_l3_resources import check_l3_resources
import mock
from nose.tools import assert_equals, assert_raises
import sys


class TestArgs(object):
    """
    Mock the argparse.parser_args return value
    returns an object with warning and critical
    settings
    """
    def __init__(self, warning, critical):
        self.warning = warning
        self.critical = critical


@mock.patch('plugins.check_l3_resources.subprocess.check_output')
def test_l3_resource_warning(mock_subproc):
    """
    set the total number of routes to within 92% of max
    set warning threshold to 90% and critical to 95%
    check tests/cl_resource_query_warning.txt for more details
    stubs the cl-resource-query output
    """
    newargs = TestArgs(90, 95)
    cl_resource_query_out = open('tests/cl_resource_query_warning.txt').read()
    mock_subproc.return_value = cl_resource_query_out
    with assert_raises(SystemExit) as cm:
        check_l3_resources(newargs)
    mock_subproc.assert_called_with(['/usr/cumulus/bin/cl-resource-query', '-k'])
    assert_equals(cm.exception.code, 1)
    assert_equals(sys.stdout.getvalue(), "WARNING: route_total_entry L3 Resource Current: 30000 Max: 32768 Threshold: 90%\n")


@mock.patch('plugins.check_l3_resources.subprocess.check_output')
def test_l3_resource_critical(mock_subproc):
    """
    set the total number of routes to within 96% of max
    set warning threshold to 90% and critical to 95%
    check tests/cl_resource_query_warning.txt for more details
    stubs the cl-resource-query output
    """
    newargs = TestArgs(90, 95)
    cl_resource_query_out = open('tests/cl_resource_query_critical.txt').read()
    mock_subproc.return_value = cl_resource_query_out
    with assert_raises(SystemExit) as cm:
        check_l3_resources(newargs)
    mock_subproc.assert_called_with(['/usr/cumulus/bin/cl-resource-query', '-k'])
    assert_equals(cm.exception.code, 2)
    assert_equals(sys.stdout.getvalue(), "CRITICAL: route_total_entry L3 Resource Current: 32000 Max: 32768 Threshold: 95%\n")
