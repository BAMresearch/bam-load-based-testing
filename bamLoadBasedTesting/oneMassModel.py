"""This model is used to calculate the return flow of a building according to the compensation load method
@author: Stephan Göbel, date: 2025-07"""
import warnings
import math

class ThermalMass:
    def __init__(self, mcp, T_start):
        """
        Thermal mass must have initial temperature
        :param mcp: heat capacity in J/K
        :param T_start: initial temperature in °C / K
        """
        self.mcp = mcp
        self.T = T_start

    def qflow(self, Q):
        """
        calculates new temperature after energy input or output
        :param Q: Energy in Joule, positiv for increasing energy
        """
        self.T = self.T + Q/self.mcp

    def setT(self, T):
        """
        Sets temperature off mass directly
        :param T: new Temperature for mass
        """
        self.T = T


class HydraulicSwitch:
    def __init__(self, m_flow_design, hydraulicSwitch):
        """
        Virtual bypass valve
        :param m_flow_design:
        """
        self.m_flow_design = m_flow_design
        self.m_flow_sh = 0
        self.m_flow_swi = 0
        self.T_ret_swi = 0
        self.T_sup_swi = 0
        self.hydraulicSwitch = hydraulicSwitch

    def calcFlows(self, m_flow_hp, T_sup_hp, T_ret_sh):
        """
        Calculates mass flows and temperatures behind hydraulic switch valve
        :param m_flow_hp:
        :param T_sup_hp:
        :param T_ret_sh:
        :return:
        """
        if self.hydraulicSwitch:
            self.m_flow_sh = self.m_flow_design # m_flow heating system always equal to m_flow design
            self.m_flow_swi = m_flow_hp-self.m_flow_sh # m_flow through hydraulic switch > 0 if hp flow higher than design
            if m_flow_hp == 0: # hp off
                self.T_ret_swi = T_ret_sh
            elif self.m_flow_swi >= 0:  # heat pump delivers equal or more mass flow than design flow
                self.T_ret_swi = (T_ret_sh*self.m_flow_sh + T_sup_hp * self.m_flow_swi)/m_flow_hp
                self.T_sup_swi = T_sup_hp
            elif self.m_flow_swi < 0:  # heat pump delivers less mass flow than design flow
                self.T_ret_swi = T_ret_sh
                self.T_sup_swi = (m_flow_hp*T_sup_hp - self.m_flow_swi*T_ret_sh)/self.m_flow_sh
        else:
            self.m_flow_swi = 0
            self.T_ret_swi = T_ret_sh
            self.T_sup_swi = T_sup_hp


