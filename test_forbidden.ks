# Test kickstart file with forbidden command
lang en_US.UTF-8
keyboard us
exec echo "This should be forbidden"
network --bootproto=dhcp 