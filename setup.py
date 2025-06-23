from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PFML",
    version="3.0.0",
    author="Maksiuhrino",
    author_email="maksiurino@gmail.com",
    description="PFML - Pythoned and Fast Multimedia Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maksiurino/pfml-dev",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
