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
        spd = round(traci.lane.getLastStepMeanSpeed(lanes[i])*3.6, 2)
        time = time_cnt
        if spd == round(traci.lane.getMaxSpeed(lanes[i])*3.6, 2):
            spd = 0

        _list = [time, id, spd]

        packBigData.append(_list)

        # print(traci.lane.getLastStepVehicleIDs(lanes[i]))

    time_cnt += 1

traci.close()
data = pd.DataFrame(packBigData, columns=['time', 'id', 'spd'])
data.to_csv("result_make.csv", index=False)


def make_h5style(use):
    dic = {}

    for k, v in use.iterrows():
        if (v['id']) not in dic.keys():
            dic[(v['id'])] = []
        dic[(v['id'])].append(v['spd'])

    return dic


nd = pd.read_csv("필요한것.csv", header=None)
a = make_h5style(data)
new = pd.DataFrame(a)
new = new[nd[0]]
new.to_csv(f"newyork_trimed_block_limit.csv", index=False)
