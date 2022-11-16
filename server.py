from flask import Flask, request
from niko import SenderTelegram
import datetime
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route("/kirimpesan/<id>/<pesan>", methods=['GET'])
async def kirimpesan(id,pesan):
    waktu = datetime.datetime.now().strftime("'%d-%b-%Y %H:%M:%S'")
    sender = SenderTelegram(target=id)
    await sender.client.start()
    await sender.client.connect() 
    teleId = await sender.getId()
    if isinstance(teleId[0], str):
        await sender.client.disconnect()    
        result = {"status":"error", "message_lenght":len(pesan), "target":id,"message": "username not found", "time_request": waktu}
        return result, 400                
    else: 
        try:
            for item in teleId:
                await sender.sendMessage(item,pesan)
        except:
            await sender.client.disconnect()    
            result = {"status":"error", "message_lenght":len(pesan), "target":id,"message": "something wrong", "time_request": waktu}
            return result, 500                     

    await sender.client.disconnect()    
    result = {"status":"success", "message_lenght":len(pesan), "target":id,"message": "message sent", "time_request": waktu}
    return result, 200    

    
   

@app.route("/kirimpesans", methods=['POST'])
async def kirimpesans():
    waktu = datetime.datetime.now().strftime("'%d-%b-%Y %H:%M:%S'")
    sender = SenderTelegram(target=request.json["usernames"])
    pesan = request.json["pesan"]
    errorProses = []
    await sender.client.start()
    await sender.client.connect() 
    try:
        teleId = await sender.getId()
        for item in teleId:
            if isinstance(item, str):
                errorProses.append(item)
            else:
                await sender.sendMessage(item,pesan)
    except:
        await sender.client.disconnect()    
        result = {"status":"error", "message_lenght":len(pesan),"target_lenght":len(request.json["usernames"]), "target":request.json["usernames"],"error_list":errorProses, "time_request": waktu}
        return result, 500        
    
    await sender.client.disconnect()
   
    result = {"status":"success", "message_lenght":len(pesan),"target_lenght":len(request.json["usernames"]), "target":request.json["usernames"],"error_list":errorProses, "time_request": waktu}
    return result, 200

if __name__ == '__main__':
    PORT = 5000
    app.run(debug=False, host='0.0.0.0', port=PORT)