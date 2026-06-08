import math

from bamLoadBasedTesting.oneMassModel import CalcParameters

"Change design power according to your heat pump"
q_design_e = 5390           # in W; design heating power in E - only value which is dependent on the heat pump
t_a_design = -10            # in °C; see T_designh in EN 14825 (average climate)
t_b = 20                    # in °C; see indoor temperature in EN 14825; constant building temperature
t_flow_design = 55          # in °C; design supply temperature

deltaT = 8                  # in K; temperature difference in condenser
mass_flow_design = q_design_e / (4183*deltaT)   # in kg/s; declared mass flow rate from manufacturer

# Parameters for one mass model
c_design = 67               # in J/K/W_design
use_dynamic_load = True     # if True use dynamic load, if False use fixed load
use_constant_mflow = True   # if True use constant flow (variable dT), if False use variable flow (constant dT)

# Design logarithmic mean temperature (only for variable flow / fixed delta T)
t_ret_design = t_flow_design - deltaT
dt_mean_design = (t_flow_design - t_ret_design) / math.log((t_b - t_flow_design) / (t_b - t_ret_design))

# Design without hydraulic switch and virtual BUH
ParaMTBui_E = CalcParameters(t_a_design=t_a_design, t_a=-10, relHum=69.38, q_design=q_design_e, PLC=1, c_design=c_design,
                             t_flow_design=t_flow_design, t_flow_plc=55, t_b=t_b, m_dot_H_design=mass_flow_design,
                             constant_mflow=use_constant_mflow, dt_mean=dt_mean_design, dt_mean_design=dt_mean_design,
                             delta_T_cond_design=deltaT, q_def_corr=0)
MTBui_E = ParaMTBui_E.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_A = CalcParameters(t_a_design=t_a_design, t_a=-7, relHum=74.69, q_design=q_design_e, PLC=0.8846, c_design=c_design,
                             t_flow_design=t_flow_design, t_flow_plc=52, t_b=t_b, m_dot_H_design=mass_flow_design,
                             constant_mflow=use_constant_mflow, dt_mean=48.3-t_b, dt_mean_design=dt_mean_design,
                             delta_T_cond_design=deltaT)
MTBui_A = ParaMTBui_A.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_B = CalcParameters(t_a_design=t_a_design, t_a=2, relHum=83.87, q_design=q_design_e, PLC=0.5385, c_design=c_design,
                             t_flow_design=t_flow_design, t_flow_plc=42, t_b=t_b, m_dot_H_design=mass_flow_design,
                             constant_mflow=use_constant_mflow, dt_mean=39.8-t_b, dt_mean_design=dt_mean_design,
                             delta_T_cond_design=deltaT)
MTBui_B = ParaMTBui_B.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_C = CalcParameters(t_a_design=t_a_design, t_a=7, relHum=86.84, q_design=q_design_e, PLC=0.3462, c_design=c_design,
                             t_flow_design=t_flow_design, t_flow_plc=36, t_b=t_b, m_dot_H_design=mass_flow_design,
                             constant_mflow=use_constant_mflow, dt_mean=34.6-t_b, dt_mean_design=dt_mean_design,
                             delta_T_cond_design=deltaT)
MTBui_C = ParaMTBui_C.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_D = CalcParameters(t_a_design=t_a_design, t_a=12, relHum=88.94, q_design=q_design_e, PLC=0.1538, c_design=c_design,
                             t_flow_design=t_flow_design, t_flow_plc=30, t_b=t_b, m_dot_H_design=mass_flow_design,
                             constant_mflow=use_constant_mflow, dt_mean=29.4-t_b, dt_mean_design=dt_mean_design,
                             delta_T_cond_design=deltaT)
MTBui_D = ParaMTBui_D.createBuilding(dynamic_load=use_dynamic_load)
