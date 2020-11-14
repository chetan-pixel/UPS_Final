from xlwt import *
import itertools
wb = Workbook()
ws0 = wb.add_sheet('sheet0')

col_width = 256 * 20 # 20 characters wide

try:
    for i in itertools.count():
        ws0.col(i).width = col_width
except ValueError:
    pass

pattern = Pattern()
pattern.pattern = Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = Style.colour_map['yellow']

fnt = Font()
fnt.name = 'Yu Gothic Light'
fnt.colour_index = 4
fnt.height = 320 #font size 16 coz 20*16 = 320
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
style.borders = borders
style.pattern = pattern


#sheet.write_merge(top_row, bottom_row, left_column, right_column, 'Long Cell')
ws0.write_merge(0, 1, 0 ,5 ,'Device Data of 80:7D:3A:78:8B:CF', style)

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
    ws0.write(3, col_num, columns[col_num], style)
wb.save('Data.xls')
