from pathlib import Path

import mkdocs_gen_files
import yaml

environments = (Path(__file__).parent.parent / "environments").glob("*")

ENVIRONMENTS_DICT = {}


def generate_table(packages, lock_dict):
    text = "| Package | Version |\n" + "| --- | --- |\n"
    for package in packages:
        version = lock_dict.get(package, package.split("=")[-1])
        text += f"| {package} | {version} |\n"

    text += "\n"
    return text


for environment in environments:
    print("Generating", environment.name)
    lock_file = environment / "conda-lock.yml"
    base_file = environment / "base.yml"
    custom_file = environment / "custom.yml"

    name = environment.name
    filename = f"environments/{name}.md"

    lock = yaml.safe_load(lock_file.read_text())
    base = yaml.safe_load(base_file.read_text()) if base_file.exists() else None
    custom = yaml.safe_load(custom_file.read_text()) if custom_file.exists() else None

    lock_dict = {dep["name"]: dep["version"] for dep in lock["package"]}

    with mkdocs_gen_files.open(filename, "w") as f:
        text = f"# {name}\n"

        if base:
            text += "## Base Packages\n"
            text += generate_table(base["dependencies"], lock_dict)

        if custom:
            text += "## Custom Packages\n"
            text += generate_table(custom["dependencies"], lock_dict)

        text += "## All Package\n"
        text += "| Package | Version |\n"
        text += "| --- | --- |\n"
        for package, version in lock_dict.items():
            text += f"| {package} | {version} |\n"

        f.write(text)

    mkdocs_gen_files.set_edit_path(filename, "gen_pages.py")

    ENVIRONMENTS_DICT[name] = filename

mkdocs_gen_files.set_edit_path("environments.md", "gen_pages.py")

index_file = Path(__file__).parent / "environments.md"
index = index_file.read_text()

with mkdocs_gen_files.open("environments.md", "w") as f:
    text = "".join(
        f"- [{name}]({filename})\n"
        for name, filename in ENVIRONMENTS_DICT.items()
    )

    f.write(index.replace("{{ ENVIRONMENT_LIST }}", text))
