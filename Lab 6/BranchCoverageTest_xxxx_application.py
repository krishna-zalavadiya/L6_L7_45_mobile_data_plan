
import pytest

from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status,
)


# ==================================================
# 1. BRANCH TESTS: overage_charge()
# ==================================================

def test_unknown_plan_branch():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("invalid", 1, False, False)


def test_negative_usage_branch():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_loyal_non_premium_branch():
    assert overage_charge("basic", 3, False, True) == 0


def test_loyal_premium_branch():
    assert overage_charge("premium", 11, False, True) == 15


def test_no_overage_branch():
    assert overage_charge("standard", 5, False, False) == 0


def test_non_roaming_branch():
    assert overage_charge("standard", 7, False, False) == 30


def test_roaming_branch():
    assert overage_charge("basic", 3, True, False) == 40


def test_extra_exactly_ten():
    assert overage_charge("standard", 15, False, False) == 150


def test_extra_more_than_ten_non_roaming():
    assert overage_charge("basic", 13, False, False) == 275


def test_extra_more_than_ten_roaming():
    assert overage_charge("basic", 13, True, False) == 605


# ==================================================
# 2. BRANCH TESTS: recharge_allowed()
# ==================================================

def test_kyc_pending_allowed():
    assert recharge_allowed(200, 5, True) is True


def test_kyc_pending_denied():
    assert recharge_allowed(201, 0, True) is False


def test_amount_above_limit():
    assert recharge_allowed(2001, 0, False) is False


def test_pending_recharges_allowed():
    assert recharge_allowed(500, 2, False) is True


def test_pending_recharges_denied():
    assert recharge_allowed(500, 3, False) is False


# ==================================================
# 3. BRANCH TESTS: validity_status()
# ==================================================

def test_prepaid_cutoff():
    assert validity_status(0, True, False) == "active"


def test_postpaid_cutoff():
    assert validity_status(3, False, False) == "active"


def test_addon_cutoff():
    assert validity_status(2, True, True) == "active"


def test_grace_period_boundary():
    assert validity_status(-15, True, False) == "grace"


def test_expired_beyond_grace_period():
    assert validity_status(-16, True, False) == "expired"


def test_addon_grace_period():
    assert validity_status(-13, True, True) == "grace"
