from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name='tree',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='Binary search tree: quick and dirty',
    version='1.0',
    author='nocticron',
    author_email='mail@example.com',
    packages=['tree'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8"
)