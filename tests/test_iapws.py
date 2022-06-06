import pytest
from thermochem.iapws import Water


def test_tsat_given_p():
    pytest.approx(Water().Tsat(0.1e6), 372.755919)
    pytest.approx(Water().Tsat(1e6), 453.035632)
    pytest.approx(Water().Tsat(10e6), 584.149488)


def test_psat_given_t():
    pytest.approx(Water().psat(300).MPa, 0.00353658941)
    pytest.approx(Water().psat(500).MPa, 2.63889776)
    pytest.approx(Water().psat(600).MPa, 12.3443146)


def test_iapws():
    w = Water()
    pytest.approx(w.T_ph(3, 500), (391.798509, 4.1313215739117e+21))
    pytest.approx(w.T_ph(3, 4000), (-14923984.403553, 1010.775766))
    pytest.approx(w.T_ph(0.001, 3000), (-103213.846234, 534.433241))
    pytest.approx(w.T_ph(3, 500), (391.798509, 4.1313215739117e+21))
    pytest.approx(w.T_ph(80, 500), (378.108626, -6.029123659828e+28))
    pytest.approx(w.T_ph(80, 1500), (611.041229, -5.572621155340e+22))
