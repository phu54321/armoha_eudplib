from ...core import (
    AllPlayers,
    EUDVariable,
    Exactly,
    Memory,
    RawTrigger,
    SetMemory,
    SetTo,
)
from .cpprint import f_raise_CCMU

LocalLocale = EUDVariable(0)


def _detect_locale():
    LOCALES = [
        "enUS",  # [1] English
        "frFR",  # [2] Français
        "itIT",  # [3] Italiano
        "deDE",  # [4] Deutsch
        "esES",  # [5] Español - España
        "esMX",  # [6] Español - Latino
        "ptBR",  # [7] Português
        "zhCN",  # [8] 简体中文
        "zhTW",  # [9] 繁體中文
        "jaJP",  # [10] 日本語
        "koUS",  # [11] 한국어 (음역)
        "koKR",  # [12] 한국어 (완역)
        "plPL",  # [13] Polski
        "ruRU",  # [14] Русский
    ]
    MAGIC_NUMBERS = {
        "enUS": (1650552405, 1948280172, 1919098991),
        "frFR": (1869638985, 1651078003, 1679844716),
        "itIT": (1869638985, 1651078003, 543517801),
        "deDE": (543516996, 1752066373, 544500069),
        "esES": (1931505486, 1634213989, 1685024800),
        "esMX": (1931505486, 1970282597, 543515749),
        "ptBR": (1869638985, 2915267443, 543974774),
        "zhCN": (3869284326, 2296747443, 3132876187),
        "zhTW": (3869344999, 3152385459, 2692803002),
        "jaJP": (3819340771, 2212727683, 2290344835),
        "koUS": (3953171692, 2649529227, 2213290116),
        "koKR": (3953171692, 2649529227, 2213290116),
        "plPL": (543517006, 3167055725, 1931501934),
        "ruRU": (3050347984, 3498299680, 3501248692),
    }

    f_raise_CCMU(AllPlayers)
    STATUS_MSG = 0x640B60 + 218 * 12
    for locale_id, locale in enumerate(LOCALES):
        magic_numbers = MAGIC_NUMBERS[locale]
        # FIXME: Can't disambiguate between koUS and koKR
        if locale == "koKR":
            continue
        RawTrigger(
            conditions=[
                Memory(STATUS_MSG, Exactly, magic_numbers[0]),
                Memory(STATUS_MSG + 4, Exactly, magic_numbers[1]),
                Memory(STATUS_MSG + 8, Exactly, magic_numbers[2]),
            ],
            actions=LocalLocale.SetNumber(locale_id + 1),
        )
    RawTrigger(actions=SetMemory(STATUS_MSG, SetTo, 0))