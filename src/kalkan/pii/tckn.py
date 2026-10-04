"""Validation of Turkish national identity numbers (TCKN)."""


def is_valid_tckn(value: str) -> bool:
    """Return True if value is a valid 11-digit TCKN according to its checksum rules."""
    # isascii() rejects non-ASCII digits such as Arabic-Indic numerals, which isdigit() accepts.
    if len(value) != 11 or not value.isascii() or not value.isdigit():
        return False

    digits = [int(c) for c in value]
    if digits[0] == 0:
        return False

    odd_sum = sum(digits[0:9:2])  # 1st, 3rd, 5th, 7th, 9th digits
    even_sum = sum(digits[1:8:2])  # 2nd, 4th, 6th, 8th digits
    # Python's % always returns a non-negative result, so a negative intermediate is safe.
    if (odd_sum * 7 - even_sum) % 10 != digits[9]:
        return False

    return sum(digits[:10]) % 10 == digits[10]
