import Tank
import Valve
import Pump
import openpyxl

data_file_path = "食品饮料流程工艺数据.xlsx"
data_workbook = openpyxl.load_workbook(data_file_path)

sheet = data_workbook[data_workbook.sheetnames[0]]

# for x in sheet.iter_cols(min_col=3, max_col=8):
#     print(x[1].value[:4])
# print()
# for x in sheet.iter_cols(min_col=9, max_col=28):
#     print(x[1].value[:4])
# print()
# for x in sheet.iter_cols(min_col=29, max_col=30):
#     print(x[1].value[:6])
# print()

Tank_list = [Tank.Tank(x[1].value[:4]) for x in sheet.iter_cols(min_col=3, max_col=8)]
Valve_list = [Valve.Valve(x[1].value[:4]) for x in sheet.iter_cols(min_col=9, max_col=28)]
Pump_list = [Pump.Pump(x[1].value[:6]) for x in sheet.iter_cols(min_col=29, max_col=30)]

outside = Tank.Tank("outside")

for row in sheet.iter_rows(min_row=3):
    for idx, cell in enumerate(row[2:8]):
        Tank_list[idx].renew_amount(cell.value)
    for idx, cell in enumerate(row[8:28]):
        Valve_list[idx].renew_switch_state(cell.value)
    for idx, cell in enumerate(row[28:30]):
        Pump_list[idx].renew_switch_state(cell.value)

