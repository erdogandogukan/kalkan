"""Validation of Turkish national identity numbers (TCKN)."""

import re
import unicodedata
from dataclasses import dataclass

# Exactly 11 digits. Only digits define the boundary, so letters may touch the number.
_ELEVEN_DIGITS = re.compile(r"(?<![0-9])[0-9]{11}(?![0-9])")


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


@dataclass(frozen=True)
class TcknMatch:
    """A TCKN found in text. start/end index the original text; value is ASCII digits."""

    value: str
    start: int
    end: int


def find_tckns(text: str) -> list[TcknMatch]:
    """Return every valid TCKN in text, with positions in the original text."""
    # Drop invisible format characters (category Cf: zero-width space, soft hyphen, ...) and map
    # every Unicode digit (Arabic-Indic, fullwidth, superscript, circled, ...) to ASCII.
    # positions[i] is the index in the original text of normalized[i].
    chars: list[str] = []
    positions: list[int] = []
    for i, c in enumerate(text):
        if unicodedata.category(c) == "Cf":
            continue
        chars.append(str(unicodedata.digit(c)) if c.isdigit() else c)
        positions.append(i)
    normalized = "".join(chars)
    # The span runs from the first digit to the last, so invisible characters inside it are
    # included and get masked too.
    return [
        TcknMatch(m.group(), positions[m.start()], positions[m.end() - 1] + 1)
        for m in _ELEVEN_DIGITS.finditer(normalized)
        if is_valid_tckn(m.group())
    ]
