import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "minnesota",
    version = "0.0.2",
    author = "Spaceb4r - SPB Production",
    author_email = "-",
    description = ("Demo Setup"),
    license = "BSD",
    packages=['minnesota', 'minnesota'],
    entry_points={
        'console_scripts': [
            'minnesota = minnesota.__main__:main',
        ],
    },
    include_package_data=True,
    package_dir={'conf':'conf'},

    data_files=[('conf',
    [
    'minnesota/conf/server.conf'
    ])],

    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 0.0.2",
        "Topic :: Utilities",
        "License :: MIT License",
    ],
)
