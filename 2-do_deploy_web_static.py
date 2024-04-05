#!/usr/bin/python3
from fabric.api import env, put, run
from os.path import exists

env.hosts = ["18.206.198.24", "54.236.43.182"]


def do_deploy(archive_path):
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
        remote_path = f"/tmp/{file}"

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create the directory where the archive will be unpacked
        run(f"mkdir -p /data/web_static/releases/{file}")

        # Unpack the archive
        run(f"tar -xzvf /tmp/{file}.tgz -C /data/web_static/releases/{file}/")

        # Remove the archive from the server's /tmp/ directory
        run(f"rm /tmp/{file}.tgz")

        # Move the contenant outside 'web_static' folder
        run(
            run(
                f"mv /data/web_static/releases/{file}/web_static/* "
                f"/data/web_static/releases/{file}/"
            )
        )

        # Delete web_static folder
        run(f"rm -rf /data/web_static/releases/{file}/web_static")
        # Delete the current symbolic link
        run("rm -f /data/web_static/current")

        # Create a new symbolic link
        run(
            f"ln -s /data/web_static/releases/{file}/ /data/web_static/current"
        )

        return True
    except Exception as e:
        return False
