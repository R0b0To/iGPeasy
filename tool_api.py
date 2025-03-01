import asyncio
import re, json, time, aiohttp, html
from bs4 import BeautifulSoup

class iGP_account:
    def __init__(self,account):
        self.session = aiohttp.ClientSession(raise_for_status=True)
        self.pyqt_elements = {}
        self.setup_pyqt_elements = [] #list because there could be 2 cars
        #self.offsets = [{'ride':0,'aero':0},{'ride':0,'aero':0}]
        self.username  = account['username']
        self.password  = account['password']
        if 'nickname' in account:
            self.nickname  = account['nickname']
        else:
            self.nickname = None
        self.row_index = None
        self.parts_button = None
    
    
    async def fetch_url(self,fetch_url):
        async with self.session.get(fetch_url) as response:
                if response.status == 200:
                    json_response = json.loads(await response.text())

                    if 'vars' not in json_response:
                       return json_response 

                    json_data = json_response['vars']
                    return json_data

    async def close(self):
        await self.session.close()
    async def async_get_general_info(self):
        try:
            url = 'https://igpmanager.com/index.php?action=fireUp&addon=igp&ajax=1&jsReply=fireUp&uwv=false&csrfName=&csrfToken='
            async with self.session.post(url) as response:
                if response.status == 200:
                    json_data = json.loads(await response.text())
                    self.all = json_data
                    self.manager = json_data['manager']
                    self.team = json_data['team']
                    self.notify = json_data['notify']
                    self.daily = None
                else:
                    print("Failed to fetch general info. Status code:", response.status)
        except Exception as e:
            print(f"Error during fetching general info: {e}")
    async def init_account(self):
        
        await self.async_get_general_info()
        self.car = await self.car_info()
        self.staff = await self.staff_info()
        self.strategy = await self.next_race_info()
        await self.get_sponsors()
        
    async def research_info(self):
        research_display = await self.fetch_url("https://igpmanager.com/index.php?action=fetch&d=research&csrfName=&csrfToken=")
        car_overview= await self.fetch_url("https://igpmanager.com/index.php?action=fetch&d=design&csrfName=&csrfToken=")
        points = car_overview['designPts']
        max_design = car_overview['dMax']
        
        car_design = [car_overview[key] for key in ['acceleration', 'braking', 'cooling', 'downforce', 'fuel_economy', 'handling', 'reliability', 'tyre_economy']]
        car_bonus = [car_overview[key] for key in ['accelerationBonus', 'brakingBonus', 'coolingBonus', 'downforceBonus', 'fuel_economyBonus', 'handlingBonus', 'reliabilityBonus', 'tyre_economyBonus']]
        tier_factor = 3 if max_design == 300 else 2

        self.research_power = research_display['researchMaxEffect']
        # remember tier have different max 

        def parse_best(attribute):
            value = int(BeautifulSoup(research_display[attribute],'html.parser').svg.get('style').split('calc(')[1].split('%')[0])
            return  value * tier_factor
        
        def is_checked(key):
            if BeautifulSoup(research_display[key],'html.parser').input.get('checked') is not None:
                return True
            else: 
                return False
        teams_design = [parse_best(key) for key in ['accelerationRating','brakingRating','coolingRating','downforceRating','fuel_economyRating','handlingRating','reliabilityRating','tyre_economyRating']]
        checked_design = [is_checked(key) for key in ['accelerationCheck','brakingCheck','coolingCheck','downforceCheck','fuel_economyCheck','handlingCheck','reliabilityCheck','tyre_economyCheck']]
        
        return {'car_design':car_design,'teams_design':teams_design,'max':max_design,'points':points,'research_power':self.research_power,'check':checked_design, 'bonus':car_bonus}

    async def get_daily(self):
        url = 'https://igpmanager.com/content/misc/igp/ajax/dailyReward.php'
        async with self.session.post(url) as response:
                try:
                    if response.status == 200:
                        json_data = json.loads(await response.text())
                        soup = BeautifulSoup(json_data['message'], 'html.parser')
                        #xp gain is '<span>5</span><img src="https://igpmanager.com/app/design/dr-xp.png" class="drSubImage" />'
                        #money '<span>$16k</span><img src="https://igpmanager.com/app/design/dr-cash.png" class="drSubImage" />'
                        #'<span>1</span><img src="https://igpmanager.com/app/design/dr-part.png" class="drSubImage" />'
                        span = soup.find('span')
                        return span.get_text() if span else False
                except:
                    return False
    def save_setup_field(self,pyqt_elements):
        self.setups = pyqt_elements
    async def async_login(self):
        try:
            login_url = "https://igpmanager.com/index.php?action=send&addon=igp&type=login&jsReply=login&ajax=1"
            # Using a bot account for the login 
            login_data =  {'loginUsername':self.username,
                        'loginPassword':self.password, 
                        'loginRemember': 'on',
                        'csrfName': '',
                        'csrfToken': ''}     
            async with self.session.post(login_url, data=login_data) as response:
                    if response.status == 200:
                        print(f"Login with {self.username}")
                        response_text  = await response.text()
                        data = json.loads(response_text)
                        if data['status'] != 1:
                            return False
                        print('Success')
                        await self.init_account()
                        return True
                    else:
                        print("Login failed. Status code:", response.status)
                        return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    async def car_info(self):
         try:
          fetch_url = "https://igpmanager.com/index.php?action=fetch&p=cars&csrfName=&csrfToken="

          async with self.session.get(fetch_url) as response:
                if response.status == 200:
                    json_data = json.loads(await response.text())['vars']
                    # if c2Hide = 'hide' the manager is in a 1 car league

                    car_list = []
                    soup_engine = BeautifulSoup(json_data['c1Engine'], 'html.parser')
                    rating_div = soup_engine.find("div", class_="ratingCircle green")
                    engine_health = rating_div.get("data-value", "N/A")
                    soup_parts = BeautifulSoup(json_data['c1Condition'], 'html.parser')
                    soup_total_engine = BeautifulSoup(json_data['totalEngines'], 'html.parser')
                    soup_total_parts = BeautifulSoup(json_data['totalParts'], 'html.parser')
                    soup_car_attributes = BeautifulSoup(json_data['carAttributes'],'html.parser')
                    
                    #is it needed?
                    if (self.team['_joinedLeague'] == None):
                        fuel_economy = int(soup_car_attributes.find('span', {'id': 'ecar_fuel_economy'}).text)
                        tyre_economy = int(soup_car_attributes.find('span', {'id': 'ecar_tyre_economy'}).text)
                    else:
                        fuel_economy = int(soup_car_attributes.find("div", id="wrap-fuel_economy").find("span", class_="ratingVal").get_text(strip=True))
                        tyre_economy = int(soup_car_attributes.find("div", id="wrap-tyre_economy").find("span", class_="ratingVal").get_text(strip=True))


                    car_list.append ({
                                 'engine': str(engine_health)+"%",
                                 'parts': str(soup_parts.find("div", class_="ratingCircle green").get("data-value", "N/A"))+"%",
                                 'fuel_economy':fuel_economy,
                                 'tyre_economy':tyre_economy,
                                 'restock':json_data['restockRaces'],
                                 'total_engines':int(soup_total_engine.find("span", id="totalEngines").get_text(strip=True)),
                                 'total_parts':int(soup_total_parts.text.split(' ')[1]),
                                 'id':json_data['c1Id'],
                                 'car_number':1,
                                 'repair_cost':int(BeautifulSoup(json_data['c1CarBtn'], 'html.parser').a.get_text(separator=" ", strip=True).split()[-1]) if "disabled" not in BeautifulSoup(json_data['c1CarBtn'], 'html.parser').a.get("class", []) else 0})
                    if json_data['c2Hide'] == '':
                       soup_parts = BeautifulSoup(json_data['c2Condition'], 'html.parser')
                       soup_engine = BeautifulSoup(json_data['c2Engine'], 'html.parser')
                       rating_div = soup_engine.find("div", class_="ratingCircle green")
                       engine_health = rating_div.get("data-value", "N/A")
                       car_list.append({'engine':str(engine_health),
                               'parts':str(soup_parts.find("div", class_="ratingCircle green").get("data-value", "N/A"))+"%",
                               'id':json_data['c2Id'],
                               'car_number':2,
                               'repair_cost':int(BeautifulSoup(json_data['c2CarBtn'], 'html.parser').a.get_text(separator=" ", strip=True).split()[-1]) if "disabled" not in BeautifulSoup(json_data['c2CarBtn'], 'html.parser').a.get("class", []) else 0})

                    return car_list
         except Exception as e:
            print(f"Error during car info: {e}")       
    async def train_driver(self,id,intensity,category):
        url =f"https://igpmanager.com/index.php?{id}={category}&action=send&addon=igp&type=train&focus=drivers&jsReply=train&ajax=1&intensity={intensity}&c[]=0&c[]={id}&csrfName=&csrfToken="
        async with self.session.get(url) as response:
                if response.status == 200:
                    json_data = json.loads(await response.text())

                    response_json = json_data
        # update the info bmi color will need to request the driver info
        self.staff = await self.staff_info()
    
    async def driver_info(self,id):
        try:
            json_data = await self.fetch_url(f"https://igpmanager.com/index.php?action=fetch&d=driver&id={id}&csrfName=&csrfToken=")
            #contract =  BeautifulSoup(BeautifulSoup(json_data['contract'], 'html.parser').find_all('a')[1]['data-tip'],'html.parser').text
            contract = BeautifulSoup(json_data['contract'], 'html.parser').find_all(attrs={"data-tip": True})
            contract_link = contract[1]

            if contract_link:
                data_tip = contract_link["data-tip"]
                decoded_tip = html.unescape(data_tip)
                clean_soup = BeautifulSoup(decoded_tip, "html.parser")
                for tag in clean_soup(["img", "div", "a", "icon"]):
                    tag.decompose()

                text = clean_soup.get_text(" ", strip=True)
                can_extend = True
            #cost = re.search(r'\$\d+(\.\d+)?.', contract).group(0)
            #duration= re.findall(r'\d+(?:\.\d+)?', contract)[0]
            bmi_color = BeautifulSoup(json_data['sBmi'], 'html.parser').span['class'][1].split('-')[1]
            self.extra_driver_info = {'contract':{'text':text},'attributes':{'weight':json_data['sWeight'],'bmi_color':bmi_color}}
            if 'disabled' in contract[1]['class']:
                can_extend = False
            return {'text':text,'can_extend':can_extend}
        except:
            print('driver problem')
    
    def h_until_next_race(self):
       current_timestamp = time.time()
       difference_seconds = self.next_race - current_timestamp
       return str(round(difference_seconds / 3600,1))
    async def pick_sponsor(self,number):
        json_data =  await self.fetch_url(f"https://igpmanager.com/index.php?action=fetch&d=sponsor&location={number}&csrfName=&csrfToken=")
        parser = {1:'span',2:'td'}
        income_soup =  BeautifulSoup(json_data['row2'],'html.parser').find_all(parser[number])
        bonus_soup = BeautifulSoup(json_data['row3'],'html.parser').find_all('td')
        id_soup = BeautifulSoup(json_data['row1'],'html.parser').find_all('i')
        income_list = [income.text for income in income_soup]
        bonus_list = [bonus.text for bonus in bonus_soup]
        id_list = [id.text.split('/')[-1].split('.gif')[0] for id in id_soup]

        return income_list,bonus_list,id_list
    async def get_last_race_report(self):
        sidebar = BeautifulSoup(self.all['vars']['league_sidebar'],'html.parser')
        link = sidebar.find("a", href=re.compile(r"^d=result&id="))
        if link:
            # Extract the id using regex
            match = re.search(r"id=(\d+)", link["href"])
            if match:
                race_id = match.group(1)
                return await self.get_report(race_id)
            else:
                print("ID not found")
        else:
            print("Link not found")
    async def get_report(self,id):
        json_data =  await self.fetch_url(f"https://igpmanager.com/index.php?action=fetch&d=result&id={id}&tier={self.team['_tier']}&tab=race&csrfName=&csrfToken=")
        race_soup = BeautifulSoup(json_data['rResult'], "html.parser")
        race_name = BeautifulSoup(json_data['raceName'], "html.parser").get_text(strip=True)
        rules = BeautifulSoup(json_data['rRules'], "html.parser")
        rows = race_soup.find_all("tr")
        def parse_row(row):
            #position = row.find("td", class_="key-pos").get_text(strip=True)
            name_and_team = row.find("td", class_="hover").get_text(separator="|", strip=True).split("|")
            report_link = row.find("a", href=re.compile(r"^d=resultDetail"))['href']
            is_my_team = "myTeam" in row.get("class", [])
            driver_name = name_and_team[0].strip()
            team_name = name_and_team[1].strip() if len(name_and_team) > 1 else ""
            lap_time = row.find_all("td")[2].get_text(strip=True)
            best_lap = row.find_all("td")[3].get_text(strip=True)
            top_speed = row.find_all("td")[4].get_text(strip=True)
            pit_stops = row.find_all("td")[5].get_text(strip=True)
            points = row.find_all("td")[6].get_text(strip=True)
            return [driver_name, team_name, lap_time, best_lap,top_speed,pit_stops,points,report_link,is_my_team]
        data = [parse_row(row) for row in rows]
        return {"data":data,"race_name":race_name}
    async def get_race_report(self,link):
        json_data =  await self.fetch_url(f"https://igpmanager.com/index.php?action=fetch&{link}&csrfName=&csrfToken=")
        race_soup = BeautifulSoup(json_data['results'], "html.parser")
        race_name = BeautifulSoup(json_data['raceName'], "html.parser").get_text(strip=True)
        rows = race_soup.find_all("tr")[1:]
        def parse_row(row):
            lap = row.find("td", class_="key").get_text(strip=True)
            is_pit= "pit" in row.get("class", [])
            if(is_pit):
                tyre = row.find_all("td")[1].get_text(strip=True)
                return [lap, tyre]
            else:
                lap_time = row.find_all("td")[1].get_text(strip=True)
                gap_to_lead = row.find_all("td")[2].get_text(strip=True)
                average_speed = row.find_all("td")[3].get_text(strip=True)
                pos = row.find_all("td")[4].get_text(strip=True)
                tyre = row.find_all("td")[5].get_text(strip=True)
                fuel = row.find_all("td")[6].get_text(strip=True)
                return [lap, lap_time, gap_to_lead,average_speed,pos,tyre,fuel]
        data = [parse_row(row) for row in rows]
        return {"data":data,"race_name":race_name}
    async def get_sponsors(self):
      def parse_sponsor(html):
        soup = BeautifulSoup(html, 'html.parser')
        sponsors = []
        # Loop through each sponsor table
        for sponsor in soup.select("table.acp"):
            sponsor_name = sponsor.select_one("th").text.strip()

            # Extract income
            income_span = sponsor.select_one(".token-cost")  # Primary sponsor has token-cost class
            if income_span:
                income = income_span.text.strip()
                sponsor_number = 1
            else:
                sponsor_number = 2
                income_td = sponsor.select("tr")[1].select("td")[1]
                income = income_td.text.strip()
            # Extract bonus
            bonus_td = sponsor.select("tr")[2].select("td")[1]
            bonus = bonus_td.text.strip()
            # Extract contract duration
            contract_td = sponsor.select("tr")[3].select("td")[1]
            contract_duration = contract_td.text.strip()


            sponsors.append({
                "number": sponsor_number,
                "Sponsor": sponsor_name,
                "Income": income,
                "Bonus": bonus,
                "Contract": contract_duration
            })
        return sponsors
            
        #json_data = await self.fetch_url("https://igpmanager.com/index.php?action=fetch&p=finances&csrfName=&csrfToken=")
      async with self.session.get('https://igpmanager.com/index.php?action=fetch&p=finances&csrfName=&csrfToken=') as response:
                if response.status == 200:
                    json_data = json.loads(await response.text())['vars']
                    empty_sponsor = {'income':'0','bonus':'0','expire':'0','status':False}
                    sponsors = {'s{}'.format(i): empty_sponsor.copy() for i in range(1, 3)}

                    sponsors_data = parse_sponsor(json_data['sponsors'])
                    
                    for sponsor in sponsors_data:
                        if sponsor['number'] == 1:  # Primary sponsor
                            sponsors['s1']['income'] = sponsor['Income']
                            sponsors['s1']['bonus'] = sponsor['Bonus']
                            sponsors['s1']['expire'] = sponsor['Contract']
                            sponsors['s1']['status'] = True
                        elif sponsor['number'] == 2:  # Secondary sponsor
                            sponsors['s2']['income'] = sponsor['Income']
                            sponsors['s2']['bonus'] = sponsor['Bonus']
                            sponsors['s2']['expire'] = sponsor['Contract']
                            sponsors['s2']['status'] = True
                    # Check if primary sponsor is missing
                    if not sponsors['s1']['status']:
                        print('Primary sponsor expired')

                    # Check if secondary sponsor is missing
                    if not sponsors['s2']['status']:
                        print('Secondary sponsor expired')
                    self.sponsors = sponsors        


    async def save_sponsor(self,number,id):
        sign_sponsor = f"https://igpmanager.com/index.php?action=send&type=contract&enact=sign&eType=5&eId={id}&location={number}&jsReply=contract&csrfName=&csrfToken="
        json_data = await self.fetch_url(sign_sponsor)

    async def staff_info(self): 
         try:
            fetch_url =(f"https://igpmanager.com/index.php?action=fetch&p=staff&csrfName=&csrfToken=")
            
            async with self.session.get(fetch_url) as response:
                   if response.status == 200:
                       response_json = json.loads(await response.text())
                       json_data = response_json['vars'] 
                       self.next_race = response_json['nextLeagueRaceTime']
                       
                       soup = BeautifulSoup(json_data['drivers'], 'html.parser')
                       driver_names = soup.select(".driverName")
                       driver_names = [name.get_text(separator=" ", strip=True) for name in driver_names]
    
                       driver_attributes = [tag["data-driver"] for tag in soup.select(".hoverData")]
                       contract_ids = [td.get_text(strip=True) for td in soup.select("td[id^='nDriverC']")]
    
                       driver_ids = []
                       for link in soup.select("a.linkParent[href]"):
                               href = link["href"]
                               if "id=" in href:
                                   driver_ids.append(href.split("id=")[-1])
    
                       salaries = [td.get_text(strip=True) for td in soup.select("td:has(img.icon-24)")]
    
                       driver = []
                       #soup_driver = BeautifulSoup(json_data['d1Name'], 'html.parser')
                       #soup_driver_info = BeautifulSoup(json_data['d1Info'], 'html.parser')
                       #attributes = soup_driver.find('span',class_='hoverData').get('data-driver').split(',')
                       driver.append ({
                                    'name':driver_names[0],
                                    'health':driver_attributes[0].split(',')[12] if 0 < len(driver_attributes) else None,
                                    'id':driver_ids[0] if 0 < len(driver_ids) else None,
                                    'height':driver_attributes[0].split(',')[13] if 0 < len(driver_attributes) else None,
                                    'salary': salaries[0] if 0 < len(salaries) else None,
                                    'contract':contract_ids[0] if 0 < len(contract_ids) else None,
                                    'attributes':driver_attributes[0].split(',')if 0 < len(driver_attributes) else None})
               
                       if json_data['d2Hide'] == '':
                          #soup_driver = BeautifulSoup(json_data['d2Name'], 'html.parser')
                          #soup_driver_info = BeautifulSoup(json_data['d2Info'], 'html.parser')
                          #attributes = soup_driver.find('span',class_='hoverData').get('data-driver').split(',')
                          driver.append ({
                                    'name':driver_names[1],
                                    'health':driver_attributes[1].split(',')[12],
                                    'id':driver_ids[1],
                                    'height':driver_attributes[1].split(',')[13],
                                    'salary': salaries[1],
                                    'contract':contract_ids[1],
                                    'attributes':driver_attributes[1].split(',')})  
                       
               
                       # also for the staff?
                       staff = {'drivers':driver}
                       
                       #to do. parse the attributes?
                       return staff
         except:
             print('staff problem')
    def handle_setup_comments(self,comment):
        soup = BeautifulSoup(comment, 'html.parser')
        ride_height = ""
        suspension = ""
        wing_levels = ""
        try:
            span_text = soup.find('p', class_='shrinkText')
            paragraph_text = span_text.get_text() if span_text else False
            if(paragraph_text == False):
             return
            ride_string, wing_string = paragraph_text.split(',')
            #print('ride',ride_string)
           # print("wing",wing_string)
            if "Ride height" in ride_string:
                if "little too high" in ride_string:
                    ride_height = "+"
                elif "much too high" in ride_string:
                    ride_height = "++"    
                elif "little too low" in ride_string:
                    ride_height = "-"
                elif "far too low" in ride_string:
                    ride_height = "--"
                elif "perfect" in ride_string:
                    ride_height = ""         

            if "suspension" in paragraph_text:
                if "right" in paragraph_text:
                    suspension = ""
                elif "too soft" in paragraph_text:
                    suspension = "too soft"
                elif "too hard" in paragraph_text:
                    suspension = "too hard"

            if "wing levels" in wing_string:
                if "little too high" in wing_string:
                    wing_levels = "+"
                elif "far too high" in wing_string:
                    wing_levels = "++"    
                elif "little too low" in wing_string:
                    wing_levels = "-"
                elif "far too low" in wing_string:
                    wing_levels = "--"    
                elif "right" in wing_string:
                    wing_levels = ""
        except Exception as e:
            print('error practice comment')     
        return {"suspension":suspension,"ride_height":ride_height,"wing_levels":wing_levels}
    async def next_race_info(self):
        
        try:
            fetch_url = ("https://igpmanager.com/index.php?action=fetch&p=race&csrfName=&csrfToken=")

            async with self.session.get(fetch_url) as response:
                    if response.status == 200:
                        json_data = json.loads(await response.text())['vars']

                        strategy = []

                        if 'd1FuelOrLaps' not in json_data:
                            self.has_league = False
                            return False
                        self.has_league = True
                        saved_strat_data = BeautifulSoup(json_data['d1FuelOrLaps'], 'html.parser')

                        ##       stint              stint
                        ## [[tyre,laps,fuel]],[[tyre,laps,fuel]]
                        saved_strat = [[json_data[f'd1s{i}Tyre'], saved_strat_data.find('input', {'name': f'laps{i}'}).get('value'), saved_strat_data.find('input', {'name': f'fuel{i}'}).get('value')] for i in range(1, 6)]
                        soup = BeautifulSoup(json_data['d1Laps'], 'html.parser')
                        string = json_data['d1Laps']
                        practice_list = []
                        if string != '<tr><td colspan="7"></td></tr>':
                            practice_list = [[tds[0]['class'][0][3:]] + [td.get_text() for td in tds[1:]] for tr in soup.find_all('tr') if (tds := tr.find_all('td'))]    

                        strategy.append({'rules':json.loads(json_data['rulesJson']),
                                         'rulesJson':json_data['rulesJson'],
                                         'advanced':json_data['d1IgnoreAdvanced'],
                                         'advancedFuel':BeautifulSoup(json_data['d1AdvancedFuel'], 'html.parser').input.get('value') if BeautifulSoup(json_data['d1AdvancedFuel'], 'html.parser').input else '0',
                                         'push':json_data['d1PushLevel'],
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
                                         'rainStart':[json_data['d1RainStartTyre'],BeautifulSoup(json_data['d1RainStartDepth'],'html.parser').find('input', {'type': 'number'})['value']],
                                         'rainStop':[json_data['d1RainStopTyre'],BeautifulSoup(json_data['d1RainStopLap'],'html.parser').find('input', {'type': 'number'})['value']],
                                         'pushLevel':BeautifulSoup(json_data['d1PushLevel'], 'html.parser').find('option',selected=True)['value'],
                                         'strat': saved_strat,
                                         'totalLaps' :json_data['d1TotalLaps'],
                                         'raceId':json_data['raceId'],
                                         'tier':json_data['setupMax'],
                                         'practice':practice_list,
                                         'setup_comment':self.handle_setup_comments(json_data['d1SetupComments'])})
                        # check if 2 cars
                        if json_data['d2Pits'] != 0:
                            soup = BeautifulSoup(json_data['d2Laps'], 'html.parser')
                            practice_list = []
                            string = json_data['d2Laps']
                            if string != '<tr><td colspan="7"></td></tr>':
                                practice_list = [[tds[0]['class'][0][3:]] + [td.get_text() for td in tds[1:]] for tr in soup.find_all('tr') if (tds := tr.find_all('td'))] 
                            saved_strat_data = BeautifulSoup(json_data['d2FuelOrLaps'], 'html.parser')
                            saved_strat = [[json_data[f'd2s{i}Tyre'], saved_strat_data.find('input', {'name': f'laps{i}'}).get('value'), saved_strat_data.find('input', {'name': f'fuel{i}'}).get('value')] for i in range(1, 6)]
                            strategy.append({'rules':json.loads(json_data['rulesJson']),
                                         'suspension':json_data['d2Suspension'],
                                         'advancedFuel':BeautifulSoup(json_data['d2AdvancedFuel'], 'html.parser').input.get('value') if BeautifulSoup(json_data['d2AdvancedFuel'], 'html.parser').input else '0',
                                         'advanced':json_data['d2IgnoreAdvanced'],
                                         'push':json_data['d2PushLevel'],
                                         'aero':json_data['d2Aerodynamics'],
                                         'ride':json_data['d2Ride'],
                                         'pits':json_data['d2Pits'],
                                         'totalLaps' :json_data['d2TotalLaps'],
                                         'rainStart':[json_data['d2RainStartTyre'],BeautifulSoup(json_data['d2RainStartDepth'],'html.parser').find('input', {'type': 'number'})['value']],
                                         'rainStop':[json_data['d2RainStopTyre'],BeautifulSoup(json_data['d2RainStopLap'],'html.parser').find('input', {'type': 'number'})['value']],
                                         'pushLevel':BeautifulSoup(json_data['d2PushLevel'], 'html.parser').find('option',selected=True)['value'],
                                         'strat':saved_strat,
                                         'practice':practice_list,
                                         'setup_comment':self.handle_setup_comments(json_data['d2SetupComments'])})

                        return strategy
        except:
            print('error next race')
    async def save_research(self,attributes,points):
        await self.fetch_url(f'https://igpmanager.com/index.php?action=send&addon=igp&type=research&jsReply=research&ajax=1&researchMaxEffect={self.research_power}{attributes}&csrfName=&csrfToken=')
        await self.fetch_url(f'https://igpmanager.com/index.php?action=send&addon=igp&type=design&jsReply=design&ajax=1{points}&csrfName=&csrfToken=')
    async def save_strategy(self):
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
                           "pushLevel":self.strategy[1]['pushLevel'],
                           "d1SavedStrategy":"1",
                           "ignoreAdvancedStrategy":self.strategy[1]['advanced'],
                           "rainStartTyre":self.strategy[1]['rainStart'][0],
                           "rainStartDepth":self.strategy[1]['rainStart'][1],
                           "rainStopTyre":self.strategy[1]['rainStop'][0],
                           "rainStopLap":self.strategy[1]['rainStop'][1]
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
                           "rules":json.dumps(str(self.strategy[0]['rulesJson']).replace('"', '\'')),
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
                           "pushLevel":self.strategy[0]['pushLevel'],
                           "d1SavedStrategy":"1",
                           "ignoreAdvancedStrategy":self.strategy[0]['advanced'],
                           "rainStartTyre":self.strategy[0]['rainStart'][0],
                           "rainStartDepth":self.strategy[0]['rainStart'][1],
                           "rainStopTyre":self.strategy[0]['rainStop'][0],
                           "rainStopLap":self.strategy[0]['rainStop'][1]
                        },
                        "d2strategyAdvanced":d2strategyAdvanced
                    }  
        for i,strat in enumerate(self.strategy):
            if strat['rules']['refuelling'] == '0':
                strat_data[f'd{i+1}strategyAdvanced']['advancedFuel'] = strat['advancedFuel']

        good_format =  str(strat_data).replace("'", "\"")
        good_format =good_format.replace('""',"\"")

        #response =  self.session.post(url, data=good_format)
        async with self.session.post(url, data=good_format) as response:
                if response.status == 200:
                    json_data = json.loads(await response.text())
                    print(f"Saving {self.username}'s strategy")
        

        
    async def request_parts_repair(self,car):
        if car['parts'] == "100%" or int(self.car[0]['total_parts']) < int(car['repair_cost']) :
            return False
        response = await self.fetch_url(f"https://igpmanager.com/index.php?action=send&type=fix&car={car['id']}&btn=%23c{car['car_number']}PartSwap&jsReply=fix&csrfName=&csrfToken=")
        if response['update'] != False:
            return response['newTotal']
        else:
            return 'err'
    async def request_engine_repair(self,car):
        if car['engine'] == "100%" or self.car[0]['total_parts'] == 0:
            return False
        
        response = await self.fetch_url( f"https://igpmanager.com/index.php?action=send&type=engine&car={car['id']}&btn=%23c{car['car_number']}EngSwap&jsReply=fix&csrfName=&csrfToken=")
        if response['update'] != False:
            return response['newTotal']
        else:
            return 'err'
    async def extend_contract_driver(self,driver):
        await self.fetch_url(f"https://igpmanager.com/index.php?action=send&type=contract&enact=extend&eType=3&eId={driver['id']}&jsReply=contract&csrfName=&csrfToken=")
        
        return '50 races'
    async def do_practice_lap(self,driver_number):
        #tyre = SS,S,M...
        ride_with_offset = int(self.setup_pyqt_elements[driver_number]['setup']['ride'].text()) + int(self.setup_pyqt_elements[driver_number]['setup']['ride_offset'].text())
        aero_with_offset = int(self.setup_pyqt_elements[driver_number]['setup']['wing'].text()) + int(self.setup_pyqt_elements[driver_number]['setup']['wing_offset'].text())
        tyre = self.setup_pyqt_elements[driver_number]['setup']['practice_tyre'].get_current_tyre_text()
        #soft = 1, neutral = 2, firm = 3
        suspension = self.setup_pyqt_elements[driver_number]['setup']['suspension'].currentIndex() + 1
        suspension_text = self.setup_pyqt_elements[driver_number]['setup']['suspension'].currentText()
        url = (f"https://igpmanager.com/index.php?action=send&addon=igp&type=setup&dNum={driver_number+1}&ajax=1&race={self.strategy[0]['raceId']}&suspension={suspension}&ride={ride_with_offset}&aerodynamics={aero_with_offset}&practiceTyre={tyre}&csrfName=&csrfToken=")
        response = await self.fetch_url(url)
        await asyncio.sleep(3)
        practice_lap = await self.fetch_url(f"https://igpmanager.com/index.php?action=fetch&type=lapTime&lapId={response["lapId"]}&dNum={driver_number+1}&addon=igp&ajax=1&jsReply=lapTime&csrfName=&csrfToken=")
        print(practice_lap)
        self.strategy[driver_number]['setup_comment'] = self.handle_setup_comments(practice_lap['comments'])
        #TODO: read the driver's comment to see if the setup is good
        if practice_lap['success'] ==True:
            good_format = [[tyre,suspension_text,ride_with_offset,aero_with_offset,practice_lap['lapFuel'],practice_lap['lapTyre'],practice_lap['lapTime']],practice_lap]
            return good_format
        else:
            return -1