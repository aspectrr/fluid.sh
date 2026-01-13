# Agent Run Command Requiring Password

## Overview

If you are running into the run command causing the virsh-sandbox API to ask about a password, the reason is that the base-VM doesn't have the base CA used in the virsh-sandbox API. You will need to regenerate the SSH CA with `./virsh-sandbox/scripts/setup-ssh-ca.sh [ssh-ca-dir]` and `./virsh-sandbox/scripts/reset-libvirt-macos.sh [vmname] [ca-pub-path] [ca-key-path]` to get this to work. It will regenerate all the certs and rebuild the test base VM.
