Fast Assembler for Bootc
===

`fab` is a somewhat opinionated build pipeline for [bootc](https://github.com/containers/bootc), allowing the modularization
of Containerfiles/bootc image building.

Fabfiles and module definitions
---

`fab` is structured as a main descriptive file for the final image, currently called "Fabfile". A Fabfile example looks like this:

```
---
metadata:
  name: fabrules
  description: My first bootc
from: quay.io/centos-bootc/centos-bootc:stream9
include:
  - modules/ssh/ssh.yaml
  - modules/dnf/install.yaml
buildargs:
  - SSHPUBKEY: (...)
  - RPMS: tmux cloud-init
```

The fields are somewhat self-explanatory:

  - `metadata`: just metadata about the bootc image
  - `from`: base image (i.e. the first `FROM` in the pipeline)
  - `include`: list of modules to include, in order in the bootc image
  - `buildargs`: list of buildargs (variables) used in the build process

For each module, there is a short descriptive file with the module definition (see `modules/` directory for examples):

```
---
metadata:
  name: dnf-install
  description: |
    Install a list of packages via dnf
containerfile: install.Containerfile
buildargs:
  - RPMS
```

Like with the top level definition, the fields should be easy to understand:

  - `metadata`: module level metadata
  - `containerfile`: filename for the Containerfile to use
  - `buildargs`: simple list of expected buildargs (without values!)

Installation
---

```
$ git clone git@github.com:kwozyman/fab.git
$ cd fab
$ python3 -m pip install --requirement requirements.txt
```

Usage
---

A simple `python3 -m fab --help` will show the full command line arguments.

In order to build the container from `Fabfile.example`:

```
$ python3 -m fab build --fabfile Fabfile.example
```

The above will trigger container image builds in sequence for each of the modules and the final one at the end.


Debugging messages can be enabled in fab with the `--log-level debug` switch, and in the underlying podman call with the `--container-tool-extra-args` switch:

```
$ python3 -m fab --container-tool-extra-args="--log-level debug" --log-level debug  build --fabfile Fabfile.example
```
