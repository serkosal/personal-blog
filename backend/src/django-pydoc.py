"""File which prepares django to work with Pydoc."""

import os
import pydoc

import django

os.environ.get('DJANGO_SETTINGS_MODULE', 'main.settings')

if __name__ == "__main__":
    django.setup()

    pydoc.cli()