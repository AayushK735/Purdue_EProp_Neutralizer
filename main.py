import math
import matplotlib.pyplot as plt
class Filament:
    def __init__(self, name, workFunction, workingTemp, dCoeff, diameter, cost, costLength, emissivity,
                 specHeatCapacity, density, resistivity):
        self.name = name
        self.workFunction = workFunction
        self.workingTemp = workingTemp  # K
        self.dCoeff = dCoeff
        self.diameter = diameter  # cm
        self.cost = cost  # $
        self.costLength = costLength  # m
        self.emissivity = emissivity
        self.specHeatCapacity = specHeatCapacity  # J/gK
        self.density = density  # g/cm^3
        self.resistivity = resistivity #micro-ohms-cm


# All Cost, Diameter, CostLength from [5]
tungsten = Filament("Tungsten", 4.55, 2500, 70, .048, 56.85, 3.048, .45, .134, 19.25, 74.70)  # [1] [2] [8] [9]

# tantalum = Filament("tantalum", 4.1, 2400, 37, .076, 25.83, .0254, .27, 0, 0) #Estimated E
thorTungsten = Filament("Thoriated Tungsten", 2.63, 1900, 3, .05, 105.58, .3, .4, .134, 18.8, 54.93)  # [2] [3] [7] [8] [9] For many properties, I'm assuming they're simialr to pure tungsten

# moly = Filament("Molybdenum", 4.2, 1900, 50, .041, 25.65, 3.048, None, None, None)

filamentList = [tungsten, thorTungsten]

k = 1.380649 * 10 ** -23
e_charge = 1.60217663 * 10 ** -19

avgDischargeCurrent = .78
marginForCurrent = 1.5 #50%
breathingCorrection = 2
targetEmissionCurrent = avgDischargeCurrent * marginForCurrent * breathingCorrection



def temp(fil: Filament, area: float):
    sigma = 5.67 * 10 ** -8
    e = fil.emissivity
    Q = sigma * area * fil.workingTemp ** 4 * e
    Q = Q/2 #Only half the radiated heat will hit the thruster, the other half will be facing the opposing way
    # Inverse square Law
    areaThruster = 64/10000 #64 cm^2 est
    standOffLength = 0.042164 # m
    Q = Q * areaThruster/(4 * math.pi * standOffLength**2)
    t = 60 # time

    areaShuntPlate = .0049 #Square meters
    thicknessShuntPlate = .005 #meters
    outerDiameterDischarge = .045 #meters
    dischargeEstArea = math.pi * (outerDiameterDischarge/2)**2
    
    finalVolume = (areaShuntPlate - dischargeEstArea) * thicknessShuntPlate
    densityCC = 7.75 * 1000000 #https://www.matweb.com/search/DataSheet.aspx?MatGUID=034970339dd14349a8297d2c83134649&ckck=1 Going on the under


    m = densityCC*finalVolume  # mass of thruster (Or Material) g

    c = 0.45  # specific heat capacity (Of Material) J/g C
    #https://www.matweb.com/search/DataSheet.aspx?MatGUID=034970339dd14349a8297d2c83134649&ckck=1 Going on the under




    #Distance is ANGLE! 1.66 inch away

    # Need to get both of these from whoever's part
    # Q = mc T

    #Perhaps discharge channel doesn't matter since its ceramic
    # I need to find area of the total surface and divide it by shunt plate and discharge channel, and then divide the Q into fractions and find the delta T of each


    deltaT = (Q * t) / (m * c)

    return deltaT

def temp2(fil: Filament, filLength: float, area: float):

    #https://assets.omega.com/pdf/tables_and_graphs/emissivity-table.pdf
    #At steady state, emmisvity is equal to absoroptivity due to kirchhoff's law of thermal radiation
    PtotalWire = powerNeeded(fil, filLength, area)

    steelAbsorptivity = 0.11
    Prad = PtotalWire * (.265/(2*math.pi)) * steelAbsorptivity
    shuntArea = (11.25*190)/1000000
    sigma = 5.67 * 10 ** -8
    steelEmissivity = 0.11#.21
    T = ((Prad)/(shuntArea*sigma*steelEmissivity))**0.25
    return T

