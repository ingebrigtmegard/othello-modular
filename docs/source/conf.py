# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../..\\src'))  # <-- CRITICAL: Points to your source code

# -- Project information -----------------------------------------------------
project = 'Othello-Modular'
copyright = '2026, Ingebrigt Megård'
author = 'Ingebrigt Megård'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',        # Auto-generate docs from docstrings
    'sphinx.ext.viewcode',       # Add links to highlighted source code
    'sphinx.ext.napoleon',       # Support for Google-style docstrings
    'sphinx.ext.autosummary',    # Generate summary tables
]

# Napoleon settings (for Google/docstring compatibility)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autoclass_content = 'both'       # Include __init__ docstring with class
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_preserve_defaults = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # Professional-looking theme
html_static_path = ['_static']

# -- Options for EPUB output
epub_show_urls = 'footnote'
