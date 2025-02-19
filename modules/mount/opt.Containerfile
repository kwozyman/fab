ARG BASEIMAGE="quay.io/centos-bootc/centos-bootc:stream9"

FROM ${BASEIMAGE}

RUN cat <<EOF > /etc/systemd/system/opt.mount
[Unit]
Description=OverlayFS for /opt
DefaultDependencies=no
After=local-fs.target
Before=multi-user.target

[Mount]
What=overlay
Where=/opt
Type=overlay
Options=lowerdir=/opt,upperdir=/var/opt/overlay-upper,workdir=/var/opt/overlay-work

[Install]
WantedBy=multi-user.target
EOF

RUN systemctl enable opt.mount
