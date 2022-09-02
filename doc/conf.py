# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "heyoka.py"
copyright = "2020, 2021, 2022, Francesco Biscani and Dario Izzo"
author = "Francesco Biscani and Dario Izzo"

# The full version, including alpha/beta/rc tags
import heyoka as hy

release = hy.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.mathjax", "myst_nb", "sphinx.ext.intersphinx"]

intersphinx_mapping = {
    "hy": ("https://bluescarni.github.io/heyoka", None),
    "mppp": ("https://bluescarni.github.io/mppp", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_logo = "images/white_logo.png"

html_theme_options = {
    "repository_url": "https://github.com/bluescarni/heyoka.py",
    "repository_branch": "main",
    "path_to_docs": "doc",
    "use_repository_button": True,
    "use_issues_button": True,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "notebook_interface": "jupyterlab",
    },
}

jupyter_execute_notebooks = "force"
execution_excludepatterns = [
    "*Trappist-1*",
    "*Outer*",
    "*Maxwell*",
    "*Keplerian billiard*",
    "*embryos*",
    "tides_spokes*",
    "ensemble_batch_perf*",
    "The restricted three-body problem*",
    "parallel_mode.ipynb",
    "vsop2013.ipynb",
    "compiled_functions.ipynb",
]

latex_engine = "xelatex"