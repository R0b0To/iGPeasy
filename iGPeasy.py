import requests,json
from tool_api import iGP_account
from gui import PopupWindow, iGPWindow
from setups import CarSetup
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QHBoxLayout, QFrame, QLabel,QGridLayout,QLineEdit,QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

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
        self.main_window = iGPWindow(self)
        self.valid_accounts = load_accounts()
        self.initUI()

    
    def load_drivers(self,account):
        inner_layout  = QGridLayout()
        row = 0
 
        for driver in account.staff['drivers']:
                name_text = QPushButton(driver['name'],self)
                name_text.setFixedWidth(90)

                name_text.clicked.connect(lambda: self.on_button_clicked(account))
                extend_contract = QPushButton(driver['contract'],self)
                extend_contract.clicked.connect(lambda: self.on_button_clicked(account))
                self.main_window.buttons.append(extend_contract)
                self.main_window.buttons.append(name_text)


                name_text.setProperty('driver_index',row)
                name_text.setProperty('type','driver')
                extend_contract.setProperty('driver_index',row)
                extend_contract.setProperty('type','contract')


                inner_layout.addWidget(name_text,row,0)# 0 is name label
                #inner_layout.addWidget(QLabel(driver['height']),row,1)# 1 is height label
                inner_layout.addWidget(extend_contract,row,1)# 2 is contract, (need to add extend contract button)
                #inner_layout.addWidget(QLabel('train'),row,3)# 3 is train this will be a button, open window with the options
                #inner_layout.addWidget(QLabel(driver['health']),row,3)# 3 is health (need to add restore with token)
                row+=1         
        self.main_window.main_grid.addLayout(inner_layout, self.account_row, 1,alignment=Qt.AlignTop)
    def load_misc(self,account):
        inner_layout  = QGridLayout() 
        button = QPushButton('Res', self)
        button.setFixedWidth(50)
        inner_layout.addWidget(button,0,2)
        self.main_window.buttons.append(button)
        button.setProperty('type','research')
        button.clicked.connect(lambda: self.on_modify_research(account))
        
        sponsors = account.get_sponsors()
        button = QPushButton(sponsors, self)
        button.setFixedWidth(50)
        button.setProperty('type','sponsor')
        inner_layout.addWidget(button,0,3)
        self.main_window.buttons.append(button)
        button.clicked.connect(lambda: self.on_sponsor_click(account))
        #self.main_window.buttons.append(button)
        self.main_window.main_grid.addLayout(inner_layout, self.account_row, 2,alignment=Qt.AlignTop)


    def load_car(self,account):
        inner_layout  = QGridLayout()
        row = 0
        for car in account.car:

                parts = car['parts']
                engine = car['engine']

                button = QPushButton(parts, self)
                button.setFixedWidth(40)
                inner_layout.addWidget(button,row,0,Qt.AlignCenter)# 0 is parts need to add repair button
                button.clicked.connect(lambda: self.on_button_clicked(account))
                
                button.setProperty('driver_index',row)
                button.setProperty('type','parts')
                
                self.main_window.buttons.append(button)
                
                if int(parts.strip('%')) == 100: 
                    button.setEnabled(False)
                button = QPushButton(engine, self)
                button.setFixedWidth(40)
                inner_layout.addWidget(button,row,1,Qt.AlignCenter)# 1 is engine
                button.clicked.connect(lambda: self.on_button_clicked(account))
                button.setProperty('driver_index',row)
                button.setProperty('type','engine')
                self.main_window.buttons.append(button)
                if int(engine.strip('%')) == 100:
                    button.setEnabled(False)              

                row+=1         
        self.main_window.main_grid.addLayout(inner_layout, self.account_row, 3,alignment=Qt.AlignTop)
    def display_strat(self,full_strategy):
            strategy = full_strategy['strat']
            pits = int(full_strategy['pits'])
            
            inner_layout  = QGridLayout()
            column = 1

            # [tyre,lap,fuel]
            for arr in strategy[:pits+1]:
                img_label = QLabel()
                label = QLabel(arr[1])
                label.setStyleSheet("color: white")
                tyre_img = QPixmap(f'tyres/{arr[0]}.png')
                img_label.setPixmap(tyre_img)
                img_label.setFixedHeight(22)
                img_label.setFixedWidth(22)
                img_label.setScaledContents(True)
                inner_layout.addWidget(img_label,0,column)
                inner_layout.addWidget(label,0,column,Qt.AlignCenter)
                column += 1
            return inner_layout
    ## setup/strategy data
    def load_strategy(self,account):

        inner_layout  = QGridLayout()
        row = 0
        strategy_data = account.strategy
        if strategy_data != False:
            setups_elements = []
            for driver in strategy_data:
                    self.main_window.setups.append(driver)
                    race_text = QLabel(account.strategy[0]['raceName'])
                    race_text.setFixedWidth(100)
                    inner_layout.addWidget(race_text,row,0)# 0 next race

                    inner_setup_layout  = QGridLayout()
                    ride_field = QLineEdit()
                    ride_field.setInputMask('99')
                    ride_field.setFixedWidth(30) 
                    ride_field.setText(str(driver['ride']))
                    aero_field = QLineEdit()
                    aero_field.setInputMask('99')
                    aero_field.setFixedWidth(30) 
                    aero_field.setText(str(driver['aero']))
                    select_box = QComboBox()
                    select_box.addItem("Soft")
                    select_box.addItem("Neutral")
                    select_box.addItem("Firm")
                    select_box.setCurrentIndex(int(driver['suspension'])-1) #index 0-2
                    select_box.setFixedWidth(60) 

                    next_time = QLabel(account.h_until_next_race())
                    next_time.setFixedWidth(30) 
                    inner_setup_layout.addWidget(next_time,0,1)
                    
                    inner_setup_layout.addWidget(select_box,0,2)
                    inner_setup_layout.addWidget((ride_field),0,3,Qt.AlignLeft)
                    inner_setup_layout.addWidget((aero_field),0,4,Qt.AlignLeft)
                    self.main_window.setups.append(inner_setup_layout)
                    inner_layout.addLayout(inner_setup_layout,row,1)# 1 setup  

                    button = QPushButton()
                    button.setIcon(QIcon('edit_icon.png'))
                    
                    button.setProperty('driver_index',row)
                    button.setProperty('type','strategy')

                    button.clicked.connect(lambda: self.on_modify_strategy(account))
                    inner_layout.addWidget(button,row,2)
                    self.main_window.buttons.append(button)
                    
                    strategy_grid = self.display_strat(driver)
                    inner_layout.addLayout(strategy_grid,row,3)  
                    
                    driver['pyqt_elemnt'] = [inner_layout,strategy_grid,row]
                    
                           
                    #inner_layout.addWidget(QLabel(display_strat(driver)),row,2)# 1 is engine
                    row+=1
                    setups_elements.append([select_box,ride_field,aero_field])         
            self.main_window.main_grid.addLayout(inner_layout, self.account_row, 4,Qt.AlignLeft)
            account.save_setup_field(setups_elements)    

    def initUI(self):
        self.setWindowTitle('iGPeasy')
        self.setLayout(self.main_window.main_grid)
        
        driver_rows = 2
        car_rows = 2

        self.account_row = 1

        #add row for every new account self.grid_layout

        for account in self.valid_accounts:
   
            inner_layout  = QGridLayout()

            account_text_label = QLabel(account.username)
            account_text_label.setFixedHeight(22)
            inner_layout.addWidget(account_text_label,0,0)
            self.main_window.main_grid.addLayout(inner_layout, self.account_row, 0,alignment=Qt.AlignTop)
            

            self.load_drivers(account)
        
            self.load_car(account)
            self.load_misc(account)
            self.load_strategy(account)
            self.account_row+=1
            
            ## backgroud color
            panel = QWidget()
            self.main_window.driver_tab.addWidget(panel, driver_rows, 0,2,5)    
            panel.setStyleSheet("background-color: grey;")    


        
        self.show()
    
    def on_setup_clicked(self):  
        for account in self.valid_accounts:
            if account.has_league:
                suggested_setup = CarSetup(account.strategy[0]['trackCode'],account.staff['drivers'][0]['height'],account.strategy[0]['tier'])
                
                ride = str(suggested_setup.ride)
                aero = str(suggested_setup.wing)
                suspension = suggested_setup.suspension

                account.setups[0][0].setCurrentIndex(suspension)
                account.setups[0][1].setText(ride)
                account.setups[0][2].setText(aero)

                account.strategy[0]['ride'] = ride
                account.strategy[0]['aero'] = aero
                
                account.strategy[0]['suspension'] = suspension +1

                ## if 2 cars 
                if len(account.setups) > 1:
                    suggested_setup = CarSetup(account.strategy[0]['trackCode'],account.staff['drivers'][1]['height'],account.strategy[0]['tier'])

                    ride = str(suggested_setup.ride)
                    aero = str(suggested_setup.wing)
                    suspension = suggested_setup.suspension

                    account.setups[1][0].setCurrentIndex(suspension)
                    account.setups[1][1].setText(ride)
                    account.setups[1][2].setText(aero)

                    account.strategy[1]['ride'] = ride
                    account.strategy[1]['aero'] = aero
                    account.strategy[1]['suspension'] = suspension +1

    def on_modify_strategy(self,account):
        sender_button = self.sender()  # Get the button that was clicked
        index = self.main_window.buttons.index(sender_button)
        
        number = sender_button.property('driver_index')
        type = sender_button.property('type')
        
        popup = PopupWindow(self,index,{'type': type,'number':number,'account':account})
        popup.exec_()         

    def on_save_strategy(self):
       for account in self.valid_accounts:
            if account.has_league:
                account.save_strategy()           
    def on_button_clicked(self,account):            
        sender_button = self.sender()  # Get the button that was clicked
        index = self.main_window.buttons.index(sender_button)

        number = sender_button.property('driver_index')
        type = sender_button.property('type')

        
        popup = PopupWindow(self,index,{'type':type,'account':account,'number':number})
        popup.exec_()
    def on_modify_research(self,account):        
        sender_button = self.sender()  # Get the button that was clicked
        index = self.main_window.buttons.index(sender_button)
        type = sender_button.property('type')
        popup = PopupWindow(self,index,{'type':type,'account':account,'number':0})
        popup.exec_()
    
    def on_sponsor_click(self,account):        
        sender_button = self.sender()  # Get the button that was clicked
        index = self.main_window.buttons.index(sender_button)
        type = sender_button.property('type')
        popup = PopupWindow(self,index,{'type':type,'account':account,'number':0})
        popup.exec_()                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = iGPeasyWindow()
    sys.exit(app.exec_())




