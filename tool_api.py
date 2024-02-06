import requests

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
         return response.json()['vars']
    def staff_info(self):
         fetch_url = "https://igpmanager.com/index.php?action=fetch&p=staff&csrfName=&csrfToken="
         response = self.session.get(fetch_url)
         #to do. parse the attributes?
         return response.json()['vars']
    def next_race_info(self):
         fetch_url = "https://igpmanager.com/index.php?action=fetch&p=race&csrfName=&csrfToken="
         response = self.session.get(fetch_url)
         #to do. parse the attributes?
         return response.json()['vars']
    def save_strategy(self):
        #to do
        #send form data with saved strategy
        url = 'https://igpmanager.com/index.php?action=send&type=saveAll&addon=igp&ajax=1&jsReply=saveAll&csrfName=&csrfName=&csrfToken=&csrfToken=&pageId=race'