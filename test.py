#!/usr/bin/python3
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
import os

env.hosts = ["18.206.198.24", "54.236.43.182"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """Function to pack web_static files into .tgz file"""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file))
        return file
    except Exception as e:
        return None


def do_deploy(archive_path=do_pack()):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not exists(archive_path):
        return False

    try:
        # Extract the filename without the extension and the path
        file = archive_path.split("/")[-1].split(".")[0]

        # Create the directory where the archive will be unpacked
        local(f"mkdir -p /data/web_static/releases/{file}/")

        # Unpack the archive
        local(f"tar -xzvf {archive_path} -C /data/web_static/releases/{file}/")

        # Remove the archive
        local(f"rm {archive_path}")

        # Move contents into host web_static
        local(
            f"mv /data/web_static/releases/{file}/web_static/* "
            f"/data/web_static/releases/{file}/"
        )

        # Remove extraneous web_static dir
        local(f"rm -rf /data/web_static/releases/{file}/web_static")

        # Delete the current symbolic link
        local("rm -f /data/web_static/current")

        # Create a new symbolic link
        local(
            f"ln -s /data/web_static/releases/{file}/ /data/web_static/current"
        )
        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create the directory where the archive will be unpacked
        run(f"mkdir -p /data/web_static/releases/{file}/")

        # Unpack the archive
        run(f"tar -xzvf /tmp/{file}.tgz -C /data/web_static/releases/{file}/")

        # Remove the archive from the server's /tmp/ directory
        run(f"rm /tmp/{file}.tgz")

        # move contents into host web_static
        run(
            f"mv /data/web_static/releases/{file}/web_static/* "
            f"/data/web_static/releases/{file}/"
        )

        # remove extraneous web_static dir
        run(f"rm -rf /data/web_static/releases/{file}/web_static")
        # Delete the current symbolic link
        run("rm -f /data/web_static/current")

        # Create a new symbolic link
        run(
            f"ln -s /data/web_static/releases/{file}/ /data/web_static/current"
        )

    except Exception as e:
        return False
    return True


def deploy():
    """Creates and distributes an archive to a web server."""
    return do_deploy()
