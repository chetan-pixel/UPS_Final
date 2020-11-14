from xlwt import *
import itertools
from django.http import HttpResponse
from data_working.models import data
import xlwt
from filter.views import numberOfDays


def export_xls(request):
    from_date = request.GET.get('f')
    to_date = request.GET.get('t')
    z = request.GET.get('z')# Device ID
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
    query = 'SELECT * FROM data_working_data WHERE device_no="'+z+'" AND time BETWEEN "' + from_date + '" AND "' + to_date + '" '
    print(query)
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




    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Data')
    col_width = 256 * 20  # 20 characters wide

    try:
        for i in itertools.count():
            ws.col(i).width = col_width
    except ValueError:
        pass

    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['yellow']

    fnt = Font()
    fnt.name = 'Yu Gothic Light'
    fnt.colour_index = 4
    fnt.height = 320  # font size 16 coz 20*16 = 320
    fnt.bold = True

    borders = Borders()
    borders.left = 6
    borders.right = 6
    borders.top = 6
    borders.bottom = 6

    al = Alignment()
    al.horz = Alignment.HORZ_CENTER
    al.vert = Alignment.VERT_CENTER

    style = XFStyle()
    style.font = fnt
    style.alignment = al
    # style.borders = borders
    style.pattern = pattern

    # sheet.write_merge(top_row, bottom_row, left_column, right_column, 'Long Cell')
    ws.write_merge(0, 1, 0, 4, 'Device Data of '+z, style)

    fnt = Font()
    fnt.name = 'Arial'
    fnt.bold = True
    fnt.colour_index = Style.colour_map['white']

    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['red']

    border_thickness = 2
    borders = Borders()
    borders.left = border_thickness
    borders.right = border_thickness
    borders.top = border_thickness
    borders.bottom = border_thickness

    al = Alignment()
    al.horz = Alignment.HORZ_CENTER
    al.vert = Alignment.VERT_CENTER

    style = XFStyle()
    style.font = fnt
    style.alignment = al
    style.borders = borders
    style.pattern = pattern

    columns = ['Time', 'Current', 'Temperature', 'Voltage', 'Humidity', ]

    for col_num in range(len(columns)):
        ws.write(3, col_num, columns[col_num], style)
    font_style = xlwt.XFStyle()
    font_style.alignment = al
    for i in range(len(time)):
        ws.write(i + 4, 0, time[i], font_style)
        ws.write(i + 4, 1, current[i], font_style)
        ws.write(i + 4, 2, temperature[i], font_style)
        ws.write(i + 4, 3, voltage[i], font_style)
        ws.write(i + 4, 4, humidity[i], font_style)

    wb.save(response)
    return response