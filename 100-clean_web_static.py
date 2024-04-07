#!/usr/bin/python3
from fabric.api import *


env.hosts = ["18.206.198.24", "54.236.43.182"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_clean(number=0):
    """Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep (0 by default).
    """
    if number == 0:
        number = 1
    local(f"rm $(ls -C | head -n $( $(ls -1 | wc -l) - {number}))")
    with cd("/tmp/"):
        run(f"rm $(ls -C | head -n $( $(ls -1 | wc -l) - {number}))")
