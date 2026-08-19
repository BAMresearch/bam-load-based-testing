import math

from bamLoadBasedTesting.oneMassModel import CalcParameters

"""This script shows some examples on how to parameterize the building models for different part load conditions, 
temperature applications as well as heating and cooling operation.

- Please adjust the parameters in the section "USER INPUT". The mass flow rates are only default values that should be exchanged!
- This script shows examples for an average climate. If you want to test other climates please adjust the plc parameter accordingly.
- The examples are for variable outlet temperature. If you want to test fixed outlet temperature please adjust t_flow_plc for each part load condition.
- The examples are for heat pumps using outdoor air at the outer heat exchanger. If you want to test with exhaust air please adjust t_a and relHum.
- Naming convention:
    - The first two letters determine the temperature application (LT, MT, HT)
    - Then it directly follows "Bui_" (for building)
    - The next letter (seventh letter) determines the part load condition (A, B, C, D, E)
    - For cooling operation, "_cool" is added at the end. Cooling is only defined for low temperature (LT)
    - For heating operation, there is no additional letter after the part load condition
"""
# TODO dt_mean for cooling

# --- START USER INPUT ---
# -- Parameters of the heat pump --
# Heating
# TODO q_design_e for all temperature application the same?
q_design_e = 5390           # in W; design heating power in E - only value which is dependent on the heat pump
t_a_design = -10            # in °C; see T_designh in EN 14825 (average climate)
mass_flow_design_heat_mt = q_design_e / (4183*8)    # in kg/s; declared mass flow rate from manufacturer
mass_flow_design_heat_lt = q_design_e / (4183*5)    # in kg/s; declared mass flow rate from manufacturer
mass_flow_design_heat_ht = q_design_e / (4183*10)   # in kg/s; declared mass flow rate from manufacturer

# Cooling
p_design_c = 5000           # in W
mass_flow_design_cool = p_design_c / (4183*5)   # in kg/s; declared mass flow rate from manufacturer

# -- Settings of the one mass model --
use_dynamic_load = True     # if True use dynamic load, if False use fixed load
use_constant_mflow = True   # if True use constant flow (variable dT), if False use variable flow (constant dT)

# --- END USER INPUT ---

# --- Parameters for one mass model (depending on operation (heating/cooling) and temperature application) ---
# Building temperatures
t_b_heat = 20               # in °C; see indoor temperature in EN 14825; constant building temperature (heating operation)
t_b_cool = 27               # in °C; building temperature for cooling operation

# Thermal design capacities for different temperature applications
c_design_mt = 67            # in J/K/W_design, medium temperature application
c_design_lt = 418           # in J/K/W_design, low temperature application
c_design_ht = 109           # in J/K/W_design, high temperature application

# --- Examples for heating operation ---
# -- Medium temperature application --
t_flow_design = 55          # in °C; design supply temperature
deltaT = 8                  # in K; temperature difference in condenser
c_design = c_design_mt
m_dot_H_design = mass_flow_design_heat_mt

# Design logarithmic mean temperature (only for variable flow / fixed delta T)
t_ret_e = t_flow_design - deltaT
dt_mean_e = (t_flow_design - t_ret_e) / math.log((t_b_heat - t_flow_design) / (t_b_heat - t_ret_e))

# Create one mass models for medium temperature application
ParaMTBui_E = CalcParameters(
    t_a_design=t_a_design,
    t_a=-10,
    relHum=69.38,
    q_design=q_design_e,
    PLC=1,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=55,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=dt_mean_e,
    delta_T_cond_design=deltaT
)
MTBui_E = ParaMTBui_E.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_A = CalcParameters(
    t_a_design=t_a_design,
    t_a=-7,
    relHum=74.69,
    q_design=q_design_e,
    PLC=0.8846,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=52,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=48.3-t_b_heat,
    delta_T_cond_design=deltaT
)
MTBui_A = ParaMTBui_A.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_B = CalcParameters(
    t_a_design=t_a_design,
    t_a=2,
    relHum=83.87,
    q_design=q_design_e,
    PLC=0.5385,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=42,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=39.8-t_b_heat,
    delta_T_cond_design=deltaT
)
MTBui_B = ParaMTBui_B.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_C = CalcParameters(
    t_a_design=t_a_design,
    t_a=7,
    relHum=86.84,
    q_design=q_design_e,
    PLC=0.3462,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=36,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=34.6-t_b_heat,
    delta_T_cond_design=deltaT
)
MTBui_C = ParaMTBui_C.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_D = CalcParameters(
    t_a_design=t_a_design,
    t_a=12,
    relHum=88.94,
    q_design=q_design_e,
    PLC=0.1538,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=30,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=29.4-t_b_heat,
    delta_T_cond_design=deltaT
)
MTBui_D = ParaMTBui_D.createBuilding(dynamic_load=use_dynamic_load)

