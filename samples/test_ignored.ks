# Test kickstart file with ignored command
lang en_US.UTF-8
keyboard us
network --bootproto=dhcp
bootloader --location=mbr
timezone UTC

%packages
@core
%end 