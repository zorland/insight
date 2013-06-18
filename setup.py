from setuptools import setup

dependencies = [
    'numpy',
    'scipy',
]

project_name = 'dineamicFoods'
project_version = '0.1'
python_version = 'py2.7'

setup(
    name=project_name,
    version=project_version,
    author="dans",
    description=("NYC Bar Hop"),
    license="UNKNOWN",
    install_requires=dependencies,
    classifiers=[
        "Development Status :: 2 - Beta",
    ],
    zip_safe=False,
)
