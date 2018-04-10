# coding=utf-8
"""
Opens an empty window

"""
import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

app = QApplication(sys.argv)
m = QMainWindow()
file_dir = '/home/aquiles/Documents/Programs/PythonForTheLab/PythonForTheLab/View'
uic.loadUi(os.path.join(file_dir, 'GUI/scan_window.ui'), m)
m.show()
app.exit(app.exec_())
