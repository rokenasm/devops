"""Password strength validator.

Scores a password into one of four bands: very weak, weak, medium, strong.
Uses character-class rules, Shannon entropy, and a blocklist of leaked
passwords. Policy is configurable so different sites can plug their own
rules in.
"""

from dataclasses import dataclass, field
from math import log2
from typing import Iterable


# Small slice of well-known leaked passwords. A real deployment would
# load HaveIBeenPwned or a SecLists file instead.
_DEFAULT_BLOCKLIST = (
    "password", "password1", "password123", "123456", "123456789",
    "qwerty", "qwerty123", "abc123", "letmein", "welcome",
    "admin", "admin123", "iloveyou", "monkey", "dragon",
    "football", "baseball", "111111", "000000", "passw0rd",
)


@dataclass
class Policy:
    min_length: int = 8
    require_upper: bool = True
    require_lower: bool = True
    require_digit: bool = True
    require_symbol: bool = True
    blocklist: Iterable[str] = field(default_factory=lambda: _DEFAULT_BLOCKLIST)


def shannon_entropy(text: str) -> float:
    # Scaled by length so a 4-char string and a 40-char string don't
    # look the same to the scorer.
    if not text:
        return 0.0
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    length = len(text)
    entropy = 0.0
    for n in counts.values():
        p = n / length
        entropy -= p * log2(p)
    return entropy * length


def _char_class_score(password: str, policy: Policy) -> int:
    score = 0
    if policy.require_lower and any(c.islower() for c in password):
        score += 1
    if policy.require_upper and any(c.isupper() for c in password):
        score += 1
    if policy.require_digit and any(c.isdigit() for c in password):
        score += 1
    if policy.require_symbol and any(not c.isalnum() for c in password):
        score += 1
    return score


def _missing_requirements(password: str, policy: Policy) -> list[str]:
    reasons = []
    if len(password) < policy.min_length:
        reasons.append(f"shorter than {policy.min_length} characters")
    if policy.require_lower and not any(c.islower() for c in password):
        reasons.append("no lowercase letter")
    if policy.require_upper and not any(c.isupper() for c in password):
        reasons.append("no uppercase letter")
    if policy.require_digit and not any(c.isdigit() for c in password):
        reasons.append("no digit")
    if policy.require_symbol and not any(not c.isalnum() for c in password):
        reasons.append("no symbol")
    return reasons


def check_password(password, policy: Policy | None = None) -> dict:
    if policy is None:
        policy = Policy()

    if not isinstance(password, str):
        raise TypeError("password must be a string")

    # Blocklist overrides everything else - leaked passwords are useless
    # no matter how complex they look.
    if password.lower() in {b.lower() for b in policy.blocklist}:
        return {
            "band": "very weak",
            "score": 0,
            "entropy": shannon_entropy(password),
            "reasons": ["found in common-password blocklist"],
        }

    reasons = _missing_requirements(password, policy)
    classes = _char_class_score(password, policy)
    entropy = shannon_entropy(password)

    score = 0
    score += min(len(password), 20)
    score += classes * 4
    score += int(entropy / 4)

    # Missing required classes caps the result at "weak" so the policy
    # is actually enforced, not just scored.
    if reasons:
        band = "very weak" if len(reasons) >= 3 else "weak"
        return {
            "band": band,
            "score": score,
            "entropy": entropy,
            "reasons": reasons,
        }

    if score >= 40:
        band = "strong"
    elif score >= 28:
        band = "medium"
    elif score >= 18:
        band = "weak"
    else:
        band = "very weak"

    return {
        "band": band,
        "score": score,
        "entropy": entropy,
        "reasons": reasons,
    }


def process_value(value):
    # Kept so the scaffold's original placeholder test still passes.
    return value
