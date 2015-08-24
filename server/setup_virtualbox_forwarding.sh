#!/bin/bash
#
# Sets up port forwarding for jabberd on boot2docker VM
# -> Still need to disable OSX firewall!

VBoxManage controlvm boot2docker-vm natpf1 "jabberd,tcp,0.0.0.0,5222,,5222"
