import requests, re, json, time
from bs4 import BeautifulSoup

class iGP_account:
    def __init__(self,account):
        self.session = requests.Session()
        self.username  = account['username']
        self.password  = account['password']
    def fetch_url(self,fetch_url):
        response = self.session.get(fetch_url)
        
        if 'vars' not in response.json():
           return 'contract?' 
        
        json_data = response.json()['vars']
        return json_data

    def init_account(self):
        self.car = self.car_info()
        self.staff = self.staff_info()
        self.strategy = self.next_race_info()
    def research_info(self):
        research_display = self.fetch_url("https://igpmanager.com/index.php?action=fetch&d=research&csrfName=&csrfToken=")
        car_overview= self.fetch_url("https://igpmanager.com/index.php?action=fetch&d=design&csrfName=&csrfToken=")
        points = car_overview['designPts']
        max_design = car_overview['dMax']
        
        car_design = [car_overview[key] for key in ['acceleration', 'braking', 'cooling', 'downforce', 'fuel_economy', 'handling', 'reliability', 'tyre_economy']]

        tier_factor = 2 if max_design == 200 else 1

        research_power = research_display['researchMaxEffect']
        # remember tier have different max 

        def parse_best(attribute):
            return int(BeautifulSoup(research_display[attribute],'html.parser').img.get('style').split('calc(')[1].split('%')[0]) * tier_factor
        
        def is_checked(key):
            if BeautifulSoup(research_display[key],'html.parser').input.get('checked') is not None:
                return True
            else: 
                return False
        teams_design = [parse_best(key) for key in ['accelerationRating','brakingRating','coolingRating','downforceRating','fuel_economyRating','handlingRating','reliabilityRating','tyre_economyRating']]
        checked_design = [is_checked(key) for key in ['accelerationCheck','brakingCheck','coolingCheck','downforceCheck','fuel_economyCheck','handlingCheck','reliabilityCheck','tyre_economyCheck']]
        
        return {'car_design':car_design,'teams_design':teams_design,'max':max_design,'points':points,'research_power':research_power,'check':checked_design}


    def save_setup_field(self,pyqt_elements):
        self.setups = pyqt_elements
    def login(self):
        try:
            login_url = "https://igpmanager.com/index.php?action=send&addon=igp&type=login&jsReply=login&ajax=1"
            # Using a bot account for the login 
            login_data =  {'loginUsername':self.username,
                        'loginPassword':self.password, 
                        'loginRemember': 'on',
                        'csrfName': '',
                        'csrfToken': ''}     
            response =  self.session.post(login_url, data=login_data)
            # Check if the login was successful
            if response.ok:
                print(f"Loading {self.username}")
                if response.json()['status']!= 1:
                    return False
                self.init_account()
                return True
            else:
                print("Login failed. Status code:", response.status_code)
            return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    def car_info(self):
         fetch_url = "https://igpmanager.com/index.php?action=fetch&p=cars&csrfName=&csrfToken="
         response = self.session.get(fetch_url)
         json_data = response.json()['vars']
         # if c2Hide = 'hide' the manager is in a 1 car league

         car_list = []
         soup_engine = BeautifulSoup(json_data['c1Engine'], 'html.parser')
         soup_parts = BeautifulSoup(json_data['c1Condition'], 'html.parser')
         soup_total_engine = BeautifulSoup(json_data['totalEngines'], 'html.parser')
         soup_total_parts = BeautifulSoup(json_data['totalParts'], 'html.parser')
         
         car_list.append ({'engine':soup_engine.div.div.get('style').split(':')[1].strip(),
                      'parts':soup_parts.div.div.get('style').split(':')[1].strip(),
                      'fuel_economy':json_data['fuel_economyBar'],
                      'tyre_economy':json_data['tyre_economyBar'],
                      'restock':json_data['restockRaces'],
                      'total_engines':int(soup_total_engine.text.split(' ')[1]),
                      'total_parts':int(soup_total_parts.text.split(' ')[1]),
                      'id':json_data['c1Id'],
                      'car_number':1,
                      'repair_cost':int(re.findall(r'\d+',BeautifulSoup(BeautifulSoup(json_data['c1Btns'], 'html.parser').a['data-tip'],'html.parser').contents[0])[0])})
         if json_data['c2Hide'] == '':
            soup_engine = BeautifulSoup(json_data['c2Engine'], 'html.parser')
            soup_parts = BeautifulSoup(json_data['c2Condition'], 'html.parser')
            engine = soup_engine.div.div.get('style').split(':')[1].strip()
            parts = soup_parts.div.div.get('style').split(':')[1].strip()
            car_list.append({'engine':engine,
                    'parts':parts,
                    'id':json_data['c2Id'],
                    'car_number':2,
                    'repair_cost':int(re.findall(r'\d+',BeautifulSoup(BeautifulSoup(json_data['c2Btns'], 'html.parser').a['data-tip'],'html.parser').contents[0])[0])})   
        
         return car_list
    def train_driver(self,id,intensity,category):
        url =f"https://igpmanager.com/index.php?{id}={category}&action=send&addon=igp&type=train&focus=drivers&jsReply=train&ajax=1&intensity={intensity}&c[]=0&c[]={id}&csrfName=&csrfToken="
        response = self.session.get(url)
        response_json = response.json()
        # update the info bmi color will need to request the driver info
        self.staff = self.staff_info()
    def driver_info(self,id):
        json_data = self.fetch_url(f"https://igpmanager.com/index.php?action=fetch&d=driver&id={id}&csrfName=&csrfToken=")
        contract =  BeautifulSoup(BeautifulSoup(json_data['contract'], 'html.parser').find_all('a')[1]['data-tip'],'html.parser').text
        cost = re.search(r'\$\d+(\.\d+)?.', contract).group(0)
        duration= re.findall(r'\d+(?:\.\d+)?', contract)[0]
        bmi_color = BeautifulSoup(json_data['sBmi'], 'html.parser').span['class'][1].split('-')[1]
        return {'contract':{'duration':duration,'cost':cost},'attributes':{'weight':json_data['sWeight'],'bmi_color':bmi_color}}
    
    def h_until_next_race(self):
       current_timestamp = time.time()
       difference_seconds = self.next_race - current_timestamp
       return str(round(difference_seconds / 3600,1))
     

    def staff_info(self): 
         response = self.session.get(f"https://igpmanager.com/index.php?action=fetch&p=staff&csrfName=&csrfToken=")
         response_json = response.json()
         json_data = response_json['vars'] 
         self.next_race = response_json['nextLeagueRaceTime']
         driver = []
         soup_driver = BeautifulSoup(json_data['d1Name'], 'html.parser')
         soup_driver_info = BeautifulSoup(json_data['d1Info'], 'html.parser')
         attributes = soup_driver.find('span',class_='hoverData').get('data-driver').split(',')
         driver.append ({'name':soup_driver.find('div').contents[4].strip(),
                      'health':attributes[12],
                      'id':re.findall(r'\d+', soup_driver.a.get('href'))[0],
                      'height':attributes[13],
                      'salary': f"{soup_driver_info.table.contents[2].contents[1].contents[0].strip()}",
                      'contract':f"{soup_driver_info.table.contents[1].contents[1].contents[0].strip()}",
                      'attributes':attributes})

         if json_data['d2Hide'] == '':
            soup_driver = BeautifulSoup(json_data['d2Name'], 'html.parser')
            soup_driver_info = BeautifulSoup(json_data['d2Info'], 'html.parser')
            attributes = soup_driver.find('span',class_='hoverData').get('data-driver').split(',')
            driver.append ({'name':soup_driver.find('div').contents[4].strip(),
                      'health':attributes[12],
                      'id':re.findall(r'\d+', soup_driver.a.get('href'))[0],
                      'height':attributes[13],
                      'salary': f"{soup_driver_info.table.contents[2].contents[1].contents[0].strip()}",
                      'contract':f"{soup_driver_info.table.contents[1].contents[1].contents[0].strip()}",
                      'attributes':attributes})  
        

         # also for the staff?
         staff = {'drivers':driver}
         
         #to do. parse the attributes?
         return staff
    def next_race_info(self):
        json_data = self.fetch_url("https://igpmanager.com/index.php?action=fetch&p=race&csrfName=&csrfToken=")
        strategy = []

        if 'd1FuelOrLaps' not in json_data:
            self.has_league = False
            return False
        self.has_league = True
        saved_strat_data = BeautifulSoup(json_data['d1FuelOrLaps'], 'html.parser')
        
        ##       stint              stint
        ## [[tyre,laps,fuel]],[[tyre,laps,fuel]]
        saved_strat = [[json_data[f'd1s{i}Tyre'], saved_strat_data.find('input', {'name': f'laps{i}'}).get('value'), saved_strat_data.find('input', {'name': f'fuel{i}'}).get('value')] for i in range(1, 6)]

        strategy.append({'rules':json.loads(json_data['rulesJson']),
                         'raceLaps':json_data['raceLaps'],
                         'raceName':BeautifulSoup(json_data['raceName'], 'html.parser').text.strip(),
                         'raceTime':json_data['raceTime'],
                         'trackId':json_data['trackId'],
                         'trackCode':BeautifulSoup(json_data['raceName'], 'html.parser').img.get('class')[1][2:],
                         'pWeather':BeautifulSoup(json_data['pWeather'], 'html.parser').text,
                         'suspension':json_data['d1Suspension'],
                         'aero':json_data['d1Aerodynamics'],
                         'ride':json_data['d1Ride'],
                         'pits':json_data['d1Pits'],
                         'pushLevel':BeautifulSoup(json_data['d1PushLevel'], 'html.parser').find('option',selected=True)['value'],
                         'strat': saved_strat,
                         'raceId':json_data['raceId'],
                         'tier':json_data['setupMax']})
        # check if 2 cars
        if json_data['d2Pits'] != 0:
            saved_strat_data = BeautifulSoup(json_data['d2FuelOrLaps'], 'html.parser')
            saved_strat = [[json_data[f'd2s{i}Tyre'], saved_strat_data.find('input', {'name': f'laps{i}'}).get('value'), saved_strat_data.find('input', {'name': f'fuel{i}'}).get('value')] for i in range(1, 6)]
            strategy.append({'rules':json.loads(json_data['rulesJson']),
                         'suspension':json_data['d2Suspension'],
                         'aero':json_data['d2Aerodynamics'],
                         'ride':json_data['d2Ride'],
                         'pits':json_data['d2Pits'],
                         'pushLevel':BeautifulSoup(json_data['d2PushLevel'], 'html.parser').find('option',selected=True)['value'],
                         'strat':saved_strat})

        return strategy
    def save_strategy(self):
        #to do
        #send form data with saved strategy
        url = 'https://igpmanager.com/index.php?action=send&type=saveAll&addon=igp&ajax=1&jsReply=saveAll&csrfName=&csrfName=&csrfToken=&csrfToken=&pageId=race'
   
        d1setup = self.strategy[0]
        d1strategy = self.strategy[0]['strat']
        if len(self.strategy)>1:
            d2strategy = self.strategy[1]['strat']
            d2setup = self.strategy[1]
            d2strategy_c = {
                           "race": d1setup['raceId'],
                           "dNum":"1",
                           "numPits":str(d2setup['pits']),
                           "tyre1":d2strategy[0][0],
                           "tyre2":d2strategy[1][0],
                           "tyre3":d2strategy[2][0],
                           "tyre4":d2strategy[3][0],
                           "tyre5":d2strategy[4][0],
                           "fuel1":d2strategy[0][2],
                           "laps1":d2strategy[0][1],
                           "fuel2":d2strategy[1][2],
                           "laps2":d2strategy[1][1],
                           "fuel3":d2strategy[2][2],
                           "laps3":d2strategy[2][1],
                           "fuel4":d2strategy[3][2],
                           "laps4":d2strategy[3][1],
                           "fuel5":d2strategy[4][2],
                           "laps5":d2strategy[4][1]
                        }
            d2strategyAdvanced = {
                           "pushLevel":"60",
                           "d1SavedStrategy":"0",
                           "ignoreAdvancedStrategy":"1",
                           "advancedFuel":"148",
                           "rainStartTyre":"I",
                           "rainStartDepth":"0",
                           "rainStopTyre":"M",
                           "rainStopLap":"0"
                        }
        else:
            d2setup = {
                           "raceId":self.strategy[0]['raceId'],
                           "suspension":"1",
                           "ride":"0",
                           "aero":"0",
                           "practiceTyre":"SS"
                        }
            d2strategy_c =   {
                           "race":self.strategy[0]['raceId'],
                           "dNum":"2",
                           "numPits":"0",
                           "tyre1":"{{d2s1Tyre}}",
                           "tyre2":"{{d2s2Tyre}}",
                           "tyre3":"{{d2s3Tyre}}",
                           "tyre4":"{{d2s4Tyre}}",
                           "tyre5":"{{d2s5Tyre}}"
                        }
            d2strategyAdvanced = {
                           "d2SavedStrategy":"{{d2Saved}}",
                           "ignoreAdvancedStrategy":"{{d2IgnoreAdvanced}}"
                        }
        strat_data =  {"d1setup":
                       {
                           "race":d1setup['raceId'],
                           "rules":"default",
                           "suspension":str(d1setup['suspension']),
                           "ride":str(d1setup['ride']),
                           "aerodynamics":str(d1setup['aero']),
                           "practiceTyre":"SS"
                        },
                        "d2setup":{
                           "race":d1setup['raceId'],
                           "suspension":str(d2setup['suspension']),
                           "ride":str(d2setup['ride']),
                           "aerodynamics":str(d2setup['aero']),
                           "practiceTyre":"SS"
                        },
                        "d1strategy":{
                           "race": d1setup['raceId'],
                           "dNum":"1",
                           "numPits":str(d1setup['pits']),
                           "tyre1":d1strategy[0][0],
                           "tyre2":d1strategy[1][0],
                           "tyre3":d1strategy[2][0],
                           "tyre4":d1strategy[3][0],
                           "tyre5":d1strategy[4][0],
                           "fuel1":d1strategy[0][2],
                           "laps1":d1strategy[0][1],
                           "fuel2":d1strategy[1][2],
                           "laps2":d1strategy[1][1],
                           "fuel3":d1strategy[2][2],
                           "laps3":d1strategy[2][1],
                           "fuel4":d1strategy[3][2],
                           "laps4":d1strategy[3][1],
                           "fuel5":d1strategy[4][2],
                           "laps5":d1strategy[4][1]
                        },
                        "d2strategy":d2strategy_c,
                        "d1strategyAdvanced":{
                           "pushLevel":"60",
                           "d1SavedStrategy":"1",
                           "ignoreAdvancedStrategy":"1",
                           "rainStartTyre":"I",
                           "rainStartDepth":"0",
                           "rainStopTyre":"M",
                           "rainStopLap":"0"
                        },
                        "d2strategyAdvanced":d2strategyAdvanced
                    }  
        good_format =  str(strat_data).replace("'", "\"")
        response =  self.session.post(url, data=good_format)
        print(f"saved strategy for: ",self.username)

        
    def request_parts_repair(self,car):
        self.fetch_url(f"https://igpmanager.com/index.php?action=send&type=fix&car={car['id']}&btn=%23c{car['car_number']}PartSwap&jsReply=fix&csrfName=&csrfToken=")
        return '100%'
    def request_engine_repair(self,car):
        self.fetch_url( f"https://igpmanager.com/index.php?action=send&type=engine&car={car['id']}&btn=%23c{car['car_number']}EngSwap&jsReply=fix&csrfName=&csrfToken=")
        #to do check response to see if engine was repaired
        return '100%'
    def extend_contract_driver(self,driver):
        self.fetch_url(f"https://igpmanager.com/index.php?action=send&type=contract&enact=extend&eType=3&eId={driver['id']}&jsReply=contract&csrfName=&csrfToken=")
        
        return '50 races'