import os
import re

from setuptools import find_packages, setup

version = re.compile(r"VERSION\s*=\s*\((.*?)\)")


def get_package_version():
    "returns package version without importing it"
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "yt_scraper/__init__.py")) as initf:
        for line in initf:
            m = version.match(line.strip())
            if not m:
                continue
            return ".".join(m.groups()[0].split(", "))


def get_requirements(filename):
    return open("requirements/" + filename).read().splitlines()


def get_long_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


setup(
    name="yt_scraper",
    version=version,
    author="Ed W",
    author_email="lgetmedi@gmail.com",
    description="Scrape YouTube videos details without API key",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/wardzxzxc/yt-scraper",
    packages=find_packages(exclude=["*tests"]),
    python_requires=">=3.7",
    install_requires=get_requirements("default.txt"),
)