# -- Low temperature application --
t_flow_design = 35          # in °C; design supply temperature
deltaT = 5                  # in K; temperature difference in condenser
c_design = c_design_lt
m_dot_H_design = mass_flow_design_heat_lt

# Design logarithmic mean temperature (only for variable flow / fixed delta T)
t_ret_e = t_flow_design - deltaT
dt_mean_e = (t_flow_design - t_ret_e) / math.log((t_b_heat - t_flow_design) / (t_b_heat - t_ret_e))

# Create one mass models for low temperature application
ParaLTBui_E = CalcParameters(
    t_a_design=t_a_design,
    t_a=-10,
    relHum=69.38,
    q_design=q_design_e,
    PLC=1,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=35,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=dt_mean_e,
    delta_T_cond_design=deltaT
)
LTBui_E = ParaLTBui_E.createBuilding(dynamic_load=use_dynamic_load)

ParaLTBui_A = CalcParameters(
    t_a_design=t_a_design,
    t_a=-7,
    relHum=74.69,
    q_design=q_design_e,
    PLC=0.8846,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=34,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=31.6-t_b_heat,
    delta_T_cond_design=deltaT
)
LTBui_A = ParaLTBui_A.createBuilding(dynamic_load=use_dynamic_load)

ParaLTBui_B = CalcParameters(
    t_a_design=t_a_design,
    t_a=2,
    relHum=83.87,
    q_design=q_design_e,
    PLC=0.5385,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=30,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=28.6-t_b_heat,
    delta_T_cond_design=deltaT
)
LTBui_B = ParaLTBui_B.createBuilding(dynamic_load=use_dynamic_load)

ParaLTBui_C = CalcParameters(
    t_a_design=t_a_design,
    t_a=7,
    relHum=86.84,
    q_design=q_design_e,
    PLC=0.3462,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=27,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=26.1-t_b_heat,
    delta_T_cond_design=deltaT
)
LTBui_C = ParaLTBui_C.createBuilding(dynamic_load=use_dynamic_load)

ParaLTBui_D = CalcParameters(
    t_a_design=t_a_design,
    t_a=12,
    relHum=88.94,
    q_design=q_design_e,
    PLC=0.1538,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=24,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=23.6-t_b_heat,
    delta_T_cond_design=deltaT
)
LTBui_D = ParaLTBui_D.createBuilding(dynamic_load=use_dynamic_load)


# -- High temperature application --
t_flow_design = 65          # in °C; design supply temperature
deltaT = 10                 # in K; temperature difference in condenser
c_design = c_design_ht
m_dot_H_design = mass_flow_design_heat_ht

# Design logarithmic mean temperature (only for variable flow / fixed delta T)
t_ret_e = t_flow_design - deltaT
dt_mean_e = (t_flow_design - t_ret_e) / math.log((t_b_heat - t_flow_design) / (t_b_heat - t_ret_e))

# Create one mass models for high temperature application
ParaHTBui_E = CalcParameters(
    t_a_design=t_a_design,
    t_a=-10,
    relHum=69.38,
    q_design=q_design_e,
    PLC=1,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=65,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=dt_mean_e,
    delta_T_cond_design=deltaT
)
HTBui_E = ParaHTBui_E.createBuilding(dynamic_load=use_dynamic_load)

ParaHTBui_A = CalcParameters(
    t_a_design=t_a_design,
    t_a=-7,
    relHum=74.69,
    q_design=q_design_e,
    PLC=0.8846,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=61,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=56.4-t_b_heat,
    delta_T_cond_design=deltaT
)
HTBui_A = ParaHTBui_A.createBuilding(dynamic_load=use_dynamic_load)

