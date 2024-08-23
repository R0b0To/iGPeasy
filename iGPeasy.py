import asyncio
import json
import os
import sys
from tool_api import iGP_account
from interface import iGPeasyWindow
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

class iGPeasy:
    def __init__(self):
        super().__init__()
        self.gui = iGPeasyWindow(self)

    async def load_accounts(self):
        """Load accounts from a JSON file or initialize a new one."""
        if not os.path.exists('accounts.json'):
            with open('accounts.json', 'w') as json_file:
                json.dump([], json_file)
                
        with open('accounts.json', 'r') as json_file:
            accounts_list = json.load(json_file)
            
        return accounts_list

    async def process_account(self, account):
        """Process a single account asynchronously."""
        igp_account = iGP_account(account)
        if await igp_account.async_login():  # Assuming login is an asynchronous operation
            return igp_account
        return None

    async def play(self):
        """Main method that handles the application logic."""
        accounts_list = await self.load_accounts()
        
        if len(accounts_list) == 0:
            await self.gui.add_accounts_to_start()
        else:
            # Schedule account processing tasks using asyncio.create_task
            tasks = [asyncio.create_task(self.process_account(account)) for account in accounts_list]

            # Optionally, await tasks and collect results
            iGP_accounts = await asyncio.gather(*tasks)

            # Filter valid accounts
            self.valid_accounts = [account for account in iGP_accounts if account is not None]

            if len(self.valid_accounts) == 0:
                print('No valid accounts | add more')
                await self.gui.add_accounts_to_start()
            else:
                print('OK, populate window')
                await self.gui.init_window()
                print('Window initialized.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    igpeasy_app = iGPeasy()

    # Setup the QEventLoop for asyncio integration
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Start the igpeasy_app.play() method automatically when the application starts
    async def main():
        await igpeasy_app.play()

    # Start the application with the integrated event loop
    with loop:
        loop.run_until_complete(main())  # Run the main async function and keep the event loop running
        loop.run_forever()

    sys.exit(app.exec())
