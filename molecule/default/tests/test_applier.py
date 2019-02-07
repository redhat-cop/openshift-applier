import os

import testinfra.utils.ansible_runner
import json
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_oc_installed(host):
    oc_file = host.file('/usr/local/bin/oc')

    assert oc_file.exists
    assert oc_file.user == 'root'
    assert oc_file.group == 'root'
    assert oct(oc_file.mode) == '0755' or oct(oc_file.mode) == '0o755'


@pytest.mark.parametrize('name, description, display_name', [
  ('oa-ci-multi-files-dir1', 'OpenShift Applier Multi-Files-Dir Test 1 (description)', 'OpenShift Applier Multi-Files-Dir Test 1 (displayName)')
])
def test_projects_exists(host, name, description, display_name):
    project_output = host.run("oc get project %s -o json" % name)

    assert project_output.rc == 0

    project_output_json = json.loads(project_output.stdout)

    assert project_output_json["metadata"]["name"] == name
    assert project_output_json["metadata"]["annotations"]["openshift.io/display-name"] == display_name
    assert project_output_json["metadata"]["annotations"]["openshift.io/description"] == description


def test_routes(host):
    routes_output = host.run('oc get routes -n oa-ci-multi-files-dir1 -o json')

    assert routes_output.rc == 0

    routes_output_json = json.loads(routes_output.stdout)

    assert len(routes_output_json["items"]) == 3
