from typing import Any

def valid_id(val: Any) -> bool:
    try:
        int_val = int(val)
        if int_val < 1: return False
        return True
    except:
        return False