FROM foobar

RUN dnf -y upgrade && dnf clean all
