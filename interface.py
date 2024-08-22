import asyncio
import json
from PyQt6.QtWidgets import QMainWindow,QGroupBox,QScrollArea,QTreeWidget,QTabWidget,QTreeWidgetItem,QVBoxLayout, QDialog, QLabel,QPushButton,QGridLayout,QWidget, QComboBox,QLineEdit,QRadioButton,QHBoxLayout,QSpinBox,QCheckBox
from PyQt6.QtGui import QPixmap, QIcon,QPalette,QIntValidator,QFont
from PyQt6.QtCore import Qt,QSize
import math
from helpers import iGPeasyHelp, Section, CustomComboBox,Track
from setups import CarSetup

class AccountPopup(QDialog):
    def __init__(self, parent=None):
         super().__init__(parent)
         self.manage_accounts_initialized = False
    def manage_accounts(self):
        self.setWindowTitle("accounts")
        def find_item_by_username(username):
            #Check if the given username is already in the tree widget.
            for index in range(self.manage_accounts_initialized['accounts_tree'].topLevelItemCount()):
                item = self.manage_accounts_initialized['accounts_tree'].topLevelItem(index)
                if item.text(0) == username:
                    return item
            return None
        def add_account_to_tree():
            username = username_line_edit.text()
            if username:  # Check if the input is not empty
                existing_item = find_item_by_username(username)
                if existing_item:
                    existing_item.setText(0, username)
                    existing_item.setText(1, password_line_edit.text())
                    existing_item.setText(2, nickname_line_edit.text())
                else:
                    item = QTreeWidgetItem([username,password_line_edit.text(),nickname_line_edit.text()])
                    self.manage_accounts_initialized['accounts_tree'].addTopLevelItem(item)
                    #clear input only on new
                    clear_inputs()
                save_to_file()              
        def delete_account_from_tree():
            """Delete the selected item from the tree widget."""
            selected_items = self.manage_accounts_initialized['accounts_tree'].selectedItems()
            if selected_items:
                # Assuming single selection mode
                item = selected_items[0]
                index = self.manage_accounts_initialized['accounts_tree'].indexOfTopLevelItem(item)
                if index != -1:
                    self.manage_accounts_initialized['accounts_tree'].takeTopLevelItem(index)
                    clear_inputs()  # Clear input fields after deletion
                    save_to_file()
        def clear_inputs():
            """Clear input fields."""
            username_line_edit.clear() 
            password_line_edit.clear()
            nickname_line_edit.clear()
            delete_button.setDisabled(True)        
        def on_selection_click():
            delete_button.setDisabled(False)
            selected_items = self.manage_accounts_initialized['accounts_tree'].selectedItems()
            if selected_items:
                # Assuming single selection mode
                item = selected_items[0]
                username_line_edit.setText(item.text(0))
                password_line_edit.setText(item.text(1))
                nickname_line_edit.setText(item.text(2))               
        def save_to_file():
            """Save the tree widget contents to a JSON file."""
            items = []
            for index in range(self.manage_accounts_initialized['accounts_tree'].topLevelItemCount()):
                item = self.manage_accounts_initialized['accounts_tree'].topLevelItem(index)
                items.append({
                    "username": item.text(0),
                    "password": item.text(1),
                    "nickname": item.text(2),
                })
            with open('accounts.json', 'w') as f:
                json.dump(items, f, indent=4)
            print("Data saved to accounts.json")
        def load_from_file():
            """Load the tree widget contents from a JSON file."""
            try:
                with open('accounts.json', 'r') as f:
                    items = json.load(f)
                self.manage_accounts_initialized['accounts_tree'].clear()
                for item_data in items:
                    item = QTreeWidgetItem([
                                            item_data.get("username", ""),  
                                            item_data.get("password", ""),  
                                            item_data.get("nickname", "")
                                            ])
                    self.manage_accounts_initialized['accounts_tree'].addTopLevelItem(item)
                print("Data loaded from accounts.json")
            except FileNotFoundError:
                print("No data file found. Please save data first.")
            except json.JSONDecodeError:
                print("Error decoding the JSON file. The file might be corrupted.")    
        #create the elements only the first time
        if self.manage_accounts_initialized == False:
            main_layout =  QHBoxLayout()
            form_layout = QVBoxLayout()
            username_line_edit = QLineEdit()
            password_line_edit = QLineEdit()
            nickname_line_edit = QLineEdit()
            username_line_edit.setPlaceholderText("Enter email address")
            password_line_edit.setPlaceholderText("Enter password")
            nickname_line_edit.setPlaceholderText("Enter nickname")
            add_button = QPushButton('Add/Update')
            add_button.clicked.connect(add_account_to_tree)
            delete_button = QPushButton('Delete')
            delete_button.setDisabled(True)
            delete_button.clicked.connect(delete_account_from_tree)
            accounts_tree = QTreeWidget()
            accounts_tree.setHeaderLabels(["username", "Password", "Nickname"])
            accounts_tree.itemClicked.connect(on_selection_click)
            form_layout.addWidget(username_line_edit)
            form_layout.addWidget(password_line_edit)
            form_layout.addWidget(nickname_line_edit)
            form_layout.addWidget(add_button)
            form_layout.addWidget(delete_button)
            form_layout.addStretch()
            main_layout.addLayout(form_layout)
            main_layout.addWidget(accounts_tree)
            #self.setGeometry(100, 100, 400, 200)
            self.manage_accounts_initialized = {"main_layout":main_layout,"accounts_tree":accounts_tree}
  
        load_from_file()
        self.setLayout(self.manage_accounts_initialized['main_layout'])
        self.show()
    
    
class PopupDialog(QDialog):
    def __init__(self,layout):
        super().__init__()
        self.setWindowTitle("Popup Window")
        #self.setGeometry(100, 100, 300, 200)
        self.setLayout(layout)

