import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDialog, QLabel

class PopupWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Popup Window')
        self.setFixedSize(200, 100)

        layout = QVBoxLayout()
        label = QLabel('This is a popup window')
        layout.addWidget(label)

        self.setLayout(layout)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a QPushButton
        button = QPushButton('Show Popup', self)

        # Connect the button's clicked signal to the show_popup method
        button.clicked.connect(self.show_popup)

        # Create a layout and add the button to it
        layout = QVBoxLayout()
        layout.addWidget(button)

        # Set the layout for the main window
        self.setLayout(layout)

        self.setWindowTitle('Popup Example')
        self.show()

    # Define a method to show the popup window
    def show_popup(self):
        popup = PopupWindow(self)
        popup.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    sys.exit(app.exec_())
