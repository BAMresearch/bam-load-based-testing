from bamLoadBasedTesting.BuildingModels import OneMassModelConfig
import numpy as np
import matplotlib.pyplot as plt

"""Script to test the parametrization of a one-mass-building model.

- Please specify the building parametrization you want to test with the variable "Building".
- Please do not change anything outside of the block "USER INPUT".
- Your parametrization is correct, if ...
"""
# TODO add explanations
# TODO add automatic print if test was successful

# --- START OF USER INPUT ---
# Create new building model
comBui = OneMassModelConfig     # If you saved your model parametrization in another file you can adjust it here
Building = comBui.MTBui_A       # TODO specify building model
# --- END OF USER INPUT ---

# Set step size of the model
stepSize = 1

# Create lists to save inputs and results
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

# Set mass flow rate
m_flow = Building.m_flow_design

# Get design supply temperature of building model
t_flow_design = Building.t_flow_design

# Loop by doing x steps (simulation over 6 hours)
for x in range(3600*6):
    # Save current time
    t.append(x * stepSize)

    # Step response: after 3 hours with constant supply temperature, the heat pump is turned off by setting the supply
    # temperature equal to the current calculated return temperature
    if x<3600*3:
        t_sup.append(t_flow_design)
    else:
        t_sup.append(Building.t_ret + 0.1)

    # Save current return temperature from the building model
    T_ret.append(Building.t_ret)

    # Do a step with the building model
    Building.doStep(
        t_sup=t_sup[-1],
        t_ret_mea=T_ret[-1],
        m_w_hp=m_flow,
        stepSize=stepSize,
        heating=True
    )
    if x==0:
        print("Start value for return temperature " + str(T_ret[-1]) + " °C")

    # Save current values
    T_H.append(Building.MassH.T)
    q_flow_hb.append(Building.q_dot_hb)
    q_flow_hp.append(Building.q_dot_hp)
    m_flow_hp.append(m_flow)

# Adjust time to hours for plots
hours = np.array(t)
hours = hours/3600

# Plot temperatures (return, transfer system, supply)
fig, ax = plt.subplots()
ax.plot(hours, T_ret, label = "return temperature")
ax.plot(hours, T_H, label = 'transfer system temperature')
ax.plot(hours, t_sup, label = 'supply temperature heat pump')
ax.legend()
plt.grid(True)
plt.ylabel('Temperature in °C')
plt.xlabel('time in hours')
plt.show()

# Plot the heat flow rates calculated within the model
fig1, ax = plt.subplots()
ax.plot(hours, q_flow_hp, label = 'heat flow heat pump --> heating system ')
ax.plot(hours, q_flow_hb, label = 'heat flow transfer --> building')
ax.legend()
plt.ylabel('Heat flow in W')
plt.xlabel('time in hours')
plt.grid(True)
plt.show()

# Plot the mass flow rate of the heat pump
fig2, ax = plt.subplots()
ax.plot(hours, m_flow_hp, label = 'm_flow_hp')
ax.legend()
plt.ylabel('mass flow in kg/s')
plt.xlabel('time in hours')
plt.grid(True)
plt.show()