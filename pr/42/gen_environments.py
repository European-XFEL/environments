from pathlib import Path

import mkdocs_gen_files
import yaml

nav = mkdocs_gen_files.Nav()

ROOT = Path(__file__).parent.parent

ENVIRONMENTS_DICT = {}
FILES_SOURCE = ("0-desy-pinned.yml", "1-base.yml", "2-custom.yml")
FILES_GENERATED = ("environment.yml", "environment.lock.yml")
FILES = set(FILES_SOURCE) | set(FILES_GENERATED)

PAGE_PREFIX = Path("euxfel-software-environments") if Path.cwd() != ROOT else Path()


def generate_table(packages, lock_dict):
    text = "| Package | Version |\n" + "| --- | --- |\n"
    for package in packages:
        package = package.split("=")[0]
        version = lock_dict.get(package, package.split("=")[-1])
        text += f"| {package} | {version} |\n"
    text += "\n"
    return text


environments = (ROOT / "environments").glob("*")

# Initial reversed sort
environments = sorted(environments, reverse=True)

# Sort by reverse numerical order for environments with numerical names, else put at end
environments = sorted(
    environments, key=lambda x: int(x.name) if x.name.isdigit() else -10, reverse=True
)

for environment in environments:
    name = environment.name
    files = {f: environment / f for f in FILES}
    files = {k: v for k, v in files.items() if v.exists()}
    page = f"environments/{name}.md"
    yamls = {k: yaml.safe_load(v.read_text()) for k, v in files.items()}
    lock_dict = {
        dep.split("=")[0]: "=".join(dep.split("=")[1:])
        for dep in yamls["environment.lock.yml"]["dependencies"]
        if isinstance(dep, str)
    }
    page_rel = Path(page).relative_to("environments")
    nav[page_rel.with_suffix("").parts] = page_rel

    if (environment / "README.md").exists():
        text = (environment / "README.md").read_text()
    else:
        text = f"# `{name}`\n"

    with mkdocs_gen_files.open(PAGE_PREFIX.joinpath(page), "w") as f:
        for category in FILES_SOURCE:
            if category in yamls:
                text += f"\n## `{category}`\n"
                text += generate_table(yamls[category]["dependencies"], lock_dict)
        text += "## environment.lock.yml\n"
        text += "| Package | Version |\n"
        text += "| --- | --- |\n"
        for package, version in lock_dict.items():
            text += f"| {package} | {version} |\n"
        f.write(text)

    mkdocs_gen_files.set_edit_path(PAGE_PREFIX.joinpath(page), "gen_pages.py")
    ENVIRONMENTS_DICT[name] = page

mkdocs_gen_files.set_edit_path(PAGE_PREFIX.joinpath("environments.md"), "gen_pages.py")
index_file = Path(__file__).parent / "environments.md"
index = index_file.read_text()


with mkdocs_gen_files.open(PAGE_PREFIX.joinpath("environments.md"), "w") as f:
    text = "".join(
        f"- [{name}]({filename})\n" for name, filename in ENVIRONMENTS_DICT.items()
    )
    f.write(index.replace("{{ ENVIRONMENT_LIST }}", text))

with mkdocs_gen_files.open(
    PAGE_PREFIX.joinpath("environments/SUMMARY.md"), "w"
) as nav_file:
    nav_file.writelines(nav.build_literate_nav())
