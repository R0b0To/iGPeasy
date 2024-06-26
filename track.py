import math
class Track():
  def __init__(self): 
    #last numbers are race laps for each tier  
    self.info = {
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
  
  #tyre, laps
  def stint_wear_calc(t,l,trackCode):
    
    t = float(t)
    l = int(l)
     
    stint = math.exp(1) ** ((-t / 100 * 1.18) * l) * 100
    stint2 = (1 - (1 * ((t) + (0.0212 * l - 0.00926) * Track().info[trackCode]['length']) / 100))
    for j in range(1, l):
        stint2 *= (1 - (1 * ((t) + (0.0212 * j - 0.00926) * Track().info[trackCode]['length']) / 100))
    stint2 *= 100

    average = ((stint + stint2) / 2)
    average = round(average, 2)
    return str(average)