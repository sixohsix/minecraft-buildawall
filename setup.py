from setuptools import setup, find_packages
import sys, os

version = '0.5'

install_requires = [
    # -*- Extra requirements: -*-
    "numpy",
    ]

setup(name='mcbuildawall',
      version=version,
      description="Build a wall around the edges of your Minecraft wall",
      long_description=open("./README.md", "r").read(),
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: End Users/Desktop",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License",
          ],
      keywords='minecraft',
      author='Mike Verdone',
      author_email='mike.verdone@gmail.com',
      url='https://github.com/sixohsix/mcbuildawall',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      buildawall=buildawall:main
      """,
      )
