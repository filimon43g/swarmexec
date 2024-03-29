from setuptools import setup

setup(
    name="swarmexec",
    version='0.4.3',
    entry_points = {
        "console_scripts": [
            "swarmexec = swarmexec.__main__:main",
        ]
    },
    install_requires=["docker", "paramiko", "configparser", "colorama", "validators"],
    packages=['swarmexec']
)