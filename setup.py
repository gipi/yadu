from setuptools import setup, find_packages

setup(
    name = "yadu",
    version = "0.1",
    url = 'https://github.com/gipi/yadu.git',
    license = 'BSD',
    description = "Simple utilities for real life Django development",
    author = 'Gianluca Pacchiella',
    author_email = 'gp@ktln2.org',

    packages = find_packages(
        'src',
        exclude=(
            'customer',
            'yadu.tests',
        )
    ),
    package_dir = {'': 'src'},

    install_requires = ['setuptools'],
)
