from enum import Enum

class SeatType(str, Enum):
    WINDOW = "window"
    AISLE = "aisle"
    MIDDLE = "middle"
    EXTRA_LEGROOM = "extra_legroom"