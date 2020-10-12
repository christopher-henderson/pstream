import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pstream",
    version="0.0.21",
    author="Christopher Henderson",
    author_email="chris@chenderson.org",
    description="Provides a Stream and AsyncStream for composing fluent lazily evaluated, stream fusion, iterators.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christopher-henderson/pstream",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["future>=0.18.2"],
    python_requires='>=2.7, >=3.6, <4',
)
