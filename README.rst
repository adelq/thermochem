Thermochem
==========

.. image:: https://travis-ci.org/adelq/thermochem.svg?branch=master
    :target: https://travis-ci.org/adelq/thermochem

.. image:: https://img.shields.io/pypi/v/thermochem.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/thermochem

.. image:: https://readthedocs.org/projects/thermochem/badge/?version=latest
   :target: http://thermochem.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://landscape.io/github/adelq/thermochem/master/landscape.svg?style=flat
   :target: https://landscape.io/github/adelq/thermochem/master
   :alt: Code Health

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

Requirements
------------

- Python 2.7 or Python 3.5+

- Linux, Windows, MacOS, BSD, and any other platform with Python support and can
  install the required dependencies.

Install
-------

The easy and quick way::

    $ pip install thermochem

For more details and alternate installation instructions, see the `installation
instructions <http://thermochem.readthedocs.io/en/stable/install.html>`_.

Dependencies
------------

This packages depends on the following modules to run. These should be installed
automatically with any of the installation instructions provided.

-  NumPy >= 1.2.1

-  SciPy >= 0.6.0

-  pandas >= 0.17.0

Development
-----------

If you want to further develop thermochem you must install nosetests for
testing.

License
-------

Thermochem is licensed under the BSD license.
