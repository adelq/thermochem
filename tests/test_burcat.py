from thermochem.burcat import Elementdb
from nose.tools import eq_, assert_almost_equals


def test_enthalpy():
    db = Elementdb()
    oxygen = db.getelementdata("O2 REF ELEMENT")
    enthalpy = oxygen.ho(298.15)
    assert_almost_equals(enthalpy, 1.94293914332e-05)


def test_nio():
    """Test NiO phases"""
    db = Elementdb()
    eq_(db.search('NiO'),
        ['NiO  Solid-A', 'NiO  Solid-B', 'NiO  Solid-C', 'NiO  Liquid'])
