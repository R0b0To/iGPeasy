import asyncio
import json
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel,QPushButton,QGridLayout,QWidget, QComboBox,QLineEdit,QRadioButton,QHBoxLayout,QSpinBox,QCheckBox
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

    def init_daily_tab(self):
        inner_layout  = QGridLayout()
        daily_button = QPushButton('Daily')
        daily_button.setFixedWidth(50)
        inner_layout.addWidget(QLabel(''), 0,0)
        inner_layout.addWidget(daily_button, 1, 0)
        daily_button.clicked.connect(lambda: self.parent.get_daily_from_all())
        self.daily_tab = inner_layout
        return inner_layout
    def init_info_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel(''), 0, 0,)
        inner_layout.addWidget(QLabel('Balance'),1,0)
        self.account_tab = inner_layout
        return inner_layout
    
    def init_accout_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel(''), 0, 0,)
        inner_layout.addWidget(QLabel('Accounts'),1,0)
        self.account_tab = inner_layout
        return inner_layout
    def init_driver_tab(self):
        inner_layout  = QGridLayout()
        #self.panel = QWidget()
        #inner_layout.addWidget(self.panel , 0, 0,2,5)
        #self.panel.setStyleSheet("background-color: grey;")
        #inner_layout.setColumnStretch(3, 1)
        driver_header = QLabel('Drivers')
        driver_header.setFixedWidth(90)
        inner_layout.addWidget(driver_header, 0, 0)
        inner_layout.addWidget(QLabel('Name'),1,0)
        #inner_layout.addWidget(QLabel('Height'),1,1)
        inner_layout.addWidget(QLabel('Contract'),1,1)
        #inner_layout.addWidget(QLabel('Train'),1,3)
        #inner_layout.addWidget(QLabel('Health'),1,3)
        self.driver_tab = inner_layout
        return inner_layout
    def init_car_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel('Car'), 0, 0)
        button = QPushButton('Parts', self)
        button.setFixedWidth(50)
        inner_layout.addWidget(button,1,0)
        button.clicked.connect(lambda: self.parent.repair_all_parts())
        inner_layout.addWidget(QLabel('Engine'),1,1)
        self.car_tab = inner_layout
        return inner_layout
    def init_misc_tab(self):
        inner_layout  = QGridLayout()
        inner_layout.addWidget(QLabel('Research'), 1, 0)
        inner_layout.addWidget(QLabel('Sponsor'), 1, 1)
        inner_layout.addWidget(QLabel(''), 0,0)
        self.research_tab = inner_layout
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
        self.main_grid.addLayout(self.init_info_tab(), 0, 1,alignment=Qt.AlignTop)
        self.main_grid.addLayout(self.init_daily_tab(), 0, 2,alignment=Qt.AlignTop)
        self.main_grid.addLayout(self.init_driver_tab(), 0, 3,alignment=Qt.AlignTop)
        self.main_grid.addLayout(self.init_misc_tab(), 0, 4,alignment=Qt.AlignTop)
        self.main_grid.addLayout(self.init_car_tab()   , 0, 5,alignment=Qt.AlignTop)
        self.main_grid.addLayout(self.init_race_tab()  , 0, 6,alignment=Qt.AlignLeft)