class PopupHandler(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.strategy_popup_initialized = False
        self.center_of_parent()
    def center_of_parent(self):
        # Center the popup on the parent window
        if self.parent():
            parent_rect = self.parent().frameGeometry()
            popup_rect = self.frameGeometry()
            popup_rect.moveCenter(parent_rect.center())
            self.move(popup_rect.topLeft())

    def load_strategy(self):
        strategy_to_load = self.sender().property('strat')
        self.account.strategy[self.driver_index]['pits'] = str(min(int(strategy_to_load['pits']),4))
        
        #calculate fuel for the strategy
        for sub_array in strategy_to_load['strat']:
            sub_array[2] = math.ceil(int(sub_array[1]) * self.fuel_lap)


        #overwrite the strategy
        self.account.strategy[self.driver_index]['strat'][:len(strategy_to_load['strat'])] = strategy_to_load['strat']
        self.strategy_popup()   
    
    def strategy_popup(self):
        self.saved_strategies = None
        self.center_of_parent()
        if self.saved_strategies == None:
            with open('save.json', 'r') as json_file:
                self.saved_strategies = json.load(json_file)['save']
        
        self.preview_slot = self.sender().property('preview')
        self.account = self.sender().property('account')
        self.driver_index = self.sender().property('driver_index')
       
        self.race_mode = 'rf' if self.account.strategy[0]['rules']['refuelling'] == '1' else 'nrf'
        race_rule = 'tyre rules is off' if self.account.strategy[0]['rules']['two_tyres'] == '0' else 'tyre rule is on'
        self.track= Track(self.account.strategy[0]['trackCode'])
        self.fuel_km = iGPeasyHelp.fuel_calc(self.account.car[0]['fuel_economy']) 
        self.fuel_lap = int(self.fuel_km * self.track.info['length'] * 100)/100

        def update_total():
           total = 0

           for stint in self.strat_stints:
                stint.set_account_and_driver(self.account,self.driver_index,self.fuel_lap)
                stint.on_fuel_change(stint.stint_fuel_label.value())
                total+= stint.get_laps()
           self.strat_widget_total_laps.setText(f"{total}/{self.account.strategy[0]['raceLaps']}")
           if self.race_mode == 'nrf':
                self.advanced_suggested_fuel.setText(f"{round(total*self.fuel_lap,2)}") 
        
        
                    
        self.setStyleSheet("""
             QSpinBox {
              
                text-align: center;
            }
            QSpinBox::up-button {
                min-width: 20px;
                min-height: 50px;
                subcontrol-origin: margin;
                subcontrol-position: right;
              
               
            }
            QSpinBox::down-button {
                min-width: 20px;
                min-height: 50px;
                subcontrol-origin: margin;
                subcontrol-position: left;

            }
        
        """)
        #add tyre text also
        def tyre_select():
            tyre_select_box = CustomComboBox()
            for option in ['tyres/_SS.png','tyres/_S.png','tyres/_M.png','tyres/_H.png','tyres/_I.png','tyres/_W.png']:
                tyre_select_box.addItem(QIcon(option),'')
            #tyre_select_box.setIconSize(QSize(47,47))
            tyre_select_box.setFixedWidth(50)

            return tyre_select_box      
        

        self.setWindowTitle(f"{self.account.strategy[0]['raceName']} - {race_rule}")
        
        
        
        opened_driver_index = self.driver_index
        
        def on_load_button():
                mainlayout = QGridLayout()
                load_buttons = []
                for row,strat in enumerate(self.valid_strat_layouts):
                    strategy_layout = display_strat(strat)
                    strat_load_button = QPushButton('load')
                    strat_load_button.clicked.connect(self.load_strategy)
                    strat_load_button.setProperty('strat',strat)
                    load_buttons.append(strat_load_button)
                    strat_load_button.setProperty('preview',self.preview_slot)
                    strat_load_button.setProperty('account',self.account)
                    strat_load_button.setProperty('driver_index',self.driver_index)
                    
                    mainlayout.addWidget(strat_load_button,row,0)  
                    mainlayout.addLayout(strategy_layout,row,1)
                
                load_popup =PopupDialog(mainlayout)
                for load_b in load_buttons:
                    load_b.clicked.connect(load_popup.close)
                load_popup.exec()
        
            
        def display_strat(full_strategy):
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
                    img_label.setFixedSize(QSize(50,50))
                    img_label.setScaledContents(True)
                    inner_layout.addWidget(img_label,0,column)
                    inner_layout.addWidget(label,0,column,Qt.AlignmentFlag.AlignCenter)
                    column += 1
                return inner_layout
            
            
          

        if self.strategy_popup_initialized == False:
            main_layout =  QVBoxLayout()
            load_save_widget = QWidget()
            load_save_layout =QGridLayout()
            self.load_button = QPushButton('Load')
            self.save_button = QPushButton('Save')
            self.load_button.setFixedHeight(50)
            self.save_button.setFixedHeight(50)
            load_save_layout.addWidget(self.load_button,0,0,1,1)
            load_save_layout.addWidget(self.save_button,0,1,1,1)
            load_save_widget.setLayout(load_save_layout)
            
            tyre_preview_section = QWidget()
            #tyre_widget = QWidget()
            tyre_widget_layout = QGridLayout()
            
            tyre_SS_img = QLabel()
            tyre_S_img = QLabel()
            tyre_M_img = QLabel()
            tyre_H_img = QLabel()
            tyre_I_img = QLabel()
            tyre_W_img = QLabel()
            tyre_SS_img.setPixmap(QPixmap(f'tyres/SS.png'))
            tyre_S_img.setPixmap(QPixmap(f'tyres/S.png'))
            tyre_M_img.setPixmap(QPixmap(f'tyres/M.png'))
            tyre_H_img.setPixmap(QPixmap(f'tyres/H.png'))
            tyre_I_img.setPixmap(QPixmap(f'tyres/I.png'))
            tyre_W_img.setPixmap(QPixmap(f'tyres/W.png'))

            for tyre in [tyre_SS_img,tyre_S_img,tyre_M_img,tyre_H_img,tyre_I_img,tyre_W_img]:
                tyre.setFixedSize(QSize(28,28))
                tyre.setScaledContents(True)
            
            tyre_SS_text = QLabel()
            tyre_S_text = QLabel()
            tyre_M_text = QLabel()
            tyre_H_text = QLabel()
            tyre_I_text = QLabel()
            tyre_W_text = QLabel()

            tyre_widget_layout.addWidget(tyre_SS_img,0,0,1,1)
            tyre_widget_layout.addWidget(tyre_S_img,0,1,1,1)
            tyre_widget_layout.addWidget(tyre_M_img,0,2,1,1)
            tyre_widget_layout.addWidget(tyre_H_img,0,3,1,1)
            tyre_widget_layout.addWidget(tyre_I_img,0,4,1,1)
            tyre_widget_layout.addWidget(tyre_W_img,0,5,1,1)
            
            tyre_widget_layout.addWidget(tyre_SS_text,1,0)
            tyre_widget_layout.addWidget(tyre_S_text,1,1)
            tyre_widget_layout.addWidget(tyre_M_text,1,2)
            tyre_widget_layout.addWidget(tyre_H_text,1,3)
            tyre_widget_layout.addWidget(tyre_I_text,1,4)
            tyre_widget_layout.addWidget(tyre_W_text,1,5)

            #tyre_widget.setLayout(tyre_widget_layout)
            tyre_preview_section.setLayout(tyre_widget_layout)

            strat_widget = QWidget()
            strat_widget_layout = QGridLayout()
            self.pit_select_box = QComboBox()
            self.pit_select_box.addItem("1 pit stop")
            self.pit_select_box.addItem("2 pit stops")
            self.pit_select_box.addItem("3 pit stops")
            self.pit_select_box.addItem("4 pit stops")
            self.pit_select_box.setFixedHeight(30)
            
            def on_pit_box_change(index):
                #index 0-3
                self.account.strategy[self.driver_index ]['pits'] = str(index+1)
                for stint in self.strat_stints:
                    stint.show()
                    stint.set_mode(self.race_mode)

                for i in range(4-(index+1)):
                    self.strat_stints[4-i].hide()   
                update_total()         
            self.pit_select_box.currentIndexChanged.connect(on_pit_box_change)
            description_widget = QWidget()
            description_layout = QVBoxLayout()
            self.fuel_lap_label = QLabel('Fuel/Lap\n1.23')
            self.fuel_label = QLabel('Fuel')
            laps_label = QLabel('Laps')
            wear_label = QLabel('Wear')

            #fuel_lap_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            #fuel_lap_label.setFixedHeight(50)
            self.fuel_label.setFixedHeight(30)
            laps_label.setFixedHeight(30)
            wear_label.setFixedHeight(30)
            
            description_layout.addStretch()
            description_layout.addWidget(self.fuel_label,)  ## in case of no refule this is not needed. remove after or before?
            description_layout.addWidget(laps_label)
            description_layout.addWidget(wear_label)
            description_widget.setLayout(description_layout)
            
            class stint_widget():
                
                def __init__(self, stint_name,index):
                    self.driver_index = opened_driver_index
                    self.index = index
                   
                    self.stint_container = QWidget()
                    stint_layout = QVBoxLayout()
                    stint_number = QLabel(stint_name)
                    self.stint_tyre_selection = tyre_select()

                    self.mode = 'rf'

                    combobox_layout= QHBoxLayout()
                    combobox_container = QWidget()
                    self.stint_fuel_label = QSpinBox()
                    self.stint_laps_label_nrf = QSpinBox()
                                        
                    combobox_layout.addWidget(self.stint_tyre_selection)
                    combobox_container.setLayout(combobox_layout)
                    
                    
                    stint_font = QFont()
                    stint_font.setPointSize(14)
                    self.stint_fuel_label.setFont(stint_font)
                    self.stint_laps_label_nrf.setFont(stint_font)
                    self.stint_laps_label = QLabel('99')
                    self.stint_wear = QLabel('99')
                    stint_layout.addWidget(stint_number)
                    stint_layout.addWidget(combobox_container)
                    stint_layout.addWidget(self.stint_fuel_label)
                    stint_layout.addWidget(self.stint_laps_label_nrf)
                    stint_layout.addWidget(self.stint_laps_label)
                    stint_layout.addWidget(self.stint_wear)
                    self.stint_container.setLayout(stint_layout)
                    #stint_container.setFixedSize(QSize(80,200))
                    
                    for item in [stint_number,self.stint_fuel_label,self.stint_laps_label_nrf, self.stint_laps_label,self.stint_wear]:
                        item.setFixedSize(QSize(80,30))
                        item.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    self.stint_fuel_label.valueChanged.connect(self.on_fuel_change)
                    self.stint_laps_label_nrf.valueChanged.connect(self.on_laps_change)
                    self.stint_tyre_selection.currentIndexChanged.connect(self.on_tyre_change)
                
                def set_account_and_driver(self,account,driver_index,fuel):
                    self.driver_index = driver_index
                    self.account = account
                    self.fuel_lap = fuel
                def set_fuel(self,value):
                    self.stint_fuel_label.setValue(int(value))  
                def set_laps(self,value):
                    if self.mode == 'rf':
                        self.stint_laps_label.setText(value)
                    elif self.mode == 'nrf':
                        self.stint_laps_label_nrf.setValue(int(value))
                def get_laps(self):
                    if not self.stint_tyre_selection.isHidden():
                        if self.mode == 'rf':
                            return math.floor(float(self.stint_laps_label.text()))
                        elif self.mode == 'nrf':
                            return self.stint_laps_label_nrf.value()
                    else: return 0
                
                def hide(self):
                    self.stint_laps_label.hide()
                    self.stint_fuel_label.hide()
                    self.stint_laps_label_nrf.hide()
                    self.stint_wear.hide()
                    self.stint_tyre_selection.hide()
                def show(self):
                    self.stint_laps_label.show()
                    self.stint_fuel_label.show()
                    self.stint_laps_label_nrf.show()
                    self.stint_wear.show()
                    self.stint_tyre_selection.show()    
                def set_wear(self,value):          
                    self.stint_wear(value)
                def set_tyres(self,value):  
                    
                    self.stint_tyre_selection.setCurrentIndex(iGPeasyHelp().tyre_map[value])       
                def set_mode(self,mode):
                    self.mode = mode
                    if mode == 'nrf':
                        self.stint_laps_label.hide()
                        self.stint_fuel_label.hide()
                        self.stint_laps_label_nrf.show()
                    elif mode == 'rf':
                        self.stint_laps_label_nrf.hide()

                        self.stint_laps_label.show()
                        self.stint_fuel_label.show()
                def block_signals(self,bool):
                    self.stint_tyre_selection.blockSignals(bool)
                    #self.stint_fuel_label.blockSignals(bool)
                    self.stint_laps_label_nrf.blockSignals(bool)
                def on_tyre_change(self):
                    selected_tyre_index = self.stint_tyre_selection.currentIndex()
                    self.account.strategy[self.driver_index ]['strat'][self.index][0] = iGPeasyHelp().tyre_map_rev[selected_tyre_index] 
                def on_fuel_change(self,fuel):
                    #print('changin fuel of',self.account.nickname,self.driver_index)
                    if self.mode == 'rf':
                        lap = int(int(fuel)/self.fuel_lap*100)/100
                        self.account.strategy[self.driver_index ]['strat'][self.index][2] = str(fuel)
                        self.stint_laps_label.setText(str(lap))
                        self.account.strategy[self.driver_index ]['strat'][self.index][1] = str(math.floor(lap))
                    

                def on_laps_change(self,lap):
                    self.account.strategy[self.driver_index]['strat'][self.index][1] = str(lap)
                    update_total()
                

            self.stint_start = stint_widget('Start',0)
            self.stint_1 = stint_widget('Pit 1',1)
            self.stint_2 = stint_widget('Pit 2',2)
            self.stint_3 = stint_widget('Pit 3',3)
            self.stint_4 = stint_widget('Pit 4',4)



            self.strat_stints = [self.stint_start,self.stint_1,self.stint_2,self.stint_3,self.stint_4]

            self.strat_widget_total_laps = QLabel('99/99')
            
            strat_widget_layout.addWidget(self.pit_select_box,0,1,1,4)
            strat_widget_layout.addWidget(self.fuel_lap_label,0,0,2,1)
            strat_widget_layout.addWidget(description_widget,1,0,1,1)
            strat_widget_layout.addWidget(self.stint_start.stint_container,1,1,1,1)
            strat_widget_layout.addWidget(self.stint_1.stint_container,1,2,1,1)
            strat_widget_layout.addWidget(self.stint_2.stint_container,1,3,1,1)
            strat_widget_layout.addWidget(self.stint_3.stint_container,1,4,1,1)
            strat_widget_layout.addWidget(self.stint_4.stint_container,1,5,1,1)
            strat_widget_layout.addWidget(self.strat_widget_total_laps ,2,0,1,5)

            strat_widget.setLayout(strat_widget_layout)
            # --- advanced section---
            self.advanced_strat = Section("Advanced", 100)
            advanced_strat_layout = QGridLayout()
            advanced_push_label = QLabel('Push')
            self.advanced_push_combobox = QComboBox()
            self.advanced_push_combobox.addItems(["very high","high","neutral","low","very low" ])
            self.advanced_fuel_nrf_label = QLabel('Fuel')
            self.advanced_fuel_nrf = QSpinBox()
            self.advanced_fuel_nrf.setRange(0,200)
            advanced_rain_use_label = QLabel('Use')
            advanced_rain_use_2_label = QLabel('Use')
            advanced_rain_description_1 = QLabel('If water depth is above:')
            advanced_rain_description_2 = QLabel('If it stops raining for:')
            self.advanced_tyre_selection_1 = tyre_select()
            self.advanced_tyre_selection_2 = tyre_select()
            self.advanced_raining = QSpinBox()
            self.advanced_rain_stop = QSpinBox()
            self.advanced_raining.setSuffix(' mm')
            self.advanced_raining.setRange(0,5)
            self.advanced_rain_stop.setSuffix(' Lap(s)')
            self.advanced_rain_stop.setRange(0,50)
            self.advanced_suggested_fuel = QLabel('')
            adv_font = QFont()
            adv_font.setPointSize(14)

            for spin in [self.advanced_fuel_nrf,self.advanced_raining,self.advanced_rain_stop]:
                spin.setFixedSize(120,30)
                spin.setFont(adv_font)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            advanced_strat_layout.addWidget(advanced_push_label,0,0)
            advanced_strat_layout.addWidget(self.advanced_push_combobox,0,1)
            
            advanced_strat_layout.addWidget(self.advanced_fuel_nrf_label,1,0)
            advanced_strat_layout.addWidget(self.advanced_fuel_nrf,1,1)
            advanced_strat_layout.addWidget(self.advanced_suggested_fuel,1,2)

            advanced_strat_layout.addWidget(advanced_rain_use_label,2,0)
            advanced_strat_layout.addWidget(advanced_rain_use_2_label,3,0)
            advanced_strat_layout.addWidget(self.advanced_tyre_selection_1,2,1)
            advanced_strat_layout.addWidget(self.advanced_tyre_selection_2,3,1)
            advanced_strat_layout.addWidget(advanced_rain_description_1,2,2)
            advanced_strat_layout.addWidget(advanced_rain_description_2,3,2)
            advanced_strat_layout.addWidget(self.advanced_raining,2,3)
            advanced_strat_layout.addWidget(self.advanced_rain_stop,3,3)
         
            self.advanced_strat.setContentLayout(advanced_strat_layout)

            main_layout.addWidget(load_save_widget)
            #main_layout.addWidget(tyre_preview_section) ## add later
            main_layout.addWidget(strat_widget)
            main_layout.addWidget(self.advanced_strat)
            main_layout.addStretch()
            self.strategy_popup_initialized = {"main_layout":main_layout}
            
            def on_advanced_fuel_change(value):
                self.account.strategy[self.driver_index ]['advancedFuel'] = str(value)
            def on_advanced_rain_change(value):
                self.account.strategy[self.driver_index ]['rainStart'][1] = str(value)
            def on_advanced_stop_change(value):
                self.account.strategy[self.driver_index ]['rainStop'][1] = str(value)
            def on_advanced_tyre_change_1(index):
                self.account.strategy[self.driver_index ]['rainStart'][0] = iGPeasyHelp().tyre_map_rev[index]
            def on_advanced_tyre_change_2(index):
                self.account.strategy[self.driver_index ]['rainStop'][0] = iGPeasyHelp().tyre_map_rev[index]
            def on_advanced_push_change(index):
                self.account.strategy[self.driver_index ]['pushLevel'] = iGPeasyHelp().push_map_rev[index]
                self.fuel_lap = ((self.fuel_km + iGPeasyHelp().added_push[self.advanced_push_combobox.currentIndex()]) * self.track.info['length'])
                update_total()
            def on_advance_toggle(bool):
                self.account.strategy[self.driver_index ]['advanced'] = "0" if bool else "1"
                self.fuel_lap = ((self.fuel_km + iGPeasyHelp().added_push[self.advanced_push_combobox.currentIndex()]) * self.track.info['length'])
                if not (bool):
                    self.fuel_lap = (self.fuel_km  * self.track.info['length'])
                update_total()
            def on_save_button():
                print('saving',self.account.nickname,self.driver_index)
                self.preview_slot.update_preview(self.account.strategy[self.driver_index ])
                #preview_slot.(QLabel('test'))
      
            
            self.save_button.clicked.connect(on_save_button)
            self.load_button.clicked.connect(on_load_button)
            self.advanced_fuel_nrf.valueChanged.connect(on_advanced_fuel_change)
            self.advanced_tyre_selection_1.currentIndexChanged.connect(on_advanced_tyre_change_1)
            self.advanced_tyre_selection_2.currentIndexChanged.connect(on_advanced_tyre_change_2)
            self.advanced_push_combobox.currentIndexChanged.connect(on_advanced_push_change)
            self.advanced_raining.valueChanged.connect(on_advanced_rain_change)
            self.advanced_rain_stop.valueChanged.connect(on_advanced_stop_change)
            self.advanced_strat.toggleButton.toggled.connect(on_advance_toggle)
            
        if self.track.track_code in self.saved_strategies:
            total_laps = int(self.account.strategy[0]['raceLaps'])
            valid_strat = False
            self.valid_strat_layouts = []
            for key, value_inner in self.saved_strategies[self.track.track_code].items():
                #print(f"pits {len(value_inner['stints'])-1}")
                if int(value_inner['laps']['total']) == total_laps:
                    valid_strat = True
                    self.load_button.setDisabled(False)
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
                self.load_button.setDisabled(True)        
        else:
            self.load_button.setDisabled(True)
        
        
        def load_game_data():
            
            
            self.advanced_push_combobox.blockSignals(True)
            self.advanced_push_combobox.setCurrentIndex(iGPeasyHelp().push_map[self.account.strategy[self.driver_index ]['pushLevel']])
            self.advanced_push_combobox.blockSignals(False)
            
            for i in range(5):
                self.strat_stints[i].set_account_and_driver(self.account,self.driver_index,self.fuel_lap)
                self.strat_stints[i].show()
                self.strat_stints[i].set_mode(self.race_mode)
                self.strat_stints[i].block_signals(True)
                self.strat_stints[i].set_laps(self.account.strategy[self.driver_index ]['strat'][i][1])
                self.strat_stints[i].set_fuel(self.account.strategy[self.driver_index ]['strat'][i][2])
                self.strat_stints[i].on_fuel_change(self.account.strategy[self.driver_index ]['strat'][i][2])
                self.strat_stints[i].set_tyres(self.account.strategy[self.driver_index ]['strat'][i][0])
                self.strat_stints[i].block_signals(False)
            
            if self.account.strategy[self.driver_index ]['advanced'] == '0':
                self.advanced_strat.setChecked(True)
                self.fuel_lap = ((self.fuel_km + iGPeasyHelp().added_push[self.advanced_push_combobox.currentIndex()]) * self.track.info['length'])
            else:
                self.advanced_strat.setChecked(False)
                self.fuel_lap = (self.fuel_km  * self.track.info['length'])
    
            
            if self.race_mode == 'rf':
                self.fuel_label.show()
                self.advanced_fuel_nrf_label.hide()
                self.advanced_fuel_nrf.hide()
                self.advanced_suggested_fuel.hide()
            else:
                self.fuel_label.hide()
                self.advanced_fuel_nrf_label.show()
                self.advanced_suggested_fuel.show()
                self.advanced_fuel_nrf.show()
                self.advanced_fuel_nrf.setValue(int(self.account.strategy[self.driver_index ]['advancedFuel']))
            
            self.advanced_raining.setValue(int(self.account.strategy[self.driver_index ]['rainStart'][1]))
            self.advanced_rain_stop.setValue(int(self.account.strategy[self.driver_index ]['rainStop'][1]))
            self.advanced_tyre_selection_1.setCurrentIndex(iGPeasyHelp().tyre_map[self.account.strategy[self.driver_index ]['rainStart'][0]])
            self.advanced_tyre_selection_2.setCurrentIndex(iGPeasyHelp().tyre_map[self.account.strategy[self.driver_index ]['rainStop'][0]])


            pit_stops = int(self.account.strategy[self.driver_index ]['pits'])
            
       
            # this will hide the elements starting from the end. 
            for i in range(4-pit_stops):
                self.strat_stints[4-i].hide()


            self.pit_select_box.blockSignals(True)
            self.pit_select_box.setCurrentIndex(pit_stops-1)
            self.pit_select_box.blockSignals(False)
            
            self.fuel_lap_label.setText(f"Fuel/Lap \n{round(self.fuel_lap,3)}")
            self.strat_widget_total_laps.setText(f"{self.account.strategy[self.driver_index ]['totalLaps']}/{self.account.strategy[0]['raceLaps']}")
            update_total()
             

        load_game_data()

        self.setLayout(self.strategy_popup_initialized['main_layout'])
        
        self.show()
       





class iGPeasyWindow(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.parent=parent
 
        self.open_account_button = False
        self.iGPeasyWindow_initialized = False
        self.main_layout =  QVBoxLayout()
        self.accounts_container = QScrollArea()
        self.accounts_container.setLayout(self.main_layout)
        self.popup = PopupHandler(self) # this is the popup element, passing the mainwindow as the parent
        self.popup_account = AccountPopup(self)
        self.setWindowTitle("iGPeasy")
        self.menuBar().addMenu('settings')
        self.setGeometry(100, 100, 1700, 1700)
        self.setCentralWidget(self.accounts_container)
        self.showMaximized()


        #self.init_window()
    
        

    def add_accounts_popup(self):
        def clear_open_account_button():
            #it will be neccessary to remove the accounts widgets when the popup is opened from the menubar
            self.open_account_button.setParent(None)
            
        self.popup_account.manage_accounts()
        self.popup_account.finished.connect(clear_open_account_button)   
        self.popup_account.exec()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.parent.play())

    async def add_accounts_to_start(self):
        #simple button
        print('no valid accounts')
        if self.open_account_button == False:
            self.open_account_button = QPushButton('You need to add valid accounts to start using this app')
            self.open_account_button.clicked.connect(self.add_accounts_popup)
        else:
            print('not the first time')
            self.open_account_button = self.open_account_button
        
        self.main_layout.addWidget(self.open_account_button)
    
    async def init_window(self):
        def save_json_offsets():
            with open('offsets.json', 'w') as f:
                json.dump(offsets, f, indent=4)
            print("Data saved to accounts.json")
        def load_json_offsets():
            try:
                with open('offsets.json', 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                print("No data file found. Please save data first.")
            except json.JSONDecodeError:
                print("Error decoding the JSON file. The file might be corrupted.") 
        def account_group_box(account):
            box = QGroupBox(f"{account.nickname} lv. {account.manager["level"]}")
            box.setMaximumSize(QSize(1920,190))
            box.setMinimumSize(QSize(500,190))
            
            
        # --- Start of Section 1, widget with money, token, daily and sponsor---
            misc_grid_layout = QGridLayout()
            box_layout = QHBoxLayout()
            misc_widget = QWidget()
            daily_button = QPushButton("Daily") #check if already pressed
            if 'page'in account.notify and'nDailyReward' in account.notify['page']:
              reward_status = False
            else:
              reward_status = True
            def get_daily():
                loop = asyncio.get_event_loop()
                response = loop.run_until_complete(account.get_daily())
                account.pyqt_elements['daily'].setDisabled(True)

            daily_button.setDisabled(reward_status)
            daily_button.clicked.connect(get_daily)
            sponsor_button = QPushButton("Sponsor")
            money_label = QLabel(iGPeasyHelp.abbreviate_number(int(account.team['_balance'])))
            token_label = QLabel(account.manager['tokens'])
            token_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            money_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            token_img = QPixmap(f'assets/token.png')
            img_label = QLabel()
            img_label.setPixmap(token_img)
            img_label.setScaledContents(True)
            img_label.setFixedSize(QSize(14,14))
            misc_grid_layout.addWidget(money_label,0,0,1,1)
            misc_grid_layout.addWidget(img_label,0,1,1,1)
            misc_grid_layout.addWidget(token_label,0,1,1,1)
            misc_grid_layout.addWidget(daily_button,1,0,1,1)
            misc_grid_layout.addWidget(sponsor_button,1,1,1,1)
            misc_widget.setLayout(misc_grid_layout) 
        # --- End of Section 1 ---
            if account.has_league:
            # --- Start of Section 2 ---
                    race_info_widget = QWidget()
                    race_info_grid_layout = QGridLayout()
                    race_name_label = QLabel(account.strategy[0]['raceName'])
                    race_time_label = QLabel(account.strategy[0]['raceTime'])
                    race_weather_label = QLabel(account.strategy[0]['pWeather'])
                    car_design_button =QPushButton('car/research')
                    race_info_grid_layout.addWidget(race_name_label,0,0,1,1)
                    race_info_grid_layout.addWidget(race_time_label,1,0,1,1)
                    race_info_grid_layout.addWidget(race_weather_label,2,0,1,1)
                    race_info_grid_layout.addWidget(car_design_button,3,0,1,1)
                    race_info_widget.setLayout(race_info_grid_layout)
                      
                    # --- End of Section 2 --- 
            car_design_button = None

            def driver_setup(driver_index):
                def repair_parts():
                    print('attempt to repair parts of',account.nickname,driver_index)
                    loop = asyncio.get_event_loop()
                    response = loop.run_until_complete(account.request_parts_repair(account.car[driver_index]))
                    if response == False:
                        print('already repaired or out of engines')
                    else:
                        account.car[0]['total_parts'] = response
                        #parts are shared so it needs to update all the labels
                        for car in account.setup_pyqt_elements:
                            car['parts'][0].setText(str(response))
                        #update the button only for the car requested   
                        account.setup_pyqt_elements[driver_index]['parts'][1].setText("100%")
                        account.setup_pyqt_elements[driver_index]['parts'][1].setDisabled(True)
                def repair_engine():
                    print('attempt to repair engine of',account.nickname,driver_index)
                    loop = asyncio.get_event_loop()
                    response = loop.run_until_complete(account.request_engine_repair(account.car[driver_index]))
                    if response == False:
                        print('already repaired or out of engines')
                    else:
                        account.car[0]['total_engines'] = response
                        for car in account.setup_pyqt_elements:
                            car['engine'][0].setText(str(response))

                        account.setup_pyqt_elements[driver_index]['engine'][1].setText("100%")
                        account.setup_pyqt_elements[driver_index]['engine'][1].setDisabled(True)
                    
                    
                strategy_widget = QWidget()
                strategy_widget_layout = QHBoxLayout()
                # --- Start of Section 3 ---
                car_condition_widget =QWidget()
                car_condition_layout = QGridLayout()
                header_car_condition_1 = QLabel('have')
                parts_car_condition_label = QLabel('parts')
                engine_car_condition_label =QLabel('Engine')
                parts_text = QLabel(str(account.car[0]['total_parts'])) #engine and parts are shared, only 1st driver has the values
                engine_text = QLabel(str(account.car[0]['total_engines']))
                parts_button = QPushButton(account.car[driver_index]['parts'])
                parts_button.clicked.connect(repair_parts)
                engine_button = QPushButton(account.car[driver_index]['engine'])
                if account.car[driver_index]['engine'] == "100%":
                    engine_button.setDisabled(True)
                if account.car[driver_index]['parts'] == "100%":
                    parts_button.setDisabled(True)
                engine_button.clicked.connect(repair_engine)
                car_condition_layout.addWidget(header_car_condition_1,0,1,1,1)
                car_condition_layout.addWidget(parts_car_condition_label,1,0,1,1)
                car_condition_layout.addWidget(engine_car_condition_label,2,0,1,1)
                car_condition_layout.addWidget(parts_text,1,1,1,1)
                car_condition_layout.addWidget(engine_text,2,1,1,1)
                car_condition_layout.addWidget(parts_button,1,2,1,1)
                car_condition_layout.addWidget(engine_button,2,2,1,1)
                car_condition_widget.setLayout(car_condition_layout)
                # --- End of Section 3 --- 
                
                # --- Start of Section 4 ---
                driver_info_widget = QTabWidget()
                tab_1 = QWidget()
                tab_1_layout = QGridLayout()
                tab_2 = QWidget()
                tab_2_layout = QGridLayout()
                tab_3 = QWidget()
                tab_3_layout = QGridLayout()
                driver_name_label = QLabel(account.staff['drivers'][driver_index]['name'])
                driver_health_value_label = QLabel(account.staff['drivers'][driver_index]['health']) #possibly button to use tokens
                #driver_fav_track_label = QLabel(self.account.staff['drivers'][driver_index]['fav']) to do
                #driver_skill_label = QLabel(self.account.staff['drivers'][driver_index]['skill'])to do
                tab_1_layout.addWidget(driver_name_label,0,0,1,1)
                tab_1_layout.addWidget(driver_health_value_label,0,1,1,1)
                tab_1.setLayout(tab_1_layout)

                contract_button = QPushButton(f'Contract: {account.staff['drivers'][driver_index]['contract']}')
                edit_skills_button = QPushButton('edit_skills')
                train_button = QPushButton('Train')
                tab_2_layout.addWidget(contract_button,0,0,1,2)
                tab_2_layout.addWidget(edit_skills_button,1,0,1,1)
                tab_2_layout.addWidget(train_button,1,2,1,1)

                practice_button = QPushButton('Practice')
                tab_3_layout.addWidget(practice_button,0,0,1,1)


                driver_info_widget.addTab(tab_1,'Driver')
                driver_info_widget.addTab(tab_2,'More')
                driver_info_widget.addTab(tab_3,'Practice')
                # --- End of Section 4 ---



                def ride_change(self):
                    account.strategy[driver_index]['ride'] = str(self)
                def wing_change(self):
                    account.strategy[driver_index]['aero'] = str(self)
                def ride_offset_change(self):
                    if self != "-":
                        driver_id = account.staff['drivers'][driver_index]['id']
                        offsets[driver_id][0] = int(self)
                def wing_offset_change(self):
                    if self != "-":
                        driver_id = account.staff['drivers'][driver_index]['id']
                        offsets[driver_id][1] = int(self)

                strategy_widget_layout.addWidget(car_condition_widget)
                strategy_widget_layout.addWidget(driver_info_widget)
                
                setup_pyqt_elements =  {'parts':0,
                                               'engine':0,
                                               'setup':{'ride':0,
                                                        'ride_offset':0,
                                                        'wing':0,
                                                        'wing_offset':0,
                                                        'suspension':0,
                                                        'ideal':0},
                                                'strategy':{'modify':0,
                                                            'preview':0,
                                                            }}
                
                if account.has_league:
                     
                # --- Start of Section 5 ---
                    strategy_setup_container = QWidget()
                    strategy_setup_container_layout = QHBoxLayout()
                    setup_container = QWidget()
                    setup_container_layout = QGridLayout()
                    suspension_selection = QComboBox()
                    suspension_selection.addItems(['Soft','Neutral','Firm'])
                    suspension_selection.setCurrentIndex(int(account.strategy[driver_index]['suspension'])-1)
                    ride_height_label = QLabel('height')
                    wing_label = QLabel('wing')
                    ride_height_input = QLineEdit()
                    #ride_height_input.setProperty('driver_index',driver_index)
                    ride_height_input.textChanged.connect(ride_change)
                    ride_height_input_offset =QLineEdit()
                    ride_height_input_offset.textChanged.connect(ride_offset_change)
                    int_validator = QIntValidator()
                    int_validator.setRange(1, 25)
                    offset_validator = QIntValidator()
                    offset_validator.setRange(-25,25)
                    ride_height_input.setValidator(int_validator)
                    ride_height_input_offset.setValidator(offset_validator)
                    # self.account -> staff -> driver -> id
                    driver_id = account.staff['drivers'][driver_index]['id']
                    if driver_id not in offsets:
                            offsets[driver_id] = [0] * 2
                    saved_ride_offset_value = offsets.get(driver_id)[1]
                    ride_height_input_offset.setText(str(saved_ride_offset_value))
                    ride_height_input.setText(str(account.strategy[driver_index]['ride']))
                    wing_input = QLineEdit()
                    wing_input_offset = QLineEdit()
                    wing_input.textChanged.connect(wing_change)
                    wing_input_offset.textChanged.connect(wing_offset_change)
                    saved_wing_offset_value = offsets.get(driver_id)[0]
                    wing_input_offset.setText(str(saved_wing_offset_value))
                    wing_input.setValidator(int_validator)
                    wing_input_offset.setValidator(offset_validator)

                    wing_input.setText(str(account.strategy[driver_index]['aero']))
                    qedit_size = QSize(30,28)
                    ride_height_input.setFixedSize(qedit_size)
                    ride_height_input_offset.setFixedSize(qedit_size)
                    wing_input.setFixedSize(qedit_size)
                    wing_input_offset.setFixedSize(qedit_size)
                    ideal_button = QPushButton("suggested")
                    def on_suggested_setup_clicked(self):
                        if account.has_league:
                            suggested_setup = CarSetup(account.strategy[0]['trackCode'],account.staff['drivers'][driver_index]['height'],account.strategy[0]['tier'])
                
                            ride = str(suggested_setup.ride)
                            aero = str(suggested_setup.wing)
                            suspension = suggested_setup.suspension

                            account.setup_pyqt_elements[driver_index]['setup']['suspension'].setCurrentIndex(suspension)
                            account.setup_pyqt_elements[driver_index]['setup']['ride'].setText(ride)
                            account.setup_pyqt_elements[driver_index]['setup']['wing'].setText(aero)

                            account.strategy[driver_index]['ride'] = ride
                            account.strategy[driver_index]['aero'] = aero
                            account.strategy[driver_index]['suspension'] = suspension +1

                    ideal_button.clicked.connect(on_suggested_setup_clicked)
                    setup_container_layout.addWidget(suspension_selection,0,0,1,3)
                    setup_container_layout.addWidget(ride_height_label,1,0,1,1)
                    setup_container_layout.addWidget(wing_label,2,0,1,1)
                    setup_container_layout.addWidget(ride_height_input,1,1,1,1)
                    setup_container_layout.addWidget(wing_input,2,1,1,1)
                    setup_container_layout.addWidget(ride_height_input_offset,1,2,1,1)
                    setup_container_layout.addWidget(wing_input_offset,2,2,1,1)
                    setup_container_layout.addWidget(ideal_button,3,0,1,3)
                    setup_container.setLayout(setup_container_layout)
                    setup_container.setMaximumSize(QSize(100,190))
                    setup_container.setMinimumSize(QSize(120,140))
                    setup_pyqt = {'ride':ride_height_input,
                                  'ride_offset':ride_height_input_offset,
                                  'wing':wing_input,
                                  'wing_offset':wing_input_offset,
                                  'suspension':suspension_selection,
                                  'ideal':ideal_button}
                    setup_pyqt_elements['setup'] = setup_pyqt
                    class display_strat():
                        def __init__(self,strategy_container,race_laps):
                              self.parent = strategy_container 
                              self.race_laps = race_laps


                        def update_preview(self,full_strategy):
                        
                            old_layout = self.container.layout()
                            for i in reversed(range(old_layout.count())): 
                                widgetToRemove = old_layout.itemAt(i).widget()
                                # remove it from the layout list
                                old_layout.removeWidget(widgetToRemove)
                                # remove it from the gui
                                widgetToRemove.setParent(None)
                            self.estimate_laps.setParent(None)  

                            self.generate_preview(full_strategy)


                        def generate_preview(self,full_strategy):
                            self.container = QWidget()
                            strategy = full_strategy['strat']
                            pits = int(full_strategy['pits'])
                            inner_layout  = QGridLayout()
                            column = 1

                            # [tyre,lap,fuel]
                            total_laps = 0
                            for arr in strategy[:pits+1]:
                                img_label = QLabel()
                                label = QLabel(arr[1])
                                label.setStyleSheet("color: white")
                                tyre_img = QPixmap(f'tyres/{arr[0]}.png')
                                total_laps += int(arr[1])
                                img_label.setPixmap(tyre_img)
                                img_label.setFixedHeight(30)
                                img_label.setFixedWidth(30)
                                img_label.setScaledContents(True)
                                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                inner_layout.addWidget(img_label,0,column)
                                inner_layout.addWidget(label,0,column,1,1)
                                column += 1

                            self.container.setLayout(inner_layout) 
                            self.estimate_laps = QLabel(f" Total laps estimate: {str(total_laps)}/ {self.race_laps}")
                            self.parent.addWidget(self.estimate_laps,3,0,1,1)
                            self.parent.addWidget(self.container,1,0,2,4)
                    
                    strategy_container = QWidget()
                    strategy_container_layout = QGridLayout()

                    preview_strat = display_strat(strategy_container_layout,str(account.strategy[0]['raceLaps']))
                    preview_strat.generate_preview(account.strategy[driver_index])
                    #strategy_container_layout.addWidget(preview_strat.generate_preview(self.account.strategy[driver_index]),1,0,2,4) # strategy displayed here ----------

                    #strategy_container.setMaximumSize(QSize(180,190))
                    #strategy_container.setMinimumSize(QSize(180,140))
                    modify_strategy_button = QPushButton('modify')
                    modify_strategy_button.setProperty('account',account)
                    modify_strategy_button.setProperty('driver_index',driver_index)
                    modify_strategy_button.setProperty('preview',preview_strat)
                    modify_strategy_button.clicked.connect(self.popup.strategy_popup)
                    def close_popup():
                        preview_strat.update_preview(account.strategy[driver_index])
                    self.popup.finished.connect(close_popup)
                    strategy_preview_container = QWidget()
                    strategy_preview_container_layout = QHBoxLayout()
                    strategy_container_layout.addWidget(modify_strategy_button,0,0,1,1)

                    strategy_preview_container.setLayout(strategy_preview_container_layout)
                    strategy_container_layout.addWidget(strategy_preview_container,1,0,4,1)
                    strategy_container.setLayout(strategy_container_layout)
                    strategy_setup_container_layout.addWidget(setup_container)
                    strategy_setup_container_layout.addWidget(strategy_container)
                    strategy_setup_container.setLayout(strategy_setup_container_layout)
                    strategy_widget_layout.addWidget(strategy_setup_container)
                    
                    
                    strategy_pyqt = {'modify':modify_strategy_button,
                                     'preview':strategy_preview_container_layout,
                                    }
                    setup_pyqt_elements['strategy'] = strategy_pyqt
                    
                
                
                # --- End of Section 5 ---
                
                
                strategy_widget.setLayout(strategy_widget_layout)
                palette = self.palette()
                background_color = palette.color(QPalette.ColorRole.Window)
                darkened_color = background_color.darker(120)
                widget_palette = self.palette()
                strategy_widget.setAutoFillBackground(True)
                widget_palette.setColor(QPalette.ColorRole.Window, darkened_color)
                strategy_widget.setPalette(widget_palette)
                #strategy_widget.setStyleSheet("background-color: lightblue;")
                
                setup_pyqt_elements['parts'] = [parts_text,parts_button]
                setup_pyqt_elements['engine'] = [engine_text,engine_button]

                
                
                account.setup_pyqt_elements.append(setup_pyqt_elements)

                return strategy_widget
                

            save_button = QPushButton('Save')
            save_button.setMinimumHeight(120)
            def on_save_strategy(self):
                if account.has_league:
                    save_json_offsets()
                    for driver_index in range(len(account.strategy)):
                        account.strategy[driver_index]['ride'] = str(int(account.strategy[driver_index]['ride']) + int(account.setup_pyqt_elements[driver_index]['setup']['ride_offset'].text()))
                        account.strategy[driver_index]['aero'] = str(int(account.strategy[driver_index]['aero']) + int(account.setup_pyqt_elements[driver_index]['setup']['wing_offset'].text()))
                        
                            
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(account.save_strategy())
            save_button.clicked.connect(on_save_strategy)


                #suspension_selection.setFixedWidth(60) 
            box_layout.addWidget(save_button)
            box_layout.addWidget(misc_widget)
            if account.has_league: box_layout.addWidget(race_info_widget)
            strategy_widget = []

            number_of_driver_widgets = 0 
            if account.strategy != False:
                number_of_driver_widgets = len(account.strategy)
            else:
                number_of_driver_widgets = min(len(account.staff['drivers']),2)
            for index in range(number_of_driver_widgets):
                strategy_widget.append(driver_setup(index))
            for strategy in strategy_widget:
                box_layout.addWidget(strategy)
            
            box_layout.addStretch()
            
            box.setLayout(box_layout)
            self.main_layout.addWidget(box)
            
            account.pyqt_elements = {'money':money_label,
                                     'tokens':token_label,
                                     'daily':daily_button,
                                     'design':car_design_button,
                                     'save':save_button}
            

        self.accounts = self.parent.valid_accounts
        offsets = load_json_offsets()
        
        ## for with list of aacounts
        for account in self.accounts:
            account_group_box(account)
        self.main_layout.addStretch()
        
        #print(self.main_layout.sizeHint())
        #print(self.accounts_container.sizeHint())
        #self.resize(self.main_layout.sizeHint())
        

    
        
        