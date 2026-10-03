from decimal import Decimal

import pytest

from para import para_coz


@pytest.mark.parametrize(
    "metin, beklenen",
    [
        ("1.250,50 TL", Decimal("1250.50")),
        ("1250,50 TL", Decimal("1250.50")),
        ("1.250 TL", Decimal("1250")),
        ("0,99 TL", Decimal("0.99")),
        ("₺1.250,50", Decimal("1250.50")),
        ("1.250,50 ₺", Decimal("1250.50")),
        ("1.250,50 TRY", Decimal("1250.50")),
        ("  1.250,50tl  ", Decimal("1250.50")),
        ("1.000.000,00 TL", Decimal("1000000.00")),
        ("-15,75 TL", Decimal("-15.75")),
        ("42", Decimal("42")),
        ("1.250", Decimal("1250")),
        ("1,5", Decimal("1.5")),
    ],
)
def test_gecerli_tutarlar(metin, beklenen):
    assert para_coz(metin) == beklenen


@pytest.mark.parametrize(
    "metin",
    ["", "TL", "abc TL", "1,2,3 TL", "1.25,50 TL", "12.34.5", None],
)
def test_gecersiz_tutarlar(metin):
    with pytest.raises(ValueError):
        para_coz(metin)


def test_float_hatasi_yok():
    assert para_coz("0,10 TL") + para_coz("0,20 TL") == Decimal("0.30")
