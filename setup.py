from setuptools import setup

import glob

setup(
    name = 'ioex',
    packages = ['ioex'],
    version = '0.8',
    description = 'extension for python\'s build-in input / output interface',
    author = 'Fabian Peter Hammerle',
    author_email = 'fabian.hammerle@gmail.com',
    url = 'https://github.com/fphammerle/ioex',
    download_url = 'https://github.com/fphammerle/ioex/tarball/0.8',
    keywords = [],
    classifiers = [],
    scripts = glob.glob('scripts/*'),
    install_requires = ['python-dateutil'],
    tests_require = ['pytest', 'pytz'],
    )
