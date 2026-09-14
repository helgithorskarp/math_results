"""Regenerate positive words; search is not trusted by the checker."""
import argparse
import json
from pathlib import Path
from verify import geometry, need, verify


def search(edges, a, b, c):
    adj = [set() for _ in range(29)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    word = [-1] * 29
    word[a], word[b] = 0, c

    def visit():
        left = [v for v in range(29) if word[v] == -1]
        if not left:
            return word.copy()
        domains = {v: set(range(4)) - {word[u] for u in adj[v]} for v in left}
        v = min(left, key=lambda u: (len(domains[u]), -len(adj[u]), u))
        for colour in sorted(domains[v]):
            word[v] = colour
            found = visit()
            if found is not None:
                return found
        word[v] = -1
        return None

    return visit()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    *_, pairs, edges = geometry()
    rows = []
    for a, b in pairs:
        for c in (0, 1):
            w = search(edges, a, b, c)
            need(w is not None, 'no positive pair witness')
            rows.append({'pair': [a, b], 'second_colour': c, 'word': ''.join(map(str, w))})
    cert = {'schema': 1, 'pair_words': rows}
    verify(cert)
    args.output.write_text(json.dumps(cert, separators=(',', ':')) + '\n')
