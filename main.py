import requests,json
from tool_api import iGP_account
from popup import PopupWindow
from setups import CarSetup
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QHBoxLayout, QFrame, QLabel,QGridLayout,QLineEdit,QComboBox
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
        button = QPushButton('Suggested', self)
        #button.setFixedWidth(60)
        inner_layout.addWidget(button, 0, 1,)
        self.buttons.append(button)
        button.clicked.connect(lambda: self.on_setup_clicked())
        race_text = QLabel('Next')
        race_text.setFixedWidth(85)
        inner_layout.addWidget(race_text,1,0)
        setup_text = QLabel('Setup')
        setup_text.setFixedWidth(110)
        inner_layout.addWidget(setup_text,1,1,Qt.AlignLeft)
        inner_layout.addWidget(QLabel('Strategy'),1,2,Qt.AlignLeft)
  
        self.grid_layout.addLayout(inner_layout , 0, 3, alignment=Qt.AlignLeft)
        self.race_tab = inner_layout

    ## remove this?
    def add_account(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel('Car Status'), 0, 0)

        inner_layout.addWidget(QLabel('Parts'),1,0)
        inner_layout.addWidget(QLabel('Engine'),1,1)
        
        self.grid_layout.addLayout(inner_layout , 0, 2, alignment=Qt.AlignTop)
    
    def load_drivers(self,account):
        inner_layout  = QGridLayout()
        driver_data = account.staff_info()
        row = 0
        for driver in driver_data['drivers']:
                inner_layout.addWidget(QLabel(driver['name']),row,0)# 0 is name label
                inner_layout.addWidget(QLabel(driver['height']),row,1)# 1 is height label
                inner_layout.addWidget(QLabel(driver['contract']),row,2)# 2 is contract, (need to add extend contract button)
                inner_layout.addWidget(QLabel('train'),row,3)# 3 is train this will be a button, open window with the options
                inner_layout.addWidget(QLabel(driver['health']),row,4)# 3 is health (need to add restore with token)
                row+=1         
        self.grid_layout.addLayout(inner_layout, self.account_row, 1,alignment=Qt.AlignTop)
    def load_car(self,account):
        inner_layout  = QGridLayout()
        row = 0
        car_data = account.car_info()
        print(car_data)
        
        for car in car_data:

                parts = car['parts']
                engine = car['engine']

                button = QPushButton(parts, self)
                inner_layout.addWidget(button,row,0,Qt.AlignCenter)# 0 is parts need to add repair button
                button.clicked.connect(lambda: self.on_repair_clicked(car,account,'parts'))
                self.buttons.append(button)
                if int(parts.strip('%')) == 100: 
                    button.setEnabled(False)
                button = QPushButton(engine, self)
                inner_layout.addWidget(button,row,1,Qt.AlignCenter)# 1 is engine
                button.clicked.connect(lambda: self.on_repair_clicked(car,account,'engine'))
                self.buttons.append(button)
                if int(engine.strip('%')) == 100:
                    button.setEnabled(False)              

                row+=1         
        self.grid_layout.addLayout(inner_layout, self.account_row, 2,alignment=Qt.AlignTop)
    
    ## setup/strategy data
    def load_strategy(self,account):
        suspension_dic = {'1':'Soft','2':'Neutral','3':'Firm'} ## remove this
        def display_strat(full_strategy):
            strategy = full_strategy['strat']
            pits = int(full_strategy['pits'])
            return ', '.join(['[' + ', '.join(map(str, arr[:2])) + ']' for arr in strategy[:pits]])
        inner_layout  = QGridLayout()
        row = 0
        strategy_data = account.next_race_info()
        if strategy_data != False:
            setups_elements = []
            for driver in strategy_data:
                    self.setups.append(driver)
                    inner_layout.addWidget(QLabel(account.strategy[0]['raceName']),row,0)# 0 next race
                    select_box = QComboBox()
                    inner_setup_layout  = QGridLayout()
                    ride_field = QLineEdit()
                    ride_field.setInputMask('99')
                    ride_field.setFixedWidth(30) 
                    ride_field.setText(driver['ride'])
                    aero_field = QLineEdit()
                    aero_field.setInputMask('99')
                    aero_field.setFixedWidth(30) 
                    aero_field.setText(driver['aero'])
                    select_box = QComboBox()
                    select_box.addItem("Soft")
                    select_box.addItem("Neutral")
                    select_box.addItem("Firm")
                    select_box.setCurrentIndex(int(driver['suspension']))
                    select_box.setFixedWidth(60) 
                    inner_setup_layout.addWidget(select_box,0,0)
                    inner_setup_layout.addWidget((ride_field),0,1,Qt.AlignLeft)
                    inner_setup_layout.addWidget((aero_field),0,2,Qt.AlignLeft)
                    self.setups.append(inner_setup_layout)
                    inner_layout.addLayout(inner_setup_layout,row,1)# 1 setup              
                    inner_layout.addWidget(QLabel(display_strat(driver)),row,2)# 1 is engine
                    row+=1
                    setups_elements.append([select_box,ride_field,aero_field])         
            self.grid_layout.addLayout(inner_layout, self.account_row, 3,Qt.AlignLeft)
            account.save_setup_field(setups_elements)    

    def initUI(self):
        self.buttons = []
        self.fields = []
        self.setups = []
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

        test_driver = ['a','b']
        driver_rows = 2
        car_rows = 2

        self.account_row = 1

        #add row for every new account self.grid_layout

        for account in self.valid_accounts:
   
            inner_layout  = QGridLayout()
            inner_layout.addWidget(QLabel(account.username),0,0)
            self.grid_layout.addLayout(inner_layout, self.account_row, 0,alignment=Qt.AlignTop)
            

            self.load_drivers(account)
            self.load_car(account)
            self.load_strategy(account)
            
            self.account_row+=1
            
            
            panel = QWidget()
            self.driver_tab.addWidget(panel, driver_rows, 0,len(test_driver),5)    
            panel.setStyleSheet("background-color: grey;")    


        
        self.show()
    
    def on_repair_clicked(self,car,account,type):
        print(self.buttons)
        sender_button = self.sender()  # Get the button that was clicked
        index = self.buttons.index(sender_button)
        popup = PopupWindow(self,index,{'type':type,'data':car,'account':account})
        popup.exec_()
    
    def on_setup_clicked(self):

        sender_button = self.sender()  # Get the button that was clicked
        index = self.buttons.index(sender_button) ## dont need this
        
        for account in self.valid_accounts:
            if account.has_league:
                suggested_setup = CarSetup(account.strategy[0]['trackCode'],account.staff['drivers'][0]['height'],account.strategy[0]['tier'])
                

                print(account.setups[0])
                account.setups[0][0].setCurrentIndex(suggested_setup.suspension)
                account.setups[0][1].setText(str(suggested_setup.ride))
                account.setups[0][2].setText(str(suggested_setup.wing))
                print (suggested_setup)
                   

            
                    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = iGPeasyWindow()
    sys.exit(app.exec_())




