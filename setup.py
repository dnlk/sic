#!/usr/bin/env python
from setuptools import setup, find_packages
from subprocess import check_call, PIPE
import sys


version = 'VERSION.txt'
if sys.argv[1] in ('develop', 'sdist'):
    check_call(['git', 'describe', '--tags', '--dirty=modified'],
               stdout=file(version, 'w'), stderr=PIPE)
    data = file(version).read().replace('-g', 'g').replace('-', '+')
    file(version, 'w').write(data)


def packages():
    packs = []
    for pack in find_packages():
        if not pack.startswith('sic.test'):
            packs.append(pack)
    return packs


setup(
    name="sic",
    packages=packages(),
    entry_points=dict(console_scripts=['sndtoimg = sic.sound_to_image:main']),
    version=file(version).read().strip(),
    url="https://github.com/christianblume-serato/sic",
    author="Christian Blume",
    author_email="christian.blume@serato.com",
    description="Image-sound conversions",
    long_description=file('README.md').read(),
    install_requires=[],
)
