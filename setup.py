from setuptools import setup, find_packages

setup(
    name="exinity_assessment",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "pytest",
    ],
)
