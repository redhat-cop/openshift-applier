FROM centos:centos7

ENV OC_CLIENT_MIRROR https://mirror.openshift.com/pub/openshift-v3/clients/3.9.14/linux/oc.tar.gz
ENV ANSIBLE_RPM http://releases.ansible.com/ansible/rpm/release/epel-7-x86_64/ansible-2.5.0-1.el7.ans.noarch.rpm
ENV INSTALL_PKGS "git"

USER root

# Install Ansible and the 'oc' client
RUN yum install -y $INSTALL_PKGS ;\
    yum install -y $ANSIBLE_RPM ;\
    curl $OC_CLIENT_MIRROR | tar -C /usr/local/bin/ -xzf - ;\
    yum clean all ;\
    rm -rf /var/cache/yum

CMD /bin/sleep infinity

