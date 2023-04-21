#!/usr/bin/env python3
import argparse
import subprocess
import json
from typing import List
import yaml
from pathlib import Path

MAXWELL_CONDA = "/software/mamba/2022.06/bin/conda"

PINNED = {
    "dask",
    "dask-core",
    "dask-labextension",
    "ipykernel",
    "ipympl",
    "ipython",
    "ipywidgets",
    "jupyter",
    "jupyterlab",
    "jupyterlab-git",
    "jupyterlab-h5web",
    "jupyterlab_code_formatter",
    "jupyterlab_widgets",
    "matplotlib",
    "matplotlib-base",
    "matplotlib-inline",
    "spyder",
    "spyder-kernels",
}


def dump_desy_environment():
    export = subprocess.check_output(
        [
            MAXWELL_CONDA,
            "env",
            "export",
            "--json",
        ]
    ).decode("utf-8")

    environment = json.loads(export)

    dependencies = environment["dependencies"]
    packages_split = [p.split("=") for p in dependencies if isinstance(p, str)]
    packages = {s[0]: s[1] for s in packages_split}

    with open("0-desy-pinned.yml", "w") as f:
        f.write("name: desy-pinned\n")
        f.write("channels:\n")
        for channel in environment["channels"]:
            f.write(f"  - {channel}\n")

        f.write("dependencies:\n")
        for package, version in packages.items():
            if package in PINNED and version:
                f.write(f"  - {package}={version}\n")


def merge_environment_files(files: List[str], name: str):
    """Read in multiple `environment.yml` files, merge them (with the later
    specified files having priority), and write the final output to
    `merged-environment.yml`.
    """

    final_package_versions = {}

    for file in files:
        with open(file, "r") as f:
            environment = yaml.safe_load(f)
            packages = environment.get("dependencies", [])
            for package in packages:
                package_split = package.split("=")
                package_name = package_split[0]

                package_version = package_split[1] if len(package_split) >= 2 else ""
                previous_version = final_package_versions.get(package, "")

                if package_version == "" and previous_version:
                    continue

                if previous_version:
                    if package_version != previous_version:
                        print(
                            f"Warning: Conflicting versions for package {package_name} in {file}"
                        )

                final_package_versions[package_name] = package_version

    if "python" in final_package_versions:
        python_version = final_package_versions.pop("python")
        final_package_versions = {"python": python_version, **final_package_versions}

    with open("environment.yml", "w") as f:
        f.write(f"name: {name}\n")
        f.write(
            "channels:\n  - conda-forge\n  - file://gpfs/exfel/sw/software/xfel_anaconda3/mambaforge-22.9/conda-bld\n"
        )
        f.write("dependencies:\n")
        for package, version in final_package_versions.items():
            if version:
                f.write(f"  - {package}={version}\n")
            else:
                f.write(f"  - {package}\n")

    print(
        f"""Next steps:

1. Sync environment with new `environment.yml` file:

    mamba env update -n {name} -f ./environment.yml

2. After update is complete create a 'lock file' by running export:

    mamba env export -n {name} --no-builds -f environment.lock.yml

3. Add and commit any new or modified files, then push.
    """
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility for managing conda environments."
    )
    subparsers = parser.add_subparsers(dest="command")

    dump_parser = subparsers.add_parser(
        "dump",
        help=(
            "Create a `0-desy-pinned.yml` environment file, containing important "
            "pinned packages which our environments must match with."
        ),
    )

    merge_default_list = ["0-desy-pinned.yml", "1-base.yml", "2-custom.yml"]
    merge_default_name = Path.cwd().parent.name
    merge_parser = subparsers.add_parser(
        "merge", help="Merge multiple environment.yml files into merged-environment.yml"
    )
    merge_parser.add_argument(
        "--name",
        help=f"Name of the merged environment, default '{merge_default_name}'",
        default=merge_default_name,
    )
    merge_parser.add_argument(
        "files",
        nargs="*",
        help=f"List of environment.yml files to merge, default {merge_default_list}",
        default=merge_default_list,
    )

    args = parser.parse_args()

    if args.command == "dump":
        dump_desy_environment()
    elif args.command == "merge":
        merge_environment_files(args.files, args.name)
