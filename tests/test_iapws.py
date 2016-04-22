from thermochem.iapws import Water
from nose.tools import assert_almost_equal


def assert_almost_equals(first, second):
    return assert_almost_equal(first, second, places=6)


def assert_tuple_equals(first, second):
    return assert_almost_equals(first[0], second[0]) and \
        assert_almost_equals(first[1], second[1])


def test_tsat_given_p():
    assert_almost_equals(Water().Tsat(0.1e6), 372.755919)
    assert_almost_equals(Water().Tsat(1e6), 453.035632)
    assert_almost_equals(Water().Tsat(10e6), 584.149488)


def test_psat_given_t():
    assert_almost_equals(Water().psat(300).MPa, 0.00353658941)
    assert_almost_equals(Water().psat(500).MPa, 2.63889776)
    assert_almost_equals(Water().psat(600).MPa, 12.3443146)


def test_iapws():
    w = Water()
    assert_tuple_equals(w.T_ph(3, 500), (391.798509, 4.1313215739117e+21))
    assert_tuple_equals(w.T_ph(3, 4000), (-14923984.403553, 1010.775766))
    assert_tuple_equals(w.T_ph(0.001, 3000), (-103213.846234, 534.433241))
    assert_tuple_equals(w.T_ph(3, 500), (391.798509, 4.1313215739117e+21))
    assert_tuple_equals(w.T_ph(80, 500), (378.108626, -6.029123659828e+28))
    assert_tuple_equals(w.T_ph(80, 1500), (611.041229, -5.572621155340e+22))
