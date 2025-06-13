"""This model is used to calculate the return flow of a building according to the compensation load method
in project EBC0955_DBU_Testmethoden_KAP_GES
@author: Stephan Göbel, date: 2023-01"""
import warnings


class ThermalMass:
    def __init__(self, mcp, T_start):
        """
        Thermal mass must have initial temperature
        :param mcp: heat capacity [J/K]
        :param T_start: initial temperature [°C / K]
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


class BypassValve:
    def __init__(self, m_flow_design):
        """
        Virtual bypass valve
        :param m_flow_design:
        """
        self.m_flow_design = m_flow_design
        self.m_flow_sh = 0
        self.m_flow_byp = 0
        self.T_ret_byp = 0


    def calcFlows(self, m_flow_hp, T_sup_hp, T_ret_sh):
        """
        Calculates mass flows and temperatures behind bypass valve
        :param m_flow_hp:
        :param T_sup_hp:
        :param T_ret_sh:
        :return:
        """
        if m_flow_hp <= self.m_flow_design:
            self.m_flow_sh = m_flow_hp
        else:
            self.m_flow_sh = self.m_flow_design

        self.m_flow_byp = m_flow_hp-self.m_flow_sh
        if m_flow_hp == 0:
            self.T_ret_byp = T_ret_sh
        else:
            self.T_ret_byp = (T_ret_sh*self.m_flow_sh + T_sup_hp * self.m_flow_byp)/m_flow_hp


class HydraulicSwitch:
    def __init__(self, m_flow_design):
        """
        Virtual bypass valve
        :param m_flow_design:
        """
        self.m_flow_design = m_flow_design
        self.m_flow_sh = 0
        self.m_flow_swi = 0
        self.T_ret_swi = 0
        self.T_sup_swi = 0

    def calcFlows(self, m_flow_hp, T_sup_hp, T_ret_sh):
        """
        Calculates mass flows and temperatures behind hydraulic switch valve
        :param m_flow_hp:
        :param T_sup_hp:
        :param T_ret_sh:
        :return:
        """
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




class TwoMassBuilding:
    def __init__(self, ua_hb, ua_ba, mcp_h,  mcp_b, t_a, t_start_h, t_flow_design, m_dot_H_design, t_start_b=20,
                 boostHeat = False, maxPowBooHea = 0, hydraulicSwitch = False, virtualBypass = False, relHum = 0):
        """
        Init function, use either °C or K but not use both
        :param ua_hb: thermal conductivity [W/K] between transfer system (H) and Building (B)
        :param ua_ba: thermal conductivity [W/K] between building and environment
        :param mcp_h: heat capacity transfer system [J/kg K]
        :param t_start_h: initial temperature transfer system (H) [°C / K]
        :param mcp_b: heat capacity building [J/ kg K]
        :param t_start_b: initial temperature building [°C / K]
        :param t_a: ambient temperature [°C / K]
        """
        self.MassH = ThermalMass(mcp_h, t_start_h)
        self.MassB = ThermalMass(mcp_b, t_start_b)
        self.virtualBypass = BypassValve(m_flow_design = m_dot_H_design)
        self.hydraulicSwitch = HydraulicSwitch(m_flow_design=m_dot_H_design)
        self.ua_hb = ua_hb
        self.ua_ba = ua_ba
        self.t_a = t_a
        self.relHum = relHum
        self.boostHeat = boostHeat
        self.q_dot_hp = 0
        self.q_dot_hb = 0
        self.q_dot_ba = 0
        self.q_dot_int = 0
        self.q_dot_bh = 0
        self.t_ret = t_start_h
        self.t_flow_design = t_flow_design
        self.maxPowBooHea = maxPowBooHea
        self.TagBypass = virtualBypass
        self.TagHydSwi = hydraulicSwitch

    def calcHeatFlows(self, m_dot, t_sup, t_ret_mea):
        """
        Calculates current heat flows between heat pump -- transfer system; transfer system -- building and
        building -- environment
        :param m_dot: measured value of mass flow [kg/s]
        :param t_sup: measured value of supply temperature [°C]
        :param t_ret_mea: measured value of return temperature [°C]
        """
        if self.boostHeat and t_sup < self.t_flow_design:
            self.q_dot_bh = m_dot*4183*(self.t_flow_design-t_sup)
            if self.q_dot_bh > self.maxPowBooHea:
                self.q_dot_bh = self.maxPowBooHea
                deltaT_bh = (self.q_dot_bh / (m_dot * 4183))
            else:
                deltaT_bh = self.t_flow_design - t_sup
        else:
            self.q_dot_bh = 0
            deltaT_bh = 0


        self.q_dot_hp = m_dot*4183*(t_sup-t_ret_mea)
        # if self.TagHydSwi:  # if hydraulic switch is active, use temperature behind switch as input
        #     self.q_dot_hb = self.ua_hb * ((self.hydraulicSwitch.T_sup_swi + deltaT_bh + self.MassH.T) / 2 - self.MassB.T)
        # else:
        #     self.q_dot_hb = self.ua_hb * ((t_sup+deltaT_bh+self.MassH.T)/2 - self.MassB.T)
        self.q_dot_hb = self.ua_ba * (self.MassB.T - self.t_a)
        self.q_dot_ba = self.q_dot_hb


    def calc_return(self, t_sup):
        """
        calculates return temperature
        assumption: temperature of heat transfer system is arithmetic mean temperature of supply and return temperature
        :param t_sup: current supply temperature
        :return: return temperature
        """
        if self.TagHydSwi:
            t_ret = self.hydraulicSwitch.T_ret_swi
        elif self.TagBypass:
            t_ret = self.virtualBypass.T_ret_byp
        else:
            t_ret = self.MassH.T
        return t_ret

    def doStep(self, t_sup, t_ret_mea, m_w_hp, stepSize, q_dot_int = 0):
        """
        step of one second:
        1) calculate current heat flows
        2) calculate new temperature of thermal masses
        3) calculates return temperature
        :param t_sup: [°C / K]
        :param m_w_hp: [kg/s]
        :param stepSize [s]
        :param t_ret_mea: measured value of return temperature [°C]
        :param q_dot_int: internal gain heat flow directly into building mass [W]
        :param boostHeat: virtual booster heater that increases temperature to set temperature
        """
        self.virtualBypass.calcFlows(m_flow_hp=m_w_hp, T_sup_hp=t_sup, T_ret_sh=self.MassH.T)
        self.hydraulicSwitch.calcFlows(m_flow_hp=m_w_hp, T_sup_hp=t_sup, T_ret_sh=self.MassH.T)
        self.q_dot_int = q_dot_int
        # calc heat flows depending on current temperatures
        self.calcHeatFlows(m_dot=m_w_hp, t_sup=t_sup, t_ret_mea=t_ret_mea)
        # heat flow heat pump & booster heater - heat flow H-->B
        self.MassH.qflow((self.q_dot_hp + self.q_dot_bh - self.q_dot_hb)*stepSize)
        # heat flow H-->B - heat flow B-->A + heat flow internal gain
        self.MassB.qflow((self.q_dot_hb - self.q_dot_ba + self.q_dot_int)*stepSize)
        #  calculate new return temperature
        self.t_ret = self.calc_return(t_sup)

class CalcParameters:
    def __init__(self, t_a_design, t_a, q_design, PLC, t_flow_design, t_flow_plc, m_dot_H_design, delta_T_cond=8, const_flow=True,  tau_b=55E6/263,
                 tau_h=505E3/258, t_b=20, boostHeat = False, maxPowBooHea = 0, hydraulicSwitch = False, virtualBypass = False, relHum = 0):
        """
        Calculate paramters for two mass building model according to given parameters of a heat pump.
        Either a mass flow or a temperature difference on condenser has to be provided.
        @param t_a_design: design nominal outdoor temperature [°C]
        @param t_a: outdoor temperature in test point
        @param q_design: nominal heating power  [W]
        @param PLC: rel heating load in test point (0...1)
        @param t_flow_design: nominal design flow temperature [°C]
        @param t_flow_plc: flow temperature in test point (°C)
        @param t_b: nominal building temperature (standard value: 20 °C) [°C]
        @param m_dot_H_design: design mass flow of heating system used if const_flow = True
        @param delta_T_cond: temperature difference t_flow-t_ret, if no constant mass flow
        @param const_flow: True/False calculate parameters with given mass flow (True) or given temperature difference (False)
        @param tau_b: time constant of building in design point (s)
        @param tau_h: time constant of heating system in design point (s)
        """
        self.t_a = t_a
        self.relHum = relHum
        self.t_a_design=t_a_design
        self.t_b = t_b
        self.q_design = q_design
        self.PLC = PLC
        self.t_flow_design = t_flow_design
        self.t_flow_plc =t_flow_plc
        self.const_flow = const_flow
        self.tau_b = tau_b
        self.tau_h = tau_h
        self.virtualBypass = virtualBypass
        self.hydraulicSwitch = hydraulicSwitch
        self.m_dot_H_design = m_dot_H_design
        if const_flow:
            self.delta_T_cond=self.q_design*self.PLC/(self.m_dot_H_design*4183)
            delta_T_cond_design = self.q_design / (self.m_dot_H_design * 4183)
        else:
            self.delta_T_cond=delta_T_cond
            delta_T_cond_design = delta_T_cond
        self.ua_ba = self.q_design*self.PLC / (self.t_b - self.t_a)
        self.ua_hb = self.q_design*self.PLC / (self.t_flow_plc - 0.5*self.delta_T_cond - self.t_b)
        self.ua_ba_design = self.q_design / (self.t_b - self.t_a_design)
        self.ua_hb_design = self.q_design / (self.t_flow_design - 0.5*delta_T_cond_design - self.t_b)
        self.t_start_h = self.t_flow_plc - self.delta_T_cond
        self.mcp_b = self.tau_b * self.ua_ba_design
        self.mcp_h = self.tau_h * self.ua_hb_design
        self.boostHeat = boostHeat
        self.maxPowBooHea = maxPowBooHea

    def createBuilding(self):
        building = TwoMassBuilding(ua_hb=self.ua_hb, ua_ba=self.ua_ba, mcp_h=self.mcp_h, mcp_b=self.mcp_b, t_a=self.t_a,
                                   t_start_h=self.t_start_h, t_start_b=self.t_b, t_flow_design=self.t_flow_plc,
                                   boostHeat=self.boostHeat, maxPowBooHea = self.maxPowBooHea,
                                   m_dot_H_design=self.m_dot_H_design, hydraulicSwitch=self.hydraulicSwitch, virtualBypass=self.virtualBypass, relHum = self.relHum)
        print(
         "Building created: Mass B = " + str(round(building.MassB.mcp,2)) + " ua_ba = " + str(round(building.ua_ba,2)) +
         " Mass H = " + str(round(building.MassH.mcp,2)) + " ua_hb = " + str(round(building.ua_hb,2)) +
         " time constant building = " + str(round(building.MassB.mcp/building.ua_ba, 2)) +
         " time constant heating system = " + str(round(building.MassH.mcp / building.ua_hb, 2))
        )
        if self.hydraulicSwitch == True and self.virtualBypass == True:
            warnings.warn('Hydraulic switch and bypass valve = true, hydraulic switch is used!')
        return building
