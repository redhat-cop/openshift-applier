Tests Info
==========

This area of the repo contains tests that can be run to check the `openshift-applier` operation.

## Requirements
- An execution environment where the `openshift-applier` can successfully operate
  - Consider using the [openshift-applier docker image](https://hub.docker.com/r/redhatcop/openshift-applier/)
- A target OpenShift environment
  - *Note:* The `openshift-applier` needs access to the `oc` command

## Dependencies

- Ansible 2.5 or later
- Operational OpenShift Cluster
- `oc` client

# Running Tests

Each "test case" is built out as an inventory with corresponding files (if applicable) in this directory. In general, and unless otherwise noted, the tests can be executed with the following command (from the repo's top level):

> ansible-playbook playbooks/openshift-cluster-seed.yml -i <path-to-inventory>

List of example test runs:

```
ansible-playbook playbooks/openshift-cluster-seed.yml -i tests/inventories/multi-files-dir
ansible-playbook playbooks/openshift-cluster-seed.yml -i tests/inventories/multi-params-dir
ansible-playbook playbooks/openshift-cluster-seed.yml -i tests/inventories/params-from-file
ansible-playbook playbooks/openshift-cluster-seed.yml -i tests/inventories/params-from-vars
ansible-playbook playbooks/openshift-cluster-seed.yml -i tests/inventories/pre-post-steps
```



License
-------

Apache License 2.0


Author Information
------------------

Red Hat Community of Practice & staff of the Red Hat Open Innovation Labs.
