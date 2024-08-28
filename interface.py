import asyncio
import json
import os
from PyQt6.QtWidgets import QMainWindow,QGroupBox,QScrollArea,QTreeWidget,QTabWidget,QTreeWidgetItem,QVBoxLayout, QDialog, QLabel,QPushButton,QGridLayout,QWidget, QComboBox,QLineEdit,QRadioButton,QHBoxLayout,QSpinBox,QCheckBox
from PyQt6.QtGui import QPixmap,QPalette,QIntValidator,QAction,QFont
from PyQt6.QtCore import Qt,QSize
import math
from helpers import iGPeasyHelp, Section,Track
from setups import CarSetup
from qasync import  asyncSlot

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
    
class ResearchPopup(QDialog):    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Car Research")
        self.initialized = False
        self.my_car = []
        self.best_car = []
        self.gap = []
        self.check_status = []
        self.checkboxes = []
        self.gain = []
        self.init_research()
    
    @asyncSlot()
    async def on_save_research(self):
        attribute_keys = ['acceleration', 'braking', 'cooling', 'downforce', 'fuel_economy', 'handling', 'reliability', 'tyre_economy']
        attributes_to_save = ['&c%5B%5D=' + value for value, flag in zip(attribute_keys, self.check_status) if flag]
        spinbox_values = [spinbox.value() for spinbox in self.my_car]
        points_spent = ['&{}={}'.format(key, value) for key, value in zip(attribute_keys, spinbox_values)]
        attributes_to_save_string = ''.join(attributes_to_save)
        points_spent_to_save_string = ''.join(points_spent)
       
        await self.account.save_research(attributes_to_save_string,points_spent_to_save_string)
        self.accept()
    
    def on_header_check_change(self, state):
        is_checked = (state == Qt.CheckState.Checked)
    
        for check in self.checkboxes:
            check.blockSignals(True)
            check.setChecked(is_checked)
            check.blockSignals(False)
        self.check_status = [is_checked] * len(self.check_status)
        self.set_research_power()       
    
    def set_research_power(self):
        selected = (self.check_status.count(True))
        if selected == 0:
           self.power.setText(str(0)) 
        else:
           self.power.setText(str(self.max_power / selected ))
        for i,check in enumerate(self.checkboxes):
            if check.checkState() == Qt.CheckState.Checked:
                check.setText(str(math.ceil(max(0, int(self.gap[i].text()))*float(self.power.text())/100)))
            else:  check.setText('')
        

    
    def on_check_change(self,state):
        attribute_check = self.sender()
        is_checked = (state == Qt.CheckState.Checked)
        index = attribute_check.property('index')
        self.check_status[index] = is_checked
        self.set_research_power()
        #needs to check all again 

    
    def on_points_change(self,new_value):
        
        attribute = self.sender()
        old_value = attribute.property('old_value')
        
        if new_value > old_value:
            #revert last increment in case out of available points 
            if self.available_points -1 < 0:
                attribute.blockSignals(True)
                attribute.setValue(attribute.value() - 1)
                new_value -= 1
                attribute.blockSignals(False) 
                self.available_points+=1
            #decrease the available points as increasing the attribute means points were used    
            self.available_points -= 1
        elif new_value < old_value:
            self.available_points += 1 

        self.points.setText(str(self.available_points))
        attribute.setProperty('old_value',new_value)   


    def init_research(self):
        if self.initialized == False:
            layout = QVBoxLayout()
            header_research = QWidget()

            header_research_layout = QHBoxLayout()
            header_research_layout.addStretch()

            my_points = QWidget()
            my_points_layout = QHBoxLayout()
            my_points_layout.addWidget(QLabel('Points'))
            self.points = QLabel()
            my_points_layout.addWidget(self.points)
            my_points.setLayout(my_points_layout)
            header_research_layout.addWidget(my_points)
            header_research_layout.addWidget(QLabel('Research Power'))
            self.power = QLabel()

            header_research_layout.addWidget(self.power)
            points_gain = QLabel()
            header_research_layout.addWidget(points_gain)
            header_research.setLayout(header_research_layout)

            save_button = QPushButton('Save')
            save_button.clicked.connect(self.on_save_research)
            layout.addWidget(header_research)


            header_titles = QWidget()
            header_area = QLabel('Area')
            header_mycar = QLabel('My Car')
            header_best_car = QLabel('Best')
            header_gap = QLabel('Gap')
            header_check = QCheckBox()
            header_check.checkStateChanged.connect(self.on_header_check_change)
               
            for item in [header_area,header_mycar,header_best_car,header_gap]:
                    item.setFixedWidth(90)
                    item.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            header_titles_layout = QHBoxLayout()
            header_titles_layout.addWidget(header_area)
            header_titles_layout.addWidget(header_mycar)
            header_titles_layout.addWidget(header_best_car)
            header_titles_layout.addWidget(header_gap)
            header_titles_layout.addWidget(header_check)
            header_titles.setLayout(header_titles_layout)

            layout.addWidget(header_titles)

            def area_widget(name):
                container = QWidget()
                layout_container = QHBoxLayout()
                area = QLabel(name)
                spinbox = QSpinBox()
                #spinbox.setReadOnly(True)
                spinbox.lineEdit().setReadOnly(True)
                spinbox.valueChanged.connect(self.on_points_change)
                best_car = QLabel()
                gap = QLabel()
                check = QCheckBox()
                check.checkStateChanged.connect(self.on_check_change)
                check.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

                for item in [area,spinbox,best_car,gap]:
                    item.setFixedWidth(90)
                    item.setAlignment(Qt.AlignmentFlag.AlignCenter)

                layout_container.addWidget(area)
                layout_container.addWidget(spinbox)
                layout_container.addWidget(best_car)
                layout_container.addWidget(gap)
                layout_container.addWidget(check)
                
                spinbox.setStyleSheet("""
                 QSpinBox {text-align: center; }
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
                container.setLayout(layout_container)
                
                self.my_car.append(spinbox)
                self.best_car.append(best_car)
                self.gap.append(gap)
                check.setProperty('index',len(self.checkboxes))
                self.checkboxes.append(check)
                
                return container
            for i, key in enumerate(['acceleration', 'braking', 'cooling', 'downforce', 'fuel economy', 'handling', 'reliability', 'tyre economy']):
                layout.addWidget(area_widget(key))
            layout.addWidget(save_button)
            self.initialized = layout
        self.setLayout(self.initialized)
        

    
    async def load_data(self,sender):
        if isinstance(sender, QPushButton):  # Check that the sender is the expected type
            self.account = sender.property('account')
            research_data = await self.account.research_info()
        
        self.max_power = research_data['research_power']
        check_count = research_data['check'].count(True)
        self.power.setText(str(self.max_power /check_count))
        self.available_points = int(research_data['points'])
        
        self.points.setText(str(self.available_points))
        gaps = []
        #rookie 1 must do /2
        #pro 2 is normal
        #elite 3 must do x2
        tier_research_map = {'1':0.5, '2':1, '3':2}
        tier = self.account.team['_tier']
        self.check_status = research_data['check']

        for i in range(8):
            my_attribute = research_data['car_design'][i] #car design is retrieved directly
            best_car_attribute = research_data['teams_design'][i] * tier_research_map[tier] #convertion of comparison table
            gaps.append(int(best_car_attribute) - int(my_attribute))
            self.my_car[i].blockSignals(True)
            self.my_car[i].setMaximum(int(research_data['max']))
            self.my_car[i].setMinimum(int(my_attribute))
            self.my_car[i].setValue(int(my_attribute))
            self.my_car[i].setProperty('old_value',int(my_attribute))
            self.my_car[i].blockSignals(False)
            self.best_car[i].setText(str(best_car_attribute ))
            self.gap[i].setText(str(gaps[i]))
            self.checkboxes[i].blockSignals(True)
            self.checkboxes[i].setChecked(research_data['check'][i])
            if self.check_status[i] == True:
                self.checkboxes[i].setText(str(math.ceil(max(0, int(gaps[i]))*float(self.power.text())/100)))
            else: self.checkboxes[i].setText("")
            self.checkboxes[i].blockSignals(False)
                

        self.show()
    

class PopupDialog(QDialog):
    def __init__(self,layout):
        super().__init__()
        self.setWindowTitle("Load Strategy")
        #self.setGeometry(100, 100, 300, 200)
        self.setLayout(layout)

class StrategyPopup(QDialog):
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
        #self.center_of_parent()
        if self.saved_strategies == None:
            with open('save.json', 'r') as json_file:
                self.saved_strategies = json.load(json_file)['save']
        
        self.preview_slot = self.sender().property('preview')
        self.account = self.sender().property('account')
        self.driver_index = self.sender().property('driver_index')

        self.race_mode = 'rf' if self.account.strategy[0]['rules']['refuelling'] == '1' else 'nrf'
        race_rule = 'tyre rules is off' if self.account.strategy[0]['rules']['two_tyres'] == '0' else 'tyre rule is on'
        self.track= Track(self.account.strategy[0]['trackCode'],self.account.strategy[0]['raceLaps'])
        self.fuel_km = iGPeasyHelp.fuel_calc(self.account.car[0]['fuel_economy']) 
        self.fuel_lap = int(self.fuel_km * self.track.info['length'] * 100)/100
        self.track.set_tyre_wear(iGPeasyHelp.wear_calc(self.account.car[0]['tyre_economy'],self.track))
        
        self.account.pyqt_elements['track'] = self.track


        def set_text_total_laps_label(text):
            self.strat_widget_total_laps.setText(f"{text}/{self.account.strategy[0]['raceLaps']}")
            
        
        def update_total():
           """recalculate the laps based on the fuel/push and set the total laps for nrf"""
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
                    self.stint_tyre_selection = iGPeasyHelp.tyre_select()

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
                def set_total_label_text(label):
                    self.strat_widget_total_laps = label
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
                    self.stint_wear.setText(str(value))
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
                    if self.mode == 'rf':
                        lap = int(int(fuel)/self.fuel_lap*100)/100
                        self.account.strategy[self.driver_index ]['strat'][self.index][2] = str(fuel)
                        self.stint_laps_label.setText(str(lap))
                        self.account.strategy[self.driver_index ]['strat'][self.index][1] = str(math.floor(lap))
                        
                        #using the strat list to do the total sum and the pit to slice it
                        total = sum(int(laps[1]) for laps in self.account.strategy[self.driver_index]['strat'][:int(self.account.strategy[self.driver_index]['pits'])+1])
                        
                       
                        #tyre_w = self.account.pyqt_elements['track'].tyre[iGPeasyHelp().tyre_map_rev[self.stint_tyre_selection.currentIndex()]]
                        
                        #self.set_wear(iGPeasyHelp.stint_wear_calc(tyre_w,,self.account.pyqt_elements['track']))
                        self.calculate_wear(self.account.strategy[self.driver_index]['strat'][self.index][1])
                        set_text_total_laps_label(str(total))

                def calculate_wear(self,laps):
                    tyre_w = self.account.pyqt_elements['track'].tyre[iGPeasyHelp().tyre_map_rev[self.stint_tyre_selection.currentIndex()]]
                    self.set_wear(iGPeasyHelp.stint_wear_calc(tyre_w,laps,self.account.pyqt_elements['track']))

                def on_laps_change(self,lap):
                    self.account.strategy[self.driver_index]['strat'][self.index][1] = str(lap)
                    
                    self.calculate_wear(lap)
                    
                    
                    
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
            self.advanced_tyre_selection_1 = iGPeasyHelp.tyre_select()
            self.advanced_tyre_selection_2 = iGPeasyHelp.tyre_select()
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
                self.preview_slot.clear_preview()
                self.preview_slot.generate_preview(self.account.strategy[self.driver_index])
                def hash_code(string):
                    hash_value = 0
                    for char in string:
                        code = ord(char)
                        hash_value = ((hash_value << 5) - hash_value) + code
                        hash_value = hash_value & 0xffffffff  # Convert to 32-bit integer
                    return hash_value
                
                save = {'stints':{},
                "length": str(self.track.length) ,
                "track": str(self.account.strategy[0]['trackCode']),
                "laps": {
                    "total": int(self.account.strategy[0]['raceLaps']),
                    "doing": sum(int(laps[1]) for laps in self.account.strategy[self.driver_index]['strat'][:int(self.account.strategy[self.driver_index]['pits'])+1])
                }}            
                stints = {i: {"tyre": f"ts-{sublist[0]}", "laps": str(sublist[1]), "push": 3} for i, sublist in enumerate(self.account.strategy[self.driver_index]['strat'][:int(self.account.strategy[self.driver_index]['pits'])+1])}   
                save['stints'] = stints
                save_id = hash_code(str(save))
                
                with open('save.json', 'r') as json_file:
                    save_list = json.load(json_file)
        
                save_list['save'][self.account.strategy[0]['trackCode']][save_id] = save   
        
                with open('save.json', 'w') as f:
                    json.dump(save_list, f)


                #preview_slot.(QLabel('test'))
            def on_close():
                self.preview_slot.clear_preview()
                self.preview_slot.generate_preview(self.account.strategy[self.driver_index])
            
            self.finished.connect(on_close)
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
                self.strat_stints[i].set_wear(iGPeasyHelp.stint_wear_calc(self.track.tyre[self.account.strategy[self.driver_index ]['strat'][i][0]],self.account.strategy[self.driver_index ]['strat'][i][1],self.track))
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
        
        self.scroll_layout = QVBoxLayout()
        self.accounts_container = QScrollArea()
        self.main_widget = QWidget()
        self.main_layout =  QVBoxLayout(self.main_widget)
        
        self.accounts_container.setWidget(self.main_widget)
        self.accounts_container.setWidgetResizable(True)
        
        self.scroll_layout.addWidget(self.accounts_container)
        
        
        self.setLayout(self.scroll_layout)
        
        
        self.popup = StrategyPopup(self) # this is the popup element, passing the mainwindow as the parent
        self.popup_account = AccountPopup(self)
        self.popup_research = ResearchPopup(self)
        
        self.setWindowTitle("iGPeasy")
        accounts_menu = self.menuBar().addMenu('Settings')
        actions_menu = self.menuBar().addMenu('Actions')

        accounts_action = QAction("Manage Accounts", self)
        accounts_action.triggered.connect(self.add_accounts_popup)
        accounts_menu.addAction(accounts_action)

        daily_action = QAction("Daily all", self)
        daily_action.triggered.connect(self.get_daily_all)
        actions_menu.addAction(daily_action)

        repair_action = QAction("Repair all", self)
        repair_action.triggered.connect(self.repair_all)
        actions_menu.addAction(repair_action)
        
        setupr_action = QAction("Setup all", self)
        setupr_action.triggered.connect(self.setup_all)
        actions_menu.addAction(setupr_action)
    
    
    
    
    async def async_load_research(self,sender):
            task = await self.popup_research.load_data(sender)
    
    def load_research(self):
        sender = self.sender()
        asyncio.create_task(self.async_load_research(sender))

        #self.init_window()
    def show_window(self):
        #self.setGeometry(100, 100, 1700, 1700)
        self.setCentralWidget(self.accounts_container)
        if not self.isVisible():
            self.showMaximized()


    
    @asyncSlot()
    async def get_daily_all(self):
        tasks = [] 
        for account in self.accounts:
            if 'page' in account.notify and 'nDailyReward' in account.notify['page']:
                tasks.append(self.process_daily_account(account))
            else:
                print('reward disabled')
        if tasks:
            await asyncio.gather(*tasks)
    async def process_daily_account(self, account):
        res = await account.get_daily()
        account.pyqt_elements['daily'].setDisabled(True) 
    @asyncSlot()
    async def setup_all(self):
        tasks = [] 
        for account in self.accounts:
            if account.has_league:
                tasks.append(self.process_setup_account(account))
        if tasks:
            await asyncio.gather(*tasks)
    async def process_setup_account(self, account):   
        for index,driver in enumerate(account.strategy):
            suggested_setup = CarSetup(account.strategy[0]['trackCode'],account.staff['drivers'][index]['height'],account.strategy[0]['tier'])
            ride = str(suggested_setup.ride)
            aero = str(suggested_setup.wing)
            suspension = suggested_setup.suspension
            account.setup_pyqt_elements[index]['setup']['suspension'].setCurrentIndex(suspension)
            account.setup_pyqt_elements[index]['setup']['ride'].setText(ride)
            account.setup_pyqt_elements[index]['setup']['wing'].setText(aero)
            driver['ride'] = ride
            driver['aero'] = aero
            driver['suspension'] = suspension +1

    @asyncSlot()
    async def repair_all(self):
        tasks = [] 
        for account in self.accounts:
            tasks.append(self.process_repair_account(account))
            
        await asyncio.gather(*tasks)
    async def process_repair_account(self, account):
        for driver_index,car in enumerate(account.car):
            if car['parts'] != "100%":
                res_parts = await account.request_parts_repair(car)
                if res_parts != False:
                    account.car[0]['total_parts'] = res_parts
                    #parts are shared so it needs to update all the labels
                    for car in account.setup_pyqt_elements:
                        car['parts'][0].setText(str(res_parts))
                    #update the button only for the car requested   
                    account.setup_pyqt_elements[driver_index]['parts'][1].setText("100%")
                    account.setup_pyqt_elements[driver_index]['header'].setText(f"Restock in: {account.car[0]['restock']} race(s)")
                    account.setup_pyqt_elements[driver_index]['parts'][1].setDisabled(True)
            else: print('parts already repaired',account.username,driver_index)
            if int(account.car[0]['total_engines']) > 0:
                res_engine = await account.request_engine_repair(car)
                if res_engine != False:
                    account.car[0]['total_engines'] = res_engine
                    for car in account.setup_pyqt_elements:
                        car['engine'][0].setText(str(res_engine))   
                    account.setup_pyqt_elements[driver_index]['engine'][1].setText("100%")
                    account.setup_pyqt_elements[driver_index]['engine'][1].setDisabled(True)
            else: print('out of engines',account.username,driver_index)


        account.pyqt_elements['daily'].setDisabled(True) 
    
    @asyncSlot()
    async def add_accounts_popup(self):
        def clearLayout(layout):
            #print("-- -- input layout: "+str(layout))
            for i in reversed(range(layout.count())):
                layoutItem = layout.itemAt(i)
                if layoutItem.widget() is not None:
                    widgetToRemove = layoutItem.widget()
                    #print("found widget: " + str(widgetToRemove))
                    widgetToRemove.setParent(None)
                    layout.removeWidget(widgetToRemove)
                #elif layoutItem.spacerItem() is not None:
                    #print("found spacer: " + str(layoutItem.spacerItem()))
                 

            #self.main_widget.setLayout(self.main_layout)
        def clear_open_account_button():
            #it will be neccessary to remove the accounts widgets when the popup is opened from the menubar
            if self.open_account_button != False:
                self.open_account_button.setParent(None)
                return
            clearLayout(self.main_layout)
            
        self.popup_account.manage_accounts()
        self.popup_account.finished.connect(clear_open_account_button)   
        self.popup_account.exec()

        await self.parent.play()
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self.parent.play())

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
        self.show_window()
    
    async def init_window(self):
        
        def save_json_offsets():
            with open('offsets.json', 'w') as f:
                json.dump(offsets, f, indent=4)
            print("Data saved to accounts.json")
        def load_json_offsets():
            try:
                if not os.path.exists('offsets.json'):
                    with open('offsets.json', 'w') as json_file:
                        json.dump([], json_file)
                with open('offsets.json', 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                print("No data file found. Please save data first.")
            except json.JSONDecodeError:
                print("Error decoding the JSON file. The file might be corrupted.") 
        
        
        async def account_group_box(account):
            #-----------------------------------------------------------------------------mail username
            box = QGroupBox(f"{account.nickname} - {account.username} - lv. {account.manager["level"]}",self.main_widget)
            #box.setMaximumSize(QSize(1920,190))
            #box.setMinimumSize(QSize(800,190))
            
            
        # --- Start of Section 1, widget with money, token, daily and sponsor---
            misc_tab_widget = QTabWidget()
            misc_tab_1 = QWidget()
            misc_tab_1_layout = QGridLayout()
            misc_tab_2 = QWidget()
            misc_tab_2_layout = QGridLayout()
            misc_tab_3 = QWidget()
            misc_tab_3_layout = QGridLayout()
            
            misc_tab_1_layout = QGridLayout()
            box_layout = QHBoxLayout()
            daily_button = QPushButton("Daily") #check if already pressed
            if 'page'in account.notify and'nDailyReward' in account.notify['page']:
              reward_status = False
            else:
              reward_status = True
            
            @asyncSlot()  
            async def get_daily(self):
                #loop = asyncio.get_event_loop()
                #response = loop.run_until_complete(account.get_daily())
                res = await account.get_daily()
                account.pyqt_elements['daily'].setDisabled(True)

            daily_button.setDisabled(reward_status)
            daily_button.clicked.connect(get_daily)
            sponsor_button_1 = QPushButton("Sponsor 1")
            sponsor_button_1.setProperty('location',1)
            sponsor_button_2 = QPushButton("Sponsor 2")
            sponsor_button_2.setProperty('location',2)
            sponsor_1_select = QComboBox()
            sponsor_2_select = QComboBox()
            #sponsor_2_select.setEditable(True)
            #sponsor_1_select.setEditable(True)
            #sponsor_2_select.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
            #sponsor_1_select.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            
            async def get_sponsor_list(number,combo):
                #task = asyncio.create_task(account.pick_sponsor(number))
                #res = await asyncio.gather(task)
                res = await asyncio.gather(account.pick_sponsor(number))
                income_list, bonus_list,id_list = res[0]
                combined_text = [f"{income_list[i]}       {bonus_list[i]}" for i in  range(min(len(income_list), len(bonus_list)))]
                combo.addItems(combined_text)
                combo.setProperty('id',id_list)

                return combo
            
            @asyncSlot()
            async def handle_sponsor_req(combo,btn):
                btn.setDisabled(True)
                combo.setDisabled(True)
                btn.setText('10 race(s)')
                #get list again
                #repopulate other combo
                sponsor_key = btn.property('location')
                #update the other keys?
                income, bonus = combo.itemText(combo.currentIndex()).split(',')
                account.sponsors[f"s{sponsor_key}"]['income'] = income
                account.sponsors[f"s{sponsor_key}"]['bonus'] = bonus
                account.sponsors[f"s{sponsor_key}"]['status'] = True
                
                await handle_sponsor(combo,btn)


            @asyncSlot()
            async def save_sponsor_contract_1(self):
                    combo = sponsor_1_select
                    id  = combo.currentIndex()
                    res = await account.save_sponsor(1,combo.property('id')[id])
                    await handle_sponsor_req(combo,sponsor_button_1)
                    #update the new sposnsors / refresh the other
                    #loop = asyncio.get_event_loop()
                    #loop.run_until_complete(self.account.get_sponsors())
            @asyncSlot()        
            async def save_sponsor_contract_2(self):
                    combo = sponsor_2_select
                    id  = combo.currentIndex()
                    res = await account.save_sponsor(2,combo.property('id')[id])
                    await handle_sponsor_req(combo,sponsor_button_2)

                    #update the new sposnsors / refresh the other
                    #loop = asyncio.get_event_loop()
                    #loop.run_until_complete(self.account.get_sponsors())
            async def handle_sponsor(sponsor_select, sponsor_button):
                sponsor_key = sponsor_button.property('location')
                sponsor = account.sponsors[f"s{sponsor_key}"]
                sponsor_select.clear()
                if not sponsor['status']:
                    await get_sponsor_list(int(sponsor_key), sponsor_select)
                    sponsor_button.setText('Press to Confirm')
                else:
                    sponsor_select.addItem(f"{sponsor['income']}, {sponsor['bonus']}")
                    sponsor_button.setText(sponsor['expire'])
                    sponsor_button.setDisabled(True)
                    sponsor_select.setDisabled(True)

            await handle_sponsor(sponsor_1_select, sponsor_button_1)
            await handle_sponsor(sponsor_2_select, sponsor_button_2)
            sponsor_button_1.clicked.connect(save_sponsor_contract_1)
            sponsor_button_2.clicked.connect(save_sponsor_contract_2)
            
            money_label = QLabel(iGPeasyHelp.abbreviate_number(int(account.team['_balance'])))
            token_label = QLabel(account.manager['tokens'])
            token_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            money_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            token_img = QPixmap(f'assets/token.png')
            img_label = QLabel()
            img_label.setPixmap(token_img)
            img_label.setScaledContents(True)
            img_label.setFixedSize(QSize(14,14))
            misc_tab_1_layout.addWidget(money_label,0,0,1,1)
            misc_tab_1_layout.addWidget(img_label,1,0,1,1)
            misc_tab_1_layout.addWidget(token_label,1,0,1,1)
            misc_tab_1_layout.addWidget(daily_button,2,0,1,1)
            misc_tab_3_layout.addWidget(sponsor_button_1,0,0,1,2)
            misc_tab_3_layout.addWidget(sponsor_button_2,2,0,1,2)
            misc_tab_3_layout.addWidget(sponsor_1_select,1,0,1,2)
            misc_tab_3_layout.addWidget(sponsor_2_select,3,0,1,2)
            misc_tab_1.setLayout(misc_tab_1_layout) 
            misc_tab_2.setLayout(misc_tab_2_layout) 
            misc_tab_3.setLayout(misc_tab_3_layout) 
            misc_tab_widget.addTab(misc_tab_1,"misc")
            misc_tab_widget.addTab(misc_tab_2,"car")
            misc_tab_widget.addTab(misc_tab_3,"sponsor")

            misc_tab_widget.setFixedWidth(170)
        # --- End of Section 1 ---
            if account.has_league:
            # --- Start of Section 2 ---
                    race_info_widget = QWidget()
                    race_info_grid_layout = QGridLayout()
                    race_name_label = QLabel(account.strategy[0]['raceName'])
                    race_time_label = QLabel(account.strategy[0]['raceTime'])
                    race_weather_label = QLabel(account.strategy[0]['pWeather'])
                    car_design_button =QPushButton('car/research')
                    car_design_button.setProperty('account',account) #----------------------------------------------------------------------
                    car_design_button.clicked.connect(self.load_research)
                    race_info_grid_layout.addWidget(race_name_label,0,0,1,1)
                    race_info_grid_layout.addWidget(race_time_label,1,0,1,1)
                    race_info_grid_layout.addWidget(race_weather_label,2,0,1,1)
                    race_info_grid_layout.addWidget(car_design_button,3,0,1,1)
                    race_info_widget.setLayout(race_info_grid_layout)
                    race_info_widget.setFixedWidth(150)
                      
                    # --- End of Section 2 --- 
            car_design_button = None

            def driver_setup(driver_index):
                @asyncSlot()
                async def repair_parts(self):
                    print('attempt to repair parts of',account.nickname,driver_index)
                    response = await account.request_parts_repair(account.car[driver_index])
                    if response == False:
                        print('already repaired or out of engines')
                    else:
                        account.car[0]['total_parts'] = response
                        #parts are shared so it needs to update all the labels
                        for car in account.setup_pyqt_elements:
                            car['parts'][0].setText(str(response))
                        #update the button only for the car requested   
                        account.setup_pyqt_elements[driver_index]['parts'][1].setText("100%")
                        account.setup_pyqt_elements[driver_index]['header'].setText(f"Restock in: {account.car[0]['restock']} race(s)")
                        account.setup_pyqt_elements[driver_index]['parts'][1].setDisabled(True)
                @asyncSlot()
                async def repair_engine(self):
                    print('attempt to repair engine of',account.nickname,driver_index)
                    if int(account.car[0]['total_engines']) > 0:
                        response = await account.request_engine_repair(account.car[driver_index])

                        if response == False:
                            print('already repaired')
                        else:
                            account.car[0]['total_engines'] = response
                            for car in account.setup_pyqt_elements:
                                car['engine'][0].setText(str(response))

                            account.setup_pyqt_elements[driver_index]['engine'][1].setText("100%")
                            account.setup_pyqt_elements[driver_index]['engine'][1].setDisabled(True)
                    else:
                        print('out of engines')
                @asyncSlot()        
                async def on_try_practice(self):
                    print('attempting to do practice lap')
                    await account.do_practice_lap(driver_index)   
                strategy_widget = QWidget()
                strategy_widget_layout = QHBoxLayout()
                # --- Start of Section 3 ---
                car_condition_widget =QWidget()
                car_condition_layout = QGridLayout()
                header_car_condition_1 = QLabel(f"Restock in: {account.car[0]['restock']} race(s)")
                if account.car[driver_index]['repair_cost'] > 0:
                    header_car_condition_1.setText(f"{header_car_condition_1.text()}\nRepair cost: {account.car[driver_index]['repair_cost']}")
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
                car_condition_layout.addWidget(header_car_condition_1,0,0,1,3)
                car_condition_layout.addWidget(parts_car_condition_label,1,0,1,1)
                car_condition_layout.addWidget(engine_car_condition_label,2,0,1,1)
                car_condition_layout.addWidget(parts_text,1,1,1,1)
                car_condition_layout.addWidget(engine_text,2,1,1,1)
                car_condition_layout.addWidget(parts_button,1,2,1,1)
                car_condition_layout.addWidget(engine_button,2,2,1,1)
                car_condition_widget.setLayout(car_condition_layout)
                car_condition_widget.setFixedWidth(150)
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

                practice_button = QPushButton('Try')
                tab_3_layout.addWidget(practice_button,0,1,1,1)
                tyre_selection = iGPeasyHelp.tyre_select()
                tyre_selection.setFixedWidth(30)
                tab_3_layout.addWidget(tyre_selection,0,0,1,1)
                tab_3.setLayout(tab_3_layout)
                practice_button.clicked.connect(on_try_practice)


                driver_info_widget.addTab(tab_1,'Driver')
                driver_info_widget.addTab(tab_2,'More')
                driver_info_widget.addTab(tab_3,'Practice')
                driver_info_widget.setFixedWidth(170)
                # --- End of Section 4 ---



                def ride_change(self):
                    account.strategy[driver_index]['ride'] = str(self)
                def wing_change(self):
                    account.strategy[driver_index]['aero'] = str(self)
                def ride_offset_change(self):
                    if self != "-":
                        driver_id = account.staff['drivers'][driver_index]['id']
                        offsets[driver_id][0] = int(self)
                        #account.offsets[driver_index]['ride'] = int(self)
                        #save_json_offsets()
                def wing_offset_change(self):
                    if self != "-":
                        driver_id = account.staff['drivers'][driver_index]['id']
                        offsets[driver_id][1] = int(self)
                        #account.offsets[driver_index]['aero'] = int(self)
                        #save_json_offsets()

                strategy_widget_layout.addWidget(car_condition_widget)
                strategy_widget_layout.addWidget(driver_info_widget)
                
                setup_pyqt_elements =  {'parts':0,
                                        'engine':0,
                                        'header':0,
                                        'track':0,
                                        'setup':{'ride':0,
                                                 'ride_offset':0,
                                                 'wing':0,
                                                 'wing_offset':0,
                                                 'suspension':0,
                                                 'ideal':0,
                                                 'practice_tyre':0},
                                        'strategy':{'modify':0,
                                                    'preview':0,}}
                
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
                                  'ideal':ideal_button,
                                  'practice_tyre':tyre_selection}
                    setup_pyqt_elements['setup'] = setup_pyqt
                    
                    class display_strat(QVBoxLayout):
                        def __init__(self,race_laps,parent=None):
                              super().__init__(parent)
                              self.race_laps = race_laps
                            

                        def clear_preview(self):
                        
                            old_layout = self.layout()
                            for i in reversed(range(old_layout.count())): 
                                widgetToRemove = old_layout.itemAt(i).widget()
                                # remove it from the layout list
                                old_layout.removeWidget(widgetToRemove)
                                # remove it from the gui
                                widgetToRemove.setParent(None)
                            self.estimate_laps.setParent(None)  

                            #self.generate_preview(full_strategy)


                        def generate_preview(self,full_strategy):
                            container = QWidget()
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

                            container.setLayout(inner_layout)
                            self.estimate_laps = QLabel(f" Total laps estimate: {str(total_laps)}/ {self.race_laps}")
                            self.addWidget(container) 
                            self.addWidget(self.estimate_laps) 

                    
                    strategy_container = QWidget()
                    strategy_container_layout = QGridLayout()
                    strategy_container.setMinimumWidth(220)

                    preview_strat = display_strat(str(account.strategy[0]['raceLaps']))
                    preview_strat.generate_preview(account.strategy[driver_index])
                    preview_strat.setProperty('info',account.username)
                    preview_container = QWidget()
                    preview_container.setLayout(preview_strat)
                    #strategy_container_layout.addWidget(laps_label,3,0,1,1)
                    strategy_container_layout.addWidget(preview_container,1,0,2,4)

                 
                    modify_strategy_button = QPushButton('modify')
                    modify_strategy_button.setProperty('account',account)
                    modify_strategy_button.setProperty('driver_index',driver_index)
                    modify_strategy_button.setProperty('preview',preview_strat)

                    modify_strategy_button.clicked.connect(self.popup.strategy_popup)

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
                
                strategy_widget_layout.addStretch()
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
                setup_pyqt_elements['header'] = header_car_condition_1

                
                
                account.setup_pyqt_elements.append(setup_pyqt_elements)

                return strategy_widget
                

            save_button = QPushButton('Save')
            save_button.setMinimumHeight(120)
            
            @asyncSlot()
            async def on_save_strategy(self):
                if account.has_league:
                    save_json_offsets()
                    for driver_index in range(len(account.strategy)):
                        account.strategy[driver_index]['ride'] = str(int(account.strategy[driver_index]['ride']) + int(account.setup_pyqt_elements[driver_index]['setup']['ride_offset'].text()))
                        account.strategy[driver_index]['aero'] = str(int(account.strategy[driver_index]['aero']) + int(account.setup_pyqt_elements[driver_index]['setup']['wing_offset'].text()))
                        
                    await account.save_strategy()        
                    #loop = asyncio.get_event_loop()
                    #loop.run_until_complete(account.save_strategy())
            save_button.clicked.connect(on_save_strategy)


                #suspension_selection.setFixedWidth(60) 
            box_layout.addWidget(save_button)
            box_layout.addWidget(misc_tab_widget)
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
            
            box_layout.addStretch(1)

            #box.setFixedHeight(400)

            box.setLayout(box_layout)
            
            #inserting always before the stretch
            
            self.main_layout.insertWidget(self.main_layout.count() -1,box)
            
            
            account.pyqt_elements = {'track':0,
                                     'money':money_label,
                                     'tokens':token_label,
                                     'daily':daily_button,
                                     'design':car_design_button,
                                     'save':save_button}

        self.accounts = self.parent.valid_accounts
        
        offsets = load_json_offsets()
        
        tasks = []
        for account in self.accounts:
            print('loading', account.username)
            tasks.append(asyncio.create_task(account_group_box(account)))

            # Await all tasks to complete
        await asyncio.gather(*tasks)

        self.main_layout.addStretch(1)
        
        
        self.show_window()

        

    
        
        