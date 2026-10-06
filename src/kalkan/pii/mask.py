"""Masking TCKNs with labels and restoring them."""

import re

from kalkan.pii.tckn import find_tckns

# Only ASCII digits, so a label with Unicode digits is not treated as a label.
_LABEL = re.compile(r"\[TCKN_[0-9]+\]")


def mask_tckns(text: str, mapping: dict[str, str] | None = None) -> tuple[str, dict[str, str]]:
    """Replace every TCKN in text with a label and return the masked text and label -> number map.

    Labels are numbered in order of first appearance; the same number always gets the same label.
    Without mapping, the map is built fresh on every call and is never stored. With mapping (a
    label -> number map from an earlier call), its labels are reused and new ones continue the
    numbering; the returned map holds both. The given mapping is not modified.
    """
    # ASCII number -> label
    labels: dict[str, str] = {value: label for label, value in (mapping or {}).items()}
    parts: list[str] = []
    prev_end = 0
    for match in find_tckns(text):
        label = labels.setdefault(match.value, f"[TCKN_{len(labels) + 1}]")
        parts.append(text[prev_end : match.start])
        parts.append(label)
        prev_end = match.end
    parts.append(text[prev_end:])
    return "".join(parts), {label: value for value, label in labels.items()}


def unmask(text: str, mapping: dict[str, str]) -> str:
    """Replace labels with their numbers. Labels missing from mapping are left as they are."""
    return _LABEL.sub(lambda m: mapping.get(m.group(), m.group()), text)
