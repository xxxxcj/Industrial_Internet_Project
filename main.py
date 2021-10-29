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

last_exporting, last_importing = -1, -1  # 上上一个输出液体的罐子的编号
exporting, importing = -1, -1  # 上一个输出液体的罐子的编号
total_count = 10 # 滑动窗口大小？
count = -1
pipe_list = []

for row in sheet.iter_rows(min_row=3):
    for idx, cell in enumerate(row[2:8]):
        Tank_list[idx].renew_amount(cell.value)
    for idx, cell in enumerate(row[8:28]):
        Valve_list[idx].renew_switch_state(cell.value)
    for idx, cell in enumerate(row[28:30]):
        Pump_list[idx].renew_switch_state(cell.value)

    flag_export, flag_import = False, False # 输出输入液体的罐子是否发生变化
    pr_exporting, pr_importing = -1, -1  # 当前输出输入液体的罐子的编号

    # 依次检测状态
    for idx, _ in enumerate(row[2:8]):
        # print(Tank_list[idx].is_exporting, Tank_list[idx].is_importing)
        if Tank_list[idx].is_exporting():
            pr_exporting = idx
            if pr_exporting != exporting:
                flag_export = True
        elif Tank_list[idx].is_importing:
            pr_importing = idx
            if pr_importing != importing:
                flag_import = True
        else:
            continue

    print(flag_export, flag_import)
    if flag_export or flag_import:
        if pr_importing != last_importing or pr_exporting != last_exporting:
            count = 0
            pipe_list = []
            last_exporting, last_importing = exporting, importing
            exporting, importing = pr_exporting, pr_importing
        flag_export, flag_import = False, False
    if 0 <= count < 10:
        count += 1
        for idx, _ in enumerate(row[8:28]):
            if Valve_list[idx].is_switch:
                pipe_list.append(idx)
        if count == 10:
            # print(pipe_list)
            pipe_list = []
            count = -1
