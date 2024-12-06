from twoMassModel import CalcParameters

"Change design power according to your heat pump"
q_design_e = 5390 # design heating power in E - only value which is dependent on the heat pump # todo change to new heat pump
t_a_design = -10 # design ambient temperature to parametrize the model
t_flow_design = 55 # flow temperature in design point
tau_b = 209125 # given time constant for building envelope
tau_h = 1957 # given time constant for radiator system
mass_flow = 720/3600 # design mass flow # todo change to new heat pump or use variable flow and provide delta T
t_b = 20 # constant building temperature

ParaMTBui_E = CalcParameters(t_a_design=t_a_design, t_a=-10, q_design=q_design_e, PLC=1, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=55, t_b=t_b, const_flow=True, mass_flow=mass_flow,
                             boostHeat=True, maxPowBooHea=7000, volBufTank=100) # booster heater is active! # todo check
MTBui_E = ParaMTBui_E.createBuilding()

ParaMTBui_A = CalcParameters(t_a_design=t_a_design, t_a=-7, q_design=q_design_e, PLC=0.885, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=52, t_b=t_b, const_flow=True, mass_flow=mass_flow)
MTBui_A = ParaMTBui_A.createBuilding()

ParaMTBui_B = CalcParameters(t_a_design=t_a_design, t_a=2, q_design=q_design_e, PLC=0.538, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=42, t_b=t_b, const_flow=True, mass_flow=mass_flow)
MTBui_B = ParaMTBui_B.createBuilding()

ParaMTBui_C = CalcParameters(t_a_design=t_a_design, t_a=7, q_design=q_design_e, PLC=0.346, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=36, t_b=t_b, const_flow=True, mass_flow=mass_flow)
MTBui_C = ParaMTBui_C.createBuilding()

ParaMTBui_D = CalcParameters(t_a_design=t_a_design, t_a=12, q_design=q_design_e, PLC=0.154, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=30, t_b=t_b, const_flow=True, mass_flow=mass_flow)
MTBui_D = ParaMTBui_D.createBuilding()
