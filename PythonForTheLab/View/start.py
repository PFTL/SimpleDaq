# coding=utf-8
"""
    start_gui
"""
import sys
from PyQt5.QtWidgets import QApplication
from PythonForTheLab.Model import Experiment
from PythonForTheLab.View.scan_window import ScanWindow


def start_gui(experiment):
    """ Starts a GUI for the ScanWindow using the provided experiment.
    :param Experiment experiment: Experiment object with a loaded config.
    """
    ap = QApplication(sys.argv)
    m = ScanWindow(experiment)
    m.show()
    ap.exit(ap.exec_())


