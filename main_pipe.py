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

total_count = 8  # 滑动窗口大小？
count = -1
pipe = [0] * 20
valve_list, last_valva_list = [], []  # 当前和之前阀门顺序列表

tank_list = [0] * 6
tank_exporting_list, tank_importing_list = [], []  # 当前输出和输入的罐子
last_tank_exporting_list, last_tank_importing_list = [], []  # 之前输入和输出的罐子

tmp = 0

# 初始化管子里的液体量
for row in sheet.iter_rows(min_row=3):
    for idx, cell in enumerate(row[2:8]):
        Tank_list[idx].init(cell.value)
    break

# 开始检测
for row in sheet.iter_rows(min_row=3):
    tmp += 1
    for idx, cell in enumerate(row[2:8]):
        Tank_list[idx].renew_amount(cell.value)
    for idx, cell in enumerate(row[8:28]):
        Valve_list[idx].renew_switch_state(cell.value)
    for idx, cell in enumerate(row[28:30]):
        Pump_list[idx].renew_switch_state(cell.value)

    # for idx, _ in enumerate(row[8:28]):
    #     pipe.append(Valve_list[idx].is_open())
    # print(pipe)
    # pipe = []

    if count == -1:
        for idx, _ in enumerate(row[8:28]):
            if Valve_list[idx].is_switch():
                count = 0
                break

    if 0 <= count < total_count:
        count += 1

        # 检测正在运行的罐子
        for idx, cell in enumerate(row[2:8]):
            if Tank_list[idx].is_exporting_state():
                tank_list[idx] -= 1
            elif Tank_list[idx].is_importing_state():
                tank_list[idx] += 1

        # 检测管道上的阀门
        for idx, _ in enumerate(row[8:28]):
            if Valve_list[idx].is_switch() and (idx not in valve_list):
                valve_list.append(idx)
            if Valve_list[idx].is_open():
                pipe[idx] += 1

        # 开关状态改变并运行到一定时间后
        if count == total_count:
            for i in range(6):
                if tank_list[i] >= 0.5 * total_count:
                    tank_importing_list.append(i)
                elif tank_list[i] <= -0.5 * total_count:
                    tank_exporting_list.append(i)
            if len(tank_importing_list) > 1 or len(tank_exporting_list) > 1:
                flag = True
                for i in last_tank_exporting_list:
                    if i not in tank_exporting_list:
                        flag = False
                for i in last_tank_importing_list:
                    if i not in tank_importing_list:
                        flag = False
                if flag:
                    for i in last_tank_exporting_list:
                        tank_exporting_list.remove(i)
                    for i in last_tank_importing_list:
                        tank_importing_list.remove(i)

            for i in range(20):
                if (i in valve_list) and (pipe[i] < 0.5 * total_count):
                    valve_list.remove(i)
            for i in range(len(last_valva_list)):
                if last_valva_list[i] not in valve_list:
                    break
                if i == len(last_valva_list) - 1:
                    for j in last_valva_list:
                        valve_list.remove(j)

            # # 连接管子和阀门
            # for i in tank_exporting_list:
            #     Tank_list[i].connect(valve_list[0])
            #     for j in range(len(valve_list) - 1):
            #         Valve_list[j].connect(Valve_list[j + 1])
            #     for k in tank_importing_list:
            #         Valve_list[-1].connect(Tank_list[k])

            print(tmp, valve_list, tank_exporting_list, tank_importing_list)
            last_valva_list = valve_list.copy()
            last_tank_exporting_list, last_tank_importing_list = tank_exporting_list.copy(), tank_importing_list.copy()
            tank_exporting_list, tank_importing_list = [], []
            tank_list = [0] * 6
            pipe = [0] * 20
            count = -1
