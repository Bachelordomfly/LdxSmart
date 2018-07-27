import os
print (os.path.abspath('.'))

import xlrd
import xlwt
from xlutils.copy import copy

old_excel = xlrd.open_workbook('TWtest3.xls', formatting_info=True)  # 只能用于xls格式
new_excel = copy(old_excel)
ws = new_excel.get_sheet(0)
ws.write(1, 0, '20180727010')
ws.write(2, 0, '20180727011')
ws.write(3, 0, '20180727012')
ws.write(4, 0, '20180727013')
ws.write(5, 0, '20180727014')
ws.write(1, 1, '20180727010')
ws.write(2, 1, '20180727011')
ws.write(3, 1, '20180727012')
ws.write(4, 1, '20180727013')
ws.write(5, 1, '20180727014')

new_excel.save('new_TWtest.xls')