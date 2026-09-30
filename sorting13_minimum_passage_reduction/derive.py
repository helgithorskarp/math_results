"""Depth-free finite reachability certificate for the minimum-passage cut."""
import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time


# Fields: positions of one-hot 6, one-hot 8, the unique zero initially at 1;
# high threshold 6+9; two-one test 4+6; q6; q9; mixed union; min hits capped at 2.
INITIAL = (6, 8, 1, 576, 80, 0, 0, 0, 0)
PAIRS = tuple(itertools.combinations(range(10), 2))


def compare(mask, a, b):
    if (mask >> a) & 1 and not (mask >> b) & 1:
        return mask ^ ((1 << a) | (1 << b))
    return mask


def transition(state, pair):
    six, eight, zero, high, test, q6, q9, union, minimum = state
    a, b = pair
    h = bool(high & ((1 << a) | (1 << b)))
    l = zero in pair
    q6 += six in pair
    q9 += 9 in pair
    union += h or l
    if q6 > 2 or q9 > 1 or union > 4:
        return None
    return (b if six == a else six, b if eight == a else eight,
            a if zero == b else zero, compare(high, a, b), compare(test, a, b),
            q6, q9, union, min(2, minimum + l))


def accepting(state):
    six, eight, zero, high, test, q6, q9, union, minimum = state
    return (six, eight, zero, high, test, minimum) == (9, 9, 0, 768, 768, 2)


def main():
    if not __debug__:
        raise RuntimeError("Run without Python optimization: assertions are part of the checker")
    p = argparse.ArgumentParser()
    p.add_argument('--path', type=Path, required=True)
    args = p.parse_args()
    started = time.monotonic()
    reached = {INITIAL}
    queue = deque([INITIAL])
    attempts = 0
    while queue:
        state = queue.popleft()
        assert not accepting(state), ('Counterexample to the proposed cut', state)
        for pair in PAIRS:
            nxt = transition(state, pair)
            attempts += 1
            if nxt is not None and nxt not in reached:
                reached.add(nxt)
                queue.append(nxt)
        if len(reached) > 100000 or time.monotonic() - started > 30:
            raise RuntimeError('INCOMPLETE: explicit local state/time cap reached')
    cert = dict(agent='six-sorting-2', role='researcher', wires=10,
                fields=['max6', 'max8', 'min1', 'high576', 'test80', 'q6', 'q9', 'union', 'min_hits_capped2'],
                initial=list(INITIAL), bounds=dict(q6=2, q9=1, union=4),
                states=[list(s) for s in sorted(reached)],
                excluded_target=dict(max6=9, max8=9, min1=0, high576=768, test80=768,
                                     min_hits_capped2=2),
                scope='Closed reachable set; all 45 comparators and arbitrary word length')
    args.path.write_text(json.dumps(cert, separators=(',', ':')) + '\n')
    result = dict(status='CLOSED_NO_ACCEPTING_STATE', states=len(reached), transitions=attempts,
                  seconds=time.monotonic()-started,
                  sha256=hashlib.sha256(args.path.read_bytes()).hexdigest(),
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    args.path.with_suffix('.result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
