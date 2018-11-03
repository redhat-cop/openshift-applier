# Welcome to the the home of the openshift-applier [![Build Status](https://travis-ci.org/redhat-cop/openshift-applier.svg)](https://travis-ci.org/redhat-cop/openshift-applier)
The `openshift-applier` is used to apply OpenShift objects to an OpenShift Cluster.


### openshift-applier role

For technical details about inventory, role parameters, etc. please see the [openshift-applier role README](roles/openshift-applier/README.md).

### openshift-applier playbook

You can either use the role within your playbooks, or you can choose to use the playbooks provided in this repo. Checkout the [playbooks](playbooks) area for more details.

### openshift-applier container image

To ensure that your execution environment meets all requirements, it is recommended to use the [openshift-applier docker image](images/openshift-applier) for the executions. Please see the image README for more details on runtime parameters, etc.

### Molecule testing

Validates the execution of the `openshift-applier` role using [Molecule](https://molecule.readthedocs.io). Please see the [README inside the molecule directory](molecule/README.md).


## Release

As these repos are under active development, it is **strongly** recommended to use one of the [releases](../../releases) to avoid interruption to your work.
