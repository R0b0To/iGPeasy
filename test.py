import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDialog, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.buttons = []

        # Add some example buttons dynamically
        for i in range(3):
            button = QPushButton(f'Button {i+1}', self)
            button.clicked.connect(self.openPopup)
            self.buttons.append(button)

        layout = QVBoxLayout()
        for button in self.buttons:
            layout.addWidget(button)
        self.setLayout(layout)

    def openPopup(self):
        sender_button = self.sender()  # Get the button that was clicked
        index = self.buttons.index(sender_button)
        popup = PopupWindow(self, index)
        popup.exec_()

class PopupWindow(QDialog):
    def __init__(self, parent=None, index=None):
        super().__init__(parent)
        self.index = index
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Popup Window {self.index+1}')
        self.button = QPushButton('Update Main Button', self)
        self.button.clicked.connect(self.updateMainButton)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f'Enter value for Popup {self.index+1}:'))
        layout.addWidget(self.button)
        self.setLayout(layout)

    def updateMainButton(self):
        new_value = 'New Value'  # Here you can retrieve the value you want
        self.parent().buttons[self.index].setText(new_value)
        self.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
