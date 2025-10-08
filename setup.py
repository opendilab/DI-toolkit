import os
import re
from codecs import open
from distutils.core import setup

from setuptools import find_packages

_package_name = "ditk"

here = os.path.abspath(os.path.dirname(__file__))
meta = {}
with open(os.path.join(here, _package_name, 'config', 'meta.py'), 'r', 'utf-8') as f:
    exec(f.read(), meta)


def _load_req(file: str):
    """Load requirements from requirements file"""
    with open(file, 'r', 'utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


requirements = _load_req('requirements.txt')

_REQ_PATTERN = re.compile('^requirements-([a-zA-Z0-9_]+)\\.txt$')
group_requirements = {
    item.group(1): _load_req(item.group(0))
    for item in [_REQ_PATTERN.fullmatch(reqpath) for reqpath in os.listdir()] if item
}

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    # Basic package information
    name=meta['__TITLE__'],
    version=meta['__VERSION__'],
    packages=find_packages(include=(_package_name, "%s.*" % _package_name)),
    package_data={package_name: ['*.yaml', '*.yml', '*.css', '*.js']
                  for package_name in find_packages(include=('*'))},
    description=meta['__DESCRIPTION__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=meta['__AUTHOR__'],
    author_email=meta['__AUTHOR_EMAIL__'],
    license='Apache License, Version 2.0',
    keywords='opendilab, toolkit, logging, documentation, tensorboard, machine learning, deep learning, reinforcement learning',
    url='https://github.com/opendilab/DI-toolkit',

    # Environment and dependency requirements
    python_requires=">=3.8",
    install_requires=requirements,
    tests_require=group_requirements.get('test', []),
    extras_require=group_requirements,

    # Package classifiers for PyPI categorization
    classifiers=[
        # Development status - indicates the package is stable and production-ready
        'Development Status :: 5 - Production/Stable',

        # Target audience - primarily for developers and researchers
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',

        # License information - Apache 2.0 license
        'License :: OSI Approved :: Apache Software License',

        # Programming language support
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: PyPy',

        # Operating system compatibility
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',

        # Topic categories - what the package is used for
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Documentation',
        'Topic :: System :: Logging',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities',

        # Environment and framework compatibility
        'Environment :: Console',
        'Environment :: Web Environment',

        # Natural language support
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',

        # Framework compatibility - particularly for ML/DL frameworks
        'Framework :: Matplotlib',

        # Additional topic classifications for ML/RL
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)
