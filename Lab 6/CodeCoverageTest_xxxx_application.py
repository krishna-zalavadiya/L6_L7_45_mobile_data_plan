
import pytest

from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status,
)


# -------------------------------
# overage_charge() tests
# -------------------------------

def test_overage_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_overage_negative_usage():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_overage_within_included_data():
    assert overage_charge("basic", 2, False, False) == 0


def test_overage_loyal_customer():
    assert overage_charge("basic", 3, False, True) == 0


def test_overage_non_roaming():
    assert overage_charge("standard", 7, False, False) == 30


def test_overage_roaming():
    assert overage_charge("basic", 3, True, False) == 40


def test_overage_large_usage_non_roaming():
    assert overage_charge("basic", 13, False, False) == 165


def test_overage_large_usage_roaming():
    assert overage_charge("basic", 13, True, False) == 495


def test_overage_premium_loyal():
    assert overage_charge("premium", 11, False, True) == 15


# -------------------------------
# recharge_allowed() tests
# -------------------------------

def test_recharge_kyc_within_limit():
    assert recharge_allowed(200, 5, True) is True


def test_recharge_kyc_over_limit():
    assert recharge_allowed(201, 0, True) is False


def test_recharge_amount_over_2000():
    assert recharge_allowed(2001, 0, False) is False


def test_recharge_pending_limit():
    assert recharge_allowed(500, 2, False) is True


def test_recharge_too_many_pending():
    assert recharge_allowed(500, 3, False) is False


# -------------------------------
# validity_status() tests
# -------------------------------

def test_validity_prepaid_active():
    assert validity_status(0, True, False) == "active"


def test_validity_postpaid_active():
    assert validity_status(3, False, False) == "active"


def test_validity_addon_active():
    assert validity_status(2, True, True) == "active"


def test_validity_grace():
    assert validity_status(-1, True, False) == "grace"


def test_validity_expired():
    assert validity_status(-15, True, False) == "expired"


def test_validity_addon_grace():
    assert validity_status(-12, True, True) == "grace"
