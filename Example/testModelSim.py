"""Script to test 2-mass-building model"""

from bamLoadBasedTesting.BuildingModels import BAM_RRT_HP3_fixedflow
import numpy as np
import matplotlib.pyplot as plt

# Create new building model:
comBui = BAM_RRT_HP3_fixedflow
Building = comBui.MTBui_D
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
T_sup_hs = []
m_flow_byp = []
m_flow_hp = []
m_flow_sh = []
internalGains = 0 # 0 W constant internal gains into building
#loop by doing x steps
m_flow = comBui.m_dot_H_design
for x in range(3600*6):
    t.append(x * stepSize)
    "Step response"
    if x<3600*6:
        t_sup.append(30)
    else:
        t_sup.append(Building.t_ret)
    T_ret.append(Building.t_ret)
    "Do step with Building Model"
    Building.doStep(t_sup=t_sup[-1], t_ret_mea=T_ret[-1], m_w_hp=m_flow, stepSize=stepSize, q_dot_int=internalGains)
    if x==0:
        print("Start value for return temperature " + str(T_ret[-1]) + " °C")
    "Save current values:"
    T_b.append(Building.MassB.T)
    T_H.append(Building.MassH.T)
    T_sup_hs.append(Building.hydraulicSwitch.T_sup_swi)
    q_flow_ba.append(Building.q_dot_ba)
    q_flow_hb.append(Building.q_dot_hb)
    q_flow_hp.append(Building.q_dot_hp)
    q_flow_int.append(Building.q_dot_int)
    q_flow_bh.append(Building.q_dot_bh)
    m_flow_byp.append(Building.hydraulicSwitch.m_flow_swi)
    m_flow_hp.append(m_flow)
    m_flow_sh.append(Building.hydraulicSwitch.m_flow_sh)

hours = np.array(t)
hours = hours/3600
fig, ax = plt.subplots()
ax.plot(hours, T_ret, label = "return temperature")
ax.plot(hours, T_H, label = 'transfer system temperature')
ax.plot(hours, t_sup, label = 'supply temperature heat pump')
ax.plot(hours, T_sup_hs, label = 'supply temperature transfer system')
ax.legend()
plt.grid(True)
plt.ylabel('Temperature in °C')
plt.xlabel('time in hours')
plt.show()

fig, ax = plt.subplots()
ax.plot(hours, q_flow_hp, label = 'heat flow heat pump --> heating system ')
ax.plot(hours, q_flow_hb, label = 'heat flow transfer --> building')
ax.plot(hours, q_flow_ba, label = 'heat flow Building --> Ambient')
#ax.plot(hours, q_flow_bh, label = 'heat flow booster heater --> heating system')
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

fig, ax = plt.subplots()
ax.plot(hours, m_flow_byp, label = 'm_flow_bypass')
ax.plot(hours, m_flow_sh, label = 'm_flow_sh')
ax.plot(hours, m_flow_hp, label = 'm_flow_hp')
ax.legend()
plt.ylabel('mass flow in kg/s')
plt.xlabel('time in hours')
plt.grid(True)
plt.show()