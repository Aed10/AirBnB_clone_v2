#!/usr/bin/python3
from fabric.api import env, put, run
from os.path import exists

env.hosts = ["18.206.198.24", "54.236.43.182"]


def do_deploy(archive_path):
    # Call do_pack if no archive_path is provided
    if not exists(archive_path):
        return False

    try:
        # Extract the filename without the extension and the path
        filename = archive_path.split("/")[-1].split(".")[0]
        remote_path = f"/tmp/{filename}"

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create the directory where the archive will be unpacked
        run(f"mkdir -p /data/web_static/releases/{filename}")

        # Unpack the archive
        run(
            f"tar -xzvf /tmp/{filename}.tgz -C /data/web_static/releases/{filename}/"
        )

        # Remove the archive from the server's /tmp/ directory
        run(f"rm /tmp/{filename}.tgz")

        # Move the contenant outside 'web_static' folder
        run(
            f"mv /data/web_static/releases/{filename}/web_static/* /data/web_static/releases/{filename}/"
        )

        # Delete web_static folder
        run("rm -rf /data/web_static/releases/{filename}/web_static")
        # Delete the current symbolic link
        run("rm -f /data/web_static/current")

        # Create a new symbolic link
        run(
            f"ln -s /data/web_static/releases/{filename}/ /data/web_static/current"
        )

        return True
    except Exception as e:
        return False
