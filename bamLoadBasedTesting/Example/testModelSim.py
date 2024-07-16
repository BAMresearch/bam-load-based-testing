"""Script to test 2-mass-building model"""

from BuildingModels import BAM_RRT_MT
import numpy as np
import matplotlib.pyplot as plt

# Create new building model:
Building = BAM_RRT_MT.MTBui_E
stepSize = 1
T_b = []
T_H = []
T_ret = []
q_flow_hp = []
q_flow_hb = []
q_flow_ba = []
q_flow_bh = []
q_flow_int = []
t = []
t_sup = []
internalGains = 0 # 0 W constant internal gains into building
#loop by doing x steps
for x in range(3600*12):
    t.append(x * stepSize)
    "Step response"
    if x<3600*12:
        t_sup.append(52)
    else:
        t_sup.append(Building.t_ret)
    T_ret.append(Building.t_ret)
    "Do step with Building Model"
    Building.doStep(t_sup=t_sup[-1], t_ret_mea=T_ret[-1], m_dot=720/3600, stepSize=stepSize, q_dot_int=internalGains)
    "Save current values:"
    T_b.append(Building.MassB.T)
    T_H.append(Building.MassH.T)
    q_flow_ba.append(Building.q_dot_ba)
    q_flow_hb.append(Building.q_dot_hb)
    q_flow_hp.append(Building.q_dot_hp)
    q_flow_int.append(Building.q_dot_int)
    q_flow_bh.append(Building.q_dot_bh)

hours = np.array(t)
hours = hours/3600
fig, ax = plt.subplots()
ax.plot(hours, T_ret, label = "return temperature")
ax.plot(hours, T_H, label = 'transfer system temperature')
ax.plot(hours, t_sup, label = 'supply temperature')
ax.legend()
plt.grid(True)
plt.ylabel('Temperature in °C')
plt.xlabel('time in hours')
plt.show()

fig, ax = plt.subplots()
ax.plot(hours, q_flow_hp, label = 'heat flow heat pump --> heating system ')
ax.plot(hours, q_flow_hb, label = 'heat flow transfer --> building')
ax.plot(hours, q_flow_ba, label = 'heat flow Building --> Ambient')
ax.plot(hours, q_flow_bh, label = 'heat flow booster heater --> heating system')
ax.legend()
plt.ylabel('Heat flow in W')
plt.xlabel('time in hours')
plt.grid(True)
plt.show()

fig, ax = plt.subplots()
ax.plot(hours, T_b, label = 'building temperature')
ax.legend()
plt.ylabel('Temperature in °C')
plt.xlabel('time in hours')
plt.grid(True)
plt.show()