#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers,"""
from fabric.api import env, put, run
from os.path import exists


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        env.hosts = ["35.174.184.151", "54.157.180.166"]
        env.user = "ubuntu"
        env.key_filename = "~/.ssh/id_rsa"
        # Set the remote path where the archive will be stored
        remote_path = "/tmp/{}".format(archive_path.split("/")[-1])
        # Upload the archive to the remote server
        put(archive_path, remote_path)
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder:
        # /data/web_static/releases/<archive filename> on the web server
        archive_filename = archive_path.split("/")[-1]
        archive_folder = "/data/web_static/releases/{}".format(
            archive_filename.split(".")[0]
        )
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))
        run("rm /tmp/{}".format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        # linked to the new version of your code
        run("ln -s {} /data/web_static/current".format(archive_folder))
        return True
    except Exception as e:
        return False
