from setuptools import setup

from PythonForTheLab import __version__
with open("README") as f:
    long_description = f.read()

setup(
    name='PythonForTheLab',
    version=__version__,
    packages=['PythonForTheLab', 'PythonForTheLab.View', 'PythonForTheLab.Model', 'PythonForTheLab.Model.daq',
              'PythonForTheLab.Model.experiment', 'PythonForTheLab.Controller'],
    url='https://github.com/PFTL/SimpleDaq',
    license='GPLv3',
    author='Aquiles Carattino',
    author_email='aquiles@uetke.com',
    description='Code for Python for the Lab Workshop',
    long_description=long_description,
    test_suite='testsuite.testsuite',
    entry_points={
        'console_scripts':[
            'py4lab = PythonForTheLab.start:start'
        ],
    },
    install_requires=[
        'pint',
        'PyQt5',
        'pyqtgraph',
        'numpy',
        'PyYAML',
        'pyserial',
    ],
)
