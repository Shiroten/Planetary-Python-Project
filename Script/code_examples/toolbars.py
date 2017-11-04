from PyQt5 import QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):
    """
        MainWindows with symbol, tooltip etc.
    """
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.resize(350, 250)
        self.setWindowTitle('MainWindow')
        textEdit = QtWidgets.QTextEdit()
        self.setCentralWidget(textEdit)
        exit = QtWidgets.QAction(
            QtGui.QIcon('exit.png'), '&Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.close)
        self.statusBar()
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)


import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
