from thermochem.combustion import SimpleCombustor, Combustor
from thermochem.burcat import Elementdb
from nose.tools import assert_almost_equals


def test_simplecombustor():
    db = Elementdb()
    methane = db.getelementdata("CH4   RRHO")
    combustor = SimpleCombustor(methane,1.1,db)
    assert combustor.heat_of_comb(298.15) == 50027136.34030433

    # Test Ta
    butane = db.getelementdata('C4H10 n-butane')
    combustor = SimpleCombustor(butane,1,db)
    assert combustor.heat_of_comb(298.15) == 45720359.22491768


def test_combustor():
    db = Elementdb()
    fuels = db.getmixturedata([("CH4   RRHO", 0.9168),
                               ("C2H6", 0.0686),
                               ("C3H8", 0.0070),
                               ("C4H10 n-butane", 0.0011)])

    combustor = Combustor(fuels, 1, db)
    assert_almost_equals(combustor.heat_of_comb(423.15), 49245710.116662093)