def temp3(fil: Filament, filLength: float, area: float):
        # https://assets.omega.com/pdf/tables_and_graphs/emissivity-table.pdf
        # At steady state, emmisvity is equal to absoroptivity due to kirchhoff's law of thermal radiation
        PtotalWire = powerNeeded(fil, filLength, area)

        steelAbsorptivity = 0.11
        Prad = PtotalWire * (.208 / (2 * math.pi)) * steelAbsorptivity
        shuntArea = (((8.75 * 216))+1500) / 1000000
        sigma = 5.67 * 10 ** -8
        steelEmissivity = 0.11  # .21
        T = ((Prad) / (shuntArea * sigma * steelEmissivity)) ** 0.25
        return T

def tempConnector():
    thermalCond = 300 #lower end is 150 #Could be higher or lower
    estContactArea = (((2 * math.pi * (0.5/2))/1000) * .00508) * .5 #.2 Inch of length, lets assume all around but thats over shooting.
    thicknessOfConnector = .09/39.37

 #   Pcond = thermalCond * estContactArea * ((1900-293)/thicknessOfConnector)
   # Pcond = 100
    sigma = 5.67 * 10 ** -8
    becuEmissivity = 0.72#TEMP
    connectorArea = 0.00013161264
  #  T = ((Pcond) / (connectorArea * sigma * becuEmissivity)) ** 0.25
    LHS = (thermalCond*estContactArea)/(connectorArea*sigma*becuEmissivity*thicknessOfConnector)
    return LHS

def powerNeeded(fil: Filament, length, area: float):
    # Q = mc T
    #mass = fil.density * length * ((fil.diameter / 2) ** 2) * math.pi
    #c = fil.specHeatCapacity
    #T = fil.workingTemp - 293.15
    #initQ = mass * c * T
    #Nick said this isn't really necessary, focus on radiative heat

    # Using radiative heat
    sigma = 5.67 * 10 ** -8
    e = fil.emissivity
    Q = sigma * area * fil.workingTemp ** 4 * e

    P_rad = area * e * sigma * fil.workingTemp ** 4
    #Power lost is the power need to put into it

    return P_rad


# Basic Equation
print("Info:")
print("Circumference of Thruster is ~15.708 cm")
print(f"Emission Current Needed: {targetEmissionCurrent} A")
for fil in filamentList:
    print("-----------------")
    chosenFilament = fil
    print(chosenFilament.name)
  #  J = chosenFilament.dCoeff * (chosenFilament.workingTemp ** 2) * (
      #          math.e ** ((-e_charge * chosenFilament.workFunction) / (k * chosenFilament.workingTemp)))

    J = chosenFilament.dCoeff * (chosenFilament.workingTemp ** 2) * (
                 math.exp (((-e_charge * chosenFilament.workFunction) / (k * chosenFilament.workingTemp))))
    print(f"Electron Emission Density: {J:.3f} A/cm^2")
    print(f"Temperature Needed for Filament: {chosenFilament.workingTemp - 273.15} C")
    surfaceAreaNeeded = targetEmissionCurrent / J #cm^2

    length = surfaceAreaNeeded / (2 * math.pi * (chosenFilament.diameter / 2)) #cm

    # SA = Circumference *  Length
    print(f"Length (cm) {length:.3f}")
    baseCost = (chosenFilament.cost) / (chosenFilament.costLength * 100)  # $/cm
    print(f"Cost Per Cm: {baseCost} ")
    print(f"Cost: ${baseCost * length:.2f} for this length")

    print("Experimental Info:")
    #print(f"Temp After 60 Seconds: {temp(fil, surfaceAreaNeeded / 10000)}")
    power = powerNeeded(fil, length, surfaceAreaNeeded / 10000)
    print(f"Energy Radiated: {power:.3f} W")
    print(f"Temp2: {temp2(fil, length, surfaceAreaNeeded / 10000)}")
    print(f"Temp3: {temp3(fil, length, surfaceAreaNeeded / 10000)}")

    #Calculate Resistance:
    uOmega = (fil.resistivity * length) / (math.pi * ((chosenFilament.diameter / 2)**2))
    omega = uOmega/1000000 #Micro to base
    print(f"Omega: {omega:.3f} R")
    amps = (power/omega)**0.5
    volts = amps * omega
    print(f"Voltage: {volts:.3f} V. Amps: {amps:.3f} A.")


print("Working with a set length with Thor Tungsten")

expTemp = 1950
J = thorTungsten.dCoeff * (expTemp ** 2) * (
    math.exp(((-e_charge * thorTungsten.workFunction) / (k * expTemp))))
SA =  (2 * math.pi * (chosenFilament.diameter / 2)) * 21.6 #cm^2

