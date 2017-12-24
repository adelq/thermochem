Thermochem
==========

.. image:: https://travis-ci.org/adelq/thermochem.svg?branch=master
    :target: https://travis-ci.org/adelq/thermochem

.. image:: https://img.shields.io/pypi/v/thermochem.svg?maxAge=2592000?style=plastic
    :target: https://pypi.python.org/pypi/thermochem

.. image:: https://readthedocs.org/projects/thermochem/badge/?version=latest
   :target: http://thermochem.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Thermochem is a package with some useful modules for Thermodynamics
and Thermochemistry. The following tools are provided:

-  IAPWS data and functions to compute the thermodynamic properties of
   water an steam.
 
-  Alexander Burcat's database and routines to compute the properties
   of more than 1300 substances from 200K to 6000K.

-  JANAF thermodynamic data pulled from NIST website to compute
   properties of more than 1200 substances from 0K to 2500K.
 
-  Simple reactor for modeling combustion of single organic compounds.
 
-  Moist gas model.

Dependencies
------------

This packages needs the following extra modules to run.

-  Python 2.7, 3.4, and 3.5

-  Numpy >= 1.1.0

-  Scipy >= 0.6.0

-  Pandas >= 0.18.0

-  setuptools >= 0.6

Development
-----------

If you want to further develop thermochem you must install nosetests for
testing.
