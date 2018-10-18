# The openshift-applier playbooks

## openshift-cluster-seed.yml (openshift-applier)
This playbook is mainly here to serve as the execution point for the [openshift-applier](../roles/openshift-applier). There are few important notes to make about how this is executed:

1. Inventory
To better integrate with other tools leveraging this playbook, the `hosts` have been defined as `seed-hosts`. This means that the inventory needs to contain a valid group for `seed-hosts`, such as:

```
[seed-hosts]
localhost
```

2. Local Execution
If the playbook is executed locally, i.e.: on your `localhost`, it's recommended to run with the local option ( `--connection=local` ) to speed up the execution. This prevents the inventory from being copied to the remote host and hence avoids the extra time it takes to iterate over the inventory content to copy the local files.

**Tip:** Adding the following to `host_vars/localhost.yml` allows you to skip the command line argument:

```
ansible_connection: local
```

```
> ansible-playbook -i <inventory> path/to/openshift-applier/playbooks/openshift-cluster-seed.yml --connection=local
```

3. Skip Version Checks
The [openshift-applier](../roles/openshift-applier) by default enforces that the appropriate versions of ansible, oc, etc. is used and will error out of minimum requirements are not met. However, in some cases you may want/need to by-pass this check and run with other versions. This can be done by setting the `skip_version_check` flag - either on the command line or part of your inventory (the latter is not recommended):

```
> ansible-playbook -i <inventory> path/to/openshift-applier/playbooks/openshift-cluster-seed.yml -e 'skip_version_checks=True'
```
