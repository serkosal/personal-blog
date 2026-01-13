# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, os.path.abspath("../../src"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

project = "Serkosal's blog"
copyright = '2026, Sergey Kosykh a.k.a. Serkosal'
author = 'Sergey Kosykh a.k.a. Serkosal'
release = '0.0.4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",               # auto documenting 
    "sphinx.ext.napoleon",              # doctring google format
    "sphinx.ext.intersphinx",           # links to an external libraries
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage" 
]

templates_path = ['_templates']
exclude_patterns = ['migrations/*']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
}

html_static_path = ['_static']
