import subprocess

def stop_and_delete_containers_and_images():
    # Stop frontend container if it's running
    print("Stopping frontend container...")
    subprocess.run(['docker', 'stop', 'frontend-container'], check=False)

    # Remove frontend container
    print("Removing frontend container...")
    subprocess.run(['docker', 'rm', 'frontend-container'], check=False)

    # Stop backend container if it's running
    print("Stopping backend container...")
    subprocess.run(['docker', 'stop', 'backend-container'], check=False)

    # Remove backend container
    print("Removing backend container...")
    subprocess.run(['docker', 'rm', 'backend-container'], check=False)

    # Remove frontend image
    print("Removing frontend image...")
    subprocess.run(['docker', 'rmi', 'nuxt-frontend'], check=False)

    # Remove backend image
    print("Removing backend image...")
    subprocess.run(['docker', 'rmi', 'express-backend'], check=False)

if __name__ == '__main__':
    stop_and_delete_containers_and_images()
