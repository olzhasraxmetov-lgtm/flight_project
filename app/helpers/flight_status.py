from enum import Enum

class FlightStatus(str, Enum):
    SCHEDULED = "scheduled"
    DELAYED = "delayed"
    DEPARTED = "departed"
    ARRIVED = "arrived"
    CANCELLED = "cancelled"