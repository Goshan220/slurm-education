class PracticeException(Exception):
    pass


class TypesOfLoad:
    decrease = "decrease"
    surges = "surges"
    stable = "stable"


class TypesOfIntensity:
    low = "low"
    middle = "middle"
    high = "high"
    enormous = "enormous"


class TypesOfDataDict:
    resource_id = "resource_id"
    measurement = "measurement"
    date_time = "date_time"
    load = "load"
    price = "price"
    average = "average"
    median = "median"
    type_of_usage = "type_of_usage"
    intensity_of_usage = "intensity_of_usage"
    decision = "decision"
