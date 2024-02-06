import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        outer_layout = QGridLayout()

        label1 = QLabel('Label in the 1st row')
        outer_layout.addWidget(label1, 0, 0)

        inner_layout = QGridLayout()

        label2 = QLabel('Label 1 in the 2nd row')
        label3 = QLabel('Label 2 in the 2nd row')
        label4 = QLabel('Label 3 in the 2nd row')

        inner_layout.addWidget(label2, 0, 0)
        inner_layout.addWidget(label3, 0, 1)
        inner_layout.addWidget(label4, 0, 2)

        outer_layout.addLayout(inner_layout, 0, 1)

        self.setLayout(outer_layout)

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('PyQt Nested GridLayouts')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    sys.exit(app.exec_())
