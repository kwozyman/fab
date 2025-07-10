ARG BASEIMAGE="quay.io/centos-bootc/centos-bootc:stream9"

FROM ${BASEIMAGE}

RUN ln -s ../cloud-init.target /usr/lib/systemd/system/default.target.wants
