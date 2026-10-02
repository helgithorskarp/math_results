"""Fresh exact bit/set tools; six-reviewer-5, independent reviewer."""
import hashlib
import json

ALL22 = (1 << 22)-1


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()


def points(mask):
    return tuple(p for p in range(mask.bit_length()) if mask >> p & 1)
