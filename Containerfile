FROM registry.fedoraproject.org/fedora-bootc:latest
RUN dnf install -y make git python3-pip python3-pytest black python3-flake8 python3-mypy python3-autopep8 python3-kickstart python3-build python3-setuptools
ADD . /src
RUN pip install pyinstaller
RUN pyinstaller /src/fab.py --distpath / --runtime-tmpdir . --onefile --runtime-tmpdir ./ --add-data $(pip show pykickstart | grep Location | awk '{print $2}')/pykickstart/handlers:pykickstart/handlers
ENTRYPOINT ["/fab"]
