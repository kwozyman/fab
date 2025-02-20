ARG BASEIMAGE="quay.io/centos-bootc/centos-bootc:stream9"

FROM ${BASEIMAGE}

RUN systemctl enable ostree-state-overlay@opt.service
