from enum import Enum

class SeatStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"
    BLOCKED = "blocked"
    CHECKED_IN = "checked_in"