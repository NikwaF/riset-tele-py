from telethon.tl.types import InputPhoneContact
from telethon import TelegramClient, errors
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

async def def_test():
    return os.getenv("TELEGRAM_API_ID") 

class SenderTelegram:
    api_id = int(os.getenv("TELEGRAM_API_ID"))
    api_hash = os.getenv("TELEGRAM_API_HASH") 
    session = os.getenv("TELEGRAM_SESSION") 
    target = ""

    def __init__(self):
        self.client = TelegramClient(self.session, api_id=self.api_id, api_hash=self.api_hash)

    async def initTelegramClient(self):
        # await self.client.start()
        await self.client.connect() 

    async def getId(self):
        listEntity = []
        if isinstance(self.target, str):
            if self.target.isnumeric():
                try:
                    await InputPhoneContact(client_id = 2, phone= self.target, first_name="", last_name="")  
                    entity = await self.client.get_entity(self.target)
                 
                    listEntity.append(entity)
                except: 
                    listEntity.append(self.target) 
            else:
                try:
                    entity = await self.client.get_entity(self.target)
                    print("fafa")
                    print(entity)
                    listEntity.append(entity)
                except Exception as s:
                    print("fafaaf")
                    print(type(s))
                    print(s) 
                    listEntity.append(self.target)
        else:
            for item in self.target:
                if item.isnumeric():
                    try:
                        await InputPhoneContact(client_id = 2, phone= item, first_name="", last_name="")  
                        entity =  await self.client.get_entity(item)
                        listEntity.append(entity)
                    except: 
                        listEntity.append(item)
                else:
                    try:
                        entity = await self.client.get_entity(item)
                        listEntity.append(entity)
                    except Exception as s:
                        print(s) 
                        listEntity.append(item)

        return listEntity
    
    async def sendMessage(self, entity, pesan):
        try: 
            await self.client.send_message(entity=entity, message=pesan)
        except ValueError as a:
            raise Exception("username not found")
        except errors.rpcerrorlist.FloodWaitError as a:
            raise Exception("telegram api has been limited")
        except Exception as a:
            raise Exception("something wrong")


async def get_entity(entity):
    # terus = 1
    # while True:
        # for i in range(1,16):
    api_id = int(os.getenv("TELEGRAM_API_ID"))
    api_hash = os.getenv("TELEGRAM_API_HASH") 
    session = os.getenv("TELEGRAM_SESSION") 
    client = TelegramClient(session, api_id=api_id, api_hash=api_hash)
    await client.start()
    await client.connect()
    try:
        tes = 1
        while True:
            test =  await client.send_message(entity,f"test {tes}")
            tes = tes+1
        # test = await client.send_file(entity,'./test.CSV')
        
        # # if int(test.peer_id.user_id) != 5627950104:
        # test =  await client.delete_messages(entity,test.id)   
    except ValueError as a:
        print(type(a))
        print(a)
    except errors.rpcerrorlist.FloodWaitError as a:
        print("limit")
    except Exception as a:
        print(type(a))
        print(a)
    await client.disconnect()
    # terus = terus+1

async def get_entity2(entity):
    # terus = 1
    # while True:
        # for i in range(1,16):
    api_id = int(os.getenv("TELEGRAM_API_ID"))
    api_hash = os.getenv("TELEGRAM_API_HASH") 
    session = os.getenv("TELEGRAM_SESSION") 
    client = TelegramClient(session, api_id=api_id, api_hash=api_hash)
    await client.start()
    await client.connect()
    try:
        while True:
            test =  await client.send_message(entity,"ttt")
            print(test)
    except ValueError as a:
        print(type(a))
        print(a)
    except Exception as a:
        print(a)
    await client.disconnect()
    # terus = terus+1

if __name__ == "__main__":
    # print(halo.peer_id.user_id)
    #1094219920 tidak bisa harus pake username dulu
    asyncio.run(get_entity("nko738827"))
    # asyncio.run(get_entity2("Nikohxh"))