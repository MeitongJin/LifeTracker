# Input data type conversion
def to_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0

def to_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0