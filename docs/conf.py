project = "infrawatch"
author = "infrawatch contributors"
release = "0.1.0"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.viewcode"]
html_theme = "alabaster"
html_theme_options = {
    "description": "DevOps platform — full infrastructure lifecycle",
    "github_user": "guykopa",
    "github_repo": "infrawatch",
}
autodoc_default_options = {"members": True, "undoc-members": False}
