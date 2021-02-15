
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="supplier",
    version="0.0.1",
    author="Evin Sellin",
    author_email="evinism@gmail.com",
    description="Simple library for passing values deeply",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evinism/supplier",
    packages=find_packages(),
    install_requires=['contextvars;python_version<"3.7"'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)