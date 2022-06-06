from thermochem.units import Pressure, Temperature


def test_temperature():
    assert Temperature(273.15).unit('K') == Temperature(0).unit('C')


def test_pressure():
    assert Pressure(760).unit('torr') == Pressure(1).unit('atm')
