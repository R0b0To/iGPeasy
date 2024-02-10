import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout

class ClickableGridLayout(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        for i in range(3):
            for j in range(3):
                button = QPushButton(f'Button {i},{j}', self)
                self.grid.addWidget(button, i, j)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Clickable Grid Layout')
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Grid Layout Clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClickableGridLayout()
    sys.exit(app.exec_())
