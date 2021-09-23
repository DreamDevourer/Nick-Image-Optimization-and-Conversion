"""
This is the setup to generate MacOS package.
Troubleshooting: sudo chown -R $(whoami) .
py2applet --make-setup Nick\ -\ Image\ Optimization\ and\ Conversion.py
"""

from setuptools import setup

APP = ['Nick - Image Optimization and Conversion.py']
DATA_FILES = ['images', 'assets', 'images/backup']
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
