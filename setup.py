#!/usr/bin/env python3
"""
Setup script for fab CLI tool.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fab-cli",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Fast Assembler for BootC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fab",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pykickstart>=3.0",
        #"anaconda>=40.0",  ## Anaconda is not distributed via PyPI
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
            "autopep8>=1.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fab=fab.cli:main",
        ],
    },
)
