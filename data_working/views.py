from django.http import JsonResponse
from django.shortcuts import render
from .models import data


def ajax_update(request):
    uid = request.COOKIES['uid']
    deviceID = request.GET.get('z')
    time = []
    current = []
    temperature = []
    voltage = []
    humidity = []
    query = "SELECT * FROM data_working_data WHERE user='"+uid+"' AND device_no = '"+deviceID+"' ORDER BY id DESC LIMIT 60"
    for i in data.objects.raw(query):
        time.append(str(i.time)[0:19])
        current.append(i.current)
        temperature.append(i.temperature)
        voltage.append(i.voltage)
        humidity.append(i.humidity)
    comb_lis = zip(time, current, temperature, voltage, humidity)
    return JsonResponse({"comb_lis": list(comb_lis)})