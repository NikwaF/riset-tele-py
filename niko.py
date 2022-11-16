from telethon.tl.types import InputPhoneContact, User
from telethon import TelegramClient
import asyncio

class SenderTelegram:
    api_id = 123123123
    api_hash = '' #bot
    session = ''

    def __init__(self, target):
        self.client = TelegramClient(self.session, api_id=self.api_id, api_hash=self.api_hash)
        self.target = target

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
        await self.client.send_message(entity=entity, message=pesan)

async def get_entity(entity):
    terus = 1
    while True:
        for i in range(1,16):
            api_id = 999999 
            api_hash = '' #bot    
            session = ''    
            client = TelegramClient(session, api_id=api_id, api_hash=api_hash)
            await client.start()
            await client.connect()
            ent = User()
            test =  await client.send_message(ent, f"test {terus}")
            await client.disconnect()
            terus = terus+1

if __name__ == "__main__":
    asyncio.run(get_entity("nikohxh"))