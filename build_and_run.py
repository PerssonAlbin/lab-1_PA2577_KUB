"""script to build and run frontend and backend containers"""

import subprocess


def stop_and_remove_containers():
    """stop and remove frontend and backend containers"""
    subprocess.run(["python3", "stop_and_delete.py"], check=True)


def build_and_run_containers():
    """build and run frontend and backend containers"""
    # Stop and remove specific containers if they are running
    print("Stopping and removing existing containers for frontend and backend...")
    stop_and_remove_containers()

    # Build and run frontend
    print("Building frontend...")
    subprocess.run(["docker", "build", "-t", "nuxt-frontend", "./frontend"], check=True)

    print("Running frontend container...")
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-p",
            "3001:80",
            "--name",
            "frontend-container",
            "nuxt-frontend",
        ],
        check=True,
    )

    # Build and run backend
    print("Building backend...")
    subprocess.run(
        ["docker", "build", "-t", "express-backend", "./backend"], check=True
    )

    print("Running backend container...")
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-p",
            "3000:80",
            "--name",
            "backend-container",
            "express-backend",
        ],
        check=True,
    )


if __name__ == "__main__":
    build_and_run_containers()
