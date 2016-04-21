from thermopy.burcat import Elementdb
from nose.tools import assert_almost_equals


def test_enthalpy():
    db = Elementdb()
    oxygen = db.getelementdata("O2 REF ELEMENT")
    enthalpy = oxygen.ho(298.15)
    assert_almost_equals(enthalpy, 1.94293914332e-05)
