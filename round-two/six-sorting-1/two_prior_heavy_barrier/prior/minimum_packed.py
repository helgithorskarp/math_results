"""Whole-cube original-domain truth columns, exact actual9525 primitives."""
import hashlib
import json


def need(test, message):
    if not test:
        raise ValueError(message)



def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()



def columns(n):
    return [sum(1 << x for x in range(1 << n) if x >> i & 1) for i in range(n)]



def packed(gates, original_low=0):
    free = [i for i in range(13) if not original_low >> i & 1]
    lows = [i for i in range(13) if original_low >> i & 1]
    initial = columns(len(free))
    values = [lows.index(i)-len(lows) if i in lows else initial[free.index(i)]
              for i in range(13)]
    carrier = [None if i in lows else free.index(i) for i in range(13)]
    retained = []
    touch = identity = 0
    for t, (a, b) in enumerate(gates):
        need(0 <= a < b < 13, 'nonstandard literal prefix')
        x, y = values[a], values[b]
        if x < 0 or y < 0:
            touch |= 1 << t
            if x > y:
                values[a], values[b] = y, x
                carrier[a], carrier[b] = carrier[b], carrier[a]
        else:
            if x & ~y:
                retained.append([carrier[a], carrier[b]])
            else:
                identity |= 1 << t
            values[a], values[b] = x & y, x | y
    output = [i for i, v in enumerate(values) if v >= 0]
    rename = {carrier[i]: j for j, i in enumerate(output)}
    record = [original_low, 0, sum(1 << i for i, v in enumerate(values) if v < 0),
              0, touch.bit_count(), identity.bit_count(), identity]
    return values, {'outer_record': record, 'marked_touch_mask': touch,
                    'input_free_wires': free, 'output_free_wires': output,
                    'input_to_output_wire': [rename[j] for j in range(len(free))],
                    'retained_prefix': [[rename[a], rename[b]] for a, b in retained]}
