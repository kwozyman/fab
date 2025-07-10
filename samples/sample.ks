# Sample Kickstart file for testing FAB
# Basic Fedora installation

group --name fabbers
group --name redhatters --gid 2000

user --name foo1
user --name foo2 --groups redhatters