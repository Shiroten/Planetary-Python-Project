from PyQt5 import QtWidgets


class MoinButton(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Moin')
        self.moinButton = QtWidgets.QPushButton('Moin', self)
        self.moinButton.setGeometry(100, 10, 60, 35)
        self.moinButton.clicked.connect(MoinButton.moin)

    @staticmethod
    def moin():
        print('MoinMoin')


import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qb = MoinButton()
    qb.show()
    sys.exit(app.exec_())
