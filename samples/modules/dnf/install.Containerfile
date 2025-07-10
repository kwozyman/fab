FROM foobar
ARG RPMS

RUN dnf install -y ${RPMS} && dnf clean all
