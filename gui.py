from tool_api import iGP_account
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel,QPushButton,QGridLayout,QWidget, QComboBox,QLineEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from track import Track
import math

class iGPWindow(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.main_grid = QGridLayout()
        self.buttons = []
        self.fields = []
        self.setups = []
        self.init_window()

    #def set_setup_function():


    def init_accout_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel(''), 0, 0,)
        inner_layout.addWidget(QLabel('Accounts'),1,0)
        self.account_tab = inner_layout
        return inner_layout
    def init_driver_tab(self):
        inner_layout  = QGridLayout()
        self.panel = QWidget()
        inner_layout.addWidget(self.panel , 0, 0,2,5)
        self.panel.setStyleSheet("background-color: grey;")
        #inner_layout.setColumnStretch(3, 1)
        driver_header = QLabel('Drivers')
        driver_header.setFixedWidth(90)
        inner_layout.addWidget(driver_header, 0, 0)
        inner_layout.addWidget(QLabel('Name'),1,0)
        inner_layout.addWidget(QLabel('Height'),1,1)
        inner_layout.addWidget(QLabel('Contract'),1,2)
        inner_layout.addWidget(QLabel('Train'),1,3)
        inner_layout.addWidget(QLabel('Health'),1,4)
        self.driver_tab = inner_layout
        return inner_layout
    def init_car_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel('Car'), 0, 0)
        inner_layout.addWidget(QLabel('Parts'),1,0)
        inner_layout.addWidget(QLabel('Engine'),1,1)
        self.car_tab = inner_layout
        return inner_layout
    def init_race_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel('Race'), 0, 0,)
        button = QPushButton('Suggested', self)
        button_save = QPushButton('Save setup/strategy', self)
        #button.setFixedWidth(60)
        inner_layout.addWidget(button, 0, 1)
        inner_layout.addWidget(button_save, 0, 2)
        self.buttons.append(button)
        self.buttons.append(button_save)
        
        button_save.clicked.connect(lambda: self.parent.on_save_strategy())

        button.clicked.connect(lambda: self.parent.on_setup_clicked())
        
        race_text = QLabel('Next')
        race_text.setFixedWidth(100)
        inner_layout.addWidget(race_text,1,0)
        setup_text = QLabel('Setup')
        setup_text.setFixedWidth(130)
        inner_layout.addWidget(setup_text,1,1,Qt.AlignLeft)
        inner_layout.addWidget(QLabel('Strategy'),1,2,Qt.AlignLeft)
        self.race_tab = inner_layout
        return inner_layout   
              
    def init_window(self):
        
        self.setWindowTitle("iGPeasy")
        self.main_grid.addLayout(self.init_accout_tab(), 0, 0,alignment=Qt.AlignTop)
        self.main_grid.addLayout(self.init_driver_tab(), 0, 1,alignment=Qt.AlignTop)
        self.main_grid.addLayout(self.init_car_tab()   , 0, 2,alignment=Qt.AlignTop)
        self.main_grid.addLayout(self.init_race_tab()  , 0, 3,alignment=Qt.AlignLeft)

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
        elif self.type == 'strategy':
            self.init_strategy_popup()
        elif self.type == 'contract':
            self.init_contract_popup()    

        
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
    
    def init_contract_popup(self):
        self.setWindowTitle('Contract')
        self.setFixedSize(200, 100)
        # fetch driver info then extend on confirm
        layout = QVBoxLayout()
        label = QLabel(f"{self.data['contract']} - {self.data['salary']}")
        #label.setAlignment(Qt.AlignCenter)
        button = QPushButton('extend', self)
        contract_info = self.account.driver_info(self.data['id'])

        button.clicked.connect(self.update_main_button)
        layout.addWidget(label)
        layout.addWidget(QLabel(f"{contract_info[0]} races - New salary: {contract_info[1]}"))
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
    
    def init_strategy_popup(self):
        def set_size(img_label):
            img_label.setFixedHeight(22)
            img_label.setFixedWidth(22)
            img_label.setScaledContents(True)

        self.setWindowTitle('Strategy')
        grid_layout  = QGridLayout()
        
        tyre_SS_img = QLabel()
        tyre_S_img = QLabel()
        tyre_M_img = QLabel()
        tyre_H_img = QLabel()
        tyre_I_img = QLabel()
        tyre_W_img = QLabel()

        for img in [tyre_SS_img,tyre_S_img,tyre_M_img,tyre_H_img,tyre_I_img,tyre_W_img]:
            set_size(img)
        
        tyreWearFactors = {'SS': 2.14,'S': 1.4,'M': 1,'H': 0.78}
        trackCode = self.account.strategy[0]['trackCode']
        
        #find tier by total laps
        tier = Track().info[trackCode][self.account.strategy[0]['raceLaps']]
        print(tier)
        
        
        ss = "{:.1f}".format((1.43 * self.account.car[0]['tyre_economy'] ** -0.0778) * (0.00364 * Track().info[trackCode]['wear'] + 0.354) * Track().info[trackCode]['length'] * 1.384612 * Track().multipliers[tier] * tyreWearFactors['SS'])
        s = "{:.1f}".format((1.43 * self.account.car[0]['tyre_economy'] ** -0.0778) * (0.00364 * Track().info[trackCode]['wear'] + 0.354) * Track().info[trackCode]['length'] * 1.384612 * Track().multipliers[tier] * tyreWearFactors['S'])
        m = "{:.1f}".format((1.43 * self.account.car[0]['tyre_economy'] ** -0.0778) * (0.00364 * Track().info[trackCode]['wear'] + 0.354) * Track().info[trackCode]['length'] * 1.384612 * Track().multipliers[tier] * tyreWearFactors['M'])
        h = "{:.1f}".format((1.43 * self.account.car[0]['tyre_economy'] ** -0.0778) * (0.00364 * Track().info[trackCode]['wear'] + 0.354) * Track().info[trackCode]['length'] * 1.384612 * Track().multipliers[tier] * tyreWearFactors['H'])
        i = "{:.1f}".format((1.43 * self.account.car[0]['tyre_economy'] ** -0.0778) * (0.00364 * Track().info[trackCode]['wear'] + 0.354) * Track().info[trackCode]['length'] * 1.384612 * Track().multipliers[tier] * tyreWearFactors['M'])
        w = "{:.1f}".format((1.43 * self.account.car[0]['tyre_economy'] ** -0.0778) * (0.00364 * Track().info[trackCode]['wear'] + 0.354) * Track().info[trackCode]['length'] * 1.384612 * Track().multipliers[tier] * tyreWearFactors['M'])
        
        tyre_SS_text = QLabel(f"{ss}%")
        tyre_S_text = QLabel(f"{s}%")
        tyre_M_text = QLabel(f"{m}%")
        tyre_H_text = QLabel(f"{h}%")
        tyre_I_text = QLabel(f"{i}%")
        tyre_W_text = QLabel(f"{w}%")
        
        tyre_SS_img.setPixmap(QPixmap(f'tyres/SS.png'))
        tyre_S_img.setPixmap(QPixmap(f'tyres/S.png'))
        tyre_M_img.setPixmap(QPixmap(f'tyres/M.png'))
        tyre_H_img.setPixmap(QPixmap(f'tyres/H.png'))
        tyre_I_img.setPixmap(QPixmap(f'tyres/I.png'))
        tyre_W_img.setPixmap(QPixmap(f'tyres/W.png'))
        
        grid_layout.addWidget(tyre_SS_img,0,0)
        grid_layout.addWidget(tyre_S_img,0,1)
        grid_layout.addWidget(tyre_M_img,0,2)
        grid_layout.addWidget(tyre_H_img,0,3)
        grid_layout.addWidget(tyre_I_img,0,4)
        grid_layout.addWidget(tyre_W_img,0,5)
        
        grid_layout.addWidget(tyre_SS_text,1,0)
        grid_layout.addWidget(tyre_S_text,1,1)
        grid_layout.addWidget(tyre_M_text,1,2)
        grid_layout.addWidget(tyre_H_text,1,3)
        grid_layout.addWidget(tyre_I_text,1,4)
        grid_layout.addWidget(tyre_W_text,1,5)

        select_box = QComboBox()
        select_box.addItem("1 pit stop")
        select_box.addItem("2 pit stops")
        select_box.addItem("3 pit stops")
        select_box.addItem("4 pit stops")
        pits = int(self.data['pits'])
        select_box.setCurrentIndex((pits)-1)
        select_box.setFixedWidth(80) 
        
        def on_pit_box_changed(index):
            self.data['pits'] = index+1
            for i in range(5):
                if index+1 < i:
                    for ele in self.elements[i]:
                        ele.hide()
                else:
                    for ele in self.elements[i]:
                        ele.show()
            update_total_laps()
        select_box.currentIndexChanged.connect(on_pit_box_changed)
        

        def tyre_select():
            tyre_select_box = QComboBox()
            for option in ['tyres/SS.png','tyres/S.png','tyres/M.png','tyres/H.png','tyres/I.png','tyres/W.png']:
                tyre_select_box.addItem(QIcon(option), '',Qt.AlignCenter)
                tyre_select_box.setMaximumWidth(40)
            
               
            return tyre_select_box    

        stints_grid_layout  = QGridLayout()
        fuel_lap = int(Track.fuel_calc(self.account.car[0]['fuel_economy']) * Track().info[self.account.strategy[0]['trackCode']]['length'] *100) /100
        layout = QVBoxLayout()
        stints_grid_layout.addWidget(select_box,0,0,1,2,Qt.AlignCenter)
        stints_grid_layout.addWidget(QLabel(f'Fuel/lap: {fuel_lap}'),0,2,1,2,Qt.AlignLeft)
        stints_grid_layout.addWidget(QLabel('Fuel'),3,0)
        stints_grid_layout.addWidget(QLabel('Laps'),4,0)
        
        tyre_map = {'SS':0,'S':1,'M':2,'H':3,'I':4,'W':5}
        tyre_map_rev = {0:'SS',1:'S',2:'M',3:'H',4:'I',5:'W'}
        self.elements = []
        self.stint_laps = 0
        for index,value in enumerate(range(5), start=1):
          if index == 1:
            stint_label = QLabel(f"Start")
          else:
            stint_label = QLabel(f"{index-1}")    
          fuel_field = QLineEdit()
          fuel_field.setInputMask('999')
          fuel_field.setMaximumWidth(30)
          fuel_field.setText(self.data['strat'][index-1][2])
          laps_label = QLabel(f"{int(int(self.data['strat'][index-1][2])/fuel_lap*100)/100}")
          tyre_select_ele = tyre_select()
         
          if index < int(self.data['pits'])+2:
                    self.stint_laps += int(self.data['strat'][index-1][1])  

          
          def on_tyre_changed(index, column):
            combobox = self.sender()
            selected_option = combobox.currentText()
            print(f"ComboBox at column {column} changed to: {selected_option}")
            self.data['strat'][column][0] = tyre_map_rev[index]
          def update_total_laps():
            pit = int(self.data['pits'])
            total_laps = 0     
            for index, stint in enumerate (self.data['strat'],start=0):
                if index < pit+1:
                    total_laps += int(stint[1])       

            self.total_laps.setText(f"{total_laps}/{self.account.strategy[0]['raceLaps']}") 
          
          def on_fuel_changed(fuel, column):
            if fuel != '':
                laps = (int(int(fuel)/fuel_lap*100)/100)
                self.elements[column][3].setText(str(laps))
                print(f"fuel at {column} changed to: {fuel}")
                self.data['strat'][column][2] = fuel
                self.data['strat'][column][1] = str(math.floor(laps))
                update_total_laps()

 
          
          tyre_select_ele.currentIndexChanged.connect(lambda index, column=index-1: on_tyre_changed(index,column)) 
          fuel_field.textChanged.connect(lambda index, column=index-1: on_fuel_changed(index,column)) 
          tyre_select_ele.setCurrentIndex(tyre_map[self.data['strat'][index-1][0]])
          stints_grid_layout.addWidget(stint_label,1,index,Qt.AlignLeft)
          stints_grid_layout.addWidget(tyre_select_ele,2,index,Qt.AlignLeft)
          stints_grid_layout.addWidget(fuel_field,3,index,Qt.AlignLeft)
          stints_grid_layout.addWidget(laps_label,4,index,Qt.AlignLeft)
          self.elements.append([stint_label,tyre_select_ele,fuel_field,laps_label])
          if index > pits+1:
             for ele in [stint_label,tyre_select_ele,fuel_field,laps_label]:
                 ele.hide()

        layout.addLayout(grid_layout)
        layout.addLayout(stints_grid_layout,Qt.AlignLeft)
        ## add tyre wear
        ## add here total laps of the strategy compared to the race
        confirm_button = QPushButton('Confirm', self)
        confirm_button.clicked.connect(self.update_main_strategy)
        self.total_laps = QLabel(f"{self.stint_laps}/{self.account.strategy[0]['raceLaps']}")
        self.total_laps.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.total_laps)
        layout.addWidget(confirm_button)
        self.setLayout(layout) 
    

    def update_main_strategy(self):
        new_strat = self.parent().display_strat(self.data)
        index = self.data['pyqt_elemnt'][2]

        for i in reversed(range(self.data['pyqt_elemnt'][1].count())):
                self.data['pyqt_elemnt'][1].itemAt(i).widget().deleteLater() 

        self.data['pyqt_elemnt'][1] = new_strat
        self.data['pyqt_elemnt'][0].addLayout(self.data['pyqt_elemnt'][1], index, 3)
        self.accept()
        

        # check if repaired
    def update_main_button(self):

        if self.type == 'parts':
           self.response = self.account.request_parts_repair(self.data)
           self.account.car[0]['total_parts'] -= self.data['repair_cost']
        elif self.type == 'engine':
           self.response = self.account.request_engine_repair(self.data)
        elif self.type == 'contract':
           self.response = self.account.extend_contract_driver(self.data)
        new_value = self.response  # Here you can retrieve the value you want
        
        self.parent().main_window.buttons[self.index].setText(new_value)
        self.parent().main_window.buttons[self.index].setEnabled(False)  
        self.accept()     