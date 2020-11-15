from django.shortcuts import HttpResponse
import pyrebase
from data_working.models import data
import json
import datetime

config = {

    'apiKey': "AIzaSyDZxw1qSdXuHDLseNh2y3TN-O8NfhpPoQc",
    'authDomain': "cpanel-c54b7.firebaseapp.com",
    'databaseURL': "https://cpanel-c54b7.firebaseio.com",
    'projectId': "cpanel-c54b7",
    'storageBucket': "cpanel-c54b7.appspot.com",
    'messagingSenderId': "82198444165",
    'appId': "1:82198444165:web:eb9e20a95d9fcaacd991ec",
    'measurementId': "G-E595RHEXVP"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()


def save_latest_data(request):
    users_dict = database.child('users').shallow().get().val()
    # Getting Users List
    user_list = []
    for user in users_dict:
        user_list.append(user)

    # Nested List For Saving Values
    for user in user_list:
        devices_dict = database.child('users').child(user).shallow().get().val()
        devices_list = []
        for device in devices_dict:
            devices_list.append(device)
        # print(devices_list)
        for device in devices_list:
            # print(device)
            data_packets = database.child('Data').child(device).get().val()
            # print(data_packets)
            keys = []
            try:
                for key in data_packets.keys():
                    keys.append(str(key))
                    # print(keys)
                    data_packets = json.dumps(data_packets)
                    response = json.loads(data_packets)
                    for key in keys:
                        tim = response[key]['Time']
                        curr = response[key]['Current']
                        temp = response[key]['Temperature']
                        pd = response[key]['Voltage']
                        humi = response[key]['Humidity']
                        print(str(user) + "/" + str(device) + "/" + str(key) + "")
                        print("Time:" + str(tim) + "      Current:" + str(curr) + "      Temperature:" + str(
                            temp) + "      Voltage:" + str(pd) + "      Humidity:" + str(humi))
                        tim = datetime.datetime.strptime(tim, '%Y-%m-%d %H:%M:%S')
                        save_data(user=user, device_no=device, time=tim, current=curr, temperature=temp, voltage=pd,
                                  humidity=humi)
                        database.child('Data').child(device).child(key).remove()
            except:
                return HttpResponse("<h1>No data pending...</h1>")
    return HttpResponse("<h1>Done....</h1>")


def save_data(user, device_no, time, current, temperature, voltage, humidity):
    dataToSave = data.objects.create(
        user=user,
        device_no=device_no,
        time=time,
        current=current,
        temperature=temperature,
        voltage=voltage,
        humidity=humidity,
    )
    dataToSave.save()