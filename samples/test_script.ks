# Test kickstart file with script sections
lang en_US.UTF-8
keyboard us
network --bootproto=dhcp
rootpw --iscrypted $6$rounds=656000$salt$hash
timezone UTC

# Package selection
%packages
@core
vim
curl
%end

# Pre-installation script
%pre
#!/bin/bash
echo "Pre-installation script running"
cat /proc/cpuinfo | grep "model name" | head -1
mkdir -p /tmp/pre-install
%end

# Post-installation script
%post
#!/bin/bash
echo "Post-installation script running"
echo "FAB - Fast Assembler for BootC" > /etc/fab-info
systemctl enable sshd
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
%end 