class OneMassBuilding:
    def __init__(self, q_design_plc, plc, ua_hb, mcp_h,  t_a, t_start_h, t_flow_design, m_dot_H_design, T_mean, t_b_design=20,
                 boostHeat = False, maxPowBooHea = 0, hydraulicSwitch = False, relHum = 0, dynamic_load=True, q_def_corr=0, constant_mflow=True):
        """
        Init function, use either °C or K but not use both
        :param q_design_plc: part-load heating power in W
        :param ua_hb: thermal conductivity in W/K between transfer system (H) and Building (B)
        :param mcp_h: heat capacity transfer system in J/kg/K
        :param t_a: ambient temperature in °C / K
        :param t_start_h: initial temperature transfer system (H) in °C / K
        :param t_flow_design: nominal design flow temperature in °C / K
        :param m_dot_H_design: design mass flow of heating system in kg/s
        :param T_mean: water mean temperature in condenser in °C / K
        :param t_b_design: constant building temperature in °C / K
        :param boostHeat: if true use virtual heater
        :param maxPowBooHea: maximal power of virtual heater in W
        :param hydraulicSwitch: if true use hydraulic switch
        :param relHum: relative humidity
        :param dynamic_load: True for dynamic load and false for fixed load
        :param q_def_corr: defrost correction in W
        :param constant_mflow: if true use constant mass flow
        """
        self.q_design_plc = q_design_plc
        self.plc = plc
        self.MassH = ThermalMass(mcp_h, t_start_h)
        self.hydraulicSwitch = HydraulicSwitch(m_flow_design=m_dot_H_design, hydraulicSwitch=hydraulicSwitch)
        self.ua_hb = ua_hb
        self.t_a = t_a
        self.t_b_design = t_b_design
        self.T_mean = T_mean
        self.relHum = relHum
        self.boostHeat = boostHeat
        self.q_dot_hp = 0
        self.q_dot_hb = 0
        self.q_dot_bh = 0
        self.t_ret = t_start_h
        self.t_flow_design = t_flow_design
        self.maxPowBooHea = maxPowBooHea
        self.TagHydSwi = hydraulicSwitch
        self.deltaBH = 0 # virtual booster heater delta T
        self.dynamic_load = dynamic_load
        self.q_def_corr = q_def_corr
        self.constant_mflow = constant_mflow

    def calcHeatFlows(self, m_dot, t_sup, t_ret_mea, heating):
        """
        Calculates current heat flows between heat pump -- transfer system; transfer system -- building and
        building -- environment
        :param m_dot: measured value of mass flow [kg/s]
        :param t_sup: measured value of supply temperature [°C]
        :param t_ret_mea: measured value of return temperature [°C]
        :param heating: true for heating and cooling, false for defrost
        """
        if self.boostHeat and t_sup < self.t_flow_design:
            self.q_dot_bh = m_dot*4183*(self.t_flow_design-t_sup)
            if self.q_dot_bh > self.maxPowBooHea:
                self.q_dot_bh = self.maxPowBooHea
                self.deltaBH = (self.q_dot_bh / (m_dot * 4183))
            else:
                self.deltaBH = self.t_flow_design - t_sup
        else:
            self.q_dot_bh = 0
            self.deltaBH = 0


        self.q_dot_hp = m_dot*4183*(t_sup-t_ret_mea)
        if self.TagHydSwi:  # if hydraulic switch is active, use temperature behind switch as input
            self.q_dot_hb = self.ua_hb * ((self.hydraulicSwitch.T_sup_swi + self.MassH.T) / 2 - self.t_b_design)
        else:
            if self.dynamic_load:
                # Dynamic load approach

                # Previous calculation with arithmetic temperature difference
                # self.q_dot_hb = self.ua_hb * ((t_sup+self.deltaBH+self.MassH.T)/2 - self.t_b_design)

                # New with logarithmic temperature difference: introduced factor -1 to adjust the direction of the heat
                # flow rate
                try:
                    self.q_dot_hb = (self.ua_hb * (self.MassH.T - (t_sup+self.deltaBH)) * (-1) /
                                     math.log((self.t_b_design - (t_sup+self.deltaBH)) /
                                              (self.t_b_design - self.MassH.T)))
                except:
                    warnings.warn("WARNING: logarithmic temperature difference failed in simulation!")
                    self.q_dot_hb = self.ua_hb * ((t_sup+self.deltaBH+self.MassH.T)/2 - self.t_b_design)

            else:
                # Fixed load approach

                if heating:                                     # heating or cooling
                    # no defrost
                    self.q_dot_hb = self.q_design_plc + self.q_def_corr       # TODO: Check equation!
                else:
                    # defrost
                    self.q_dot_hb = 0

    def calc_return(self):
        """
        calculates return temperature
        assumption: temperature of heat transfer system is arithmetic mean temperature of supply and return temperature
        :return: return temperature
        """
        if self.TagHydSwi:
            t_ret = self.hydraulicSwitch.T_ret_swi
        else:
            t_ret = self.MassH.T
        return t_ret

    def doStep(self, t_sup, t_ret_mea, m_w_hp, stepSize, heating, q_dot_int = 0):
        """
        step of one second:
        1) calculate current heat flows
        2) calculate new temperature of thermal masses
        3) calculates return temperature
        :param t_sup: [°C / K]
        :param m_w_hp: [kg/s]
        :param stepSize [s]
        :param t_ret_mea: measured value of return temperature [°C]
        :param heating: true for heating, false for defrost
        :param q_dot_int: internal gain heat flow directly into building mass [W]
        """
        self.hydraulicSwitch.calcFlows(m_flow_hp=m_w_hp, T_sup_hp=t_sup+self.deltaBH, T_ret_sh=self.MassH.T)
        self.q_dot_int = q_dot_int
        # calc heat flows depending on current temperatures
        self.calcHeatFlows(m_dot=m_w_hp, t_sup=t_sup, t_ret_mea=t_ret_mea, heating=heating)
        # heat flow heat pump & booster heater - heat flow H-->B
        self.MassH.qflow((self.q_dot_hp + self.q_dot_bh - self.q_dot_hb)*stepSize)
        #  calculate new return temperature
        self.t_ret = self.calc_return()

