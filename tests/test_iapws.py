from thermochem.iapws import Water
from nose.tools import assert_almost_equal


def assert_almost_equals(first, second):
    return assert_almost_equal(first, second, places=6)


def test_tsat_given_p():
    assert_almost_equals(Water().Tsat(0.1e6), 372.755919)
    assert_almost_equals(Water().Tsat(1e6), 453.035632)
    assert_almost_equals(Water().Tsat(10e6), 584.149488)


def test_psat_given_t():
    assert_almost_equals(Water().psat(300).MPa, 0.00353658941)
    assert_almost_equals(Water().psat(500).MPa, 2.63889776)
    assert_almost_equals(Water().psat(600).MPa, 12.3443146)
