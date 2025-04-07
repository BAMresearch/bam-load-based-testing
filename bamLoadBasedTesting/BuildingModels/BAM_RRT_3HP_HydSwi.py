from twoMassModel import CalcParameters

"Change design power according to your heat pump"
q_design_e = 5390 # design heating power in E - only value which is dependent on the heat pump # todo change to new heat pump
t_a_design = -10 # design ambient temperature to parametrize the model
t_flow_design = 55 # flow temperature in design point
tau_b = 209125 # given time constant for building envelope
tau_h = 1957 # given time constant for radiator system
mass_flow = q_design_e/(4183*8) # design mass flow # todo change to new heat pump or use variable flow and provide delta T
t_b = 20 # constant building temperature
mass_flow_ufh =q_design_e/(4183*5)
tau_h_ufh = 21380

Para_Bui_A_m10 = CalcParameters(t_a_design=t_a_design,  t_a=-10, relHum=69, q_design=q_design_e, PLC=1, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=55, t_b=t_b, const_flow=True, mass_flow=mass_flow,
                             boostHeat=False, maxPowBooHea=7000, hydraulicSwitch=True, delta_T_cond=8) # booster heater is active! # todo check
Bui_A_m10 = Para_Bui_A_m10.createBuilding()

Para_Bui_A_m7 = CalcParameters(t_a_design=t_a_design, t_a=-7, relHum=75, q_design=q_design_e, PLC=0.8846, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=52, t_b=t_b, const_flow=True, mass_flow=mass_flow,
                             hydraulicSwitch=True, delta_T_cond=8)
Bui_A_m7 = Para_Bui_A_m7.createBuilding()

ParaBui_A_2 = CalcParameters(t_a_design=t_a_design, t_a=2, relHum=84, q_design=q_design_e, PLC=0.5385, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=42, t_b=t_b, const_flow=True, mass_flow=mass_flow,
                             hydraulicSwitch=True, delta_T_cond=8)
Bui_A_2 = ParaBui_A_2.createBuilding()

ParaBui_A_7 = CalcParameters(t_a_design=t_a_design, t_a=7, relHum=87, q_design=q_design_e, PLC=0.3462, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=36, t_b=t_b, const_flow=True, mass_flow=mass_flow,
                             hydraulicSwitch=True, delta_T_cond=8)
Bui_A_7 = ParaBui_A_7.createBuilding()

ParaBui_A_12 = CalcParameters(t_a_design=t_a_design, t_a=12, relHum=89, q_design=q_design_e, PLC=0.1538, tau_b=tau_b, tau_h=tau_h,
                             t_flow_design=t_flow_design, t_flow_plc=30, t_b=t_b, const_flow=True, mass_flow=mass_flow,
                             hydraulicSwitch=True, virtualBypass=False, delta_T_cond=8)
Bui_A_12 = ParaBui_A_12.createBuilding()

Para_Bui_A_m7_UFH = CalcParameters(t_a_design=t_a_design, t_a=-7, relHum=75, q_design=q_design_e, PLC=0.8846, tau_b=tau_b, tau_h=tau_h_ufh,
                             t_flow_design=35, t_flow_plc=34, t_b=t_b, const_flow=True, mass_flow=mass_flow_ufh,
                             hydraulicSwitch=True, delta_T_cond=5)
Bui_A_m7_UFH = Para_Bui_A_m7_UFH.createBuilding()

Para_Bui_A_7_UFH = CalcParameters(t_a_design=t_a_design, t_a=7, relHum=87, q_design=q_design_e, PLC=0.3462, tau_b=tau_b, tau_h=tau_h_ufh,
                             t_flow_design=35, t_flow_plc=27, t_b=t_b, const_flow=True, mass_flow=mass_flow_ufh,
                             hydraulicSwitch=True, delta_T_cond=5)
Bui_A_7_UFH = Para_Bui_A_7_UFH.createBuilding()
