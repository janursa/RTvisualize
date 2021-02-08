import setuptools
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def extract_longDiscription(file_name):
    with open(file_name, "r") as fh:
        long_description = fh.read()
    return long_description
setuptools.setup(
    name="RTvisualize",
    version='1.01.17',
    author="Jalil Nourisa",
    author_email="jalil.nourisa@gmail.com",
    description="A general purpose realtime visualization",
    long_description=extract_longDiscription("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/janursa/RTvisualize",
    packages=setuptools.find_packages(),
    install_requires=['dash >=1.12', 'plotly >= 4.6.0', 'pandas >= 1.0.3', 'numpy >= 1.18.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
