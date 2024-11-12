from PyQt6.QtWidgets import*

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import figure
from matplotlib.figure import Figure


    
class MplWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        self.figure = figure(figsize=(100, 100))
        self.figure.gca().axis('off')
        self.canvas = FigureCanvas(self.figure)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.figure.add_subplot(111)
        self.setLayout(vertical_layout)