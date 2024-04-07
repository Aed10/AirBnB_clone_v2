#!/usr/bin/python3
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
import os

env.hosts = [""]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_clean(number=0):
    """Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep (0 by default).
    """
    number = int(number)
    if number < 0:
        return

    # Get a list of all files in the versions directory
    files = local("ls -1t versions", capture=True).split("\n")

    # Remove all but the most recent archives
    for file in files[number:]:
        local("rm versions/{}".format(file))