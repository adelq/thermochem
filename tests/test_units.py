from thermochem.units import Pressure, Temperature
from nose.tools import assert_equals


def test_temperature():
    assert_equals(Temperature(273.15).unit('K'), Temperature(0).unit('C'))


def test_pressure():
    assert_equals(Pressure(760).unit('torr'), Pressure(1).unit('atm'))
