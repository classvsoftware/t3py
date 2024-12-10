from setuptools import find_packages, setup

setup(
    name="t3py",
    version="0.1.0",
    author="Matt Frisbie",
    author_email="matt@classvsoftware.com",
    description="Toolkit for using the Track & Trace Tools API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/msfrisbie/t3py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["typer", "requests"],
    entry_points={
        'console_scripts': [
            't3=t3py.main:app'
        ],
    },
)
