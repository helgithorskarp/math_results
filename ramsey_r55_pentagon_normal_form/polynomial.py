"""Independent combinatorial clause counts, without five-set enumeration."""
from collections import Counter
from math import comb


def multiply(a, b):
    result = Counter()
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            if i + k <= 5:
                result[i + k, j + l] += x * y
    return result


def count(n=43, cycles=5, joined=True):
    # x tracks selected vertices, y tracks fixed same-color physical pairs.
    cycle = {(0, 0): 1, (1, 0): 5, (2, 1): 5}
    answer = {}
    for color in (1, 0):
        if joined and color:
            current = Counter()
            for r in range(3):
                for c, choices in enumerate((1, 5, 5)):
                    current[r + c, comb(r, 2) + r * c + comb(c, 2)] += comb(2, r) * choices
        elif joined:
            current = Counter(cycle); current[1, 0] += 2
        else:
            current = Counter({(0, 0): 1})
        for _ in range(cycles - int(joined)):
            current = multiply(current, cycle)
        unused = n - 5 * cycles - 2 * int(joined)
        current = multiply(current, {(k, 0): comb(unused, k) for k in range(min(5, unused) + 1)})
        answer[color] = {str(10 - fixed): value for (vertices, fixed), value in current.items() if vertices == 5}
    return {"red": dict(sorted(answer[1].items(), key=lambda p: int(p[0]))),
            "blue": dict(sorted(answer[0].items(), key=lambda p: int(p[0]))),
            "total": sum(sum(c.values()) for c in answer.values())}
