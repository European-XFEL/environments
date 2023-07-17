#!/bin/env python
import argparse
from pathlib import Path
from pprint import pprint

import pandas as pd
import yaml

parser = argparse.ArgumentParser(description="Compare two environment.lock.yaml files")
parser.add_argument("new", type=str, help="path to first environment.lock.yaml file")
parser.add_argument("old", type=str, help="path to second environment.lock.yaml file")

parser.add_argument(
    "--added_removed", action="store_true", help="only show added/removed packages"
)

parser.add_argument(
    "--versions", action="store_true", help="only show differences in versions"
)

args = parser.parse_args()


def load_env(file: Path):
    data = yaml.safe_load(file.open("r"))

    dependencies_versioned = dict([d.split("=") for d in data["dependencies"]])

    data["dependencies"] = dependencies_versioned

    return data


def added_removed(env_old: dict, env_new: dict):
    added = set(env_new["dependencies"]) - set(env_old["dependencies"])
    removed = set(env_old["dependencies"]) - set(env_new["dependencies"])

    return added, removed


def version_diff(env_old: dict, env_new: dict, major_only: bool = True):
    pkg_old = env_old["dependencies"]
    pkg_new = env_new["dependencies"]

    diff = {}
    for pkg, version in pkg_new.items():
        if version_old := pkg_old.get(pkg):
            if version_old != version:
                if major_only and version_old.split(".")[0] == version.split(".")[0]:
                    continue
                diff[pkg] = (version_old, version)

    return diff


def main(env_old_path: str | Path, env_new_path: str | Path, ar: bool, v: bool):
    env_old = load_env(Path(env_old_path))
    env_new = load_env(Path(env_new_path))

    if ar:
        added, removed = added_removed(env_old, env_new)
        print("Added packages:\n  - ", "\n  - ".join(added))

        print("\nRemoved packages:\n  - ", "\n  - ".join(removed))

    if v:
        diff = version_diff(env_old, env_new)
        data = [{"package": k, "old": v[0], "new": v[1]} for k, v in diff.items()]
        df = pd.DataFrame(data)
        df.set_index("package", inplace=True)
        print(df.to_markdown())

if __name__ == "__main__":
    main(args.old, args.new, args.added_removed, args.versions)
