"""
Worker Thread
=============
A Worker Thread is a simple class that re-implements QThread in order to perform a task in a
separate thread.
This is a very simple example, that could be further expanded, but it is more than enough if it is aimed at
working with methods from an Experiment class. The only requisite of QThreads is to reimplement the ``run``
method.
This may not be the correct way of doing things, as pointed out in this `blog post
<https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/>`_
"""

from PyQt5 import QtCore


class WorkThread(QtCore.QThread):
    def __init__(self,  function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    # def __del__(self):
    #     self.wait()

    def run(self):
        self.function(*self.args,**self.kwargs)
        return