from __future__ import absolute_import
from .constants import *


class Temperature(float):
    """
    Class that models a temperature measure with conversion utilities

    Supported units are

    * Kelvin

    * Celsius

    * Fahrenheit

    Normal instantiation is a temperature in Kelvin

    >>> T = Temperature(100)
    >>> T
    100.0

    But you can instantiate and specify if unit is Celsius or
    Fahrenheit

    >>> T = Temperature(100).unit('F')
    >>> T
    310.92777777777775

    Unit conversion is as easy as it gets.

    >>> T.C
    37.777777777777...
    >>> T.F
    99.999999999999...

    You can compute with temperatures because inherits from the float
    built-in

    >>> T1 = Temperature(200)
    >>> T2 = Temperature(0).unit('C')
    >>> round(T1+T2, 2)
    473.15

    If you don't want to use the class' attribute you can use the
    function `getattr` to get a value using the unit code.

    >>> getattr(T,'C')
    37.77777777777...
    """

    def __init__(self, data):
        self.data = float(data)

    @classmethod
    def __factory(cls, data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self, units='K'):
        """Specify temperature units, default is Kelvin.

        Unit one of 'K', 'C', or 'F' for Kelvin, Celsius, or Fahrenheit
        """
        if units == 'K':
            return self.__factory(self.data)
        elif units == 'C':
            return self.__factory(C2K(self.data))
        elif units == 'F':
            return self.__factory(F2K(self.data))
        else:
            raise ValueError("Wrong temperature input code")

    @property
    def C(self):
        """Convert temperature to Celsius"""
        return self.__factory(K2C(self.data))

    @property
    def F(self):
        """Convert temperature to Fahrenheit"""
        return self.__factory(K2F(self.data))


class Pressure(float):
    """
    Class that models a Pressure measure with conversion utilities

    Suported units are

    * Pascal (Pa)

    * Mega Pascal (MPa)

    * Bar (bar)

    * Pound per square inch (psi)

    * Atmosphere (atm)

    * Millimeters of water column (mmwc)

    * Torricelli (torr)

    Normal instantiation is pressure in Pa. How much is an athmosphere?

    >>> p = Pressure(1.0).unit('atm')
    >>> p
    101325.0
    >>> p.torr
    760.0
    >>> p.mmwc
    10285.839999999998
    >>> p.psi
    14.69594877551345
    """

    def __init__(self, data):
        self.data = float(data)

    @classmethod
    def __factory(cls, data):
        """
        This factory makes that any returned value is a Measure
        instead of a float.
        """
        return cls(data)

    def unit(self, units='Pa'):
        """Specify pressure units, default is Pascal (Pa).

        Unit one of 'Pa', 'MPa', 'bar', 'psi', 'atm', 'mmwc', 'torr'.
        """
        if units == 'Pa':
            return self.__factory(self.data)
        elif units == 'MPa':
            return self.__factory(mega * self.data)
        elif units == 'bar':
            return self.__factory(self.data * bar)
        elif units == 'psi':
            return self.__factory(self.data * psi)
        elif units == 'atm':
            return self.__factory(self.data * atm)
        elif units == 'mmwc':
            return self.__factory(self.data * (torr * 1000 / 13534))
        elif units == 'torr':
            return self.__factory(self.data * torr)
        else:
            raise ValueError("wrong pressure unit input code")

    @property
    def MPa(self):
        """Convert pressure to megapascals"""
        return self.__factory(self.data / mega)

    @property
    def bar(self):
        """Convert pressure to bars"""
        return self.__factory(self.data / bar)

    @property
    def psi(self):
        """Convert pressure to pounds per square inch (psi)"""
        return self.__factory(self.data / psi)

    @property
    def atm(self):
        """Convert pressure to atmospheres (atm)"""
        return self.__factory(self.data / atm)

    @property
    def mmwc(self):
        """Convert pressure to millimeters of water column (mmwc)"""
        return self.__factory(self.data / (torr * 1000 / 13534))

    @property
    def torr(self):
        """Convert pressure to torrs"""
        return self.__factory(self.data / torr)


HUNITS = ['si', 'kJkg', 'kcalkg', 'Btulb']


