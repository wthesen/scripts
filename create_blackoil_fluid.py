'''
    PIPESIM Python Toolkit
    Example: Create a black oil fluid

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from sixgill.pipesim import Model
from sixgill.definitions import ModelComponents, Parameters, Constants
import tempfile

def query_API_and_DOD(model):
    print("API: {}".format(model.get_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.API)))
    print("DOD: {}".format(model.get_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.DEADOILDENSITY)))

# Open the model
filename = tempfile.gettempdir() + "/NewBlackoilModel.pips"
print("Opening model '{}'".format(filename))
model = Model.new(filename, overwrite=True)

print ("Create black oil fluid BK111...")
model.add(ModelComponents.BLACKOILFLUID, "BK111")

with model.batch_update():
    # set the basic black oil properties
    print ("Set black oil properties...")
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.GOR, value=200)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.WATERCUT, value=5)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.GASSPECIFICGRAVITY, value=0.7)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.WATERSPECIFICGRAVITY, value=1.05)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.FRACTIONCO2, value=0.05)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.FRACTIONH2S, value=0.001)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.FRACTIONN2, value=0.1)
    
    # set the viscosity properties
    print ("Set black oil viscosity properties...")
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.UNDERSATURATEDOILVISCOSITYCORR, value=Constants.UndersaturatedOilViscosityCorrelation.VASQUEZANDBEGGS)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.LIVEOILVISCOSITYCORR, value=Constants.LiveOilViscCorrelation.ELSHARKAWY)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.DEADOILVISCOSITYCORR, value=Constants.DeadOilViscosityCorrelation.ELSHARKAWY)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.DEADOILDENSITY, value=125)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.DEADOILTEMPERATURE1, value=190)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.DEADOILTEMPERATURE2, value=70)

    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.LIQUIDVISCOSITYCALC, value=Constants.EmulsionViscosityMethod.RICHARDSON)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.RICHARDSONKOIW, value=3.9)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.RICHARDSONKWIO, value=6.7)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.USERWATERCUTCUTOFF, value=65)

    # set the calibration data
    print ("Set black oil calibration data...")
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.ABOVEBBPTYPE, value=Constants.OilCalibrationType.OFVF)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.ABOVEBBPOFVF_PRESSURE, value=1000)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.ABOVEBBPOFVF_TEMPERATURE, value=150)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.ABOVEBBPOFVF_VALUE, value=0.9)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.ABOVEBBPDENSITY_PRESSURE, value=1000)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.ABOVEBBPDENSITY_TEMPERATURE, value=150)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.ABOVEBBPDENSITY_VALUE, value=200)

    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.SOLUTIONGAS, value=Constants.BlackOilCalibrationSolutionGas.VASQUEZANDBEGGS)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BUBBLEPOINTSATGAS_PRESSURE, value=2424)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BUBBLEPOINTSATGAS_TEMPERATURE, value=250)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BUBBLEPOINTSATGAS_VALUE, value=202.63)

    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPTYPE, value=Constants.OilCalibrationType.DENSITY)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.OILFVFCORRELATION, value=Constants.OilFVFCorrelation.STANDING)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPDENSITY_PRESSURE, value=1600)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPDENSITY_TEMPERATURE, value=250)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPDENSITY_VALUE, value=201)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPOFVF_PRESSURE, value=1600)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPOFVF_TEMPERATURE, value=250)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPOFVF_VALUE, value=0.95)

    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.LIVEOILVISCCORRELATION, value=Constants.LiveOilViscosityCorrelation.CHEWANDCONNALY)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPLIVEOILVISCOSITY_PRESSURE, value=1600)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPLIVEOILVISCOSITY_TEMPERATURE, value=250)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPLIVEOILVISCOSITY_VALUE, value=38)

    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.GASVISCCORRELATION, value=Constants.GasViscCorrelation.LEEETAL)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPGASVISCOSITY_PRESSURE, value=1600)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPGASVISCOSITY_TEMPERATURE, value=250)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPGASVISCOSITY_VALUE, value=0.06)

    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.GASCOMPRESSCORRELATION, value=Constants.GasCompressCorrelation.ROBINSONETAL)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPGASZ_PRESSURE, value=1600)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPGASZ_TEMPERATURE, value=250)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.SinglePointCalibration.BELOWBBPGASZ_VALUE, value=0.945)

    # set the thermal data
    print ("Set black oil thermal data...")
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.ThermalData.GASHEATCAPACITY, value=0.50)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.ThermalData.GASCONDUCTIVITY, value=0.02)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.ThermalData.OILHEATCAPACITY, value=0.40)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.ThermalData.OILCONDUCTIVITY, value=0.08)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.ThermalData.WATERHEATCAPACITY, value=1.01)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.ThermalData.WATERCONDUCTIVITY, value=0.36)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.ThermalData.ENTHALPYCALCMETHOD, value=Constants.EnthalpyCalcMethod.METHOD2009)
    model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.ThermalData.LATENTHEATOFVAPORIZATION, value=141)

# set API 
print("Original values")
query_API_and_DOD(model)

print("Set API to 21")
model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.USEDEADOILDENSITY, value=False)
model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.API, value=21)
query_API_and_DOD(model)

# set dead oil density
print("Set dead oil density to 55")
model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.USEDEADOILDENSITY, value=True)
model.set_value(BlackOilFluid="BK111", parameter=Parameters.BlackOilFluid.DEADOILDENSITY, value=55)
query_API_and_DOD(model)

print("Saving model as " + filename)
model.save()

model.close()
