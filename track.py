class Track():
  def __init__(self):
    self.info = {
                        'au': { 'length': 5.3017135, 'wear': 40, 'avg':226.1090047 },
                        'my': { 'length': 5.5358276, 'wear': 80, 'avg':208.879 },
                        'cn': { 'length': 5.4417996, 'wear': 80, 'avg':207.975 },
                        'bh': { 'length': 4.7273, 'wear': 60, 'avg':184.933 },
                        'es': { 'length': 4.4580207, 'wear': 85, 'avg':189.212 },
                        'mc': { 'length': 4.0156865, 'wear': 20, 'avg':187 },
                        'tr': { 'length': 5.1630893, 'wear': 90, 'avg':196 },
                        'de': { 'length': 4.1797523, 'wear': 50, 'avg':215.227 },
                        'hu': { 'length': 3.4990127, 'wear': 30, 'avg':165.043 },
                        'eu': { 'length': 5.5907145, 'wear': 45, 'avg':199.05 },
                        'be': { 'length': 7.0406127, 'wear': 60, 'avg':217.7 },
                        'it': { 'length': 5.4024186, 'wear': 35, 'avg':263.107 },
                        'sg': { 'length': 5.049042, 'wear': 45, 'avg':187.0866142 },
                        'jp': { 'length': 5.0587635, 'wear': 70, 'avg':197.065 },
                        'br': { 'length': 3.9715014, 'wear': 60, 'avg':203.932 },
                        'ae': { 'length': 5.412688, 'wear': 50, 'avg':213.218309 },
                        'gb': { 'length': 5.75213, 'wear': 65, 'avg':230.552 },
                        'fr': { 'length': 5.882508, 'wear': 80, 'avg':215.1585366 },
                        'at': { 'length': 4.044372, 'wear': 60, 'avg':228.546 },
                        'ca': { 'length': 4.3413563, 'wear': 45, 'avg':221.357243 },
                        'az': { 'length': 6.053212, 'wear': 45, 'avg':220.409 },
                        'mx': { 'length': 4.3076024, 'wear': 60, 'avg':172.32 },
                        'ru': { 'length': 6.078335, 'wear': 50, 'avg':197.092 },
                        'us': { 'length': 4.60296, 'wear': 65, 'avg':186.568 }}
    self.multipliers = { 100: 1, 75: 1.25, 50: 1.5, 25: 3 }