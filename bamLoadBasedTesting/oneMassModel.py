"""This model is used to calculate the return flow of a building according to the compensation load method
@author: Stephan Göbel, date: 2025-07"""
import warnings
import math
from pyfluids import Fluid, FluidsList, Input

class ThermalMass:
    def __init__(self, mcp, T_start):
        """
        Thermal mass must have initial temperature.
        :param mcp: heat capacity in J/K.
        :param T_start: initial temperature in °C / K.
        """
        self.mcp = mcp
        self.T = T_start

    def qflow(self, Q):
        """
        Calculates new temperature after energy input or output.
        :param Q: Energy in Joule, positiv for increasing energy.
        """
        self.T = self.T + Q/self.mcp

    def setT(self, T):
        """
        Sets temperature off mass directly.
        :param T: new Temperature for mass.
        """
        self.T = T

class OneMassBuilding:
    def __init__(self, q_design_plc, plc, ua_hb, mcp_h,  t_a, t_start_h, t_flow_design, m_dot_H_design, T_mean,
                 t_b_design=20, relHum = 0, dynamic_load=True, q_def_corr=0, constant_mflow=True):
        """
        Init function, use either °C or K but not use both.
        :param q_design_plc: part-load heating power in W.
        :param plc: relative heating load in test point (0...1).
        :param ua_hb: thermal conductivity in W/K between transfer system (H) and Building (B).
        :param mcp_h: heat capacity transfer system in J/K.
        :param t_a: ambient temperature in °C / K.
        This parameter has currently no impact on the calculations and is just listed for completeness.
        :param t_start_h: initial temperature transfer system (H) in °C / K.
        :param t_flow_design: nominal design flow temperature in °C / K.
        This parameter has currently no impact on the calculations and is just listed for completeness.
        :param m_dot_H_design: design mass flow of heating system in kg/s.
        :param T_mean: water mean temperature in condenser in °C / K.
        This parameter has currently no impact on the calculations and is just listed for completeness.
        :param t_b_design: constant building temperature in °C / K.
        :param relHum: relative humidity in %.
        This parameter has currently no impact on the calculations and is just listed for completeness.
        :param dynamic_load: True for dynamic load and false for fixed load.
        :param q_def_corr: defrost correction in W.
        :param constant_mflow: if true use constant mass flow.
        """
        # Initialize given values
        self.q_design_plc = q_design_plc
        self.plc = plc
        self.ua_hb = ua_hb
        self.t_a = t_a
        self.t_ret = t_start_h
        self.t_flow_design = t_flow_design
        self.m_flow_design = m_dot_H_design
        self.T_mean = T_mean
        self.t_b_design = t_b_design
        self.relHum = relHum
        self.dynamic_load = dynamic_load
        self.q_def_corr = q_def_corr
        self.constant_mflow = constant_mflow

        # Create class ThermalMass for the heating system (one mass)
        self.MassH = ThermalMass(mcp_h, t_start_h)

        # Set default values for heat flow rates and temperature difference of virtual booster heater
        self.q_dot_hp = 0       # in W, heat flow rate from heat pump to heating system
        self.q_dot_hb = 0       # in W, heat flow rate from heating system to building

        # Create fluid instances for water (supply and return conditions)
        self.water_sup = Fluid(FluidsList.Water).factory()
        self.water_ret = Fluid(FluidsList.Water).factory()

    def calcHeatFlows(self, m_dot, t_sup, t_ret_mea, heating):
        """
        Calculates current heat flows between heat pump -- transfer system (q_dot_hp) and transfer system -- building (q_dot_hb).
        :param m_dot: measured value of mass flow [kg/s].
        :param t_sup: measured value of supply temperature [°C].
        :param t_ret_mea: measured value of return temperature [°C].
        :param heating: true for heating and cooling, false for defrost.
        """

        # Calculate heat flow rate from the heat pump to the heat transfer system
        try:
            # Try to calculate this based on enthalpy differences determined with water data

            # Assumption for the water pressure
            p_water = 3e5

            # Get enthalpy for supplied water
            self.water_sup.update(Input.temperature(t_sup), Input.pressure(p_water))
            h_sup = self.water_sup.enthalpy                                             # in J/kg

            # Get enthalpy for returned water
            self.water_ret.update(Input.temperature(t_ret_mea), Input.pressure(p_water))
            h_ret = self.water_ret.enthalpy                                             # in J/kg

            # Heat flow rate from the heat pump to the heat transfer system
            self.q_dot_hp = m_dot * (h_sup - h_ret)                                     # in W

        except:
            warnings.warn("WARNING: enthalpies could not be determined!")

            # If enthalpy cannot be determined (e.g. T < Tmelt), use the temperature difference with constant cp=4183 J/kg/K
            self.q_dot_hp = m_dot * 4183 * (t_sup - t_ret_mea)


        # Heat flow rate from the heat transfer system to the building
        if self.dynamic_load:
            # Dynamic load approach

            try:
                # Calculation with logarithmic temperature difference: introduced factor -1 to adjust the direction of the heat flow rate
                self.q_dot_hb = (self.ua_hb * (self.MassH.T - t_sup) * (-1) /
                                 math.log((self.t_b_design - t_sup) /
                                          (self.t_b_design - self.MassH.T)))
            except:
                warnings.warn("WARNING: logarithmic temperature difference failed in simulation!")

                # Previous calculation with arithmetic temperature difference used as backup
                self.q_dot_hb = self.ua_hb * ((t_sup+self.MassH.T)/2 - self.t_b_design)

        else:
            # Fixed load approach

            if heating:                                     # heating or cooling
                # no defrost
                self.q_dot_hb = self.q_design_plc + self.q_def_corr
            else:
                # defrost
                self.q_dot_hb = 0

    def doStep(self, t_sup, t_ret_mea, m_w_hp, stepSize, heating):
        """
        Calculate the new return temperature for the heat pump.
        Step of 'stepSize' (e.g. 1 second):
        1) Calculate current heat flows.
        2) Calculate new temperature of thermal masses based on energy balance.
        3) Get return temperature (= temperature of thermal mass).
        :param t_sup: supply temperature of the heat pump [°C / K].
        :param t_ret_mea: measured value of return temperature [°C].
        :param m_w_hp: secondary mass flow rate of the heat exchanger on the inside (for heating this is the condenser) [kg/s].
        :param stepSize: step size of the building model (also sampling frequency of the test bench) [s].
        :param heating: true for heating, false for defrost.
        """

        # Calculate heat flows depending on current temperatures
        self.calcHeatFlows(m_dot=m_w_hp, t_sup=t_sup, t_ret_mea=t_ret_mea, heating=heating)

        # Update the thermal mass (heating system) with the calculated heat flows (energy balance)
        self.MassH.qflow((self.q_dot_hp - self.q_dot_hb)*stepSize)

        # Get new return temperature
        self.t_ret = self.MassH.T