emissionCurrent = J * SA

print(f"E Current: {emissionCurrent} ")

print(f"Thermal Cond: {tempConnector()}")



fil = thorTungsten
testing_list = list(range(1,15))

resistivty_coeffs = [0.0307282, -5.46184] #https://www.desmos.com/calculator/gj2wpkrh0c This is resisitvity as a function of temperature 
print("---------")
# Method One
last_temp = 500 
first_res = True
for a in testing_list:
     length = 150/10
     amps = float(a)
     print(f"Current: {amps}")
     calc_resistivity = resistivty_coeffs[0] * last_temp + resistivty_coeffs[1]
     if first_res:
          calc_resistivity = 10.56
          first_res = False
     uOmega = (calc_resistivity * length) / (math.pi * ((chosenFilament.diameter / 2)**2))
     omega = uOmega/1000000 #Micro to base
     print(f"Resistivity: {calc_resistivity}")
     power = amps**2 * omega
     print(f"Power: {power}")
     sigma = 5.67 * 10 ** -8
     area = (length * math.pi * chosenFilament.diameter)
     area_m = area/(10**4)

     T = ((power)/(area_m*sigma*fil.emissivity))**0.25
     last_temp = T
     print(f"Fil Temp: {T}")

     J = chosenFilament.dCoeff * (T ** 2) * (
                 math.exp (((-e_charge * chosenFilament.workFunction) / (k * T))))
     estEmissionCurrent = J * area
     print(f"Est Eimission Current: {estEmissionCurrent}")
     print("---------")

# Method Two
x_vals = []
y_vals = []
for a in testing_list:
     length = 150/10 # cm
     amps = float(a)
     print(f"Current: {amps}")

     T_guess = 273
     sigma = 5.67 * 10 ** -8
     
     for _ in range(10000):
          calc_resistivity = resistivty_coeffs[0] * T_guess + resistivty_coeffs[1]
          uOmega = (calc_resistivity * length) / (math.pi * ((chosenFilament.diameter / 2)**2))
          omega = uOmega/1000000 #Micro to base
          #print(f"Resistivity: {calc_resistivity}")
          power = amps**2 * omega
          #print(f"Power: {power}")
          area = (length * math.pi * chosenFilament.diameter)
          area_m = area/(10**4)
          T_new = (((power)/(area_m*sigma*fil.emissivity)))**0.25 # Maybe add T_Inf

          T_guess = T_new
     print(f"Power: {power}")
     print(f"T_guess : {T_guess}")
     print("---------")
     x_vals.append(a)
     y_vals.append(power)

     J = chosenFilament.dCoeff * (T ** 2) * (
                 math.exp (((-e_charge * chosenFilament.workFunction) / (k * T))))
     estEmissionCurrent = J * area
     print(f"Est Eimission Current: {estEmissionCurrent}")

# To Do:

plt.plot(x_vals, y_vals)
plt.show()


#Consider gauge of wires



# How much current PPU


# Input
# Material
# Required Emission current

# output
# Wire Length
# Filament V and I, taking into account resistivty. Can only control one of two parameters. Estimate the voltage. P is a function of temp


# References:
# [1] https://www.sciencedirect.com/science/article/abs/pii/S0042207X23000349#:~:text=The%20results%20show%20that%20the,after%20T%20exceeds%202700%20K.
# [2] https://books.google.com/books?id=lTUNWOR_cDgC&pg=PA345#v=onepage&q&f=false
# [3] https://www.researchgate.net/publication/350937327_Thermionic_electron_gun_design_and_prototyping#pf3
# [4] https://simion.com/definition/richardson_dushman.html#:~:text=The%20Richardson%2DDushman%20equation%20relates,emission%20(mA/mm2)
# [5] Prices: https://electrontubestore.com/item/2830
# [6] https://www.omega.co.uk/literature/transactions/volume1/emissivitya.html
# [7]# Density: https://expressweldcare.co.uk/wp-content/uploads/2024/04/Super-6-2-Thoriated-Tungsten-Electrodes-Red-Datasheet.pdf?srsltid=AfmBOopB0xuF4sq0AQa_1ANvYrfF8sydO0M-a9qfOsEizmni8J6sJ1wt
# [8] https://hypertextbook.com/facts/2004/DeannaStewart.shtml#:~:text=Tungsten%20is%20a%20metallic%20element,temperature%20increases%2C%20also%20does%20resistivity.
# [9] https://www.desmos.com/calculator/wjq05doekw