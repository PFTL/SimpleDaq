from setuptools import setup

setup(
    name='PythonForTheLab',
    version='0.1',
    packages=['PythonForTheLab', 'PythonForTheLab.View', 'PythonForTheLab.Model', 'PythonForTheLab.Model.daq',
              'PythonForTheLab.Model.experiment', 'PythonForTheLab.Controller'],
    url='https://github.com/PFTL/SimpleDaq',
    license='MIT',
    author='Aquiles Carattino',
    author_email='aquiles@uetke.com',
    description='',
    test_suite='testsuite.testsuite',
)
