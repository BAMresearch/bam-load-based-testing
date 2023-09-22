from bamLoadBasedTesting.twoMassModel import CalcParameters

"Change design power according to your heat pump"
q_design_e = 5390 # design heating power in E - only value which is dependent on the heat pump
tau_b = 209125
tau_h = 1957
mass_flow = 720/3600
t_b = 20 # constant building temperature

ParaMTBui_E = CalcParameters(t_a=-10, q_design=q_design_e, tau_b=tau_b, tau_h=tau_h, t_flow_design=55, t_b=t_b,
                             const_flow=True, mass_flow=mass_flow, boostHeat=True, maxPowBooHea=7000)
MTBui_E = ParaMTBui_E.createBuilding()

ParaMTBui_A = CalcParameters(t_a=-7, q_design=q_design_e*0.885, tau_b=tau_b, tau_h=tau_h, t_flow_design=52, t_b=t_b,
                             const_flow=True, mass_flow=mass_flow)
MTBui_A = ParaMTBui_A.createBuilding()

ParaMTBui_B = CalcParameters(t_a=2, q_design=q_design_e*.538, tau_b=tau_b, tau_h=tau_h, t_flow_design=42, t_b=t_b,
                             const_flow=True, mass_flow=mass_flow)
MTBui_B = ParaMTBui_B.createBuilding()

ParaMTBui_C = CalcParameters(t_a=7, q_design=q_design_e*0.346, tau_b=tau_b, tau_h=tau_h, t_flow_design=36, t_b=t_b,
                             const_flow=True, mass_flow=mass_flow)
MTBui_C = ParaMTBui_C.createBuilding()

ParaMTBui_D = CalcParameters(t_a=12, q_design=q_design_e *0.154, tau_b=tau_b, tau_h=tau_h, t_flow_design=30, t_b=t_b,
                             const_flow=True, mass_flow=mass_flow)
MTBui_D = ParaMTBui_D.createBuilding()
