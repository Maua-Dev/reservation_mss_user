import os
import shutil
import subprocess
from pathlib import Path

IAC_DIRECTORY_NAME = "iac"
SOURCE_DIRECTORY_NAME = "src"
LAMBDA_LAYER_PREFIX = os.path.join("python", "src")
# Dependências pip necessárias nas lambdas (evita subir pytest etc. na layer)
LAMBDA_PIP_PACKAGES = [
    "PyJWT==2.10.1",
    "cryptography==44.0.2",
]


def adjust_layer_directory(shared_dir_name: str, destination: str):
    # Get the root directory of the source directory
    root_directory = Path(__file__).parent.parent
    iac_directory = os.path.join(root_directory, IAC_DIRECTORY_NAME)

    print(f"Root directory: {root_directory}")
    print(f"Root direcotry files: {os.listdir(root_directory)}")
    print(f"IaC directory: {iac_directory}")
    print(f"IaC directory files: {os.listdir(iac_directory)}")


    # Get the destination and source directory
    destination_directory = os.path.join(root_directory, IAC_DIRECTORY_NAME, destination)
    source_directory = os.path.join(root_directory, SOURCE_DIRECTORY_NAME, shared_dir_name)

    # Delete the destination directory if it exists
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)

    # Copy the source directory to the destination directory
    shutil.copytree(source_directory, os.path.join(destination_directory, LAMBDA_LAYER_PREFIX, shared_dir_name))
    print(
        f"Copying files from {source_directory} to {os.path.join(destination_directory, LAMBDA_LAYER_PREFIX, shared_dir_name)}")

    python_site_packages = os.path.join(destination_directory, "python")
    print(f"Installing lambda pip packages into {python_site_packages}: {LAMBDA_PIP_PACKAGES}")
    subprocess.check_call(
        [
            "pip",
            "install",
            *LAMBDA_PIP_PACKAGES,
            "-t",
            python_site_packages,
            "--no-cache-dir",
            "--platform",
            "manylinux2014_x86_64",
            "--python-version",
            "3.13",
            "--only-binary=:all:",
        ]
    )


if __name__ == '__main__':
    adjust_layer_directory(shared_dir_name="shared", destination="lambda_layer_ReservationMssUser")
