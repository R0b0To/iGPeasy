import requests
from bs4 import BeautifulSoup

class iGP_account:
    def __init__(self,account):
        self.session = requests.Session()
        self.username  = account['username']
        self.password  = account['password']

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
                      'total_engines':soup_total_engine.text.split(' ')[1],
                      'total_parts':soup_total_parts.text.split(' ')[1],
                      'id':json_data['c1Id'],
                      'car_number':1})

         if json_data['c2Hide'] == 'hide':
            soup_engine = BeautifulSoup(json_data['c2Engine'], 'html.parser')
            soup_parts = BeautifulSoup(json_data['c2Condition'], 'html.parser')
            car.append = ({'engine':soup_engine.div.div.get('style').split(':')[1].strip(),
                         'parts':soup_parts.div.div.get('style').split(':')[1].strip(),
                         'id':json_data['c2Id'],
                         'car_number':2})   
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
         #to do. parse the attributes?
         return staff
    def next_race_info(self):
         fetch_url = "https://igpmanager.com/index.php?action=fetch&p=race&csrfName=&csrfToken="
         response = self.session.get(fetch_url)
         #to do. parse the attributes?
         return response.json()['vars']
    def save_strategy(self):
        #to do
        #send form data with saved strategy
        url = 'https://igpmanager.com/index.php?action=send&type=saveAll&addon=igp&ajax=1&jsReply=saveAll&csrfName=&csrfName=&csrfToken=&csrfToken=&pageId=race'
    def request_parts_repair(self,car):
        fetch_url = f"https://igpmanager.com/index.php?action=send&type=fix&car={car['id']}&btn=%23c{car['car_number']}PartSwap&jsReply=fix&csrfName=&csrfToken="
        response = self.session.get(fetch_url)
        print(response.json())
    def request_engine_repair(self,car):
        fetch_url = f"https://igpmanager.com/index.php?action=send&type=engine&car={car['id']}&btn=%23c{car['car_number']}EngSwap&jsReply=fix&csrfName=&csrfToken="
        response = self.session.get(fetch_url)
        print(response.json())
