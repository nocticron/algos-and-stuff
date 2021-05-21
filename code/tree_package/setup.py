try:
    from setuptools import setup
except ImportError:
    from distutils import setup 

setup(
    name='tree',
    description='Binary search tree: quick and dirty',
    version='1.0',
    author='nocticron',
    author_email='mail@example.com',
    packages=['tree'],
)