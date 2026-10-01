"""Different binary-mask generator and codegree decoder for full local stars."""
from incidence import SUPPORTS, need


def formula_domains(spec, words):
    columns = [sum(1 << i for i, w in enumerate(words) if j in SUPPORTS[w]) for j in range(6)]
    decoded = []
    for i, word in enumerate(words):
        support = set(SUPPORTS[word])
        degree = 9-len(support)
        root_common = [len(support & row) for row in spec['roots']]
        cap = [3 if j < 4 or j in support else 5 for j in range(6)]
        got = []
        # The complete 16-bit domain is scanned independently for every vertex.
        for mask in range(1 << 16):
            if mask >> i & 1 or mask.bit_count() != degree:
                continue
            defects = []
            for j in range(6):
                value = cap[j]-root_common[j]-(mask & columns[j]).bit_count()
                if value < 0 or j in spec['saturated'] and value != 0:
                    break
                defects.append(value)
            else:
                got.append((mask, tuple(defects[j] for j in spec['active'])))
        decoded.append(got)
    return decoded


def replay_rounds(domains, result):
    """Check every proposed deletion by literal lack of a matching row."""
    rows = [list(row) for row in domains]
    deletions = 0
    for record in result['rounds']:
        need(list(map(len, rows)) == record['before'], 'round source sizes')
        next_rows = []
        for i, row in enumerate(rows):
            kept = []
            for candidate in row:
                unsupported = False
                for j in range(len(rows)):
                    if not any(bool(candidate >> j & 1) == bool(other >> i & 1) for other in rows[j]):
                        unsupported = True
                        break
                if unsupported:
                    deletions += 1
                else:
                    kept.append(candidate)
            next_rows.append(kept)
        need(list(map(len, next_rows)) == record['after'], 'all literal round deletions')
        rows = next_rows
    need(any(not row for row in rows) == result['excluded'], 'literal replay conclusion')
    return deletions
