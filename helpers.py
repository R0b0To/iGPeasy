
import math
from PyQt6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, QSize, Qt
from PyQt6.QtWidgets import QWidget, QToolButton, QFrame, QScrollArea, QGridLayout, QSizePolicy,QComboBox, QStyledItemDelegate,QStylePainter,QWidget
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
  def get_league_length_multiplier(self):
        return self.multipliers[self.info[self.race_laps]]
  def set_tyre_wear(self,tyre):
        self.tyre = tyre
    
class iGPeasyHelp():
    def __init__(self, parent=None):
        self.tyre_map = {'SS':0,'S':1,'M':2,'H':3,'I':4,'W':5}
        self.tyre_map_rev = {0:'SS',1:'S',2:'M',3:'H',4:'I',5:'W'}
        self.push_map = {'100':0,'80':1,'60':2,'40':3,'20':4}
        self.push_map_rev = {0:'100',1:'80',2:'60',3:'40',4:'20'}
        self.added_push = {0:0.02,1:0.0081,2:0,3:-0.004,4:-0.007}
        
        
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
   
class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(50, 50))  # Set icon size for the dropdown
        self.setItemDelegate(CustomDelegate(self))

    def paintEvent(self, event):
        # Create a painter object for the combo box
        painter = QStylePainter(self)

        # Draw the custom icon with a smaller size (30x30) when the combobox is closed
        if self.currentIndex() >= 0:
            icon = self.itemIcon(self.currentIndex())
            rect = self.rect()
            pixmap = icon.pixmap(QSize(50, 50))  # Set icon size to 30x30 when closed
            x = rect.x()
            y = rect.y() + (rect.height() - 50) // 2
            painter.drawPixmap(x, y, pixmap)
class CustomDelegate(QStyledItemDelegate):
    def __init__(self, comboBox):
        super().__init__(comboBox)
        self.comboBox = comboBox
    def paint(self, painter, option, index):
        # Adjust the icon size for the selected item
            # Reduce icon size to 30x30 for the selected item
            icon = index.data(Qt.ItemDataRole.DecorationRole)
            icon = icon.pixmap(50,50)
            painter.drawPixmap(option.rect.x(), option.rect.y(), icon)   