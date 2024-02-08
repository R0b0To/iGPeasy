from tool_api import iGP_account
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel,QPushButton

class PopupWindow(QDialog):
    def __init__(self, parent=None, index= None, config=None):
        super().__init__(parent)
        self.data = config['data']
        self.type = config['type']
        self.account = config['account']
        self.index = index

        if self.type == 'parts':
            self.init_parts_popup()
        elif self.type == 'engine':
            self.init_engine_repair_popup()

        
    def init_parts_popup(self):
        self.setWindowTitle('Parts repair')
        self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        
        label = QLabel(f"You have {self.account.car[0]['total_parts']} parts \n Repair cost: {self.data['repair_cost']} part(s)")
        button = QPushButton('repair', self)
        
        button.clicked.connect(self.update_main_button)
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def init_engine_repair_popup(self):
        self.setWindowTitle('Parts repair')
        self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        label = QLabel(f"You have {self.data['total_engines']}, restocking in: {self.data['restock']}")
        button = QPushButton('repair', self)
        button.clicked.connect(self.update_main_button)
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout) 
        
        
        # check if repaired
    def update_main_button(self):

        if self.type == 'parts':
           self.response = self.account.request_parts_repair(self.data)
           self.account.car[0]['total_parts'] -= self.data['repair_cost']
            

        elif self.type == 'engine':
           self.response = self.account.request_engine_repair(self.data)
        
        new_value = self.response  # Here you can retrieve the value you want
        self.parent().buttons[self.index].setText(new_value)
        self.parent().buttons[self.index].setEnabled(False)  
        self.accept()