import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="real-time-general-purpose-visualization", # Replace with your own username
    version="0.0.1",
    author="Jalil Nourisa",
    author_email="jalil.nourisa@gmail.com",
    description="A general purpose realtime visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/janursa/realtime_monitoring",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)