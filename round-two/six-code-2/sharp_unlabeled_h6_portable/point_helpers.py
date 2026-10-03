"""Literal helpers credited to six-code-2's prior separate point-set audit.

No producer is imported. These four generic standard-library functions
are unchanged from the retained audit_two_hole.py; no two-hole theorem
or MRV function is used in this standalone one-Q proof.
"""
import json

def require(ok, message):
    if not ok:
        raise ValueError(message)

def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()

def literal(ps):
    return sum(1 << p for p in ps)

def point_set(w, k):
    require(type(w) is int and 0 <= w < 1 << 17 and w.bit_count() == k, 'physical old-point word')
    return frozenset(p for p in range(17) if w >> p & 1)
