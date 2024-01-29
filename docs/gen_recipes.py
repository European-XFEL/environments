from pathlib import Path

import mkdocs_gen_files

ROOT = Path(__file__).parent.parent
recipes = list((ROOT / "custom-recipes" / "recipes").rglob("recipe.yaml"))

nav = mkdocs_gen_files.Nav()

PAGE_PREFIX = Path("euxfel-software-environments") if Path.cwd() != ROOT else Path()

for recipe in recipes:
    name = recipe.relative_to(ROOT / "custom-recipes" / "recipes").parent
    page = recipe.relative_to(ROOT / "custom-recipes").parent.with_suffix(".md")
    page_rel = Path(page).relative_to("recipes")
    nav[page_rel.with_suffix("").parts] = page_rel

    page = PAGE_PREFIX.joinpath(page)

    with mkdocs_gen_files.open(page, "w") as f:
        text = f"# `{name}`\n"
        text += f"```yaml\n{recipe.read_text()} \n```\n"
        f.write(text)

    mkdocs_gen_files.set_edit_path(page, "gen_recipes.py")

summary_page = PAGE_PREFIX.joinpath(Path("recipes/SUMMARY.md"))
with mkdocs_gen_files.open(summary_page, "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
