
# Load-based-testing method for heat pumps

This repository contains a simple one-mass building model for load-based testing of heat pumps.
The model is used to define the inertial behavior of the heat sink.

## Installation 

LoadBasedTesting can be installed as a package. 
In order to use this package, you can either install it via pip install (see
below) or simply download the Python files and use them in your own script. 
Installation steps are:
1.  Download or clone the repository via git: 
`git clone https://github.com/BAMresearch/bam-load-based-testing/`
2. Install the package via pip. Use conda prompt console or the terminal within pycharm:
`pip install -e <local path to git repo>`
3. If you do not need the package anymore you can deinstall it via git:
`pip uninstall bamLoadBasedTesting`

## One-mass model

The one-mass model consists of mass H, representing the heat transfer system.
The mass is characterized by a heat capacity MCp and an initial temperature $`\vartheta_\mathrm{start}`$. 

The heat output provided by the heat pump $`\dot{Q}_\mathrm{HP}`$ is delivered to mass H. $`\dot{Q}_\mathrm{HP}`$ is 
calculated based on the supply temperature $`\vartheta_\mathrm{S}`$ provided by the heat pump, the measured return
temperature of the heat pump $`\vartheta_\mathrm{ret,mea}`$ and the mass flow rate through the heat transfer system
$`\dot{m}_\mathrm{w}`$.

$`\dot{Q}_\mathrm{HP} = \dot{m}_\mathrm{w} \cdot 4183~\mathrm{J/kg/K} \cdot (\vartheta_\mathrm{S} - \vartheta_\mathrm{ret,mea})`$

Furthermore, mass H (heat transfer system) is connected to a building with a constant temperature of 
$`\vartheta_\mathrm{B}=20 \mathrm{°C}`$ for heating or $`\vartheta_\mathrm{B}=27 \mathrm{°C}`$ for cooling. 
For the heat flow rate between the heat transfer system and the building ($`\dot{Q}_\mathrm{HB}`$), there are two approaches.
1. Dynamic load approach: 
Depending on the temperatures of the mass H and the supply temperature $`\vartheta_\mathrm{S}`$ provided by the heat 
pump, the heat flow is determined by the thermal conductivity $`UA_\mathrm{HB}`$ between the heat transfer system and 
the building, and a logarithmic temperature difference.
>> $`\dot{Q}_\mathrm{HB} =  UA_\mathrm{HB} \frac{\vartheta_\mathrm{S} - \vartheta_\mathrm{H}}{\ln(\frac{\vartheta_\mathrm{B} - \vartheta_\mathrm{S}}{\vartheta_\mathrm{B} - \vartheta_\mathrm{H}})}`$

2. Fixed load approach: 
The heat flow rate $`\dot{Q}_\mathrm{HB}`$ is fixed and corresponds to the design heat flow rate of the part load condition specified for the building model ($`P_\mathrm{designh} \cdot pl(T)`$, see EN 14825).
There is an option to add a defrost correction $`\dot{Q}_\mathrm{def,corr}`$. During a defrost it is $`\dot{Q}_\mathrm{HB}=0`$.
>> $`\dot{Q}_\mathrm{HB} = P_\mathrm{designh} \cdot pl(T) + \dot{Q}_\mathrm{def,corr}`$


The associated energy balances of the subsystems determine the temperature changes of the mass H. 
$`C_\mathrm{H}`$ is the thermal capacity of the heat transfer system.

$`\frac{\mathrm{d}\vartheta_\mathrm{H}}{\mathrm{d}t} = \frac{\dot{Q}_\mathrm{HP} - \dot{Q}_\mathrm{HB}}{C_\mathrm{H}}`$

With this Equation the temperature of the heating system $`\vartheta_\mathrm{H}`$ can be recalculated.
This temperature is then used as the new return temperature $`\vartheta_\mathrm{ret,calc}`$ for the heat pump.

$`\vartheta_\mathrm{ret,calc} = \vartheta_\mathrm{H}`$

This model can be used for heat pumps with fixed and variable (water) mass flow rate in the heat transfer system.

## Implementation in python

### The script oneMassBuilding()
This script contains the main classes for the calculation of the above mentioned equations. 
Please find a short description below. For further information please look at the documentation in the script
#### The class OneMassBuilding
The building model is defined in the class "OneMassBuilding" in "oneMassModel.py" and consists of one object of the 
class "ThermalMass" (mass with capacity and temperature) that represents the heat transfer system.
The "OneMassBuilding" has two functions:
1. "calcHeatFlows()": This function is used to calculate the above mentioned heat flow rates $`\dot{Q}_\mathrm{HB}`$ and $`\dot{Q}_\mathrm{HP}`$.
2. "doStep()": This function is used to first uses "calcHeatFlows()" and then calculates the above mentioned energy balance to calculate the new return temperature of the heat pump.

#### The class CalcParameters
To configure a new building model, the class "CalcParameters" can be used (also in defined in "oneMassModel.py"). 
A building model can be configured for a heat pump with constant mass flow or a constant temperature difference 
(t_flow - t_ret; variable flow). In both cases, the nominal heating power and the nominal flow temperature of the heat 
pump must be specified. Additionally, the thermal design capacity of the mass as well as the ambient temperature are required.
Also conditions for the specific part load (e.g. PLC-A) have to be specified.
The calculations in this class mainly happen in two functions:
1. In the "__init__()" function, the temperature difference of the water in the condenser and the mean temperatures for the one mass model are parameterized.
Furthermore, the thermal conductivity between heat transfer system and building, the initial return temperature and the thermal capacity of the heat transfer system are calculated.
2. The function "createBuilding()" then determines all necessary parameters and instantiates the building model ("OneMassBuilding").

### Scripts to apply the one mass model
To use the one mass model, the following scripts should be used in the following order. 
More information on how to use the scripts is documented directly in the scripts.

1. First, the building models need to be parameterized. 
This can be done as shown in "BuildingModels/OneMassModelConfig.py".
The script has several examples for different applications (heating/cooling, medium/low temperature).
You can adjust this script for your use case or simply add new scripts in the directory BuildingModels.
In the last case, please make sure to adjust the import statements of the building models for the following two scripts.
2. Parameterized models can be tested by using the script "testModelSim.py" in the "Example" folder. 
3. Finally, building models can be used for experimental testing on the test bench with the script "Example/modelOnTestBench.py". 
Further instructions are documented within the script.