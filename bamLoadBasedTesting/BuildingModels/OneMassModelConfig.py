from bamLoadBasedTesting.oneMassModel import CalcParameters

"Change design power according to your heat pump"
q_design_e = 5390 # design heating power in E - only value which is dependent on the heat pump
t_a_design = -10
t_flow_design = 55
tau_h = 1957
deltaT = 8
mass_flow_design = q_design_e / (4183*deltaT)
t_b = 20 # constant building temperature

# Design without hydraulic switch and virtual BUH
ParaMTBui_E = CalcParameters(t_a_design=t_a_design, t_a=-10, q_design=q_design_e, PLC=1, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=55, t_b=t_b, m_dot_H_design=mass_flow_design,
                             boostHeat=False, maxPowBooHea=7000)
MTBui_E = ParaMTBui_E.createBuilding()

ParaMTBui_A = CalcParameters(t_a_design=t_a_design, t_a=-7, q_design=q_design_e, PLC=0.885,  tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=52, t_b=t_b, m_dot_H_design=mass_flow_design)
MTBui_A = ParaMTBui_A.createBuilding()

ParaMTBui_B = CalcParameters(t_a_design=t_a_design, t_a=2, q_design=q_design_e, PLC=0.538, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=42, t_b=t_b, m_dot_H_design=mass_flow_design)
MTBui_B = ParaMTBui_B.createBuilding()

ParaMTBui_C = CalcParameters(t_a_design=t_a_design, t_a=7, q_design=q_design_e, PLC=0.346, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=36, t_b=t_b, m_dot_H_design=mass_flow_design)
MTBui_C = ParaMTBui_C.createBuilding()

ParaMTBui_D = CalcParameters(t_a_design=t_a_design, t_a=12, q_design=q_design_e, PLC=0.154, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=30, t_b=t_b, m_dot_H_design=mass_flow_design)
MTBui_D = ParaMTBui_D.createBuilding()
