from thermochem.psicrometry import MoistAir
from thermochem.burcat import Elementdb
from thermochem.units import Pressure, Temperature


def test_wark():
    """
    This function runs the 10.7 example from Wark and Richard's
    Thermodynamics, Spanish translation.
    """
    db = Elementdb()
    gas = db.getmixturedata([("AIR", 1), ("H2O", 0.015)])
    ma = MoistAir(gas)
    assert ma.w == 0.0093294500500255822
    assert ma.phi(Pressure(14.7).unit('psi'),
                  Temperature(70).unit('F')) == 0.59790008408358786
    assert ma.wet_bulb_T(Pressure(14.7).unit('psi')) == 286.14757997335232
