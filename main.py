import requests,json
from tool_api import iGP_account
from popup import PopupWindow
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QHBoxLayout, QFrame, QLabel,QGridLayout
from PyQt5.QtCore import Qt

def load_accounts():
    with open('accounts.json', 'r') as json_file:
        accounts_list = json.load(json_file)
    
    iGP_accounts = []
    for account in accounts_list:
        account = iGP_account(account)
        if account.login():
            iGP_accounts.append(account)

    return iGP_accounts


class iGPeasyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout()
        self.valid_accounts = load_accounts()
        self.initUI()

    

    def init_driver_tab(self):
        inner_layout  = QGridLayout()
        self.panel = QWidget()
        inner_layout.addWidget(self.panel , 0, 0,2,5)
        self.panel.setStyleSheet("background-color: grey;")
        #inner_layout.setColumnStretch(3, 1)
        inner_layout.addWidget(QLabel('Drivers'), 0, 0)
        inner_layout.addWidget(QLabel('Name'),1,0)
        inner_layout.addWidget(QLabel('Height'),1,1)
        inner_layout.addWidget(QLabel('Contract'),1,2)
        inner_layout.addWidget(QLabel('Train'),1,3)
        inner_layout.addWidget(QLabel('Health'),1,4)
        
        self.grid_layout.addLayout(inner_layout , 0, 1, alignment=Qt.AlignTop)
        
        self.driver_tab = inner_layout

    def init_car_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel('Car'), 0, 0)

        inner_layout.addWidget(QLabel('Parts'),1,0)
        inner_layout.addWidget(QLabel('Engine'),1,1)
        
        self.grid_layout.addLayout(inner_layout , 0, 2, alignment=Qt.AlignTop)

    def init_race_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel('Race'), 0, 0,)

        inner_layout.addWidget(QLabel('Next'),1,0)
        inner_layout.addWidget(QLabel('Setup'),1,1)
        inner_layout.addWidget(QLabel('Strategy'),1,2)
  
        self.grid_layout.addLayout(inner_layout , 0, 3, alignment=Qt.AlignTop)
        self.race_tab = inner_layout

    def add_account(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel('Car Status'), 0, 0)

        inner_layout.addWidget(QLabel('Parts'),1,0)
        inner_layout.addWidget(QLabel('Engine'),1,1)
        
        self.grid_layout.addLayout(inner_layout , 0, 2, alignment=Qt.AlignTop)
    
    def load_drivers(self,driver_data):
        inner_layout  = QGridLayout()
        row = 0
        for driver in driver_data['drivers']:
                inner_layout.addWidget(QLabel(driver['name']),row,0)# 0 is name label
                inner_layout.addWidget(QLabel(driver['height']),row,1)# 1 is height label
                inner_layout.addWidget(QLabel(driver['contract']),row,2)# 2 is contract, (need to add extend contract button)
                inner_layout.addWidget(QLabel('train'),row,3)# 3 is train this will be a button, open window with the options
                inner_layout.addWidget(QLabel(driver['health']),row,4)# 3 is health (need to add restore with token)
                row+=1         
        self.grid_layout.addLayout(inner_layout, self.account_row, 1,alignment=Qt.AlignTop)
    def load_car(self,car_data):
        inner_layout  = QGridLayout()
        row = 0
        print(car_data)
        for car in car_data:
                parts = car['parts']
                engine = car['engine']

                if int(parts.strip('%')) == 100:
                    inner_layout.addWidget(QLabel(parts),row,0,Qt.AlignCenter)# 0 is parts need to add repair button
                else:
                    button = QPushButton(parts, self)
                    button.clicked.connect(self.on_parts_clicked)
                    inner_layout.addWidget(button,row,0)# 0 is parts need to add repair button
                
                if int(engine.strip('%')) == 100:              
                    inner_layout.addWidget(QLabel(engine),row,1,Qt.AlignCenter)# 1 is engine
                else:
                    button = QPushButton(parts, self)
                    button.clicked.connect(self.on_engine_clicked)
                    inner_layout.addWidget(button,row,1)# 0 is parts need to add repair button

                row+=1         
        self.grid_layout.addLayout(inner_layout, self.account_row, 2,alignment=Qt.AlignTop)
    def load_strategy(self,strategy_data):
        inner_layout  = QGridLayout()
        row = 0
        for driver in strategy_data:
                inner_layout.addWidget(QLabel('race'),row,0)# 0 next race
                inner_layout.addWidget(QLabel('setup'),row,1)# 1 setup              
                inner_layout.addWidget(QLabel('strategy'),row,2)# 1 is engine
                row+=1         
        self.grid_layout.addLayout(inner_layout, self.account_row, 3,alignment=Qt.AlignTop)    

    def initUI(self):
        
        self.setWindowTitle("iGPeasy")
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel(''), 0, 0,)
        inner_layout.addWidget(QLabel('Accounts'),1,0)
        self.grid_layout.addLayout(inner_layout, 0, 0,alignment=Qt.AlignTop)
        self.accounts_tab = inner_layout
      

        self.init_driver_tab()
        self.init_car_tab()
        self.init_race_tab()
        self.setLayout(self.grid_layout)
        
        self.driver_tab
        #data will be displayed from row 2
        test_accounts = ['bob','john']
        test_driver = ['a','b']
        driver_rows = 2
        car_rows = 2

        self.account_row = 1

        #add row for every new account self.grid_layout

        for account in self.valid_accounts:
   
            inner_layout  = QGridLayout()
            inner_layout.addWidget(QLabel(account.username),0,0)
            self.grid_layout.addLayout(inner_layout, self.account_row, 0,alignment=Qt.AlignTop)
            

            self.load_drivers(account.staff_info())
            self.load_car(account.car_info())
            self.load_strategy(test_driver)
            
            self.account_row+=1
            
            
            panel = QWidget()
            self.driver_tab.addWidget(panel, driver_rows, 0,len(test_driver),5)    
            panel.setStyleSheet("background-color: grey;")    


        
        self.show()
    
    def on_parts_clicked(self):
        #display available parts and then confirmation
        popup = PopupWindow()
        popup.exec_()
        print('sending request to repair parts')
    def on_engine_clicked(self):
        #display available parts and then confirmation
        print('sending request to repair engine')          

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = iGPeasyWindow()
    sys.exit(app.exec_())




