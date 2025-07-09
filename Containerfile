FROM registry.fedoraproject.org/fedora-bootc:latest
RUN dnf install -y make git python3-pip python3-pytest black python3-flake8 python3-mypy python3-autopep8 python3-kickstart anaconda
ADD . /fab
RUN INSTALL_USER="--root / --prefix /usr" make --directory /fab install
ENTRYPOINT ["/usr/bin/fab"]

