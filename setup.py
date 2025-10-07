from setuptools import find_packages, setup

setup(
    name="cliutils",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "argcomplete",
        "lorem-text",
        "Pillow",
        "PyYAML",
        "tomli",
        "tomli-w",
        "xmltodict",
    ],
    entry_points={"console_scripts": ["util = util.main:main"]},
)
