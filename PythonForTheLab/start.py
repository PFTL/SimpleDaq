import sys
from .View.start import start_gui


def start():
    args = sys.argv[1:]
    if len(args) != 1:
        print(help_message)

    from PythonForTheLab.Model.experiment.IV_measurement import Experiment
    from PythonForTheLab.View.scan_window import ScanWindow

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
pftl.start Config/experiment.yml
"""