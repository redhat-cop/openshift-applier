OpenShift Applier Docker Client
===============================

Produces a container capable of acting as a control host for `openshift-applier`

**_NOTE:_** This is also used to enable the use of versions that may not be quite main stream (or a pre-release).


## Setup

The following steps are required to run the docker client.

1. Install docker and docker-compose
  1. on RHEL/Fedora: ```{yum/dnf} install docker docker-compose```
  2. on Windows: [Install Docker for Windows](https://docs.docker.com/windows/step_one/)
  3. on OSX: [Max OS X](https://docs.docker.com/installation/mac/)
  4. on all other Operating Systems: [Supported Platforms](https://docs.docker.com/installation/)
2. Give your user access to run Docker containers (this is only required in Linux/Unix distros)
```
groupadd docker
usermod -a -G docker ${USER}
systemctl enable docker
systemctl restart docker
```

## Running

The simplest possible run of the image would look like:

```
docker run -u $(id -u) \
  -v $HOME/.kube/config:/openshift-applier/.kube/config:z
  -t redhat-cop/openshift-applier
```

NOTE: The above commands expects the following inputs:
* You already have a valid session with the OpenShift cluster (i.e.: using `oc login`) with the session data stored at `$HOME/.kube/config`

Running the above command will kick off an openshift-applier run that will execute against a [Test inventory](../../tests/) by default. This however doesn't account for inventories or changes you've made locally. The following subsections cover alternate uses of the image for these scenarios

### Running a local inventory

Running an openshift-applier inventory that you may have locally requires two things:

```
docker run -u $(id -u) \
  -v $HOME/.kube/config:/openshift-applier/.kube/config:z
  -v $HOME/src/my-inventory/:/tmp/my-inventory <1>
  -e INVENTORY_PATH=/tmp/my-inventory <2>
  -t redhat-cop/openshift-applier
```
1. Your inventory must be mounted into the container
2. You need to tell the container's run script about the inventory

### Testing local changes to OpenShift Applier

For convenience, the container image packages the openshift-applier ansible code inside of the container file system at `/openshift-applier/`. By default, the run script will run the basic applier playbook at `/openshift-applier/playbooks/openshift-cluster-seed.yml`. If you would like to run your local version of applier, you can override this default by adding the following:

```
docker run -u $(id -u) \
  -v $HOME/.kube/config:/openshift-applier/.kube/config:z
  -v $HOME/src/openshift-applier/:/tmp/openshift-applier <1>
  -e PLAYBOOK=/tmp/openshift-applier/playbooks/my-new-playbook.yml <2>
  -t redhat-cop/openshift-applier
```
1. Your copy of openshift-applier must be mounted into the container
2. You must tell the container's run script which playbook to run

## Building the Image

This image is built and published to quay.io, so there's no reason to build it if you're just wanting to use the latest stable version. However, if you need to build it for development reasons, here's how:

```
cd ./openshift-applier
docker build -t redhat-cop/openshift-applier -f images/openshift-applier/Dockerfile .
```

## Troubleshooting

TBD
