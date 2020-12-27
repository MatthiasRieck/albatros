from setuptools import setup

setup(
   name='albatros',
   version='0.1',
   description='Optimal control with ipopt in python',
   author='Matthias Rieck',
   author_email='matthias.rieck@icloud.com',
   packages=['albatros'],  # same as name
   install_requires=['numpy'],  # external packages as dependencies
)
