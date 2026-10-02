"""Packed original-domain carrier pruning, credited actual9420 primitives."""
import hashlib
import json


def need(test, message):
    if not test:
        raise ValueError(message)



def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()



def pruning(gates, low, high, semantic):
    free = [i for i in range(13) if not (low | high) >> i & 1]
    columns = iter(semantic.truth_columns(len(free)))
    values = ['L' if low >> i & 1 else 'H' if high >> i & 1 else next(columns)
              for i in range(13)]
    carrier = [free.index(i) if i in free else None for i in range(13)]
    word = []
    d = r = redundant = touches = 0
    for t, (a, b) in enumerate(gates):
        x, y = values[a], values[b]
        if isinstance(x, str) or isinstance(y, str):
            d += 1
            touches |= 1 << t
            rank = lambda z: -1 if z == 'L' else 1 if z == 'H' else 0
            if rank(x) > rank(y):
                values[a], values[b] = y, x
                carrier[a], carrier[b] = carrier[b], carrier[a]
        else:
            if not x & ~y:
                r += 1
                redundant |= 1 << t
            else:
                word.append([carrier[a], carrier[b]])
            values[a], values[b] = x & y, x | y
    current = semantic.marked_ports(values)
    output = [i for i in range(13) if isinstance(values[i], int)]
    rename = {carrier[i]: j for j, i in enumerate(output)}
    record = [low, high, *current, d, r, redundant]
    return {'outer_record': record, 'marked_touch_mask': touches,
            'input_free_wires': free, 'output_free_wires': output,
            'input_to_output_wire': [rename[i] for i in range(len(free))],
            'retained_prefix': [[rename[a], rename[b]] for a, b in word]}
