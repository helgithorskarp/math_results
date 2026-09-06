"""Exact bipartite degree criterion and deterministic integral-flow lifting."""
from collections import deque


def need(ok, message):
    if not ok:
        raise ValueError(message)


def obstruction(rows, columns):
    """Return a literal violated bound/balance/subset certificate, or None."""
    need(isinstance(rows, (list, tuple)) and isinstance(columns, (list, tuple)), 'margin sequences')
    need(all(type(x) is int for x in (*rows, *columns)), 'integer margins')
    m, n = len(rows), len(columns)
    for side, values, bound in (('row', rows, n), ('column', columns, m)):
        for i, value in enumerate(values):
            if not 0 <= value <= bound:
                return {'kind': 'bound', 'side': side, 'index': i, 'value': value, 'upper': bound}
    if sum(rows) != sum(columns):
        return {'kind': 'balance', 'row_total': sum(rows), 'column_total': sum(columns)}
    for mask in range(1, 1 << m):
        subset = [i for i in range(m) if mask >> i & 1]
        lhs = sum(rows[i] for i in subset)
        rhs = sum(min(x, len(subset)) for x in columns)
        if lhs > rhs:
            return {'kind': 'subset', 'rows': subset, 'lhs': lhs, 'rhs': rhs}
    return None


def lift(rows, columns):
    """Return a 0/1 matrix, or None; no inequality oracle is used by the flow."""
    need(all(type(x) is int for x in (*rows, *columns)), 'integer margins')
    m, n = len(rows), len(columns)
    if any(not 0 <= x <= n for x in rows) or any(not 0 <= x <= m for x in columns):
        return None
    if sum(rows) != sum(columns):
        return None
    source, sink, order = m+n, m+n+1, m+n+2
    capacity = [[0]*order for _ in range(order)]
    for i, value in enumerate(rows):
        capacity[source][i] = value
        for j in range(n):
            capacity[i][m+j] = 1
    for j, value in enumerate(columns):
        capacity[m+j][sink] = value
    total = 0
    while True:
        previous = [-1]*order
        previous[source] = source
        queue = deque([source])
        while queue and previous[sink] < 0:
            u = queue.popleft()
            for v, cap in enumerate(capacity[u]):
                if cap and previous[v] < 0:
                    previous[v] = u
                    queue.append(v)
        if previous[sink] < 0:
            break
        amount, v = sum(rows), sink
        while v != source:
            u = previous[v]
            amount = min(amount, capacity[u][v])
            v = u
        v = sink
        while v != source:
            u = previous[v]
            capacity[u][v] -= amount
            capacity[v][u] += amount
            v = u
        total += amount
    if total != sum(rows):
        return None
    matrix = [[1-capacity[i][m+j] for j in range(n)] for i in range(m)]
    need([sum(row) for row in matrix] == list(rows), 'lift row sums')
    need([sum(matrix[i][j] for i in range(m)) for j in range(n)] == list(columns), 'lift column sums')
    return matrix
