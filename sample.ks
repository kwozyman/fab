# Sample Kickstart file for testing FAB
# Basic Fedora installation

# System language
lang en_US.UTF-8

# Keyboard layout
keyboard us

# Root password
rootpw --iscrypted $6$rounds=656000$salt$hash

# System timezone
timezone UTC

# Package selection
%packages
@core
%end

# Post-installation script
%post
echo "FAB - Fast Assembler for BootC" > /etc/fab-info
%end 