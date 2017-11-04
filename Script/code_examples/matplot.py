from PyQt5 import QtWidgets, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange, sin, cos, pi


class MatplotlibDemo(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('matplotlib_demo.ui')
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.figureCanvas = FigureCanvas(self.fig)
        self.figureCanvas.setParent(self.ui.drawWidget)

        self.axes = self.fig.add_subplot(111)
        self.figureCanvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
        self.figureCanvas.updateGeometry()
        self.ui.show()
        self.__zeichneFunktion(lambda x: 0 * x)
        self.ui.sinusKnopf.clicked.connect(self.zeichneSinus)
        self.ui.cosinusKnopf.clicked.connect(self.zeichneCosinus)
        self.ui.sincKnopf.clicked.connect(self.zeichneSinc)

    def __zeichneFunktion(self, f, yGrenzen=(-1.2, 1.2)):
        xGrenzen = (-5 * pi, 5 * pi)
        x = arange(xGrenzen[0], xGrenzen[1], .01)
        self.axes.clear()
        self.axes.plot(x, f(x))
        self.axes.set_xlim(xGrenzen)
        self.axes.set_ylim(yGrenzen)
        self.figureCanvas.draw()

    def zeichneSinus(self):
        self.ui.statusZeile.showMessage('Sinus-Kurve')
        self.__zeichneFunktion(sin)

    def zeichneCosinus(self):
        self.ui.statusZeile.showMessage('Cosinus-Kurve')
        self.__zeichneFunktion(cos)

    def zeichneSinc(self):
        self.ui.statusZeile.showMessage('Sinc-Kurve, sin(x)/x')
        self.__zeichneFunktion(lambda x: sin(x) / x,
                               yGrenzen=(-0.3, 1.1))


import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    matplotlibDemo = MatplotlibDemo()
    sys.exit(app.exec_())