ParaHTBui_B = CalcParameters(
    t_a_design=t_a_design,
    t_a=2,
    relHum=83.87,
    q_design=q_design_e,
    PLC=0.5385,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=49,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=46.2-t_b_heat,
    delta_T_cond_design=deltaT
)
HTBui_B = ParaHTBui_B.createBuilding(dynamic_load=use_dynamic_load)

ParaHTBui_C = CalcParameters(
    t_a_design=t_a_design,
    t_a=7,
    relHum=86.84,
    q_design=q_design_e,
    PLC=0.3462,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=41,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=39.2-t_b_heat,
    delta_T_cond_design=deltaT
)
HTBui_C = ParaHTBui_C.createBuilding(dynamic_load=use_dynamic_load)

ParaHTBui_D = CalcParameters(
    t_a_design=t_a_design,
    t_a=12,
    relHum=88.94,
    q_design=q_design_e,
    PLC=0.1538,
    c_design=c_design,
    t_flow_design=t_flow_design,
    t_flow_plc=32,
    t_b=t_b_heat,
    m_dot_H_design=m_dot_H_design,
    constant_mflow=use_constant_mflow,
    dt_mean=31.2-t_b_heat,
    delta_T_cond_design=deltaT
)
HTBui_D = ParaHTBui_D.createBuilding(dynamic_load=use_dynamic_load)

# --- Examples for cooling operation (only at low temperature) ---
# Explanation: the main difference here is the negative value for PLC!
# Cooling is only defined for one temperature application (low)
t_a_design_cool = 35
t_flow_design_cool = 7
deltaT_cool = 5

# Cool PLC-A
para_bui_cool_plc_a = CalcParameters(
    t_a_design=t_a_design_cool,
    t_flow_design=t_flow_design_cool,
    q_design=p_design_c,
    m_dot_H_design=mass_flow_design_cool,
    delta_T_cond_design=deltaT_cool,
    t_a=35,
    # relHum=...,
    t_flow_plc=t_flow_design_cool,
    PLC=-1,
    c_design=c_design_lt,
    t_b=t_b_cool,
    constant_mflow=use_constant_mflow,
    dt_mean=...,  # TODO!
)
LTBui_A_cool = para_bui_cool_plc_a.createBuilding(dynamic_load=use_dynamic_load)

# Cool PLC-B
para_bui_cool_plc_b = CalcParameters(
    t_a_design=t_a_design_cool,
    t_flow_design=t_flow_design_cool,
    q_design=p_design_c,
    m_dot_H_design=mass_flow_design_cool,
    delta_T_cond_design=deltaT_cool,
    t_a=30,
    # relHum=...,
    t_flow_plc=8.5,
    PLC=-0.7368,
    c_design=c_design_lt,
    t_b=t_b_cool,
    constant_mflow=use_constant_mflow,
    dt_mean=...,  # TODO!
)
LTBui_B_cool = para_bui_cool_plc_b.createBuilding(dynamic_load=use_dynamic_load)

# Cool PLC-C
para_bui_cool_plc_c = CalcParameters(
    t_a_design=t_a_design_cool,
    t_flow_design=t_flow_design_cool,
    q_design=p_design_c,
    m_dot_H_design=mass_flow_design_cool,
    delta_T_cond_design=deltaT_cool,
    t_a=25,
    # relHum=...,
    t_flow_plc=10,
    PLC=-0.4737,
    c_design=c_design_lt,
    t_b=t_b_cool,
    constant_mflow=use_constant_mflow,
    dt_mean=...,  # TODO!
)
LTBui_C_cool = para_bui_cool_plc_c.createBuilding(dynamic_load=use_dynamic_load)

# Cool PLC-D
para_bui_cool_plc_d = CalcParameters(
    t_a_design=t_a_design_cool,
    t_flow_design=t_flow_design_cool,
    q_design=p_design_c,
    m_dot_H_design=mass_flow_design_cool,
    delta_T_cond_design=deltaT_cool,
    t_a=20,
    # relHum=...,
    t_flow_plc=11.5,
    PLC=-0.2105,
    c_design=c_design_lt,
    t_b=t_b_cool,
    constant_mflow=use_constant_mflow,
    dt_mean=...,  # TODO!
)
LTBui_D_cool = para_bui_cool_plc_d.createBuilding(dynamic_load=use_dynamic_load)
