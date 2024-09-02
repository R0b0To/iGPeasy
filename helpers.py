
import math
from PyQt6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, QSize, Qt, QPoint, QRect
from PyQt6.QtWidgets import QWidget,QHBoxLayout,QLabel,QVBoxLayout, QToolButton, QFrame, QScrollArea, QGridLayout, QSizePolicy,QComboBox, QStyledItemDelegate,QStylePainter,QWidget
from PyQt6.QtGui import QIcon,QPixmap
class Track():
  def __init__(self,track_code,race_laps):
    #last numbers are race laps for each tier  
    self.track_code = track_code
    self.race_laps = race_laps
    info = {
                    'au': { 'length': 5.3017135, 'wear': 40, 'avg':226.1090047, '14':25,'28':50,'42':75,'57':100 },
                    'my': { 'length': 5.5358276, 'wear': 80, 'avg':208.879, '13':25,'27':50,'41':75,'55':100 },
                    'cn': { 'length': 5.4417996, 'wear': 80, 'avg':207.975, '13':25,'27':50,'41':75,'55':100 },
                    'bh': { 'length': 4.7273, 'wear': 60, 'avg':184.933, '14':25,'29':50,'44':75,'59':100 },
                    'es': { 'length': 4.4580207, 'wear': 85, 'avg':189.212, '15':25,'31':50,'46':75,'62':100 },
                    'mc': { 'length': 4.0156865, 'wear': 20, 'avg':187, '14':25,'29':50,'44':75,'59':100 },
                    'tr': { 'length': 5.1630893, 'wear': 90, 'avg':196, '13':25,'27':50,'40':75,'54':100 },
                    'de': { 'length': 4.1797523, 'wear': 50, 'avg':215.227, '16':25,'33':50,'50':75,'67':100 },
                    'hu': { 'length': 3.4990127, 'wear': 30, 'avg':165.043, '19':25,'39':50,'59':75,'79':100 },
                    'eu': { 'length': 5.5907145, 'wear': 45, 'avg':199.05, '12':25,'25':50,'37':75,'50':100 },
                    'be': { 'length': 7.0406127, 'wear': 60, 'avg':217.7, '10':25,'21':50,'32':75,'43':100 },
                    'it': { 'length': 5.4024186, 'wear': 35, 'avg':263.107, '12':25,'25':50,'38':75,'51':100 },
                    'sg': { 'length': 5.049042, 'wear': 45, 'avg':187.0866142, '15':25,'30':50,'45':75,'60':100 },
                    'jp': { 'length': 5.0587635, 'wear': 70, 'avg':197.065, '13':25,'27':50,'41':75,'55':100 },
                    'br': { 'length': 3.9715014, 'wear': 60, 'avg':203.932, '17':25,'34':50,'51':75,'69':100 },
                    'ae': { 'length': 5.412688, 'wear': 50, 'avg':213.218309, '12':25,'25':50,'37':75,'50':100 },
                    'gb': { 'length': 5.75213, 'wear': 65, 'avg':230.552, '12':25,'24':50,'36':75,'48':100 },
                    'fr': { 'length': 5.882508, 'wear': 80, 'avg':215.1585366, '12':25,'24':50,'36':75,'48':100 },
                    'at': { 'length': 4.044372, 'wear': 60, 'avg':228.546, '17':25,'34':50,'51':75,'68':100 },
                    'ca': { 'length': 4.3413563, 'wear': 45, 'avg':221.357243, '15':25,'31':50,'47':75,'63':100 },
                    'az': { 'length': 6.053212, 'wear': 45, 'avg':220.409, '11':25,'23':50,'34':75,'46':100 },
                    'mx': { 'length': 4.3076024, 'wear': 60, 'avg':172.32, '17':25,'35':50,'52':75,'70':100 },
                    'ru': { 'length': 6.078335, 'wear': 50, 'avg':197.092, '11':25,'23':50,'34':75,'46':100 },
                    'us': { 'length': 4.60296, 'wear': 65, 'avg':186.568, '15':25,'30':50,'45':75,'60':100 }}
    
    self.multipliers = { 100: 1, 75: 1.25, 50: 1.5, 25: 3 }
    self.info = info[track_code]
    self.length = self.info[self.race_laps]
  def get_league_length_multiplier(self):
        return self.multipliers[self.length]
  def set_tyre_wear(self,tyre):
        self.tyre = tyre
    
