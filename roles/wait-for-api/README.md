wait-for-api
============

Role used to wait for the k8s/Openshift API to be ready/available

Requirements
------------

Relies on the `k8s_info` Ansible module

Role Variables
--------------

Defaults file has all the variables that can be used. These can be overridden to fit the callers need.

| Variable | Description | Required | Defaults |
|:--------:|:-----------:|:--------:|:--------:|
|**wait_for_api_retries**| number of seconds to wait between retries | no | 15 |
|**wait_for_api_delay**| number of retries before the role gives up | no | 30 |


Example Playbook
----------------

```
- name: 'Wait for API to be available'
  hosts: k8s_host
  roles:
    - wait-for-api
```

License
-------

Apache License 2.0

Author Information
------------------

Red Hat Community of Practice & staff of the Red Hat Open Innovation Labs.
