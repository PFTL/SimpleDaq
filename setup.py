from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='py4lab',
    version="0.1.2",
    packages=find_packages(),
    url='https://github.com/PFTL/SimpleDaq',
    license='GPLv3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    author='Aquiles Carattino',
    author_email='aquiles@uetke.com',
    description='Code for Python for the Lab Workshop',
    long_description=long_description,
    long_description_content_type='text/markdown',
    test_suite='testsuite.testsuite',
    entry_points={
        'console_scripts': [
            'py4lab = PythonForTheLab.start:start'
        ],
    },
    install_requires=[
        'pint',
        'pyqt5',
        'pyqtgraph',
        'numpy',
        'PyYAML',
        'pyserial',
    ],
)
