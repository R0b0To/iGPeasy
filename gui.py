from tool_api import iGP_account
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel,QPushButton,QGridLayout,QWidget, QComboBox,QLineEdit,QRadioButton,QHBoxLayout
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
        #inner_layout.addWidget(QLabel('Train'),1,3)
        inner_layout.addWidget(QLabel('Health'),1,3)
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
        inner_layout.addWidget(QLabel(''), 0, 1,)
        inner_layout.addWidget(button, 0, 2)
        inner_layout.addWidget(button_save, 0, 3)
        self.buttons.append(button)
        self.buttons.append(button_save)
        
        button_save.clicked.connect(lambda: self.parent.on_save_strategy())

        button.clicked.connect(lambda: self.parent.on_setup_clicked())
        
        race_text = QLabel('Next')
        race_text.setFixedWidth(100)
        inner_layout.addWidget(race_text,1,0)
        time_text = QLabel('In:')
        time_text.setFixedWidth(30)
        inner_layout.addWidget(time_text,1,1,Qt.AlignLeft)
        setup_text = QLabel('Setup')
        setup_text.setFixedWidth(130)
        inner_layout.addWidget(setup_text,1,2,Qt.AlignLeft)
        inner_layout.addWidget(QLabel('Strategy'),1,3,Qt.AlignLeft)
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
        self.number = config['number']
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
        elif self.type == 'driver':
            self.init_driver_popup()      

        
    def init_parts_popup(self):
        self.setWindowTitle('Parts repair')
        self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        
        label = QLabel(f"You have {self.account.car[0]['total_parts']} parts \n Repair cost: {self.account.car[self.number]['repair_cost']} part(s)")
        button = QPushButton('repair', self)
        
        button.clicked.connect(self.update_main_button)
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
    def init_driver_popup(self):
        self.setWindowTitle('training') 
        #self.setFixedSize(400, 100)
        layout = QVBoxLayout()
        attributes_grid_layout  = QGridLayout()
        driving_button = QPushButton('Driving', self)
        mental_button = QPushButton('Mental', self)
        physical_button = QPushButton('Physical', self)


        print('training of: ',self.account.staff['drivers'][self.number])
        
        driver = self.account.staff['drivers'][self.number]
        
        attributes_grid_layout.addWidget(driving_button,0,0)
        attributes_grid_layout.addWidget(mental_button,0,1)
        attributes_grid_layout.addWidget(physical_button,0,2)
        extra_driver_info = self.account.driver_info(driver['id'])



        self.talent =  QLabel(f"{driver['attributes'][1]} Talent")
        self.fast = QLabel(f"{driver['attributes'][2]} Fast")
        self.slow = QLabel(f"{driver['attributes'][3]} Slow")
        self.defending = QLabel(f"{driver['attributes'][4]} Defending")
        self.attacking = QLabel(f"{driver['attributes'][5]} Attacking")
        
        self.composure = QLabel(f"{driver['attributes'][6]} Composure")
        self.experience = QLabel(f"{driver['attributes'][7]} Experience")
        self.focus = QLabel(f"{driver['attributes'][8]} Focus")
        self.morale = QLabel(f"{driver['attributes'][9]} Morale")
        self.knowledge = QLabel(f"{driver['attributes'][10]} Knowledge")

        self.stamina = QLabel(f"{driver['attributes'][11]} Stamina")
        self.health = QLabel(f"{driver['attributes'][12]} Health")
        self.bmi_label = QLabel(f"{driver['attributes'][14]} BMI")
        self.height_text = QLabel(f"{driver['attributes'][13]} Height")
        self.weight = QLabel(f"{extra_driver_info['attributes']['weight']} Weight")

        self.attributes = [self.talent,self.fast,self.slow,self.defending,self.attacking,self.composure,self.experience,self.focus,self.morale,self.knowledge,self.stamina,self.health,self.bmi_label,self.height_text,self.weight]
        
        attributes_grid_layout.addWidget(self.talent,1,0)
        attributes_grid_layout.addWidget(self.fast,2,0)
        attributes_grid_layout.addWidget(self.slow,3,0)
        attributes_grid_layout.addWidget(self.defending,4,0)
        attributes_grid_layout.addWidget(self.attacking,5,0)

        attributes_grid_layout.addWidget(self.composure,1,1)
        attributes_grid_layout.addWidget(self.experience,2,1)
        attributes_grid_layout.addWidget(self.focus ,3,1)
        attributes_grid_layout.addWidget(self.morale,4,1)
        attributes_grid_layout.addWidget(self.knowledge,5,1)

        attributes_grid_layout.addWidget(self.stamina ,1,2)
        attributes_grid_layout.addWidget(self.health,2,2)
        
        self.bmi_label.setStyleSheet(f"color: {extra_driver_info['attributes']['bmi_color']};")
        attributes_grid_layout.addWidget(self.bmi_label,3,2)
        attributes_grid_layout.addWidget(self.height_text,4,2)
        attributes_grid_layout.addWidget(self.weight,5,2)
        

        strength_layout = QHBoxLayout()
        options = [1, 2, 3, 5, 10]
        self.radio_buttons = []
        for option in options:
            radio_button = QRadioButton(str(option))
            #radio_button.clicked.connect(self.on_radio_button_clicked)
            strength_layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        all_button = QPushButton('All', self)
        
        self.radio_buttons[-1].setChecked(True)
        
        for button in [driving_button,mental_button,physical_button,all_button]:
         button.clicked.connect(self.train_driver)

        layout.addLayout(strength_layout)
        layout.addWidget(all_button)
        layout.addLayout(attributes_grid_layout)

        self.setLayout(layout)
    
    def init_contract_popup(self):
        self.setWindowTitle('Contract')
        self.setFixedSize(200, 100)
        driver_info = self.account.staff['drivers'][self.number]
        layout = QVBoxLayout()
        label = QLabel(f"{driver_info['contract']} - {driver_info['salary']}")

        button = QPushButton('extend', self)
        contract_info = self.account.driver_info(driver_info['id'])['contract']

        button.clicked.connect(self.update_main_button)
        layout.addWidget(label)
        layout.addWidget(QLabel(f"{contract_info['duration']} races - New salary: {contract_info['cost']}"))
        layout.addWidget(button)
        self.setLayout(layout)

    def init_engine_repair_popup(self):
        self.setWindowTitle('Parts repair')
        self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        # cars share same engines and parts count number
        label = QLabel(f"You have {self.account.car[0]['total_engines']}, restocking in: {self.account.car[0]['restock']}")
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
        
        
        car_strategy = self.account.strategy[self.number]
        
        
        pits = int(car_strategy['pits'])
        select_box.setCurrentIndex((pits)-1)
        select_box.setFixedWidth(80) 
        
        def on_pit_box_changed(index):
            car_strategy['pits'] = index+1
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
        tyre_map_text = {'SS':ss,'S':s,'M':m,'H':h,'I':i,'W':w}
        tyre_map = {'SS':0,'S':1,'M':2,'H':3,'I':4,'W':5}
        tyre_map_rev = {0:'SS',1:'S',2:'M',3:'H',4:'I',5:'W'}
        self.elements = []
        self.stint_laps = 0
        for index,value in enumerate(range(5), start=1):
          
          selected_tyre = car_strategy['strat'][index-1][0]
          
          if index == 1:
            stint_label = QLabel(f"Start")
          else:
            stint_label = QLabel(f"{index-1}")    
          fuel_field = QLineEdit()
          fuel_field.setInputMask('999')
          fuel_field.setMaximumWidth(30)
          fuel_field.setText(car_strategy['strat'][index-1][2])
          laps_label = QLabel(f"{int(int(car_strategy['strat'][index-1][2])/fuel_lap*100)/100}")
          
          wear_label = QLabel(f"{Track.stint_wear_calc(tyre_map_text[selected_tyre],car_strategy['strat'][index-1][1],self.account.strategy[0]['trackCode'])}")
          
          tyre_select_ele = tyre_select()
         
          if index < int(car_strategy['pits'])+2:
                    self.stint_laps += int(car_strategy['strat'][index-1][1])  

          
          def on_tyre_changed(index, column):
            car_strategy['strat'][column][0] = tyre_map_rev[index]
            tyre_wear = tyre_map_text[tyre_map_rev[index]]
            laps = car_strategy['strat'][column][1]
            track = self.account.strategy[0]['trackCode']
            self.elements[column][4].setText(Track.stint_wear_calc(tyre_wear,laps,track))
          
          def update_total_laps():
            pit = int(car_strategy['pits'])
            total_laps = 0     
            for index, stint in enumerate (car_strategy['strat'],start=0):
                if index < pit+1:
                    total_laps += int(stint[1])       

            self.total_laps.setText(f"{total_laps}/{self.account.strategy[0]['raceLaps']}") 
          
          def on_fuel_changed(fuel, column):
            if fuel != '':
                laps = (int(int(fuel)/fuel_lap*100)/100)
                self.elements[column][3].setText(str(laps))
                #tyre wear
                
                tyre_wear = tyre_map_text[tyre_map_rev[self.elements[column][1].currentIndex()]]
                track = self.account.strategy[0]['trackCode']
                car_strategy['strat'][column][2] = fuel
                laps = car_strategy['strat'][column][1] = str(math.floor(laps))
                self.elements[column][4].setText(Track.stint_wear_calc(tyre_wear,laps,track))

                update_total_laps()


          tyre_select_ele.setCurrentIndex(tyre_map[selected_tyre])
          stints_grid_layout.addWidget(stint_label,1,index,Qt.AlignLeft)
          stints_grid_layout.addWidget(tyre_select_ele,2,index,Qt.AlignLeft)
          stints_grid_layout.addWidget(fuel_field,3,index,Qt.AlignLeft)
          stints_grid_layout.addWidget(laps_label,4,index,Qt.AlignLeft)
          
          stints_grid_layout.addWidget(wear_label,5,index,Qt.AlignLeft)
          self.elements.append([stint_label,tyre_select_ele,fuel_field,laps_label,wear_label])
          if index > pits+1:
             for ele in [stint_label,tyre_select_ele,fuel_field,laps_label,wear_label]:
                 ele.hide()
          tyre_select_ele.currentIndexChanged.connect(lambda index, column=index-1: on_tyre_changed(index,column)) 
          fuel_field.textChanged.connect(lambda index, column=index-1: on_fuel_changed(index,column))   
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
    
    def train_driver(self):
        driver = self.account.staff['drivers'][self.numbers]
        for radio_button in self.radio_buttons:
            if radio_button.isChecked():
                intensity = int(radio_button.text())
                break
        print(self.sender().text())
        train_type_map = {'Driving':'ability','Mental':'mental','Physical':'physical','All':'all'} 
        train_type = self.sender().text()
        print(f"{driver['id']} training {train_type} x{intensity}")
        self.account.train_driver(driver['id'],intensity,train_type_map[train_type])
         

    def update_main_strategy(self):
        
        new_strat = self.parent().display_strat(self.account.strategy[self.number])
        
        index = self.account.strategy[self.number]['pyqt_elemnt'][2]

        for i in reversed(range(self.account.strategy[self.number]['pyqt_elemnt'][1].count())):
                self.account.strategy[self.number]['pyqt_elemnt'][1].itemAt(i).widget().deleteLater() 

        self.account.strategy[self.number]['pyqt_elemnt'][1] = new_strat
        self.account.strategy[self.number]['pyqt_elemnt'][0].addLayout(self.account.strategy[self.number]['pyqt_elemnt'][1], index, 3)
        self.accept()
        

        # check if repaired
    def update_main_button(self):

        if self.type == 'parts':
           self.response = self.account.request_parts_repair(self.account.car[self.number])
           self.account.car[0]['total_parts'] -= self.account.car[self.number]['repair_cost']
        elif self.type == 'engine':
           self.response = self.account.request_engine_repair(self.account.car[self.number])
        elif self.type == 'contract':
           self.response = self.account.extend_contract_driver(self.account.staff['drivers'][self.number])
        new_value = self.response  # Here you can retrieve the value you want
        
        self.parent().main_window.buttons[self.index].setText(new_value)
        self.parent().main_window.buttons[self.index].setEnabled(False)  
        self.accept()     