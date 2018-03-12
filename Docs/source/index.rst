Welcome to Python For The Lab's documentation!
==============================================
Python for the Lab (PFTL) is a simple program to acquire data from a DAQ device. It is designed following the MVC design pattern, splitting the code into Controllers for defining drivers, Models for specifying the logic on how to use devices and perform an experiment. The View is where all the GUI is developed.

PFTL was developed by `Uetke <https://www.uetke.com>`_ to explain to researchers, through simple examples, what can be achieved quickly with little programming knowledge. The ultimate goal of this project is to serve as a reference place for people interested in instrumentation written in Python.

You can find the code of this package at `Github <https://github.com/PFTL/SimpleDaq/>`_, the documentation is hosted at `Read The Docs <https://readthedocs.org/projects/python-for-the-lab/>`_. If you are interesting in learning more about Python For The Lab, you can check `Uetke's courses offer <https://uetke.com/courses/>`_.

The GUI
-------
.. image:: _static/GUI_Python_For_The_Lab.png
   :scale: 50 %
   :alt: Screenshot of the GUI

If you follow the Python for the Lab course, the GUI is going to be the last step. You perform an analog output scan while acquiring the voltage on a different port. This will allow the users to acquire an I-V scan, or any other voltage dependent measurement.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   PythonForTheLab
   PythonForTheLab.Controller
   PythonForTheLab.Model
   PythonForTheLab.View



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
