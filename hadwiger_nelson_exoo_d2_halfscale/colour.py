"""Deterministic graph colouring and compact colour-row encoding."""


ROW_VERTICES = 52
ROW_BYTES = 13


def colour_graph(order, edges, colours):
    """Return a colouring and search-node count, or (None, nodes)."""
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        if left == right or not (0 <= left < order and 0 <= right < order):
            raise ValueError("malformed edge")
        adjacency[left].add(right)
        adjacency[right].add(left)
    row = [-1] * order
    nodes = 0

    def search(depth):
        nonlocal nodes
        nodes += 1
        if depth == order:
            return True
        candidates = []
        for vertex, colour in enumerate(row):
            if colour >= 0:
                continue
            used = {row[nbr] for nbr in adjacency[vertex] if row[nbr] >= 0}
            candidates.append((len(used), len(adjacency[vertex]), -vertex,
                               vertex, used))
        _sat, _degree, _minus_vertex, vertex, used = max(candidates)
        choices = (0,) if depth == 0 else range(colours)
        for colour in choices:
            if colour in used:
                continue
            row[vertex] = colour
            if search(depth + 1):
                return True
            row[vertex] = -1
        return False

    if search(0):
        return tuple(row), nodes
    return None, nodes


def valid_colouring(order, edges, row, colours=4):
    return (
        len(row) == order
        and all(isinstance(value, int) and 0 <= value < colours for value in row)
        and all(row[left] != row[right] for left, right in edges)
    )


def pack_row(row):
    if len(row) > ROW_VERTICES or any(not 0 <= value < 4 for value in row):
        raise ValueError("colour row cannot be packed")
    padded = tuple(row) + (0,) * (ROW_VERTICES - len(row))
    result = bytearray(ROW_BYTES)
    for index, colour in enumerate(padded):
        result[index // 4] |= colour << (2 * (index % 4))
    return bytes(result)


def unpack_row(data, order):
    if len(data) != ROW_BYTES or not 0 <= order <= ROW_VERTICES:
        raise ValueError("malformed packed colour row")
    values = tuple(
        (data[index // 4] >> (2 * (index % 4))) & 3
        for index in range(ROW_VERTICES)
    )
    if any(values[order:]):
        raise ValueError("nonzero padding in packed colour row")
    return values[:order]
