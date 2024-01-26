from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="raincoat-takehome-science",
    version="0.1.0",
    description='Software package for calculating wind speed',
    url='https://github.com/bzohidov/raincoat-takehome-science.git',
    author="Bahtiyor Zohidov",
    author_email="bakhtiyor87@gmail.com",
    packages=find_packages(),
    scripts=["scripts/bdeck_cli.py"],
    #license="LICENSE.txt",
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=[
        "pandas>=1.5.3",
        "numpy>=1.23.5",
        "matplotlib>=3.7.1",
        "cartopy>=0.22.0",
        "xarray>=2023.7.0",
        "pyyaml>=6.0.1",
        "argparse>=1.1",
        "netCDF4>=1.6.5"
    ],
)