class iGPeasyHelp():
    def __init__(self, parent=None):
        self.tyre_map = {'SS':0,'S':1,'M':2,'H':3,'I':4,'W':5}
        self.tyre_map_rev = {0:'SS',1:'S',2:'M',3:'H',4:'I',5:'W'}
        self.push_map = {'100':0,'80':1,'60':2,'40':3,'20':4}
        self.push_map_rev = {0:'100',1:'80',2:'60',3:'40',4:'20'}
        self.added_push = {0:0.02,1:0.0081,2:0,3:-0.004,4:-0.007}
    def create_row_widget(row_data, comments = None):
        
        if comments is None:
            comments = {"suspension":"","ride_height":"","wing_levels":""}
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        
        row_layout.setContentsMargins(0,0,0,0)
        tyre = QLabel()
        tyre.setPixmap(QPixmap(f"tyres/_{row_data[0]}.png"))
        tyre.setFixedSize(QSize(20,20))
        tyre.setScaledContents(True)
        suspension_text = comments["suspension"] if comments["suspension"] != "" else row_data[1]
        suspension = QLabel(suspension_text)
        ride = QLabel(f"{row_data[2]}{comments["ride_height"]}")
        aero = QLabel(f"{row_data[3]}{comments["wing_levels"]}")
        fuel = QLabel(str(row_data[4]))
        wear = QLabel(str(row_data[5]))
        lap = QLabel(str(row_data[6]))
        

        for item in [tyre,suspension,ride,aero,fuel,wear,lap]:
            item.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignTop)
            row_layout.addWidget(item)
           
        return row_widget    
        
    def abbreviate_number(n):
        """Convert a large number into a more readable string with a suffix."""
        suffixes = ['', 'K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
        magnitude = 0
    
        while abs(n) >= 1000 and magnitude < len(suffixes) - 1:
            magnitude += 1
            n /= 1000.0
    
        return f'{n:.1f}{suffixes[magnitude]}'  
    def wear_calc(tyre_eco,track):
        print(track)
        tyreWearFactors = {'SS': 2.14,'S': 1.4,'M': 1,'H': 0.78}
        calculation = (1.43 * tyre_eco ** -0.0778) * (0.00364 * track.info['wear'] + 0.354) * track.info['length'] * 1.384612 * track.get_league_length_multiplier()
        return {    "SS": "{:.1f}".format(calculation * tyreWearFactors['SS']),
                    "S" : "{:.1f}".format(calculation * tyreWearFactors['S']),
                    "M" : "{:.1f}".format(calculation * tyreWearFactors['M']),
                    "H" : "{:.1f}".format(calculation * tyreWearFactors['H']),
                    "I" : "{:.1f}".format(calculation * tyreWearFactors['M']),
                    "W" : "{:.1f}".format(calculation * tyreWearFactors['M'])
                }
    #add tyre text also
    def tyre_select(w,h):
        tyre_select_box = CustomComboBox(w,h)
        for option in ['tyres/_SS.png','tyres/_S.png','tyres/_M.png','tyres/_H.png','tyres/_I.png','tyres/_W.png']:
            tyre = QIcon(option)
            tyre_select_box.addItem(tyre,'')
        #tyre_select_box.setIconSize(QSize(47,47))
        tyre_select_box.setFixedWidth(w)
        return tyre_select_box      
    #tyre laps TRACK
    def stint_wear_calc(t,l,track):
    
        t = float(t)
        l = int(l)

        stint = math.exp(1) ** ((-t / 100 * 1.18) * l) * 100
        stint2 = (1 - (1 * ((t) + (0.0212 * l - 0.00926) * track.info['length']) / 100))
        for j in range(1, l):
            stint2 *= (1 - (1 * ((t) + (0.0212 * j - 0.00926) * track.info['length']) / 100))
        stint2 *= 100

        average = ((stint + stint2) / 2)
        average = round(average, 2)
        return str(average)
    def fuel_calc(f):
        if f >= 100:
            return (f ** -0.0792) * 0.652
        elif f >= 80:
            return (f ** -0.081) * 0.657
        elif f >= 60:
            return (f ** -0.0835) * 0.665
        elif f >= 40:
            return (f ** -0.0854) * 0.669
        elif 20 <= f < 40:
            return (f ** -0.0886) * 0.678
        else:
            return (f ** -0.0947) * 0.69 

class Section(QWidget):
    def __init__(self, title="", animationDuration=100, parent=None):
        super().__init__(parent)
        self.animationDuration = animationDuration
        self.toggleButton = QToolButton(self)
        self.headerLine = QFrame(self)
        self.toggleAnimation = QParallelAnimationGroup(self)
        self.contentArea = QScrollArea(self)
        self.mainLayout = QGridLayout(self)
    
        self.toggleButton.setStyleSheet("QToolButton {border: none;}")
        self.toggleButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggleButton.setArrowType(Qt.ArrowType.RightArrow)
        self.toggleButton.setText(title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)
    
        self.headerLine.setFrameShape(QFrame.Shape.HLine)
        self.headerLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.headerLine.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
    
        self.contentArea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
    
        # let the entire widget grow and shrink with its content
        self.toggleAnimation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggleAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggleAnimation.addAnimation(QPropertyAnimation(self.contentArea, b"maximumHeight"))
    
        self.mainLayout.setVerticalSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
    
        row = 0
        self.mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        self.mainLayout.addWidget(self.contentArea, row+1, 0, 1, 3)
        self.setLayout(self.mainLayout)
    
        self.toggleButton.toggled.connect(self.toggle)
    def isChecked(self):
        return self.toggleButton.isChecked()
    def setChecked(self,bool):
        self.toggleButton.setChecked(bool)   
    def setContentLayout(self, contentLayout):
        layout = self.contentArea.layout()
        if layout:
            layout.deleteLater()
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(0, self.toggleAnimation.animationCount()-1):
            SectionAnimation = self.toggleAnimation.animationAt(i)
            SectionAnimation.setDuration(self.animationDuration)
            SectionAnimation.setStartValue(collapsedHeight)
            SectionAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

    def toggle(self, collapsed):
        if collapsed:
            print('open')
            self.toggleButton.setArrowType(Qt.ArrowType.DownArrow)
            self.toggleAnimation.setDirection(QAbstractAnimation.Direction.Forward)
        else:
            self.toggleButton.setArrowType(Qt.ArrowType.RightArrow)
            self.toggleAnimation.setDirection(QAbstractAnimation.Direction.Backward)
        self.toggleAnimation.start()
class PseudoComboBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.dropdown = QWidget()
        self.dropdown_layout = QVBoxLayout()
        self.dropdown.setLayout(self.dropdown_layout)
        self.dropdown.setWindowFlags(Qt.WindowType.Popup)
        
    def add_event(self,widget):
        widget.mousePressEvent = self.show_dropdown

    
    def set_main_widget(self,widget):
        if self.main_layout.count() > 0:
            old_widget = self.main_layout.itemAt(0).widget()

            if old_widget is not None:
                self.main_layout.removeWidget(old_widget)
                self.add_items(old_widget)
        widget.mousePressEvent = self.show_dropdown
        self.main_layout.addWidget(widget)
    def add_items(self, item):
        self.dropdown_layout.insertWidget(0,item)
        
    
    def show_dropdown(self, event):
        pos = self.mapToGlobal(self.pos())
        dropdown_width = self.sizeHint().width() + 50
        dropdown_height = self.sizeHint().height() 
        self.dropdown.setGeometry(QRect(pos + QPoint(0, self.height()-40),QSize(dropdown_width, dropdown_height)))
        self.dropdown.show()   
class CustomComboBox(QComboBox):
    def __init__(self,w,h,parent=None):
        super().__init__(parent)
        self.incon_size = QSize(w,h)
        self.setIconSize(self.incon_size)
        self.setItemDelegate(CustomDelegate(self,w,h))

        
    def get_current_tyre_text(self):
        return iGPeasyHelp().tyre_map_rev[self.currentIndex()]
    def paintEvent(self, event):
        # Create a painter object for the combo box
        painter = QStylePainter(self)

        # Draw the custom icon with a smaller size (30x30) when the combobox is closed
        if self.currentIndex() >= 0:
            icon = self.itemIcon(self.currentIndex())
            rect = self.rect()
            pixmap = icon.pixmap(self.incon_size)  
            x = rect.x()
            y = rect.y() + (rect.height() - self.incon_size.width()) // 2
            painter.drawPixmap(x, y, pixmap)

class CustomDelegate(QStyledItemDelegate):
    def __init__(self, comboBox,w,h):
        super().__init__(comboBox)
        self.comboBox = comboBox
        self.icon_size = [w,h]
    def paint(self, painter, option, index):
        # Adjust the icon size for the selected item
            # Reduce icon size to 30x30 for the selected item
            icon = index.data(Qt.ItemDataRole.DecorationRole)
            icon = icon.pixmap(self.icon_size[0],self.icon_size[1])
            painter.drawPixmap(option.rect.x(), option.rect.y(), icon)   