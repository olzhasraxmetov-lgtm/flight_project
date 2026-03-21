from enum import Enum

class CabinClass(str, Enum):
    ECONOMY = "economy"
    BUSINESS = "business"
    FIRST = "first"