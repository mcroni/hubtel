import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hubtel",
    version="0.0.1",
    author="joey daniel darko",
    author_email="joeydanieldarko@gmail.com",
    description="python interface for Hubtel's Payment Gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcroni/hubtel",
    packages=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
