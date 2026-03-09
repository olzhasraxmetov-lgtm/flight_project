from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def check_timezone(tz_name: str) -> str:
    try:
        ZoneInfo(tz_name)
        return tz_name
    except ZoneInfoNotFoundError:
        raise ValueError(
            f"Таймзона '{tz_name}' не найдена. Используйте формат IANA (напр. 'Asia/Almaty')"
        )