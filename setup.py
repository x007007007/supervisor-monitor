#!/usr/bin/env python
import os
import re
import glob

from setuptools import setup
from setuptools import find_packages
import versioneer


packages = find_packages("src", exclude=['docs'])

package_data = {
    'supervisor_monitor': ["static/**"],
}

setup(
    name='supervisor-monitor',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A django app of supervisor monitor',
    author='x007007007',
    author_email='x007007007@hotmail.com',
    url='https://github.com/x007007007/',
    package_data=package_data,
    install_requires=[
        'Django>=1.7',
    ],
    dependency_links=[],
    package_dir={
        '': "src",
    },  # yapf:disable
    packages=packages,
    entry_points={
        'console_scripts': [
            'supervisor_monitor_manager=supervisor_monitor.manage:main'  # yapf:disable
        ]
    },
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7"
    ]
)
