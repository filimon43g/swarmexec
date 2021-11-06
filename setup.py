from setuptools import setup

setup(
    name="swarmexec",
    version='0.1.8',
    entry_points = {
        "console_scripts": [
            "swarmexec = swarmexec.__main__:main",
        ]
    },
    install_requires=["docker", "paramiko", "configparser"],
    packages=['swarmexec']
)