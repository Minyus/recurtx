from setuptools import find_packages, setup

entry_point = "recurtx = recurtx.__main__:main"


with open("requirements.txt", encoding="utf-8") as f:
    requires = []
    for line in f:
        req = line.split("#", 1)[0].strip()
        if req and not req.startswith("--"):
            requires.append(req)

long_description = """
Please see:
https://github.com/Minyus/recurtx
"""

setup(
    name="recurtx",
    version="0.0.2",
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": [entry_point]},
    install_requires=requires,
    description="CLI to transform text files recursively",
    license="Apache Software License (Apache 2.0)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Minyus/recurtx",
    author="Yusuke Minami",
    author_email="me@minyus.github.com",
    zip_safe=False,
    keywords="CLI, recursive, text, find, xargs, sed",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
