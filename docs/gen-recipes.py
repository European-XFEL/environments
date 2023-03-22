from pathlib import Path

import yaml
from jinja2 import Template


recipes = Path(__file__).parent / "recipes"

packages = recipes.glob("*/meta.yaml")

TABLE_HEADER = "| Package | Version | Source URL |"


def package_info(f: Path):
    text = f.read_text()
    text = Template(text).render(compiler=lambda x: x, pin_compatible=lambda x: x)
    data = yaml.load(text, yaml.UnsafeLoader)

    return data


for package in packages:
    info = package_info(package)

    name = info["package"]["name"]
    version = info["package"]["version"]
    url = info["about"].get("home", None) or info["about"].get("dev_url", "N/A")

    row = f"| {name} | {version} | {url} |"
    print(row)
