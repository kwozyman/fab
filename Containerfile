FROM registry.fedoraproject.org/fedora-bootc:latest
RUN dnf install -y make git python3-pip python3-pytest black python3-flake8 python3-mypy python3-autopep8 python3-kickstart python3-build python3-setuptools anaconda
ADD . /src
RUN INSTALL_USER="" make --directory /src install && rm -rf /src
ENTRYPOINT ["/usr/local/bin/fab"]

