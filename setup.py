#!/usr/bin/env python3
"""Setup script for the duplicate code detection tool."""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="duplicate-code-detection-tool",
    version="2.0.0",
    author="Flext Team",
    author_email="team@flext.dev",
    description="A Python library for detecting code similarities and duplications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flext-sh/duplicate-code-detection-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "duplicate-code-detection=duplicate_code_tool.duplicate_code_detection:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
