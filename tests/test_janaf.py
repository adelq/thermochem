from thermochem.janaf import Janafdb
from nose.tools import eq_
from numpy.testing import assert_allclose


def test_titanium():
    db = Janafdb()
    ti = db.search('Ti')
    eq_(len(ti), 88)


def test_rutile():
    db = Janafdb()
    rutile = db.getphasedata(formula='O2Ti', name='Rutile', phase='cr', cache=False)
    assert_allclose(rutile.cp([500, 550, 1800]), [67.203, 68.567, 78.283])
