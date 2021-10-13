from setuptools import setup, find_packages
from os import path

from linkedin import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="linkedin-client",
    version=__version__,
    description="Python wrapper for the LinkedIn API V2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rawbinz/linkedin-client",
    author="Robin",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["tests"]),
    keywords="linkedin python",
    license="Apache License 2.0",
    zip_safe=False,
    install_requires=["requests>=2.25.1", "requests-oauthlib>=1.2.0"],
    python_requires=">=3.7",
)
