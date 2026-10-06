"""Portable checked helper subset; used function bodies are unchanged."""
from check_lyra_boundary import require

def full_encode(rows, columns, guard_rows, guard_columns):
    r = len(rows)
    word, tags = [], []
    for i in range(r):
        for label in rows[i]:
            j = label - 1
            tags.append(('old', i, j))
            word.append(j * (2 * r - 1) + columns[j][i])
        if i < r - 1:
            for label in guard_rows[i]:
                j = label - 1
                tags.append(('guard', i, j))
                word.append(j * (2 * r - 1) + r + guard_columns[j][i])
    require(sorted(word) == list(range(1, r * r + (r - 1) ** 2 + 1)), 'Band word is not a permutation')
    return tuple(word), tuple(tags)

def full_decode(word, r):
    cols = [[0] * r for _ in range(r)]
    gcols = [[0] * (r - 1) for _ in range(r - 1)]
    rows, grows = [], []
    for i in range(r):
        start = i * (2 * r - 1)
        row = []
        for value in word[start:start + r]:
            j, rank = divmod(value - 1, 2 * r - 1)
            rank += 1
            require(rank <= r, 'Old band has a guard value')
            row.append(j + 1)
            cols[j][i] = rank
        rows.append(tuple(row))
        if i < r - 1:
            row = []
            for value in word[start + r:start + 2 * r - 1]:
                j, rank = divmod(value - 1, 2 * r - 1)
                rank += 1
                require(rank > r and j < r - 1, 'Guard band has an old value')
                row.append(j + 1)
                gcols[j][i] = rank - r
            grows.append(tuple(row))
    return tuple(rows), tuple(map(tuple, cols)), tuple(grows), tuple(map(tuple, gcols))

def selected_box(word, selected):
    a, b, c, d = selected
    return a < b < c < d and word[b] < word[a] < word[d] < word[c] and all(
        k in selected or not word[b] < word[k] < word[c] for k in range(a + 1, d))
