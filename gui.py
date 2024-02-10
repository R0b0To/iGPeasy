from tool_api import iGP_account
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel,QPushButton,QGridLayout,QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from track import Track

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
        print (self.parent)
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
        tier = 100
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
        
        
        
        layout = QVBoxLayout()

        layout.addLayout(grid_layout)

        self.setLayout(layout) 
            
        
        # check if repaired
    def update_main_button(self):

        if self.type == 'parts':
           self.response = self.account.request_parts_repair(self.data)
           self.account.car[0]['total_parts'] -= self.data['repair_cost']
            

        elif self.type == 'engine':
           self.response = self.account.request_engine_repair(self.data)
        
        new_value = self.response  # Here you can retrieve the value you want
        self.parent().main_window.buttons[self.index].setText(new_value)
        self.parent().main_window.buttons[self.index].setEnabled(False)  
        self.accept()     