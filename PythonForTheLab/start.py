"""
Start Function
==============
After installing Python for the Lab it is possible to start it directly from within the command line using `pftl.start`. It takes one argument that is the path to the configuration file.

    $ pftl.start Config/experiment.yml

"""

import sys


def start():
    """Starts the GUI for the experiment using the config file specified as system argument.
    """
    args = sys.argv[1:]
    if len(args) != 1:
        print(help_message)
        return

    from PythonForTheLab.Model.experiment.IV_measurement import Experiment
    from PythonForTheLab.View.start import start_gui

    experiment = Experiment()
    experiment.load_config(args[0])
    experiment.load_daq()
    start_gui(experiment)


help_message = \
"""
Welcome to Python For The Lab
-----------------------------
In order to run the program, you need to supply the path to the config file.
For example, you can invoke this program as:
py4lab Config/experiment.yml
"""

if __name__ == "__main__":
    start()