class CalcParameters:
    def __init__(self, t_a_design, t_a, q_design, PLC, t_flow_design, t_flow_plc, m_dot_H_design, constant_mflow,
                 delta_T_cond_design, c_design, dt_mean=0, t_b=20, relHum = 0, q_def_corr=0):
        """
        Calculate parameters for one mass building model according to given parameters of a heat pump.

        :param t_a_design: design nominal outdoor temperature in °C.
        This parameter has currently no impact on the calculations and is just listed for completeness.
        :param t_a: outdoor temperature in test point in °C.
        This parameter has currently no impact on the calculations and is just listed for completeness.
        :param q_design: nominal heating power in W.
        :param PLC: relative heating load in test point (0...1).
        :param t_flow_design: nominal design flow temperature in °C.
        (e.g. 55 °C for medium temperature or 35 °C for low temperature).
        This parameter has currently no impact on the calculations and is just listed for completeness.
        :param t_flow_plc: flow temperature of test point in °C
        (e.g. 52 °C for PLC-A at medium temperature application).
        :param m_dot_H_design: design mass flow of heating system in kg/s.
        :param constant_mflow: if true use constant mass flow.
        :param delta_T_cond_design: design temperature difference in condenser (for heating) in K.
        :param c_design: design thermal capacity in J/K/W_design.
        :param dt_mean: logarithmic mean temperature difference in K
        (for the specific part load e.g. PLC-A).
        :param t_b: nominal building temperature (standard value: 20 °C) in °C.
        :param relHum: relative humidity in %.
        This parameter has currently no impact on the calculations and is just listed for completeness.
        :param q_def_corr: defrost correction in W.
        """

        # Initialize given values
        self.t_a_design = t_a_design
        self.t_a = t_a
        self.q_design = q_design
        self.PLC = PLC
        self.t_flow_design = t_flow_design
        self.t_flow_plc = t_flow_plc
        self.m_dot_H_design = m_dot_H_design
        self.constant_mflow = constant_mflow
        # delta_T_cond_design is used depending on the mass flow (see below)
        self.c_design = c_design
        # dt_mean is used depending on the mass flow (see below)
        self.t_b = t_b
        self.relHum = relHum
        self.q_def_corr = q_def_corr

        # Calculate heat capacity for the given test point in W
        self.q_design_plc = q_design * PLC

        # Temperature difference in condenser
        # Mass flow in config configured
        # Difference between variable and fixed flow
        if constant_mflow:
            # Fixed flow

            # Recalculate temperature differences in the condenser in K
            self.delta_T_cond = self.q_design * self.PLC / (self.m_dot_H_design * 4183)         # PLC
            self.delta_T_cond_design = self.q_design / (self.m_dot_H_design * 4183)             # Design

            # Calculate return temperature (intermediate step for dt_mean) in °C
            t_ret = self.t_flow_plc - self.delta_T_cond                                         # PLC

            # Calculate mean temperature differences in K
            try:
                self.dt_mean = (self.t_flow_plc - t_ret) / math.log((self.t_b - self.t_flow_plc) / (self.t_b - t_ret))  # PLC
            except:
                raise ValueError("Logarithmic temperature difference failed. Check parameters of building model!")

        else:
            # Variable flow

            # Use given mean temperatures
            self.dt_mean = dt_mean                                                              # PLC

            # Use given design temperature difference in the condenser (heating)
            self.delta_T_cond_design = delta_T_cond_design                                      # Design

            # Calculate temperature difference for this part load condition in K
            self.delta_T_cond = self.delta_T_cond_design * self.PLC                                  # PLC

        # Calculate thermal conductivities between transfer system and building for PLC and design conditions in W/K
        self.ua_hb = self.q_design * self.PLC / self.dt_mean                                    # PLC

        # Calculate mean logarithmic temperature in °C
        self.T_mean_log = self.dt_mean + self.t_b

        # Initial temperature of heating system in °C
        self.t_start_h = self.t_flow_plc - self.delta_T_cond

        # Thermal capacity of heating system in J/K
        self.mcp_h = self.c_design * self.q_design

        # Time constant of heating system in s
        self.tau_h = self.mcp_h / self.ua_hb

    def update(self):
        """Update this class after changing one of the init parameters."""
        self.__init__(
            t_a_design=self.t_a_design,
            t_a=self.t_a,
            q_design=self.q_design,
            PLC=self.PLC,
            t_flow_design=self.t_flow_design,
            t_flow_plc=self.t_flow_plc,
            m_dot_H_design=self.m_dot_H_design,
            c_design=self.c_design,
            t_b=self.t_b,
            relHum=self.relHum,
            q_def_corr=self.q_def_corr,
            delta_T_cond_design=self.delta_T_cond_design,
            constant_mflow=self.constant_mflow,
            dt_mean=self.dt_mean,
        )

    def set_q_design(self, q_design):
        """Set function for design load."""
        self.q_design = q_design
        self.update()

    def set_plc(self, PLC):
        """Set function for PLC."""
        self.PLC = PLC
        self.update()

    def set_t_flow_plc(self, t_flow_plc):
        """Set function for PLC flow temperature."""
        self.t_flow_plc = t_flow_plc
        self.update()

    def set_plc_and_t_flow_plc(self, PLC, t_flow_plc):
        """Combined set function for PLC and PLC flow temperature."""
        self.PLC = PLC
        self.t_flow_plc = t_flow_plc
        self.update()

    def set_q_def_corr(self, q_def_corr):
        """Set function for defrost correction."""
        self.q_def_corr = q_def_corr
        self.update()

    def createBuilding(self, dynamic_load=True):
        """Create one mass building model.

        :param dynamic_load: True for dynamic load and false for fixed load.
        :return one mass building.
        """
        building = OneMassBuilding(
            q_design_plc = self.q_design_plc, plc=self.PLC, ua_hb=self.ua_hb, mcp_h=self.mcp_h, t_a=self.t_a,
            t_start_h=self.t_start_h, t_flow_design=self.t_flow_plc, m_dot_H_design=self.m_dot_H_design,
            relHum = self.relHum, T_mean = self.T_mean_log, dynamic_load = dynamic_load, q_def_corr = self.q_def_corr,
            constant_mflow=self.constant_mflow, t_b_design=self.t_b
        )
        print(
         "Building created:"  +
         " Mass H = " + str(round(building.MassH.mcp,2)) + " ua_hb = " + str(round(building.ua_hb,2)) +
         " time constant heating system = " + str(round(building.MassH.mcp / building.ua_hb, 2)) +
         " ambient temperature = " + str(round(building.t_a, 2)) + " °C"
         " log mean temperature = " + str(round(building.T_mean, 2)) + " °C"
        )
        return building
