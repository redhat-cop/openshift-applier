FROM centos:centos7

ENV OC_CLIENT_MIRROR https://mirror.openshift.com/pub/openshift-v3/clients/3.11.115/linux/oc.tar.gz
ENV ANSIBLE_RPM https://releases.ansible.com/ansible/rpm/release/epel-7-x86_64/ansible-2.8.0-1.el7.ans.noarch.rpm
ENV INSTALL_PKGS "git"
ENV WORK_DIR /openshift-applier
ENV HOME ${WORK_DIR}
ENV USER_UID 1001

USER root

# Install Ansible and the 'oc' client
RUN yum install -y $INSTALL_PKGS ;\
    yum install -y $ANSIBLE_RPM ;\
    curl $OC_CLIENT_MIRROR | tar -C /usr/local/bin/ -xzf - ;\
    yum clean all ;\
    rm -rf /var/cache/yum

COPY . ${WORK_DIR}
COPY images/openshift-applier/root /
RUN /usr/local/bin/user_setup_casl

USER ${USER_UID}

WORKDIR ${WORK_DIR}

ENTRYPOINT [ "/usr/local/bin/entrypoint" ]
CMD /usr/local/bin/run
