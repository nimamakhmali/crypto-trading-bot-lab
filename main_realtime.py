import asyncio
import subprocess
from websockets_data import kbar_handler, live_ticker


async def convert_to_candles():
    while True:  
        subprocess.run(["python", "change_to_1min.py"])
        await asyncio.sleep(5) 
        '''
        Process = await asyncio.create_subprocess_exec(
            "python", "websockets_data."
        )
        '''  

async def main():
    await asyncio.gather(
        kbar_handler(),
        live_ticker(),
        convert_to_candles(),
    )            

if __name__ == "main":
    asyncio.run(main())           
