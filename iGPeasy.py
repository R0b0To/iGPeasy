import asyncio
import json
import os
from tool_api import iGP_account
from interface import iGPeasyWindow
#from setups import CarSetup
import sys
from PyQt6.QtWidgets import QApplication



class iGPeasy:
    def __init__(self):
        super().__init__()
        self.gui = iGPeasyWindow(self)
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self.main())

    async def play(self):
        if not os.path.exists('accounts.json'):
        # Create an empty JSON file with an empty list or dictionary
            with open('accounts.json', 'w') as json_file:
                json.dump([], json_file)
        with open('accounts.json', 'r') as json_file:
            accounts_list = json.load(json_file)
        async def process_account(account):
            igp_account = iGP_account(account)
            if await igp_account.async_login():  # Assuming login is an asynchronous operation
                return igp_account

        
        if len(accounts_list) == 0:
            await self.gui.add_accounts_to_start()
        else:
            iGP_accounts = await asyncio.gather(*[process_account(account) for account in accounts_list])
         
            self.valid_accounts = [account for account in iGP_accounts if account is not None]
      
            if len(self.valid_accounts) == 0:
                print('no valid accounts | add more')
                await self.gui.add_accounts_to_start()
            else:
                print('ok, populate window')
                await self.gui.init_window()
                print('test -----------')

    
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
       
    igpeasy_app = iGPeasy()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(igpeasy_app.play())

    sys.exit(app.exec())

