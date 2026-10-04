import pytest

from kalkan.pii.tckn import is_valid_tckn


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("10000000146", True, id="valid-basic"),
        pytest.param("34567891238", True, id="valid-mixed-digits"),
        # Intermediate result is negative: 7*1 - 36 = -29
        pytest.param("19090909018", True, id="valid-negative-intermediate"),
        # Looks fake but satisfies the algorithm
        pytest.param("11111111110", True, id="valid-repeated-ones"),
        pytest.param("10000000147", False, id="wrong-11th-digit"),
        pytest.param("10000000157", False, id="wrong-10th-digit"),
        pytest.param("12345678901", False, id="sequential-invalid"),
        # Project decision: a TCKN starting with 0 is not valid
        pytest.param("01234567840", False, id="leading-zero"),
        pytest.param("1000000014", False, id="ten-digits"),
        pytest.param("1000000014a", False, id="contains-letter"),
    ],
)
def test_is_valid_tckn(value: str, expected: bool) -> None:
    assert is_valid_tckn(value) is expected
