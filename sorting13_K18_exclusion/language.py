"""Complete36-word K18 minimum language; no unary front-loading.

Author: six-sorting-2, researcher. Stationary passages count as events.
"""

POSITIONS = ((0, 1, 5), (0, 1, 2), (0, 1, 3), (0, 1, 4),
             (0, 1, 5), (0, 1, 2), (0, 1, 3), (0, 1, 4),
             (0, 1, 5), (0, 1, 0), (0, 0, 0))
FIRST = {(2, 5): 1, (3, 5): 2, (4, 5): 3,
         (5, 6): 4, (5, 7): 4, (5, 8): 4}


def destination(state, pair):
    if not any(p in pair for p in POSITIONS[state]):
        return state
    if state == 0:
        return FIRST.get(pair)
    if 1 <= state <= 4:
        p = POSITIONS[state][2]
        if p in pair and all(2 <= endpoint <= 8 for endpoint in pair):
            return 5 + pair[0] - 2
        return None
    if 5 <= state <= 8 and pair == (0, POSITIONS[state][2]):
        return 9
    if state == 9 and pair == (0, 1):
        return 10
    return None


def encode(w, choices, pairs, gates):
    phase = [[w.var() for _ in POSITIONS] for _ in range(gates + 1)]
    for row in phase:
        w.exactly_one(row)
    w.add(phase[0][0])
    w.add(phase[-1][10])
    for t in range(gates):
        for state in range(len(POSITIONS)):
            for j, pair in enumerate(pairs):
                target = destination(state, pair)
                if target is None:
                    w.add(-phase[t][state], -choices[t][j])
                else:
                    w.add(-phase[t][state], -choices[t][j], phase[t + 1][target])
    return phase
