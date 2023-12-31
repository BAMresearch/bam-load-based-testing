from bamLoadBasedTesting.BuildingModels import BAM_RRT_MT
import time

# Step Size
stepSize = 1

# Create Reduced building
BamBuilding = BAM_RRT_MT.MTBui_A

while True:
    t1 = time.time()

    t_sup_test_bench = 52 #TODO Connect your test bench here!
    v_flow = 720/3600 #in l/s  #TODO Connect your test bench here!
    t_ret_test_bench = 45 #TODO Connect your test bench here!
    #Calculate time step in Building model
    BamBuilding.doStep(t_sup=t_sup_test_bench, m_dot=v_flow, stepSize=stepSize, t_ret_mea=t_ret_test_bench)

    print("Has to be connected to test bench! Set return temperature for test bench:" + str(BamBuilding.t_ret)) #TODO Connect your test bench here!

    print("Supply Temperature: " + str(round(t_sup_test_bench, 2)) +
          " V_flow : " + str(round(v_flow, 2)) +
          " Return Temperature: " + str(round(BamBuilding.t_ret, 2)))
    print(" T_H = " + str(round(BamBuilding.MassH.T, 2)) +
          " T_B = " + str(round(BamBuilding.MassB.T, 2)) +
          " q_flow_hp = " + str(round(BamBuilding.q_dot_hp, 2)) +
          " q_flow_hb = " + str(round(BamBuilding.q_dot_hb, 2)) +
          " q_flow_ba = " + str(round(BamBuilding.q_dot_ba, 2)))

    "Sleep to run in real time"
    t2 = time.time()
    sleepTime = stepSize-(t2-t1)
    if sleepTime > 0:
        print('Sleep time = ' + str(sleepTime) + ' s')
        time.sleep(sleepTime)
    else:
        print('Warning: Loop too slow!!')
        sleepTime = 0




