FROM registry.access.redhat.com/ubi8/ubi

ENV pip_packages "ansible"

ENV OC_CLIENT_MIRROR https://mirror.openshift.com/pub/openshift-v3/clients/3.11.115/linux/oc.tar.gz
ENV INSTALL_PKGS "git python3"
ENV WORK_DIR /openshift-applier
ENV HOME ${WORK_DIR}

RUN yum -y install --disableplugin=subscription-manager $INSTALL_PKGS ;\
    curl $OC_CLIENT_MIRROR | tar -C /usr/local/bin/ -xzf - ;\
    yum --disableplugin=subscription-manager clean all ;\
    rm -rf /var/cache/yum

# Install Ansible via Pip.
RUN pip3 install ansible molecule yamllint pytest

RUN mkdir -p /etc/ansible
RUN echo -e '[local]\nlocalhost ansible_connection=local' > /etc/ansible/hosts

COPY . ${WORK_DIR}
COPY images/openshift-applier/root /

WORKDIR ${WORK_DIR}

CMD /usr/local/bin/run