class CalcParameters:
    def __init__(self, t_a_design, t_a, q_design, PLC, t_flow_design, t_flow_plc, m_dot_H_design, constant_mflow,
                 delta_T_cond_design, c_design, dt_mean=0, dt_mean_design=0, t_b=20, boostHeat = False,
                 maxPowBooHea = 0, hydraulicSwitch = False, relHum = 0, q_def_corr=0):
        """
        Calculate parameters for one mass building model according to given parameters of a heat pump.

        :param t_a_design: design nominal outdoor temperature in °C
        :param t_a: outdoor temperature in test point
        :param q_design: nominal heating power in W
        :param c_design: design thermal capacity in J/K/W_design
        :param PLC: rel heating load in test point (0...1)
        :param t_flow_design: nominal design flow temperature in °C
        :param t_flow_plc: flow temperature in test point in °C
        :param t_b: nominal building temperature (standard value: 20 °C) in °C
        :param m_dot_H_design: design mass flow of heating system in kg/s
        :param boostHeat: if true use virtual heater
        :param maxPowBooHea: maximal power of virtual heater in W
        :param hydraulicSwitch: if true use hydraulic switch
        :param relHum: relative humidity
        :param q_def_corr: defrost correction in W
        :param constant_mflow: if true use constant mass flow
        :param delta_T_cond_design: design temperature difference in condenser
        :param dt_mean: logarithmic mean temperature difference
        :param dt_mean_design: design logarithmic mean temperature difference
        """
        self.q_design_plc = q_design*PLC
        self.t_a = t_a
        self.m_dot_H_design = m_dot_H_design
        self.relHum = relHum
        self.t_a_design = t_a_design
        self.t_b = t_b
        self.q_design = q_design
        self.PLC = PLC
        self.t_flow_design = t_flow_design
        self.t_flow_plc = t_flow_plc
        self.c_design = c_design
        self.hydraulicSwitch = hydraulicSwitch
        self.boostHeat = boostHeat
        self.maxPowBooHea = maxPowBooHea
        self.q_def_corr = q_def_corr
        self.constant_mflow = constant_mflow

        # Temperature difference in condenser
        # Mass flow in config configured
        # Difference between variable and fixed flow
        if constant_mflow:
            self.delta_T_cond = self.q_design * self.PLC / (self.m_dot_H_design * 4183)         # PLC
            self.delta_T_cond_design = self.q_design / (self.m_dot_H_design * 4183)             # Design

            t_ret = self.t_flow_plc - self.delta_T_cond                                         # PLC
            t_ret_design = self.t_flow_design - self.delta_T_cond_design                        # Design

            self.dt_mean = (self.t_flow_plc - t_ret) / math.log((self.t_b - self.t_flow_plc) / (self.t_b - t_ret))
            self.dt_mean_design = (self.t_flow_design - t_ret_design) / math.log((self.t_b - self.t_flow_design) / (self.t_b - t_ret_design))
        else:
            self.dt_mean = dt_mean
            self.dt_mean_design = dt_mean_design

            self.delta_T_cond_design = delta_T_cond_design
            self.delta_T_cond = delta_T_cond_design * self.PLC

        self.ua_hb = self.q_design * self.PLC / self.dt_mean
        self.ua_hb_design = self.q_design / self.dt_mean_design

        self.T_mean_log = self.dt_mean + self.t_b

        # --- Thermal conductivities and mean water temperature ---
        # 1) Arithmetic:
        # PLC:
        # self.ua_hb = self.q_design * self.PLC / (self.t_flow_plc - 0.5 * self.delta_T_cond - self.t_b)
        # Design:
        # self.ua_hb_design = self.q_design / (self.t_flow_design - 0.5 * delta_T_cond_design - self.t_b)
        # Mean temperature
        # self.T_mean = self.t_flow_plc - 0.5 * self.delta_T_cond

        # 2) Logarithmic temperature difference: if logarithm fails, use arithmetic calculations
        # Return temperatures
        # t_ret = self.t_flow_plc - self.delta_T_cond                 # PLC
        # t_ret_design = self.t_flow_design - delta_T_cond_design     # Design
        # PLC
        # self.ua_hb = (self.q_design * self.PLC * math.log((self.t_b - self.t_flow_plc) / (self.t_b - t_ret)) /
        #               (-1 * (t_ret - self.t_flow_plc)))
        # Design
        # self.ua_hb_design = (self.q_design * math.log((self.t_b - self.t_flow_design) / (self.t_b - t_ret_design)) /
        #                      (-1 * (t_ret_design - self.t_flow_design)))
        # Mean temperature
        # self.T_mean_log = (self.t_flow_plc - t_ret) / math.log(
        #     (self.t_b - self.t_flow_plc) / (self.t_b - t_ret)) + self.t_b

        # Initial temperature of heating system
        self.t_start_h = self.t_flow_plc - self.delta_T_cond

        # Thermal capacity of heating system
        # self.mcp_h = self.tau_h * self.ua_hb_design
        self.mcp_h = self.c_design * self.q_design
        self.tau_h = self.mcp_h / self.ua_hb
        # print("tau_h: ", self.tau_h)

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
            boostHeat=self.boostHeat,
            maxPowBooHea=self.maxPowBooHea,
            hydraulicSwitch=self.hydraulicSwitch,
            relHum=self.relHum,
            q_def_corr=self.q_def_corr,
            delta_T_cond_design=self.delta_T_cond_design,
            constant_mflow=self.constant_mflow,
            dt_mean=self.dt_mean,
            dt_mean_design=self.dt_mean_design,
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

    def set_q_def_corr(self, q_def_corr):
        """Set function for defrost correction."""
        self.q_def_corr = q_def_corr
        self.update()

    def set_mass_flow(self, constant_mflow, delta_T_cond):
        """Set function for constant/variable mass flow and temperature difference."""
        self.constant_mflow = constant_mflow
        self.delta_T_cond = delta_T_cond
        self.update()

    def createBuilding(self, dynamic_load=True):
        """Create one mass building model.

        :param dynamic_load: True for dynamic load and false for fixed load
        :return one mass building
        """
        building = OneMassBuilding(q_design_plc = self.q_design_plc, plc=self.PLC, ua_hb=self.ua_hb, mcp_h=self.mcp_h, t_a=self.t_a,
                                   t_start_h=self.t_start_h, t_flow_design=self.t_flow_plc,
                                   boostHeat=self.boostHeat, maxPowBooHea = self.maxPowBooHea,
                                   m_dot_H_design=self.m_dot_H_design, hydraulicSwitch=self.hydraulicSwitch,
                                   relHum = self.relHum, T_mean = self.T_mean_log, dynamic_load = dynamic_load,
                                   q_def_corr = self.q_def_corr, constant_mflow=self.constant_mflow)
        print(
         "Building created:"  +
         " Mass H = " + str(round(building.MassH.mcp,2)) + " ua_hb = " + str(round(building.ua_hb,2)) +
         " time constant heating system = " + str(round(building.MassH.mcp / building.ua_hb, 2)) +
         " ambient temperature = " + str(round(building.t_a, 2)) + " °C"
         " log mean temperature = " + str(round(building.T_mean, 2)) + " °C"
        )
        return building