class PopupWindow(QDialog):
    def __init__(self, parent=None, index= None, config=None, optional=None):
        super().__init__(parent)
        
        if index is None and config is None and optional is not None:
            self.data = optional
            self.type = 'load'
        else:
            self.number = config['number']
            self.type = config['type']
            self.account = config['account']
            self.index = index 
        init_functions ={
                         'parts': self.init_parts_popup,
                         'engine': self.init_engine_repair_popup,
                         'strategy': self.init_strategy_popup,
                         'contract': self.init_contract_popup,
                         'research': self.init_research_popup,
                         'sponsor': self.init_sponsor_popup,
                         'load': self.init_load_popup
                        }
        if self.type in init_functions:
            init_functions[self.type]()      
    def on_save_pressed(self):
        def hash_code(string):
            hash_value = 0
            for char in string:
                code = ord(char)
                hash_value = ((hash_value << 5) - hash_value) + code
                hash_value = hash_value & 0xffffffff  # Convert to 32-bit integer
            return hash_value
        tyre_map_rev = {0:'SS',1:'S',2:'M',3:'H',4:'I',5:'W'}
        pit_stop = self.strategy_pits.currentIndex()+1
        save = {'stints':{},
                "length": str(self.tier) ,
                "track": str(self.trackCode),
                "laps": {
                    "total": int(self.account.strategy[0]['raceLaps']),
                    "doing": 0
                }}
        doing_laps = 0
        for i in range(pit_stop+1):
            lap = math.floor(float(self.elements[i][3].text()))
            doing_laps+=lap
            tyre =  f"ts-{tyre_map_rev[self.elements[i][1].currentIndex()]}"
            save['stints'][str(i)] = {'tyre':tyre,'laps':str(lap),'push':3}
        save['laps']['doing'] = int(doing_laps)
        save_id = hash_code(str(save))
        
        
        with open('save.json', 'r') as json_file:
            save_list = json.load(json_file)
        
        save_list['save'][self.trackCode][save_id] = save   
        
        with open('save.json', 'w') as f:
            json.dump(save_list, f)    

    
    def on_load_pressed(self):
        strategy_popup = PopupWindow(self,optional=self.valid_strat_layouts)
        strategy_popup.exec_()

    def init_load_popup(self):
        mainlayout = QGridLayout()
        for row,strat in enumerate(self.data):
            strategy_layout = self.parent().parent().display_strat(strat)
            load_button = QPushButton('load')
            load_button.clicked.connect(self.load_strategy)
            load_button.setProperty('strat',strat)
            mainlayout.addWidget(load_button,row,0)  
            mainlayout.addLayout(strategy_layout,row,1)    
          
        self.setLayout(mainlayout)
    def load_strategy(self):
        
        self.setWindowTitle('load strategy')
        self.accept()
        strategy_window = self.parent()
        strategy_to_load = self.sender().property('strat')
        strategy_window.strategy_pits.setCurrentIndex(strategy_to_load['pits']-1)
        
        tyre_map = {'SS':0,'S':1,'M':2,'H':3,'I':4,'W':5}


        for i,stint in enumerate(strategy_to_load['strat']):
            #in case the imported strategy have more than 4 pit stops
            if i < 5:
                stint_fuel = int(stint[1]) * strategy_window.fuel_lap
                ## to be replaced by self.elements[]
                if strategy_window.fuel_rules != '0':
                    strategy_window.stint_fuel[i].setValue(math.ceil(stint_fuel)) 
                else:
                    strategy_window.elements[i][3].setValue(int(stint[1]))      
                strategy_window.stint_tyre[i].setCurrentIndex(tyre_map[stint[0]])

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
    
    def init_sponsor_popup(self):
        self.setWindowTitle('sponsor')

        grid_layout  = QGridLayout()
        
        label1 = QLabel(f"Primary Sponsor")
        label2 = QLabel(f"Secondary Sponsor")
        grid_layout.addWidget(label1,0,0)
        grid_layout.addWidget(label2,0,1)
        comboboxes = []
        ids = []
        if self.account.sponsors['s1']['income'] != '0':
            grid_layout.addWidget(QLabel(self.account.sponsors['s1']['income']),1,0)
            grid_layout.addWidget(QLabel(self.account.sponsors['s1']['bonus']),2,0)
            grid_layout.addWidget(QLabel(self.account.sponsors['s1']['expire']),3,0)
        else:
            loop = asyncio.get_event_loop()
            income_list, bonus_list,id_list = loop.run_until_complete(self.account.pick_sponsor(1))
            
            combo1 = QComboBox()
            ids.append(id_list)
            combined_text = [f"{income_list[i]} , {bonus_list[i]}" for i in  range(min(len(income_list), len(bonus_list)))]
            combo1.addItems(combined_text)
            grid_layout.addWidget(combo1,1,0)
            combo1.setProperty('location',1)
            comboboxes.append(combo1)   
        if self.account.sponsors['s2']['income'] != '0':
            grid_layout.addWidget(QLabel(self.account.sponsors['s2']['income']),1,1)
            grid_layout.addWidget(QLabel(self.account.sponsors['s2']['bonus']),2,1)
            grid_layout.addWidget(QLabel(self.account.sponsors['s2']['expire']),3,1)
        else:
            loop = asyncio.get_event_loop()
            income_list, bonus_list,id_list = loop.run_until_complete(self.account.pick_sponsor(2))
            combo2 = QComboBox()
            ids.append(id_list)
            combined_text = [f"{income_list[i]} , {bonus_list[i]}" for i in  range(min(len(income_list), len(bonus_list)))]
            combo2.addItems(combined_text)
            grid_layout.addWidget(combo2,1,1)
            combo2.setProperty('location',2)
            comboboxes.append(combo2)


        if len(comboboxes) > 0:
            confirm_button = QPushButton('Confirm')
            grid_layout.addWidget(confirm_button,4,0,1,2)

            def send_sponsor_contract():
                for i,combo in enumerate(comboboxes):
                    id  = combo.currentIndex()
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.account.save_sponsor(combo.property('location'),ids[i][id]))
                    self.parent().main_window.buttons[self.index].setText('2/2')
                    #update the new sposnsors
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.account.get_sponsors())
                    
                    self.accept()    

            confirm_button.clicked.connect(send_sponsor_contract)
            

        #button = QPushButton('repair', self)
        
        #button.clicked.connect(self.update_main_button)
        #layout.addWidget(label)
        #layout.addLayp(grid_layout)
        self.setLayout(grid_layout)
    

    def points_handler(self):
        new_total_points = sum(spinbox.value() for spinbox in self.spinboxes)
        sender_spinbox = self.sender()

        if new_total_points <= self.car_total_points:
            # Disconnect the signal to prevent recursive calls
            sender_spinbox.textChanged.disconnect()
            last_value = sender_spinbox.value() - 1
            sender_spinbox.setValue(last_value)

            sender_spinbox.textChanged.connect(self.points_handler)
            self.points += 1
            self.points_label.setText(str(self.points)) 

            self.old_total_points = new_total_points

            return 
        elif new_total_points < self.old_total_points: 
            self.points += 1 
            self.points_label.setText(str(self.points)) 
        else: 
            if self.points > 0:
                self.points -= 1
                self.points_label.setText(str(self.points)) 
            else:
                sender_spinbox.textChanged.disconnect()
                last_value = sender_spinbox.value() - 1
                sender_spinbox.setValue(last_value)
                sender_spinbox.textChanged.connect(self.points_handler)

        self.old_total_points = new_total_points

        for i, gap in enumerate(self.gaps):
            gap.setText(str(int(self.best[i].text()) - self.spinboxes[i].value()))
        self.calculate_points_gain()
    
    def calculate_points_gain(self):
        for i,attribute in enumerate(self.gains):
            if self.is_checked[i]:
                attribute.setText(str(math.ceil(max(0, int(self.gaps[i].text()))*self.power/100)))
            else:
                attribute.setText('0')
        self.power_label.setText(str(self.power))            
    def checkbox_changed(self,state):
        checkbox_index = self.sender().property('index')
        if state == Qt.Checked:
            self.is_checked[checkbox_index] = True
        else:
            self.is_checked[checkbox_index] = False
        check_count   = max(1,self.is_checked.count(True)) 
        self.power = round(self.max_power/check_count,2)   
        self.calculate_points_gain()
    def init_research_popup(self):
        
        self.setWindowTitle('research')
        inner_layout  = QGridLayout()

        #{'car_design':car_design,'teams_design':teams_design,'max':max_design,'points':points,'research_power':research_power}
        
        
 
        loop = asyncio.get_event_loop()
        research_data = loop.run_until_complete(self.account.research_info())
        
        
        self.options = []
        self.total_points = 200
        self.remaining_points = self.total_points
        self.points_label = QLabel(research_data['points'])
        inner_layout.addWidget(self.points_label,0,0)
        inner_layout.addWidget(QLabel('You'),0,1)
        inner_layout.addWidget(QLabel('Gap'),0,2)
        inner_layout.addWidget(QLabel('Best'),0,3)
        self.is_checked = research_data['check']
        check_count = self.is_checked.count(True)
        self.checked = check_count
        self.max_power = research_data['research_power']
        self.power = self.max_power /check_count
        self.points = int(research_data['points'])
        self.power_label = QLabel(str(self.power))
        inner_layout.addWidget(self.power_label,0,5)
        checkboxes = []
        self.spinboxes = []
        self.gaps = []
        self.best = []
        self.gains = []
        #can't go below this
        self.car_total_points = 0
        for i, key in enumerate(['acceleration', 'braking', 'cooling', 'downforce', 'fuel economy', 'handling', 'reliability', 'tyre economy']):
            
            spin_box = QSpinBox()
            line_best = QLineEdit()
            line_gap = QLineEdit()
            line_gain= QLineEdit()
            checkbox = QCheckBox()
            
            for widget in [line_best, line_gap, line_gain, spin_box.lineEdit()]:
                    widget.setReadOnly(True)
            
            checkbox.setChecked(research_data['check'][i])
            line_best.setAlignment(Qt.AlignCenter)
            line_gain.setAlignment(Qt.AlignCenter)
            line_gap.setAlignment(Qt.AlignCenter)
            #spin_box.setProperty('index',i)
            #line_gap.setProperty('index',i)
            checkbox.setProperty('index',i)
            gap = research_data['teams_design'][i] - int(research_data['car_design'][i])
            line_gap.setText(str(gap))
            line_best.setText(str(research_data['teams_design'][i]))
            
            if research_data['check'][i]:
                line_gain.setText(str(math.ceil(gap*self.power/100)))
            else:
                line_gain.setText('0')
            
            spin_box.setProperty("class", "dual-arrows")
            
            spin_box.setFixedWidth(100)
            spin_box.setMaximum(int(research_data['max']))
            spin_box.setAlignment(Qt.AlignCenter) 
            attribute = int(research_data['car_design'][i])
            spin_box.setMinimum(attribute)
            spin_box.setValue(attribute)
            self.car_total_points += attribute
            #spin_box.valueChanged.connect(self.update_points)
            self.options.append((spin_box))
            inner_layout.addWidget(QLabel(key),i+1,0)
            inner_layout.addWidget(spin_box,i+1,1)
            inner_layout.addWidget(line_gap,i+1,2)
            inner_layout.addWidget(line_best,i+1,3)
            inner_layout.addWidget(checkbox,i+1,4)
            inner_layout.addWidget(line_gain,i+1,5)
            spin_box.textChanged.connect(self.points_handler)
            checkbox.stateChanged.connect(self.checkbox_changed)
            checkboxes.append(checkbox)
            self.spinboxes.append(spin_box)
            self.gaps.append(line_gap)
            self.best.append(line_best)
            self.gains.append(line_gain)
        self.old_total_points = self.car_total_points
        self.setStyleSheet("""
             QSpinBox {
              
                text-align: center;
            }
            QSpinBox::up-button {
                min-width: 24px;
                min-height: 24px;
                subcontrol-origin: margin;
                subcontrol-position: right;
              
               
            }
            QSpinBox::down-button {
                min-width: 24px;
                min-height: 24px;
                subcontrol-origin: margin;
                subcontrol-position: left;

            }
        """)
        
        self.setFixedSize(420, 280)
        save_research = QPushButton('Save')
        def on_save_research():
            attribute_keys = ['acceleration', 'braking', 'cooling', 'downforce', 'fuel_economy', 'handling', 'reliability', 'tyre_economy']
            attributes_to_save = ['&c%5B%5D=' + value for value, flag in zip(attribute_keys, self.is_checked) if flag]
            spinbox_values = [spinbox.value() for spinbox in self.options]
            points_spent = ['&{}={}'.format(key, value) for key, value in zip(attribute_keys, spinbox_values)]
            attributes_to_save_string = ''.join(attributes_to_save)
            points_spent_to_save_string = ''.join(points_spent)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.account.save_research(attributes_to_save_string,points_spent_to_save_string))
            self.accept()
        save_research.clicked.connect(on_save_research)

        inner_layout.addWidget(save_research,9,0,1,7)
        self.setLayout(inner_layout)

    def init_driver_popup(self):
        self.setWindowTitle('training') 
        #self.setFixedSize(400, 100)
        layout = QVBoxLayout()
        attributes_grid_layout  = QGridLayout()
        driving_button = QPushButton('Driving', self)
        mental_button = QPushButton('Mental', self)
        physical_button = QPushButton('Physical', self)


        #print('training of: ',self.account.staff['drivers'][self.number])
        
        driver = self.account.staff['drivers'][self.number]
        
        attributes_grid_layout.addWidget(driving_button,0,0)
        attributes_grid_layout.addWidget(mental_button,0,1)
        attributes_grid_layout.addWidget(physical_button,0,2)
        
        extra_driver_info = self.account.extra_driver_info


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
        loop = asyncio.get_event_loop()
        
        loop.run_until_complete(self.account.driver_info(driver_info['id']))
        contract_info =  self.account.extra_driver_info['contract']

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
    
    def fuel_load_changed(self,value):
        self.account.strategy[self.number]['advancedFuel'] = str(value)
        
    def init_strategy_popup(self):
        
        ## init strategy parameters
        self.stint_fuel = []
        self.stint_tyre = []
        tyreWearFactors = {'SS': 2.14,'S': 1.4,'M': 1,'H': 0.78}
        reversed_push_map = {0:'100',1:'80',2:'60',3:'40',4:'20'}
        added_push = {0:0.02,1:0.0081,2:0,3:-0.004,4:-0.007}
        car_strategy = self.account.strategy[self.number]
        self.trackCode = self.account.strategy[0]['trackCode']
        self.tier = Track().info[self.trackCode][self.account.strategy[0]['raceLaps']]
        self.fuel_km = Track.fuel_calc(self.account.car[0]['fuel_economy'])
        self.track_length = Track().info[self.trackCode]['length']
        self.fuel_lap = int(self.fuel_km  * self.track_length  *100) /100
        
        def set_size(img_label):
            img_label.setFixedHeight(22)
            img_label.setFixedWidth(22)
            img_label.setScaledContents(True)

        self.setWindowTitle(f"{self.account.strategy[0]['raceName']} - two tyres: {self.account.strategy[0]['rules']['two_tyres']}")
        grid_layout  = QGridLayout()
        
        tyre_SS_img = QLabel()
        tyre_S_img = QLabel()
        tyre_M_img = QLabel()
        tyre_H_img = QLabel()
        tyre_I_img = QLabel()
        tyre_W_img = QLabel()

        for img in [tyre_SS_img,tyre_S_img,tyre_M_img,tyre_H_img,tyre_I_img,tyre_W_img]:
            set_size(img)
        
        
        #find tier by total laps
       
        calculation = (1.43 * self.account.car[0]['tyre_economy'] ** -0.0778) * (0.00364 * Track().info[ self.trackCode]['wear'] + 0.354) * self.track_length * 1.384612 * Track().multipliers[self.tier ]
        ss = "{:.1f}".format(calculation * tyreWearFactors['SS'])
        s = "{:.1f}".format(calculation * tyreWearFactors['S'])
        m = "{:.1f}".format(calculation * tyreWearFactors['M'])
        h = "{:.1f}".format(calculation * tyreWearFactors['H'])
        i = "{:.1f}".format(calculation * tyreWearFactors['M'])
        w = "{:.1f}".format(calculation * tyreWearFactors['M'])
        
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
        
        self.strategy_pits = select_box
        
        
        
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
                        if ele.property('refuel') is None:
                            ele.show()
           
            update_total_laps()
        select_box.currentIndexChanged.connect(on_pit_box_changed)
        def on_push_box_changed(index):
            self.fuel_lap = (self.fuel_km + added_push[index]) * self.track_length
            car_strategy['pushLevel'] = reversed_push_map[index]
            update_total_laps()

        def on_depth_box_changed(index):
            car_strategy['rainStart'][0] =  tyre_map_rev[index]

        def on_stop_box_changed(index):
            car_strategy['rainStop'][0] =  tyre_map_rev[index]
        
        def on_depth_changed(text):
            car_strategy['rainStart'][1] = text
        def on_stop_changed(text):
            car_strategy['rainStop'][1] = text


        def tyre_select():
            tyre_select_box = QComboBox()
            for option in ['tyres/SS.png','tyres/S.png','tyres/M.png','tyres/H.png','tyres/I.png','tyres/W.png']:
                tyre_select_box.addItem(QIcon(option), '',Qt.AlignCenter)
                tyre_select_box.setFixedWidth(50)
            
               
            return tyre_select_box    
        self.setStyleSheet("""
             QSpinBox {
              
                text-align: center;
            }
            QSpinBox::up-button {
                min-width: 5px;
                min-height: 24px;
                subcontrol-origin: margin;
                subcontrol-position: right;
              
               
            }
            QSpinBox::down-button {
                min-width: 5px;
                min-height: 24px;
                subcontrol-origin: margin;
                subcontrol-position: left;

            }
        """)
        stints_grid_layout  = QGridLayout()
        
        
        
        
        layout = QVBoxLayout()
        stints_grid_layout.addWidget(select_box,0,0,1,2,Qt.AlignCenter)
        stints_grid_layout.addWidget(QLabel(f'Fuel/lap: {self.fuel_lap}'),0,2,1,2,Qt.AlignLeft)

        
        save_button = QPushButton('save')
        #save_button.setDisabled(True)
        load_button = QPushButton('load')
        save_button.setFixedWidth(40)
        load_button.setFixedWidth(40)
        stints_grid_layout.addWidget(save_button,1,0)
        stints_grid_layout.addWidget(load_button,2,0)
        save_button.clicked.connect(self.on_save_pressed)
        load_button.clicked.connect(self.on_load_pressed)
        #try to read strategies from file save.json
        with open('save.json', 'r') as json_file:
            save_list = json.load(json_file)['save']

        # trackcode has the code
        if self.trackCode in save_list:
            total_laps = int(self.account.strategy[0]['raceLaps'])
            valid_strat = False
            self.valid_strat_layouts = []
            for key, value_inner in save_list[self.trackCode].items():
                #print(f"pits {len(value_inner['stints'])-1}")
                if int(value_inner['laps']['total']) == total_laps:
                    valid_strat = True
                    saved_pits = len(value_inner['stints'])-1
                    stints = []
                    for stint_key, value in value_inner['stints'].items():
                         tyre =  value['tyre'].split('-')[1]
                         laps = value['laps']
                          # [tyre,lap,fuel]
                         stints.append([tyre,laps,0])
                    strategy = {'strat':stints,'pits':saved_pits}
                    self.valid_strat_layouts.append(strategy)
            if not valid_strat:
                load_button.setDisabled(True)        
        else:
            load_button.setDisabled(True)

        self.fuel_rules  = self.account.strategy[0]['rules']['refuelling']
        if self.fuel_rules != '0' :    
            stints_grid_layout.addWidget(QLabel('Fuel'),3,0)
        stints_grid_layout.addWidget(QLabel('Laps'),4,0)
        stints_grid_layout.addWidget(QLabel('Wear'),5,0)
        tyre_map_text = {'SS':ss,'S':s,'M':m,'H':h,'I':i,'W':w}
        tyre_map = {'SS':0,'S':1,'M':2,'H':3,'I':4,'W':5}
        tyre_map_rev = {0:'SS',1:'S',2:'M',3:'H',4:'I',5:'W'}
        self.elements = []
        self.stint_laps = 0
        self.total_laps_value = 1
        self.total_fuel = 0
        self.total_laps = QLabel(f"{self.stint_laps}/{self.account.strategy[0]['raceLaps']}")
        def update_total_laps():
            pit = int(car_strategy['pits'])
            self.total_laps_value = 0 
            self.total_fuel = 0  
            for index, stint in enumerate (car_strategy['strat'],start=0):
                if index < pit+1:
                    self.total_laps_value += int(stint[1])
                    self.total_fuel += int(stint[2]) 
            if self.fuel_rules == '0':
                self.suggested_fuel.setText(f"{round(self.total_laps_value* self.fuel_lap,2) } L")                
            self.total_laps.setText(f"{self.total_laps_value}/{self.account.strategy[0]['raceLaps']}") 
        
        def on_laps_changed(laps, stint):
                
                if laps != '':
                    
                    fuel = math.floor(int(laps) * float(self.fuel_lap))
                    
                    self.elements[stint][2].setValue(int(fuel))
                    #tyre wear

                    tyre_wear = tyre_map_text[tyre_map_rev[self.elements[stint][1].currentIndex()]]

                    car_strategy['strat'][stint][2] = fuel
                    car_strategy['strat'][stint][1] = laps

                    self.elements[stint][4].setText(Track.stint_wear_calc(tyre_wear,laps,self.trackCode))

                    update_total_laps() 
       
        def advanced_status_changed(state):
            if Qt.Checked == state:
                car_strategy['advanced'] = '0'
            else:
                car_strategy['advanced'] = '1'
        advanced_grid = QGridLayout()
        tyre_select_if_rain = tyre_select()
        tyre_select_if_rain.setCurrentIndex(tyre_map[car_strategy['rainStart'][0]]) 
        tyre_select_if_stop = tyre_select()
        tyre_select_if_stop.setCurrentIndex(tyre_map[car_strategy['rainStop'][0]]) 
        
        adv_checkbox = QCheckBox('Enable advanced')
        if car_strategy['advanced'] == '0':
            adv_checkbox.setChecked(True)
        push_combobox = QComboBox()
        push_combobox.addItems(["very high","high","neutral","low","very low" ])
        push_map = {'100':0,'80':1,'60':2,'40':3,'20':4}
        push_combobox.currentIndexChanged.connect(on_push_box_changed)
        tyre_select_if_rain.currentIndexChanged.connect(on_depth_box_changed)
        tyre_select_if_stop.currentIndexChanged.connect(on_stop_box_changed)
        adv_checkbox.stateChanged.connect(advanced_status_changed)
        
        advanced_grid.addWidget(adv_checkbox,0,0)
        advanced_grid.addWidget(QLabel('Push'),1,0)
        advanced_grid.addWidget(push_combobox,1,1)
        advanced_grid.addWidget(QLabel('Use'),3,0)
        advanced_grid.addWidget(QLabel('Use'),4,0)
        advanced_grid.addWidget(tyre_select_if_rain,3,1)
        advanced_grid.addWidget(tyre_select_if_stop,4,1)
        advanced_grid.addWidget(QLabel('If raining (mm)'),3,2)
        advanced_grid.addWidget(QLabel('If stops for (laps)'),4,2)
        
        def spinbox(max,value):
            spinbox_ele = QSpinBox()
            spinbox_ele.setMaximum(max)
            spinbox_ele.setFixedWidth(100)
            spinbox_ele.setAlignment(Qt.AlignCenter)
            spinbox_ele.setValue(int(value))
            return spinbox_ele
        


        depth = spinbox(5,car_strategy['rainStart'][1])
        stop = spinbox(50,car_strategy['rainStop'][1])
        
        depth.textChanged.connect(on_depth_changed)
        stop.textChanged.connect(on_stop_changed)
        
        advanced_grid.addWidget(depth,3,3)
        advanced_grid.addWidget(stop,4,3)
        
        if self.fuel_rules == '0':
            fuel_load = spinbox(200,car_strategy['advancedFuel'])
            self.account.strategy[self.number]['fuel_load'] = car_strategy['advancedFuel']
            fuel_load.textChanged.connect(self.fuel_load_changed)  
            self.fuel_lap = round((self.fuel_km + added_push[push_combobox.currentIndex()]) * self.track_length,2)
            self.suggested_fuel = QLabel(f"{self.total_laps_value * self.fuel_lap} L")
            update_total_laps()
            

            advanced_grid.addWidget(self.suggested_fuel,2,0)
            advanced_grid.addWidget(fuel_load,2,1)

        push_combobox.setCurrentIndex(push_map[car_strategy['pushLevel']])
        for index,value in enumerate(range(5), start=1):
          
          selected_tyre = car_strategy['strat'][index-1][0]
          
          if index == 1:
            stint_label = QLabel(f"Start")
          else:
            stint_label = QLabel(f"{index-1}")    
          
          
          fuel_field = QSpinBox()
          self.stint_fuel.append(fuel_field)
          #fuel_field.setInputMask('999')
          fuel_field.setFixedWidth(50)
          fuel_field.setAlignment(Qt.AlignCenter)
          
          
          
          
          if self.fuel_rules != '0' :
            laps_label = QLabel(f"{int(int(car_strategy['strat'][index-1][2])/self.fuel_lap*100)/100}")
          else:
            ## calculate the fuel based on the laps if norefuel
            car_strategy['strat'][index-1][2] = (int(car_strategy['strat'][index-1][1]) * self.fuel_lap)
            fuel_field.setProperty('refuel',False)
            laps_label = QSpinBox()
            laps_label.setFixedWidth(50)
            laps_label.setAlignment(Qt.AlignCenter)
            laps_label.setValue(int(car_strategy['strat'][index-1][1]))
            laps_label.textChanged.connect(lambda index, column=index-1: on_laps_changed(index,column))  
            
          
          fuel_field.setValue(int(car_strategy['strat'][index-1][2]))
          wear_label = QLabel(f"{Track.stint_wear_calc(tyre_map_text[selected_tyre],car_strategy['strat'][index-1][1],self.account.strategy[0]['trackCode'])}")
          
          tyre_select_ele = tyre_select()
         
          self.stint_tyre.append(tyre_select_ele)
          if index < int(car_strategy['pits'])+2:
                    self.stint_laps += int(car_strategy['strat'][index-1][1])  
          
          def on_tyre_changed(index, column):
            car_strategy['strat'][column][0] = tyre_map_rev[index]
            tyre_wear = tyre_map_text[tyre_map_rev[index]]
            laps = car_strategy['strat'][column][1]
            track = self.account.strategy[0]['trackCode']
            self.elements[column][4].setText(Track.stint_wear_calc(tyre_wear,laps,track))
          
          

          def on_fuel_changed(fuel, column):
            
            if self.fuel_rules != '0':
                if fuel != '':

                    laps = (int(int(fuel)/self.fuel_lap*100)/100)
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
          
          if self.fuel_rules != '0' :
            stints_grid_layout.addWidget(fuel_field,3,index,Qt.AlignLeft)

          stints_grid_layout.addWidget(laps_label,4,index,Qt.AlignLeft)
          
          stints_grid_layout.addWidget(wear_label,5,index,Qt.AlignLeft)
          ## saving strategy elements ---------------------------------------------------<<<
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
        
        self.total_laps.setAlignment(Qt.AlignCenter)
        
        
        layout.addWidget(self.total_laps)
        

         

        layout.addLayout(advanced_grid)
        
        layout.addWidget(confirm_button)
        self.setLayout(layout) 
    
    def train_driver(self):
        driver = self.account.staff['drivers'][self.number]
        for radio_button in self.radio_buttons:
            if radio_button.isChecked():
                intensity = int(radio_button.text())
                break

        train_type_map = {'Driving':'ability','Mental':'mental','Physical':'physical','All':'all'} 
        train_type = self.sender().text()
        print(f"{driver['id']} type {train_type} x{intensity}")
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.account.train_driver(driver['id'],intensity,train_type_map[train_type]))
       
    
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

        loop = asyncio.get_event_loop()
        if self.type == 'parts':
           self.response= loop.run_until_complete(self.account.request_parts_repair(self.account.car[self.number]))
           self.account.car[0]['total_parts'] -= self.account.car[self.number]['repair_cost']
        elif self.type == 'engine':
           self.response = loop.run_until_complete(self.account.request_engine_repair(self.account.car[self.number]))
        elif self.type == 'contract':
           self.response = loop.run_until_complete(self.account.extend_contract_driver(self.account.staff['drivers'][self.number]))
        new_value = self.response  # Here you can retrieve the value you want
        
        self.parent().main_window.buttons[self.index].setText(new_value)
        self.parent().main_window.buttons[self.index].setEnabled(False)  
        self.accept()     