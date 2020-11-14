from xlwt import *
import itertools
from django.http import HttpResponse
from django.shortcuts import render
from data_working.models import data
import xlwt


def filter_btw_dates(request):
    if request.method == 'POST':
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')
        original_from_date = from_date
        original_to_date = to_date
        # print(from_date)
        # print(to_date)
        year = int(to_date[0:4])
        month = int(to_date[5:7])
        days = numberOfDays(year, month)
        day = int(to_date[8:10])
        if day == days:
            if month <= 11:
                to_date = str(year) + "-" + str(month + 1) + "-" + "01"
            else:
                to_date = str(year + 1) + "-" + "01" + "-" + "01"
        else:
            if month <= 11:
                to_date = str(year) + "-" + str(month) + "-" + str(day + 1)
            else:
                to_date = str(year) + "-" + "01" + "-" + str(day + 1)
        query = 'SELECT * FROM data_working_data WHERE time BETWEEN "' + from_date + '" AND "' + to_date + '" '
        time = []
        current = []
        temperature = []
        voltage = []
        humidity = []
        for i in data.objects.raw(query):
            time.append(str(i.time)[0:19])
            current.append(i.current)
            temperature.append(i.temperature)
            voltage.append(i.voltage)
            humidity.append(i.humidity)
        comb_lis = zip(time, current, temperature, voltage, humidity)

        uid = request.COOKIES['uid']
        deviceID = request.GET.get('z')
        min_time = None
        max_time = None
        min_query = "SELECT id,MIN(time) FROM data_working_data WHERE user = '" + uid + "' AND device_no = '" + str(
            deviceID) + "'"
        max_query = "SELECT id,time FROM data_working_data WHERE user = '" + uid + "' AND device_no = '" + str(deviceID) + "'"
        for i in data.objects.raw(min_query):  # This query gives MIN time
            min_time = i.time
        for i in data.objects.raw(max_query):  # This query gives MAX time don't know how
            max_time = i.time
        min_date = str(min_time)[0:10]
        max_date = str(max_time)[0:10]

        return render(request, "filter/filter.html", {'min': min_date,
                                                      'max': max_date,
                                                      'value_from': original_from_date,
                                                      'value_to': original_to_date,
                                                      'comb_lis': comb_lis,
                                                     })
    else:
        uid = request.COOKIES['uid']
        deviceID = request.GET.get('z')
        min_time = None
        max_time = None
        min_query = "SELECT id,MIN(time) FROM data_working_data WHERE user = '" + uid + "' AND device_no = '" + str(
            deviceID) + "'"
        max_query = "SELECT id,time FROM data_working_data WHERE user = '" + uid + "' AND device_no = '" + str(deviceID) + "'"
        for i in data.objects.raw(min_query):  # This query gives MIN time
            min_time = i.time
        for i in data.objects.raw(max_query):  # This query gives MAX time don't know how
            max_time = i.time
        min_date = str(min_time)[0:10]
        max_date = str(max_time)[0:10]
        query = "SELECT * FROM data_working_data WHERE user='" + uid + "' AND device_no = '" + deviceID + "'"
        time = []
        current = []
        temperature = []
        voltage = []
        humidity = []
        for i in data.objects.raw(query):
            time.append(str(i.time)[0:19])
            current.append(i.current)
            temperature.append(i.temperature)
            voltage.append(i.voltage)
            humidity.append(i.humidity)
        comb_lis = zip(time, current, temperature, voltage, humidity)
        return render(request, "filter/filter.html", {'min': min_date, 'max': max_date, 'comb_lis': comb_lis})


def numberOfDays(y, m):
    leap = 0
    if y % 400 == 0:
        leap = 1
    elif y % 100 == 0:
        leap = 0
    elif y % 4 == 0:
        leap = 1
    if m == 2:
        return 28 + leap
    list = [1, 3, 5, 7, 8, 10, 12]
    if m in list:
        return 31
    return 30
