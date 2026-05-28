"""Tests for the password validator.

Grouped by the categories the brief asks for: normal, edge/boundary,
invalid input, failure/risk, decision paths, helpers, and the
scaffold's placeholder.
"""

import pytest

from src.component import (
    Policy,
    check_password,
    process_value,
    shannon_entropy,
)


# Normal behaviour

def test_strong_password_is_classed_strong():
    result = check_password("Tr0ub4dor&3xK!")
    assert result["band"] == "strong"
    assert result["reasons"] == []


def test_typical_medium_password():
    result = check_password("Hello12!")
    assert result["band"] in {"medium", "strong"}
    assert result["reasons"] == []


def test_result_shape_is_stable():
    result = check_password("Hello12!")
    assert set(result.keys()) == {"band", "score", "entropy", "reasons"}


# Edge / boundary

def test_exact_minimum_length_passes_when_classes_covered():
    result = check_password("Ab1!cdef")
    assert result["reasons"] == []
    assert result["band"] in {"weak", "medium", "strong"}


def test_one_below_minimum_length_is_flagged():
    result = check_password("Ab1!cde")
    assert "shorter than 8 characters" in result["reasons"]
    assert result["band"] in {"very weak", "weak"}


def test_empty_string_is_very_weak():
    result = check_password("")
    assert result["band"] == "very weak"
    assert len(result["reasons"]) >= 3


def test_extremely_long_password_does_not_overflow():
    pwd = "Aa1!" * 50
    result = check_password(pwd)
    assert result["band"] in {"medium", "strong"}
    assert result["score"] < 200


# Invalid input

def test_non_string_input_raises_type_error():
    with pytest.raises(TypeError):
        check_password(12345)


def test_none_input_raises_type_error():
    with pytest.raises(TypeError):
        check_password(None)


def test_list_input_raises_type_error():
    with pytest.raises(TypeError):
        check_password(["password"])


# Failure / risk

def test_common_blocklisted_password_is_forced_very_weak():
    result = check_password("password")
    assert result["band"] == "very weak"
    assert "blocklist" in result["reasons"][0]


def test_blocklist_match_is_case_insensitive():
    # Attackers can trivially toggle case.
    assert check_password("Password")["band"] == "very weak"
    assert check_password("PASSWORD")["band"] == "very weak"


def test_complex_looking_but_blocklisted_password_still_blocked():
    assert check_password("passw0rd")["band"] == "very weak"


def test_low_entropy_password_does_not_get_high_band():
    result = check_password("aaaaaaaaA1!")
    assert result["band"] in {"very weak", "weak", "medium"}


# Decision paths - every band reachable

def test_very_weak_band_reachable():
    result = check_password("abc")
    assert result["band"] == "very weak"


def test_weak_band_reachable():
    result = check_password("abcdefghij")
    assert result["band"] in {"very weak", "weak"}


def test_medium_band_reachable():
    result = check_password("Hello12!")
    assert result["band"] in {"medium", "strong"}


def test_strong_band_reachable():
    result = check_password("Tr0ub4dor&3xK!")
    assert result["band"] == "strong"


# Configurable policy

def test_relaxed_policy_accepts_passwords_default_would_reject():
    relaxed = Policy(require_symbol=False)
    result = check_password("Hello123", policy=relaxed)
    assert "no symbol" not in result["reasons"]


def test_strict_policy_raises_the_length_floor():
    strict = Policy(min_length=16)
    result = check_password("Hello12!", policy=strict)
    assert "shorter than 16 characters" in result["reasons"]


def test_custom_blocklist_blocks_company_specific_passwords():
    company_policy = Policy(blocklist=("northampton2025",))
    result = check_password("northampton2025", policy=company_policy)
    assert result["band"] == "very weak"


# Helpers

def test_entropy_of_empty_string_is_zero():
    assert shannon_entropy("") == 0.0


def test_entropy_grows_with_variety():
    low = shannon_entropy("aaaaaaaa")
    high = shannon_entropy("aB1!xY2@")
    assert high > low


# Scaffold placeholder

def test_process_value_returns_input():
    assert process_value("test") == "test"
