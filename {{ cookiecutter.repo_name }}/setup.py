from setuptools import find_packages, setup

setup(
    name='{{ cookiecutter.module_name }}',
    packages=find_packages(),
    version='{{ cookiecutter.version }}',
    description='{{ cookiecutter.description }}',
    author='{{ cookiecutter.author_name }}',
    author_email='{{ cookiecutter.author_email }}',
    license='{{ cookiecutter.license }}'
)
