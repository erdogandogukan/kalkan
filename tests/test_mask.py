import pytest

from kalkan.pii.mask import mask_tckns, unmask


@pytest.mark.parametrize(
    ("text", "expected_text", "expected_mapping"),
    [
        pytest.param(
            "TC'm 10000000146",
            "TC'm [TCKN_1]",
            {"[TCKN_1]": "10000000146"},
            id="M1-single",
        ),
        pytest.param(
            "10000000146 ve 34567891238",
            "[TCKN_1] ve [TCKN_2]",
            {"[TCKN_1]": "10000000146", "[TCKN_2]": "34567891238"},
            id="M2-two-tckns",
        ),
        # The same number gets the same label
        pytest.param(
            "10000000146, tekrar: 10000000146",
            "[TCKN_1], tekrar: [TCKN_1]",
            {"[TCKN_1]": "10000000146"},
            id="M3-repeated",
        ),
        pytest.param("Merhaba", "Merhaba", {}, id="M4-no-tckn"),
        # The invisible character inside the number is masked too
        pytest.param(
            "TC 10000​000146",
            "TC [TCKN_1]",
            {"[TCKN_1]": "10000000146"},
            id="M5-zero-width-space",
        ),
        # The mapping holds the ASCII form of the number
        pytest.param(
            "TC'm ١٠٠٠٠٠٠٠١٤٦",
            "TC'm [TCKN_1]",
            {"[TCKN_1]": "10000000146"},
            id="M6-arabic-indic-digits",
        ),
    ],
)
def test_mask_tckns(text: str, expected_text: str, expected_mapping: dict[str, str]) -> None:
    assert mask_tckns(text) == (expected_text, expected_mapping)


@pytest.mark.parametrize(
    ("text", "mapping", "expected"),
    [
        pytest.param(
            "[TCKN_1] numaralı müşteri",
            {"[TCKN_1]": "10000000146"},
            "10000000146 numaralı müşteri",
            id="U1-known-label",
        ),
        # Labels missing from the mapping, and broken labels, are left alone
        pytest.param(
            "[TCKN_9] ve TCKN_1",
            {"[TCKN_1]": "10000000146"},
            "[TCKN_9] ve TCKN_1",
            id="U2-unknown-or-broken-label",
        ),
    ],
)
def test_unmask(text: str, mapping: dict[str, str], expected: str) -> None:
    assert unmask(text, mapping) == expected


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("TC'm 10000000146", id="M1"),
        pytest.param("10000000146 ve 34567891238", id="M2"),
        pytest.param("10000000146, tekrar: 10000000146", id="M3"),
    ],
)
def test_unmask_reverses_mask(text: str) -> None:
    assert unmask(*mask_tckns(text)) == text
