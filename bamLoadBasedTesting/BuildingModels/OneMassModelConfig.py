from bamLoadBasedTesting.oneMassModel import CalcParameters

"Change design power according to your heat pump"
q_design_e = 5390           # in W; design heating power in E - only value which is dependent on the heat pump
t_a_design = -10            # in °C; see T_designh in EN 14825 (average climate)
t_b = 20                    # in °C; see indoor temperature in EN 14825; constant building temperature
t_flow_design = 55          # in °C; design supply temperature

deltaT = 8                  # in K; temperature difference in condenser
# TODO use mass flow rate from norm test?!
mass_flow_design = q_design_e / (4183*deltaT)   # in kg/s; design mass flow of heating system

# Parameters for one mass model
tau_h = 1957                # in s; time constant of mass
use_dynamic_load = True     # if True use dynamic load, if False use fixed load

# Design without hydraulic switch and virtual BUH
ParaMTBui_E = CalcParameters(t_a_design=t_a_design, t_a=-10, q_design=q_design_e, PLC=1, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=55, t_b=t_b, m_dot_H_design=mass_flow_design,
                             delta_T_cond=deltaT)
MTBui_E = ParaMTBui_E.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_A = CalcParameters(t_a_design=t_a_design, t_a=-7, q_design=q_design_e, PLC=0.885,  tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=52, t_b=t_b, m_dot_H_design=mass_flow_design,
                             delta_T_cond=deltaT)
MTBui_A = ParaMTBui_A.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_B = CalcParameters(t_a_design=t_a_design, t_a=2, q_design=q_design_e, PLC=0.538, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=42, t_b=t_b, m_dot_H_design=mass_flow_design,
                             delta_T_cond=deltaT)
MTBui_B = ParaMTBui_B.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_C = CalcParameters(t_a_design=t_a_design, t_a=7, q_design=q_design_e, PLC=0.346, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=36, t_b=t_b, m_dot_H_design=mass_flow_design,
                             delta_T_cond=deltaT)
MTBui_C = ParaMTBui_C.createBuilding(dynamic_load=use_dynamic_load)

ParaMTBui_D = CalcParameters(t_a_design=t_a_design, t_a=12, q_design=q_design_e, PLC=0.154, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=30, t_b=t_b, m_dot_H_design=mass_flow_design,
                             delta_T_cond=deltaT)
MTBui_D = ParaMTBui_D.createBuilding(dynamic_load=use_dynamic_load)
