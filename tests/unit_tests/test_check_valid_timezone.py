from app.utils.check_valid_timezone import check_timezone
import pytest

def test_check_valid_timezone_valid():
    tz = "America/New_York"
    assert check_timezone(tz) == tz
    assert check_timezone("UTC") == "UTC"

def test_check_timezone_invalid():
    with pytest.raises(ValueError, match="Таймзона 'Mars/City' не найдена"):
        check_timezone("Mars/City")

@pytest.mark.parametrize("tz_name", [
    "Europe/Moscow",
    "Asia/Almaty",
    "UTC",
    "America/Los_Angeles"
])
def test_check_multiple_valid_timezones(tz_name):
    assert check_timezone(tz_name) == tz_name