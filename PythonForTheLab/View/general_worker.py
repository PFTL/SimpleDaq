"""Very simple worker thread for executing a function in a separate Qt Thread."""
from PyQt4 import QtCore


class WorkThread(QtCore.QThread):
    def __init__(self,  function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function(*self.args,**self.kwargs)
        return