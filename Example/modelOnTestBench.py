from bamLoadBasedTesting.BuildingModels import OneMassModelConfig
import os
import time
import datetime
import pandas as pd
import keyboard
import warnings

"""Script to emulate the compensation method on the test bench.

- Please set your parameters in the main function in the section USER INPUT.
- After that you can test the script without connecting it to your test bench.
- To use the script with your test bench, please adjust all the code with the comment 
  "TODO Connect your test bench here!"
- Then you can run the script with your test bench
- You can save intermediate results by pressing ctrl + s at the same time. The saving process will also be printed in 
  the console. IMPORTANT: Note that this can effect the real-time ability of this script. Saving could take more time
  than the duration of one time step (stepSize)!
- You can stop the calculations by pressing ctrl + h + p at the same time. After that all results and settings will be 
  saved.
- If the above keyboard shortcuts do not seem to work, hold all keys for one or two seconds.
"""

def save_results_and_settings(final):
    """Save results and settings to Excel files.

    :param final: if True, save final results; if False, save intermediate results.
    """
    # Save results
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    if final:
        res_path = export_path + f"\\results_final_{test_name}.xlsx"
        set_path = export_path + f"\\settings_final_{test_name}.xlsx"
    else:
        res_path = export_path + f"\\results_v{count_intermediate_results}_{test_name}.xlsx"
        set_path = export_path + f"\\settings_v{count_intermediate_results}_{test_name}.xlsx"

    print(f"Saving results (path={res_path})")
    res_tb_df = pd.DataFrame(res_tb)
    res_bui_df = pd.DataFrame(res_bui)
    results_df = pd.concat([res_tb_df, res_bui_df], axis=1)
    results_df.to_excel(res_path)

    # Save settings
    print(f"Saving settings (path={set_path})")
    set_dict = {
        "test_name": test_name,
        "export_path": export_path,
        "stepSize": stepSize,
        "time_start": time_start,
        "time_end": time_end,
        "current time": datetime.datetime.now(),
    }
    set_dict.update({"info": "the following settings are from the one mass building"})
    set_dict.update(BamBuilding.__dict__)
    settings_df = pd.DataFrame.from_dict(set_dict, orient='index')
    settings_df.to_excel(set_path)


if __name__ == "__main__":
    time_start = datetime.datetime.now()
    time_end = None

    # --- START OF USER INPUT ---
    # Name of this test: do not use spaces or special characters
    test_name = "test"      # TODO Insert a name for the test here

    # Export path
    export_path = ""        # TODO Insert an export path here, where the results will be stored

    # Step Size
    stepSize = 1            # in seconds; TODO Align step size with your own step size

    # Create Reduced building
    # TODO Specify all parameters for the test point and the one mass model in
    #  "bamLoadBasedTesting/BuildingModels/OneMassModelConfig.py" or add a new script under
    #  "bamLoadBasedTesting/BuildingModels" with the same parameters with adjusted values.
    BamBuilding = OneMassModelConfig.MTBui_A

    # --- END OF USER INPUT ---

    # Lists to store results
    res_tb = []                     # measurements from test bench
    res_bui = []                    # data from one mass model
    count_intermediate_results = 1  # counter for versions of intermediate results

    # --- Start of measurements and calculations ---
    print("\nStarting measurements at test bench and calculations of one mass model")
    print("Press ctrl + h + p to stop measurements and calculations (results will be saved afterwards)")
    while True:
        t1 = time.time()

        # Get current measurements from test bench
        t_sup_test_bench = 52       # in °C;    TODO Connect your test bench here!
        m_w_hp = 720/3600           # in kg/s;  TODO Connect your test bench here!
        t_ret_test_bench = 45       # in °C;    TODO Connect your test bench here!
        heating_test_bench = True   # Boolean value: True if heating (or cooling), False if defrosting TODO Connect your test bench here!

        # Save current state of test bench (tb) and one mass building (bui)
        res_tb.append(
            {
                "t_sup_test_bench": t_sup_test_bench,
                "t_ret_test_bench": t_ret_test_bench,
                "m_w_hp": m_w_hp,
                "heating_test_bench": heating_test_bench
            }
        )
        res_bui.append(
            {
                "T_h": BamBuilding.MassH.T,
                "q_dot_hp": BamBuilding.q_dot_hp,
                "q_dot_hb": BamBuilding.q_dot_hb,
                "m_dot_H_design": BamBuilding.hydraulicSwitch.m_flow_design,
                "T_set_supply": BamBuilding.t_flow_design,
                "T_bui": BamBuilding.t_b_design + 273.15,
            }
        )

        # Stop measurements and calculations with keyboard
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("h") and keyboard.is_pressed("p"):
            time_end = datetime.datetime.now()
            print("\nMeasurements and calculations were stopped by keyboard interrupt!\n")
            break

        # Save intermediate results
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("s"):
            print("\nSaving intermediate results!\n")
            save_results_and_settings(final=False)
            count_intermediate_results += 1

        # Calculate time step in Building model
        BamBuilding.doStep(
            t_sup=t_sup_test_bench,
            t_ret_mea=t_ret_test_bench,
            m_w_hp=m_w_hp,
            stepSize=stepSize,
            heating=heating_test_bench
        )

        # Set the return temperature from one mass model (BamBuilding.t_ret) at the test bench
        # TODO Connect your test bench here! After that you can comment the following print
        print("Has to be connected to test bench! Set return temperature for test bench: " + str(BamBuilding.t_ret))

        # Print current state of test bench and one mass model
        print("TEST BENCH: Supply Temperature: " + str(round(t_sup_test_bench, 2)) + " °C;" +
              " m_flow : " + str(round(m_w_hp, 2)) + " kg/s;" +
              " Return Temperature: " + str(round(BamBuilding.t_ret, 2)) + " °C; " +
              "ONE MASS MODEL: T_H = " + str(round(BamBuilding.MassH.T, 2)) + " °C;" +
              " q_flow_hp = " + str(round(BamBuilding.q_dot_hp, 2)) + " W;" +
              " q_flow_hb = " + str(round(BamBuilding.q_dot_hb, 2)) + " W")

        # Sleep to run in real time
        t2 = time.time()
        sleepTime = stepSize-(t2-t1)
        if sleepTime > 0:
            print('Sleep time = ' + str(sleepTime) + ' s\n')
            time.sleep(sleepTime)
        else:
            warnings.warn('Warning: Loop too slow!\n')
            sleepTime = 0

    # Save final results and settings
    save_results_and_settings(final=True)
