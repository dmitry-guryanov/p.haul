from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

setup(
	name='phaul',
	version='0.1',
	description='Tool to live-migrate containers and processes',
	url='https://criu.org/P.Haul',
	author='OpenVZ team',
	author_email='criu@openvz.org',
	license='GPLv2',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Topic :: System :: Operating System Kernels :: Linux',
		'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
	],
	keywords='development virtualization containers',
	packages=['phaul', 'phaul.shell'],
	entry_points={
		'console_scripts': [
			'p.haul=phaul.shell.phaul_client:main',
			'p.haul-service=phaul.shell.phaul_service:main',
		],
	},
)
