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
    url="https://github.com/robintiwari/linkedin-client",
    author="Robin Tiwari",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests"]),
    keywords="linkedin python",
    license="Apache License 2.0",
    zip_safe=False,
    install_requires=["requests>=1.1.0", "requests-oauthlib>=0.3"],
    python_requires=">=3.7",
)
