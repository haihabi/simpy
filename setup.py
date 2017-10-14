
#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='simpy',
      version='1.0',
      description='Python Simulation Test Manger',
      author='Hai Victor Habi',
      packages=find_packages(exclude=['tests']),
     )