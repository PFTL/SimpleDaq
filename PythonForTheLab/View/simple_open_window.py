import sys
import os

from PyQt4 import QtGui, uic
from PyQt4.Qt import QApplication

# app = QApplication(sys.argv)
# m = QtGui.QMainWindow()
# p = os.path.dirname(__file__)
# uic.loadUi(os.path.join(p, 'GUI/main_window.ui'), m)
# m.show()
# app.exit(app.exec_())

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

#        p = os.path.dirname(__file__)
#        uic.loadUi(os.path.join(p, 'GUI/main_window.ui'), self)
        uic.loadUi('GUI/main_window.ui', self)
        self.startButton.clicked.connect(self.clicked)

    def clicked(self):
        print('Clicked')

if __name__ == '__main__':
    print(os.getcwd())
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    app.exit(app.exec_())

