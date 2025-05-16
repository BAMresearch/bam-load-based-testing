from twoMassModel import CalcParameters

"Change design power according to your heat pump"
q_design_e = 7550 # design heating power in E - only value which is dependent on the heat pump
t_a_design = -10
t_flow_design = 55
tau_b = 209125
tau_h = 1957
m_dot_H_design = 0.129 #kg/s equal to 464/3600
t_b = 20 # constant building temperature


#TLF: T_biv=-5°C
ParaMTBui_F = CalcParameters(t_a_design=t_a_design, t_a=-5, q_design=q_design_e, PLC=0.81, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=49.8, t_b=t_b, const_flow=True, m_dot_H_design=m_dot_H_design,
                             hydraulicSwitch = True)
MTBui_F = ParaMTBui_F.createBuilding()


ParaMTBui_B = CalcParameters(t_a_design=t_a_design, t_a=2, q_design=q_design_e, PLC=0.538, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=42, t_b=t_b, const_flow=True, m_dot_H_design=m_dot_H_design,
                             hydraulicSwitch = True)
MTBui_B = ParaMTBui_B.createBuilding()


ParaMTBui_C = CalcParameters(t_a_design=t_a_design, t_a=7, q_design=q_design_e, PLC=0.346, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=36, t_b=t_b, const_flow=True, m_dot_H_design=m_dot_H_design,
                             hydraulicSwitch = True)
MTBui_C = ParaMTBui_C.createBuilding()


ParaMTBui_D = CalcParameters(t_a_design=t_a_design, t_a=12, q_design=q_design_e, PLC=0.154, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=30, t_b=t_b, const_flow=True, m_dot_H_design=m_dot_H_design,
                             hydraulicSwitch = True)
MTBui_D = ParaMTBui_D.createBuilding()
