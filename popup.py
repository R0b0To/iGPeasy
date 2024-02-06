from tool_api import iGP_account
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel,QPushButton

class PopupWindow(QDialog):
    def __init__(self, config):
        super().__init__()
        self.data = config['data']
        self.type = config['type']
        self.account = config['account']

        if self.type == 'parts':
            self.init_parts_popup()
        elif self.type == 'engine':
            self.init_engine_repair_popup()

        
    def init_parts_popup(self):
        self.setWindowTitle('Parts repair')
        self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        label = QLabel(f"You have {self.data['total_parts']} parts")
        button = QPushButton('repair', self)
        button.clicked.connect(lambda: self.account.request_parts_repair(self.data))
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def init_engine_repair_popup(self):
        self.setWindowTitle('Parts repair')
        self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        label = QLabel(f"You have {self.data['total_engines']}, restocking in: {self.data['restock']}")
        button = QPushButton('repair', self)
        button.clicked.connect(lambda: self.account.request_engine_repair(self.data))
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)    