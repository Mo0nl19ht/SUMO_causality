import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd
from tqdm import tqdm
import numpy as np

sumoCmd = ["sumo", "-c", "osm.sumocfg"]
traci.start(sumoCmd)

time_cnt = 0

packBigData = []

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    lanes = traci.lane.getIDList()

    for i in range(len(lanes)):
        id = lanes[i]
        if id == "274886548#1_1":
            continue

        spd = round(traci.lane.getLastStepMeanSpeed(lanes[i])*3.6, 2)
        time = time_cnt

        num = traci.lane.getLastStepVehicleNumber(lanes[i])
        if num <= 0:
            spd = 0

        if id == '274886548#1_0':
            spd2 = round(traci.lane.getLastStepMeanSpeed(
                "274886548#1_1")*3.6, 2)
            num2 = traci.lane.getLastStepVehicleNumber("274886548#1_1")

            if num2 <= 0:
                spd2 = 0

            if spd2 > 0:
                print(spd2)

            if num > 0:
                if num2 > 0:
                    spd = spd*num
                    spd2 = spd2*num2
                    spd += spd2
                    num += num2
                    spd /= num

            else:
                if num2 > 0:
                    spd = spd2
                    num = num2

        _list = [time, id, spd, num]

        packBigData.append(_list)

        # print(traci.lane.getLastStepVehicleIDs(lanes[i]))

    time_cnt += 1
    if time_cnt == 3600:
        break


traci.close()
data = pd.DataFrame(packBigData, columns=['time', 'id', 'spd', 'num'])
data.to_csv("result_make_2.csv", index=False)


def make_spd(use):
    dic = {}

    for k, v in tqdm(use.iterrows()):
        if (v['id']) not in dic.keys():
            dic[(v['id'])] = []
        dic[(v['id'])].append(v['spd'])

    return dic


def make_num(use):
    dic = {}

    for k, v in tqdm(use.iterrows()):
        if (v['id']) not in dic.keys():
            dic[(v['id'])] = []
        dic[(v['id'])].append(v['num'])

    return dic


def make_spd_num(use):
    dic = {}

    for k, v in tqdm(use.iterrows()):
        if (v['id']) not in dic.keys():
            dic[(v['id'])] = []
        dic[(v['id'])].append(v['spd']*v['num'])

    return dic


nd = pd.read_csv("필요한것.csv", header=None)
a = make_spd(data)
new = pd.DataFrame(a)
new = new[nd[0]]

# new.to_csv(f"newyork_trimed_block_limit.csv", index=False)
n = new.copy()
for i in new.columns:
    if new[i].sum() == 0:
        n = n.drop(i, axis=1)
n.to_csv("limited_spd.csv", index=False)


a = make_num(data)
new = pd.DataFrame(a)
new = new[nd[0]]

# new.to_csv(f"newyork_trimed_block_limit.csv", index=False)
n = new.copy()
for i in new.columns:
    if new[i].sum() == 0:
        n = n.drop(i, axis=1)
n.to_csv("limited_num.csv", index=False)


a = make_spd_num(data)
new = pd.DataFrame(a)
new = new[nd[0]]

# new.to_csv(f"newyork_trimed_block_limit.csv", index=False)
n = new.copy()
for i in new.columns:
    if new[i].sum() == 0:
        n = n.drop(i, axis=1)
n.to_csv("limited_spd_num.csv", index=False)
