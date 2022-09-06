from staticjinja import Site
from pathlib import Path
from distutils.dir_util import copy_tree
import os


def render_jinja(site, template, **kwargs):
    # i.e. posts/post1.md -> build/posts/post1.html
    if os.path.basename(template.name) != template.name:
        return

    out = site.outpath / Path(template.name).with_suffix(".html")
    os.makedirs(out.parent, exist_ok=True)
    site.get_template(template.name).stream(**kwargs).dump(str(out), encoding="utf-8")


if __name__ == "__main__":
    site = Site.make_site(
        searchpath="templates",
        outpath="docs",
        extensions=['jinja_markdown.MarkdownExtension'],
        rules=[(r".*\.jinja", render_jinja)]
    )

    copy_tree("static", str(site.outpath / Path("static")))

    # enable automatic reloading
    site.render(use_reloader=True)
