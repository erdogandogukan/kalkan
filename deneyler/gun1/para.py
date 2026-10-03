"""Türkçe yazılmış para tutarlarını (ör. "1.250,50 TL") sayıya çevirir."""

import re
from decimal import Decimal

_PARA_BIRIMI = re.compile(r"^(?:₺|TRY|TL)\s*|\s*(?:₺|TRY|TL)$", re.IGNORECASE)
_SAYI = re.compile(r"^[+-]?(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d+)?$")


def para_coz(metin: str) -> Decimal:
    """Türk biçimli tutarı Decimal'e çevirir: '.' binlik, ',' ondalık ayırıcıdır.

    Geçersiz girdide ValueError fırlatır.
    """
    if not isinstance(metin, str):
        raise ValueError(f"Metin bekleniyordu, gelen: {type(metin).__name__}")

    sayi = _PARA_BIRIMI.sub("", metin.strip()).strip()
    if not _SAYI.match(sayi):
        raise ValueError(f"Geçersiz para tutarı: {metin!r}")

    return Decimal(sayi.replace(".", "").replace(",", "."))
