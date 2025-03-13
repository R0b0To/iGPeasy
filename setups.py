class CarSetup:
    def __init__(self,track_code,height,tier):
        tier_mapping = {20: 1, 50: 2, 100: 3} #tier should be somewhere in the account.
        self.track_code = track_code
        self.driver_height = (int(height) // 5) * 5
        self.tier = tier_mapping[tier]
        self.suggested_setup = self.const_setup()


    def const_setup(self):
        scale = {
  190: { 3: -8, 2: -4, 1: -2 },
  185: { 3: -6, 2: -3, 1: -1 },
  180: { 3: -4, 2: -2, 1: -1 },
  175: { 3: -2, 2: -1, 1: 0 },
  170: { 3: 0, 2: 0, 1: 0 },
  165: { 3: 2, 2: 1, 1: 0 },
  160: { 3: 2, 2: 1, 1: 0 },
}
        circuits = {
  # rookie
  1: {
    'ae': { 'ride': 6, 'wing': 1, 'suspension': 1, 'pit': 23 },
    'at': { 'ride': 4, 'wing': 0, 'suspension': 2, 'pit': 27 },
    'au': { 'ride': 9, 'wing': 4, 'suspension': 1, 'pit': 24 }, 
    'az': { 'ride': 8, 'wing': 1, 'suspension': 1, 'pit': 17 },
    'be': { 'ride': 6, 'wing': 3, 'suspension': 1, 'pit': 15 }, 
    'bh': { 'ride': 4, 'wing': 0, 'suspension': 2, 'pit': 23 }, 
    'br': { 'ride': 4, 'wing': 2, 'suspension': 1, 'pit': 21 }, 
    'ca': { 'ride': 4, 'wing': -1,'suspension': 2, 'pit': 17 },
    'cn': { 'ride': 2, 'wing': 2, 'suspension': 1, 'pit': 26 },
    'de': { 'ride': 4, 'wing': 2, 'suspension': 1, 'pit': 17 },
    'es': { 'ride': 2, 'wing': 5, 'suspension': 0, 'pit': 25 },
    'eu': { 'ride': 6, 'wing': 5, 'suspension': 0, 'pit': 17 },
    'fr': { 'ride': 8, 'wing': 2, 'suspension': 1, 'pit': 20 },
    'gb': { 'ride': 4, 'wing': 0, 'suspension': 2, 'pit': 23 },
    'hu': { 'ride': 5, 'wing': 6, 'suspension': 0, 'pit': 17 },
    'it': { 'ride': 6, 'wing': -2,'suspension': 2, 'pit': 24 },
    'jp': { 'ride': 6, 'wing': 5, 'suspension': 0, 'pit': 20 },
    'mc': { 'ride': 11,'wing': 9, 'suspension': 0, 'pit': 16 },
    'mx': { 'ride': 3, 'wing': 2, 'suspension': 1, 'pit': 19 },
    'my': { 'ride': 6, 'wing': 1, 'suspension': 1, 'pit': 22 },
    'ru': { 'ride': 2, 'wing': 2, 'suspension': 1, 'pit': 21 },
    'sg': { 'ride': 8, 'wing': 7, 'suspension': 0, 'pit': 20 },
    'tr': { 'ride': 6, 'wing': 2, 'suspension': 1, 'pit': 18 },
    'us': { 'ride': 2, 'wing': 2, 'suspension': 1, 'pit': 16 }, 
  },
  # pro
  2: {
    'ae': { 'ride': 13,'wing': 3,'suspension': 1,'pit': 23 }, 
    'at': { 'ride': 9,'wing': 0,'suspension': 2,'pit': 27 },
    'au': { 'ride': 19,'wing': 8,'suspension': 1,'pit': 24 }, 
    'az': { 'ride': 17,'wing': 3,'suspension': 1,'pit': 17 }, 
    'be': { 'ride': 12,'wing': 6,'suspension': 1,'pit': 15 }, 
    'bh': { 'ride': 8,'wing': 0,'suspension': 2,'pit': 23 },
    'br': { 'ride': 8,'wing': 5,'suspension': 1,'pit': 21 },
    'ca': { 'ride': 9,'wing': -3,'suspension': 2,'pit': 17 }, 
    'cn': { 'ride': 5,'wing': 5,'suspension': 1,'pit': 26 },
    'de': { 'ride': 8,'wing': 5,'suspension': 1,'pit': 17 },
    'es': { 'ride': 5,'wing': 10,'suspension': 0,'pit': 25 }, 
    'eu': { 'ride': 12,'wing': 10,'suspension': 0,'pit': 17 },
    'fr': { 'ride': 17,'wing': 5,'suspension': 1,'pit': 20 }, 
    'gb': { 'ride': 9,'wing': 0,'suspension': 2,'pit': 23 },
    'hu': { 'ride': 10,'wing': 13,'suspension': 0,'pit': 17 },
    'it': { 'ride': 12,'wing': -5,'suspension': 2,'pit': 24 },
    'jp': { 'ride': 12,'wing': 10,'suspension': 0,'pit': 20 },
    'mc': { 'ride': 22,'wing': 18,'suspension': 0,'pit': 16 },
    'mx': { 'ride': 7,'wing': 5,'suspension': 1,'pit': 19 },
    'my': { 'ride': 12,'wing': 3,'suspension': 1,'pit': 22 }, 
    'ru': { 'ride': 4,'wing': 5,'suspension': 1,'pit': 21 },
    'sg': { 'ride': 17,'wing': 14,'suspension': 0,'pit': 20 },
    'tr': { 'ride': 13,'wing': 5,'suspension': 1,'pit': 18 }, 
    'us': { 'ride': 4,'wing': 4,'suspension': 1,'pit': 16 },
  },
  # elite
  3: {
    'ae': { 'ride': 25, 'wing': 5, 'suspension': 1, 'pit': 23 },
    'at': { 'ride': 18, 'wing': 0, 'suspension': 2, 'pit': 27 },
    'au': { 'ride': 38, 'wing': 15, 'suspension': 1, 'pit': 24 },
    'az': { 'ride': 33, 'wing': 5, 'suspension': 1, 'pit': 17 },
    'be': { 'ride': 23, 'wing': 12, 'suspension': 1, 'pit': 15 },
    'bh': { 'ride': 15, 'wing': 0, 'suspension': 2, 'pit': 23 },
    'br': { 'ride': 15, 'wing': 10, 'suspension': 1, 'pit': 21 },
    'ca': { 'ride': 18, 'wing': -5, 'suspension': 2, 'pit': 17 },
    'cn': { 'ride': 10, 'wing': 10, 'suspension': 1, 'pit': 26 },
    'de': { 'ride': 15, 'wing': 10, 'suspension': 1, 'pit': 17 },
    'es': { 'ride': 10, 'wing': 20, 'suspension': 0, 'pit': 25 },
    'eu': { 'ride': 23, 'wing': 20, 'suspension': 0, 'pit': 17 },
    'fr': { 'ride': 33, 'wing': 10, 'suspension': 1, 'pit': 20 },
    'gb': { 'ride': 18, 'wing': 0, 'suspension': 2, 'pit': 23 },
    'hu': { 'ride': 20, 'wing': 25, 'suspension': 0, 'pit': 17 },
    'it': { 'ride': 23, 'wing': -10, 'suspension': 2, 'pit': 24 },
    'jp': { 'ride': 23, 'wing': 20, 'suspension': 0, 'pit': 20 },
    'mc': { 'ride': 43, 'wing': 35, 'suspension': 0, 'pit': 16 },
    'mx': { 'ride': 13, 'wing': 10, 'suspension': 1, 'pit': 19 },
    'my': { 'ride': 23, 'wing': 5, 'suspension': 1, 'pit': 22 },
    'ru': { 'ride': 8, 'wing': 10, 'suspension': 1, 'pit': 21 },
    'sg': { 'ride': 33, 'wing': 27, 'suspension': 0, 'pit': 20 },
    'tr': { 'ride': 25, 'wing': 10, 'suspension': 1, 'pit': 18 },
    'us': { 'ride': 8, 'wing': 7, 'suspension': 1, 'pit': 16 },
  }
}
        setup = circuits[self.tier][self.track_code]
        setup['ride'] += scale[self.driver_height][self.tier]
        if setup['ride'] == 0:
          setup['ride']=1
        if setup['wing'] <= 0:
          setup['wing']=1
        self.suspension =setup['suspension']
        self.ride = setup['ride']
        self.wing = setup['wing']
        return setup