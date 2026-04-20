"""Setup configuration for omlx package."""

from setuptools import setup, find_packages
import re
import os


def get_version():
    """Extract version from omlx.py without importing it."""
    version_file = os.path.join(os.path.dirname(__file__), "omlx.py")
    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    if match:
        return match.group(1)
    return "0.1.0"


def get_long_description():
    """Read the README for the long description."""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


setup(
    name="omlx",
    version=get_version(),
    author="jundot",
    description="A lightweight app launcher and manager for macOS",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/jundot/omlx",
    py_modules=["omlx"],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies — uses only stdlib
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "omlx=omlx:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    keywords="macos launcher app manager cli",
    project_urls={
        "Bug Reports": "https://github.com/jundot/omlx/issues",
        "Source": "https://github.com/jundot/omlx",
    },
)
