from flask import Flask, request
from niko import SenderTelegram
from dotenv import load_dotenv
import datetime
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(12)
load_dotenv()

@app.route("/kirimpesan/<id>/<pesan>", methods=['GET'])
async def kirimpesan(id,pesan):
    waktu = datetime.datetime.now().strftime("'%d-%b-%Y %H:%M:%S'")
    sender = SenderTelegram()

    await sender.initTelegramClient()
    
    try: 
        await sender.sendMessage(id,pesan)
        await sender.client.disconnect()  
        result = {"status":"success", "message_length":len(pesan), "target":id,"message": "message sent", "time_request": waktu}
        return result, 200          
    except Exception as a:
        print("test exec")
        await sender.client.disconnect()  
        error_code = 500
        err_msg = str(a)
        if err_msg == "username not found":
            error_code = 400
        
        result = {"status":"error", "message_length":len(pesan), "target":id,"message": err_msg, "time_request": waktu}
        return result, error_code


@app.route("/kirimpesans", methods=['POST'])
async def kirimpesans():
    waktu = datetime.datetime.now().strftime("'%d-%b-%Y %H:%M:%S'")
    sender = SenderTelegram()
    usernames = request.json["usernames"]
    pesan = request.json["pesan"]
    errorProsesUsernames = []
    errorProsesMessage = []
    limit = False
    
    await sender.initTelegramClient()

    try:
        for item in usernames:
            try:
                await sender.sendMessage(item,pesan)
            except Exception as e: 
                if str(e) == "telegram api has been limited":
                    limit = True

                errorProsesUsernames.append(item)
                errorProsesMessage.append({item:str(e)})

    except Exception as hehe:
        await sender.client.disconnect()    
        result = {"status":"error", "message_length":len(pesan),"total_target":len(request.json["usernames"]), "target":request.json["usernames"],"usernames_error_list":errorProsesUsernames,"error_message": "something wrong","usersnames_error_messages":errorProsesMessage, "time_request": waktu}
        return result, 500        
    
    await sender.client.disconnect()

    if len(usernames) == len(errorProsesUsernames) and limit:
        result = {"status":"error", "message_length":len(pesan),"total_target":len(request.json["usernames"]), "target":request.json["usernames"],"usernames_error_list":errorProsesUsernames,"error_message": "telegram api has been limited", "usersnames_error_messages":errorProsesMessage, "time_request": waktu}
        return result, 500

    result = {"status":"success", "message_length":len(pesan),"total_target":len(request.json["usernames"]), "target":request.json["usernames"],"usernames_error_list":errorProsesUsernames,"error_message": None, "usersnames_error_messages":None, "time_request": waktu}
    return result, 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=os.getenv("PORT_APPS"))