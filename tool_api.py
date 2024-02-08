import requests, re, json
from bs4 import BeautifulSoup

class iGP_account:
    def __init__(self,account):
        self.session = requests.Session()
        self.username  = account['username']
        self.password  = account['password']
        
    def save_setup_field(self,pyqt_elements):
        self.setups = pyqt_elements
        print(self.setups)
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
                print(response.json())
                if response.json()['status']!= 1:
                    return False
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

         car = []
         soup_engine = BeautifulSoup(json_data['c1Engine'], 'html.parser')
         soup_parts = BeautifulSoup(json_data['c1Condition'], 'html.parser')
         soup_total_engine = BeautifulSoup(json_data['totalEngines'], 'html.parser')
         soup_total_parts = BeautifulSoup(json_data['totalParts'], 'html.parser')
         car.append ({'engine':soup_engine.div.div.get('style').split(':')[1].strip(),
                      'parts':soup_parts.div.div.get('style').split(':')[1].strip(),
                      'restock':json_data['restockRaces'],
                      'total_engines':int(soup_total_engine.text.split(' ')[1]),
                      'total_parts':int(soup_total_parts.text.split(' ')[1]),
                      'id':json_data['c1Id'],
                      'car_number':1,
                      'repair_cost':int(re.findall(r'\d+',BeautifulSoup(BeautifulSoup(json_data['c1Btns'], 'html.parser').a['data-tip'],'html.parser').contents[0])[0])})

         if json_data['c2Hide'] == 'hide':
            soup_engine = BeautifulSoup(json_data['c2Engine'], 'html.parser')
            soup_parts = BeautifulSoup(json_data['c2Condition'], 'html.parser')
            car.append = ({'engine':soup_engine.div.div.get('style').split(':')[1].strip(),
                         'parts':soup_parts.div.div.get('style').split(':')[1].strip(),
                         'id':json_data['c2Id'],
                         'car_number':2,
                         'repair_cost':int(re.findall(r'\d+',BeautifulSoup(BeautifulSoup(json_data['c2Btns'], 'html.parser').a['data-tip'],'html.parser').contents[0])[0])})   
         self.car = car
         return car
    def staff_info(self):
         fetch_url = "https://igpmanager.com/index.php?action=fetch&p=staff&csrfName=&csrfToken="
         response = self.session.get(fetch_url)
         json_data = response.json()['vars']

         driver = []
         soup_driver = BeautifulSoup(json_data['d1Name'], 'html.parser')
         soup_driver_info = BeautifulSoup(json_data['d1Info'], 'html.parser')
         attributes = soup_driver.find('span',class_='hoverData').get('data-driver').split(',')
         driver.append ({'name':soup_driver.find('div').contents[4].strip(),
                      'health':attributes[12],
                      'height':attributes[13],
                      'contract':f"{soup_driver_info.table.contents[1].contents[1].contents[0].strip()}"})

         if json_data['d2Hide'] == 'hide':
            soup_driver = BeautifulSoup(json_data['d2Name'], 'html.parser')
            soup_driver_info = BeautifulSoup(json_data['d2Info'], 'html.parser')
            driver.append ({'name':soup_driver.find('div').contents[4].strip(),
                      'health':attributes[12],
                      'height':attributes[13],
                      'contract':f"{soup_driver_info.table.contents[1].contents[1].contents[0].strip()}"})  
         
         staff = {'drivers':driver}
         self.staff = staff
         #to do. parse the attributes?
         return staff
    def next_race_info(self):
        fetch_url = "https://igpmanager.com/index.php?action=fetch&p=race&csrfName=&csrfToken="
        response = self.session.get(fetch_url)
        json_data = response.json()['vars']
        strategy = []

        if 'd1FuelOrLaps' not in json_data:
            self.has_league = False
            return False
        self.has_league = True
        saved_strat_data = BeautifulSoup(json_data['d1FuelOrLaps'], 'html.parser')
        ## [stint] ->[tyre,laps,fuel]
        saved_strat = [[json_data['d1s1Tyre'],saved_strat_data.find('input',{'name':'laps1'})['value'],saved_strat_data.find('input',{'name':'fuel1'})['value']],
                       [json_data['d1s2Tyre'],saved_strat_data.find('input',{'name':'laps2'})['value'],saved_strat_data.find('input',{'name':'fuel2'})['value']],
                       [json_data['d1s3Tyre'],saved_strat_data.find('input',{'name':'laps3'})['value'],saved_strat_data.find('input',{'name':'fuel3'})['value']],
                       [json_data['d1s4Tyre'],saved_strat_data.find('input',{'name':'laps4'})['value'],saved_strat_data.find('input',{'name':'fuel4'})['value']],
                       [json_data['d1s5Tyre'],saved_strat_data.find('input',{'name':'laps5'})['value'],saved_strat_data.find('input',{'name':'fuel5'})['value']]]

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
            saved_strat = [[json_data['d1s1Tyre'],saved_strat_data.find('input',{'name':'laps1'})['value'],saved_strat_data.find('input',{'name':'fuel1'})['value']],
                       [json_data['d2s2Tyre'],saved_strat_data.find('input',{'name':'laps2'})['value'],saved_strat_data.find('input',{'name':'fuel2'})['value']],
                       [json_data['d2s3Tyre'],saved_strat_data.find('input',{'name':'laps3'})['value'],saved_strat_data.find('input',{'name':'fuel3'})['value']],
                       [json_data['d2s4Tyre'],saved_strat_data.find('input',{'name':'laps4'})['value'],saved_strat_data.find('input',{'name':'fuel4'})['value']],
                       [json_data['d2s5Tyre'],saved_strat_data.find('input',{'name':'laps5'})['value'],saved_strat_data.find('input',{'name':'fuel5'})['value']]]
            strategy.append({'rules':json.loads(json_data['rulesJson']),
                         'suspension':json_data['d2Suspension'],
                         'aero':json_data['d2Aerodynamics'],
                         'ride':json_data['d2Ride'],
                         'pits':json_data['d2Pits'],
                         'pushLevel':BeautifulSoup(json_data['d2PushLevel'], 'html.parser').find('option',selected=True)['value'],
                         'strat':saved_strat})

        self.strategy = strategy
        return strategy
    def save_strategy(self):
        #to do
        #send form data with saved strategy
        url = 'https://igpmanager.com/index.php?action=send&type=saveAll&addon=igp&ajax=1&jsReply=saveAll&csrfName=&csrfName=&csrfToken=&csrfToken=&pageId=race'
    def request_parts_repair(self,car):
        fetch_url = f"https://igpmanager.com/index.php?action=send&type=fix&car={car['id']}&btn=%23c{car['car_number']}PartSwap&jsReply=fix&csrfName=&csrfToken="
        response = self.session.get(fetch_url)
        return '100%'
    def request_engine_repair(self,car):
        fetch_url = f"https://igpmanager.com/index.php?action=send&type=engine&car={car['id']}&btn=%23c{car['car_number']}EngSwap&jsReply=fix&csrfName=&csrfToken="
        response = self.session.get(fetch_url)
        #to do check response to see if engine was repaired
        return '100%'
    