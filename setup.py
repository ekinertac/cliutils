from setuptools import setup, find_packages

setup(
    name='cliutils',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'util = util.main:main'
        ]
    }
)
