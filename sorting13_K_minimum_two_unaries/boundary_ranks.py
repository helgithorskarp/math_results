"""Exact consequences of a future-disconnected Boolean rank boundary.

Author: six-sorting-2, researcher. No new variables or solver dependency.
"""


def zero_one_obligations(wires, weight, boundary):
    """Return (wire, required bit) when the side counts are final counts.

    The threshold lies after all wires carrying a zero in the sorted row.
    Equality to the threshold forces both sides. Constants are handled by
    the writer, so including initial/final and sorted rows is safe.
    """
    assert 0 <= weight <= wires and 0 <= boundary < wires - 1
    threshold = wires - weight
    result = []
    if boundary + 1 <= threshold:
        result.extend((i, False) for i in range(boundary + 1))
    if boundary + 1 >= threshold:
        result.extend((i, True) for i in range(boundary + 1, wires))
    return result


def encode(w, cuts, bits, wires, gates):
    for state, histories in bits.items():
        assert len(histories) == gates + 1
        for k in range(wires - 1):
            obligations = zero_one_obligations(wires, state.bit_count(), k)
            for t in range(gates + 1):
                for i, value in obligations:
                    literal = histories[t][i]
                    if not value:
                        literal = not literal if isinstance(literal, bool) else -literal
                    w.add(-cuts[t][k], literal)
