from setuptools import setup
from pmfind import __version__

setup(
    name='pmfind',
    # see https://github.com/click-contrib/click-man/issues/72
    version=__version__,
    install_requires=[
        'lxml',
        'requests',
        'click',
    ],
    extras_require={
        'dev': [
            'click-man',
        ],
    },
    packages=['pmfind'],
    entry_points={
        'console_scripts': ['pmfind = pmfind.cli:main']
    },
    data_files=[
        ('share/man/man1', ['man/pmfind.1']),
    ],
)
