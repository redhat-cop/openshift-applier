# Molecule Testing

[Molecule](https://molecule.readthedocs.io) can be used to validate the execution of the `openshift-applier` role. This section describes how to install, configure and execute the testing scenarios.

## Overview

Molecule testing performs an end to end integration with a Bring Your Own OpenShift environment to validate the execution of the `openshift-applier` role using one of the provided [tests](../tests). Docker containers are used to provide a testing environment to execute the role. The specific mechanisms for connecting to OpenShift can be configured as detailed in the following sections.

## Prerequisites

The following requirements must be met:

* Proper [installation and configuration of Molecule](https://molecule.readthedocs.io/en/latest/installation.html)
* Docker
** Python docker dependencies

## OpenShift Environment

The primary goal of the `openshift-applier` role is to manage resources in an OpenShift cluster. An existing OpenShift cluster must be available for the role to be executed against. The location and credentials are driven by environment variables. Authentication can be provided in the following forms:

    * .kubeconfig file
    * Username/password
    * OAuth token

## Configuration Options

The following configuration options are available to tune the execution:

| Environment Variable | Description | Default  | 
| ---------------------| ----------- | -------- |
| `USE_KUBE_FILE` | Use an exising .kubeconfig file to authenticate to OpenShift | `~/.kube/config` |
| `OC_BINARY_URL` | Location of the `oc` binary | `https://mirror.openshift.com/pub/openshift-v3/clients/3.10.45/linux/oc.tar.gz` |
| `OC_MASTER_URL` | Location of the OpenShift master | `https://localhost:8443` |
| `OC_USERNAME` | OpenShift username to authenticate as | `admin` |
| `OC_PASSWORD` | OpenShift password to authenticate as | `admin` |
| `OC_TOKEN` | OAuth token to use for authentication | |

## Execution

Run the following command to exercise the Molecule testing scenario:

```
molecule test
```

A typical testing scenario will execute the following actions:

* Create a new docker container environment for execution
* Lint the playbooks/role
* Prepare the testing environment
    * Download oc binary
    * Login to OpenShift
* Execute `openshift-applier`
* Execute tests to verify execution
* Cleanup applier actions
* Destroy container environment