import sys
from PyQt5 import QtGui, QtWidgets, QtCore
class SigSlot(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle('signal & slot')
        self.dial = QtWidgets.QDial()
        self.dial.setNotchesVisible(True)
        self.spinbox = QtWidgets.QSpinBox()
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.dial)
        self.layout.addWidget(self.spinbox)
        self.setLayout(self.layout)
        self.dial.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.dial.setValue)



import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qb = SigSlot()
    qb.show()
    sys.exit(app.exec_())
