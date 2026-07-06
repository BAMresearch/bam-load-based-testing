
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

## One-mass model

The one-mass model consists of mass H, representing the heat transfer system.
The mass is characterized by a heat capacity MCp and an initial temperature $`\vartheta_\mathrm{start}`$. 

The heat output provided by the heat pump is delivered to mass H. Mass H is connected to a building with a constant temperature of $`\vartheta_\mathrm{B}=20 \mathrm{°C}`$.
Depending on the temperatures of the mass H and the supply temperature $`\vartheta_\mathrm{S}`$ provided by the heat pump, the heat flow is determined by the thermal conductivity $`UA_\mathrm{HB}`$ between the heat transfer system and the building:

$`\dot{Q}_\mathrm{HB} =  UA_\mathrm{HB} \frac{\vartheta_\mathrm{S} - \vartheta_\mathrm{H}}{\ln(\frac{\vartheta_\mathrm{B} - \vartheta_\mathrm{S}}{\vartheta_\mathrm{B} - \vartheta_\mathrm{H}})}`$


The associated energy balances of the subsystems determine the temperature changes of the mass H:

$`\frac{\mathrm{d}\vartheta_\mathrm{H}}{\mathrm{d}t} = \frac{\dot{Q}_\mathrm{HP} - \dot{Q}_\mathrm{HB}}{C_\mathrm{H}}`$

The return temperature $`\vartheta_\mathrm{R}`$ of the heat pump corresponds to the temperature $`\vartheta_\mathrm{H}`$ of mass H.

## Implementation in python

The building model is defined in the class "OneMassBuilding" in "oneMassModel.py" and consists of one object of the class "ThermalMass".

To configure a new building model, the class "CalcParameters" can be used. A building model can be configured for a heat pump with constant mass flow or a constant temperature difference (t_flow - t_ret). In both cases, the nominal heating power and the nominal flow temperature of the heat pump must be specified.
Additionally, the thermal design capacity of the mass as well as the ambient temperature are required.
The function "createBuilding" determines all necessary parameters of the building model.

Building models can be parameterized as shown in "BuildingModels/OneMassModelConfig.py".

Models can be tested by using the script "testModelSim.py" in the "Example" folder.

Building models can be used for experimental testing on the test bench with the script "Example/modelOnTestBench.py". Further instructions are documented within the script.