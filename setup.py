import os.path
from setuptools import find_packages, setup


def source_root_dir():
    """Return the path to the root of the source distribution"""
    return os.path.abspath(os.path.dirname(__file__))


def read_long_description():
    """Read from README file in root of source directory"""
    readme = os.path.join(source_root_dir(), 'README.rst')
    with open(readme) as fin:
        return fin.read()


setup(
    name='ssh-proxy',
    version='0.1.1',
    description='Run a SOCKS proxy over an SSH dynamic forwarding connection',
    long_description=read_long_description(),
    url='https://acroz.github.io',
    author='Andrew Crozier',
    author_email='wacrozier@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='ssh socks proxy',
    packages=find_packages(),
    install_requires=[
        'six'
    ],
    entry_points={
        'console_scripts': [
            'sshproxy=sshproxy:main'
        ]
    }
)
