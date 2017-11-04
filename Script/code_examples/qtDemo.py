from PyQt5 import QtWidgets, uic


class UiDemo(QtWidgets.QDialog):
    # constructor
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        # load and show the user interface from Designer.
        self.ui = uic.loadUi('qtDemo.ui')
        self.ui.show()

        # Connect up the button.
        self.ui.myPushButton.clicked.connect(self.printLcdNumber)

    # own function to print a number
    def printLcdNumber(self):
        number = self.ui.myHorizontalSlider.value()
        print('number: ', number)


import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = UiDemo()
    sys.exit(app.exec_())
