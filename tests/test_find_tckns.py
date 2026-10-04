import pytest

from kalkan.pii.tckn import find_tckns


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param(
            "TC kimliğim 10000000146, borcumu öğrenmek istiyorum.",
            [("10000000146", 12, 23)],
            id="in-sentence",
        ),
        pytest.param("Kimlik no:10000000146", [("10000000146", 10, 21)], id="after-colon"),
        # Starts with 0, so not a valid TCKN
        pytest.param("Telefonum 05321234567", [], id="phone-number"),
        # 11 digits but the checksum fails
        pytest.param("Sipariş no 12345678901", [], id="order-number"),
        # Part of a longer number
        pytest.param("Hesap 1000000014612", [], id="inside-longer-number"),
        # Project decision: spaced-out digits are not detected for now
        pytest.param("TC: 100 000 001 46", [], id="spaced-digits"),
        # Digits are normalized first; positions still refer to the original text
        pytest.param("TC'm ١٠٠٠٠٠٠٠١٤٦", [("10000000146", 5, 16)], id="arabic-indic-digits"),
        pytest.param(
            "TC'm １０００００００１４６",
            [("10000000146", 5, 16)],
            id="fullwidth-digits",
        ),
        pytest.param(
            "10000000146 ve 34567891238",
            [("10000000146", 0, 11), ("34567891238", 15, 26)],
            id="two-tckns",
        ),
        # Only digits define the boundary, letters do not
        pytest.param("TC10000000146", [("10000000146", 2, 13)], id="letters-adjacent"),
        # Superscript and circled digits are digits too: normalized, and they count as a boundary
        pytest.param("TC 1000000014⁶", [("10000000146", 3, 14)], id="superscript-digit"),
        pytest.param("TC ①0000000146", [("10000000146", 3, 14)], id="circled-digit"),
        pytest.param("²10000000146", [], id="superscript-before-number"),
    ],
)
def test_find_tckns(text: str, expected: list[tuple[str, int, int]]) -> None:
    assert [(m.value, m.start, m.end) for m in find_tckns(text)] == expected


@pytest.mark.parametrize(
    ("text", "original"),
    [
        pytest.param("TC'm ١٠٠٠٠٠٠٠١٤٦", "١٠٠٠٠٠٠٠١٤٦", id="arabic-indic-digits"),
        pytest.param(
            "TC'm １０００００００１４６",
            "１０００００００１４６",
            id="fullwidth-digits",
        ),
    ],
)
def test_positions_point_into_original_text(text: str, original: str) -> None:
    [match] = find_tckns(text)
    assert text[match.start : match.end] == original