class Enthalpy(float):
    """
    Class that models an enthalpy measure with conversion utilities

    Supported units are

    * Joule per kg (default)

    * Kilojoule per kg (kJkg)

    * Kilocalorie per kg (kcalkg)

    * BTU per pound (Btulb)

    >>> h = Enthalpy(1000)
    >>> h.kJkg
    1.0
    >>> h.kcalkg
    0.2390057361376...
    >>> h.Btulb
    0.42992261392949266
    """

    def __init__(self, data):
        self.data = float(data)

    @classmethod
    def __factory(cls, data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self, units='si'):
        """Specify enthalpy units, default is joules per kg.

        Unit one of:
          'si':      joules per kg
          'kJkg':    kilojoules per kg
          'kcalkg':  kilocalories per kg
          'Btulb':   BTU per pound
        """
        if units == 'si':
            return self.__factory(self.data)
        elif units == 'kJkg':
            return self.__factory(self.data * kilo)
        elif units == 'kcalkg':
            return self.__factory(self.data * calorie * kilo)
        elif units == 'Btulb':
            return self.__factory(self.data * Btu / lb)
        raise ValueError("wrong enthalpy unit input code")

    @property
    def kJkg(self):
        """Convert enthalpy to kilojoules per kg"""
        return self.__factory(self.data / kilo)

    @property
    def kcalkg(self):
        """Convert enthalpy to kilocalories per kg"""
        return self.__factory(self.data / kilo / calorie)

    @property
    def Btulb(self):
        """Convert enthalpy to BTU per pound"""
        return self.__factory(self.data * lb / Btu)


class Length(float):
    """
    Class that models a length measure with conversion utilities

    Supported units are

    * meter (default)

    * millimeter (mm)

    * inch (inch)

    * foot (ft)

    >>> l = Length(1).unit('inch')
    >>> round(l.mm, 1)
    25.4
    >>> l.ft
    0.0833333333333...
    >>> round(l, 4)
    0.0254
    """

    def __init__(self, data):
        self.data = float(data)

    @classmethod
    def __factory(cls, data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self, units='m'):
        """Specify length units, default is meters (m).

        Unit one of 'm', 'mm', 'inch', 'ft'.
        """
        if units == 'm':
            return self.__factory(self.data)
        elif units == 'mm':
            return self.__factory(self.data * milli)
        elif units == 'inch':
            return self.__factory(self.data * inch)
        elif units == 'ft':
            return self.__factory(self.data * foot)
        else:
            raise ValueError("wrong length unit input code")

    @property
    def mm(self):
        """Convert length to millimeters"""
        return self.__factory(self.data / milli)

    @property
    def inch(self):
        """Convert length to inches"""
        return self.__factory(self.data / inch)

    @property
    def ft(self):
        """Convert length to feet"""
        return self.__factory(self.data / foot)


class Massflow(float):
    """
    Class that models a mass flow measure with conversion utilities

    Supported units are

    * kg per second (default)

    * kg per hour (kgh)

    * pounds per second (lbs)

    * pounds per hour (lbh)
    """

    def __init__(self, data):
        self.data = float(data)

    @classmethod
    def __factory(cls, data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self, units='kgs'):
        """Specify mass flow units, default is kg per second.

        Unit one of:
          'kgs': kg per second
          'kgh': kg per hour
          'lbs': pounds per second
          'lbh': pounds per hour
        """
        if units == 'kgs':
            return self.__factory(self.data)
        elif units == 'kgh':
            return self.__factory(self.data / hour)
        elif units == 'lbs':
            return self.__factory(self.data * lb)
        elif units == 'lbh':
            return self.__factory(self.data * lb / hour)
        else:
            raise ValueError("wrong massflow unit input code")

    @property
    def kgh(self):
        """Convert mass flow to kg per hour"""
        return self.__factory(self.data * hour)

    @property
    def lbs(self):
        """Convert mass flow to pounds per second"""
        return self.__factory(self.data / lb)

    @property
    def lbh(self):
        """Convert mass flow to pounds per hour"""
        return self.__factory(self.data * hour / lb)


class Massflowrate(float):
    """
    Class that models a mass flow measure with conversion utilities

    Supported units are

    * :math:`\\frac{kg}{s\ m^2}` (default)

    * :math:`\\frac{lb}{s\ ft^2}` (Btu)
    """

    def __init__(self, data):
        self.data = float(data)

    @classmethod
    def __factory(cls, data):
        """
        This factory makes that any returned value is a measure
        instead of a float.
        """
        return cls(data)

    def unit(self, units='default'):
        if units == 'default':
            return self.__factory(self.data)
        elif units == 'Btu':
            return self.__factory(self.data * lb / foot ** 2)
        else:
            raise ValueError("wrong massflow unit input code")

    @property
    def Btu(self):
        return self.__factory(self.data * foot ** 2 / lb)
