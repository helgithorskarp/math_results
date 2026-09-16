"""Frozen balanced deletion cohort in the exact archived Haugland G3."""
from pathlib import Path
from hashlib import sha256
import heapq
import json

HERE = Path(__file__).resolve().parent
GRAPH_SHA = '201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d'
EDGE_SHA = '980bdb02e133be0e4257bab1a204f2942f554e59822136fab632f45494a6c113'
N = 2131
PINS = frozenset((0, 303, 435, 1368, 1500))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest_labels(labels):
    return sha256(''.join(f'{v}\n' for v in sorted(labels)).encode()).hexdigest()

def digest_edges(edges):
    return sha256(''.join(f'{u} {v}\n' for u,v in edges).encode()).hexdigest()

def load():
    path = HERE.parent/'hadwiger_nelson_haugland2131_exact_reproduction/graph.json'
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == GRAPH_SHA, 'source hash')
    edges = [tuple(e) for e in json.loads(raw)['G3_edges']]
    require(len(edges) == 12530 and edges == sorted(set(edges)), 'edge census')
    require(digest_edges(edges) == EDGE_SHA, 'strict edge hash')
    adj = [set() for _ in range(N)]
    for u,v in edges:
        require(0 <= u < v < N, 'edge labels')
        adj[u].add(v); adj[v].add(u)
    return edges, adj

def tie(seed, v):
    return sha256(f'HN2131-nonlocal-cap508-v1:{seed}:{v}'.encode('ascii')).digest()

def half(v):
    return int(v >= 1066)

def support(seed, orientation, adj):
    """Producer: incrementally updated degrees and a lazy priority heap."""
    require(seed in range(8) and orientation in (0,1), 'cohort parameter')
    quotas = (254,253) if orientation == 0 else (253,254)
    counts = [1065,1065]
    live = set(range(N))
    degree = [len(a) for a in adj]
    keys = [tie(seed,v) for v in range(N)]
    heap = [(degree[v],keys[v],v) for v in range(N) if v not in PINS]
    heapq.heapify(heap)
    while len(live) > 508:
        deg, key, v = heapq.heappop(heap)
        if v not in live or deg != degree[v] or counts[half(v)] <= quotas[half(v)]:
            continue
        live.remove(v); counts[half(v)] -= 1
        for u in adj[v] & live:
            degree[u] -= 1
            if u not in PINS:
                heapq.heappush(heap,(degree[u],keys[u],u))
    require(tuple(counts) == quotas and PINS <= live, 'quota or pin failure')
    return sorted(live)

def support_reference(seed, orientation, adj):
    """Checker: recompute all current degrees from induced neighbor sets."""
    quotas = (254,253) if orientation == 0 else (253,254)
    live = set(range(N))
    keys = [tie(seed,v) for v in range(N)]
    while len(live) > 508:
        counts = [sum(0 < v < 1066 for v in live), sum(v >= 1066 for v in live)]
        candidates = [v for v in live-PINS if counts[half(v)] > quotas[half(v)]]
        v = min(candidates, key=lambda v:(len(adj[v]&live),keys[v],v))
        live.remove(v)
    return sorted(live)

def induced(vertices, edges):
    selected = set(vertices)
    return [(u,v) for u,v in edges if u in selected and v in selected]

def check_word(vertices, edges, word, colours):
    require(type(word) is str and len(word) == len(vertices), 'word length')
    require(set(word) <= set(map(str,range(colours))), 'word palette')
    values = dict(zip(vertices, map(int,word)))
    require(all(values[u] != values[v] for u,v in edges), 'monochromatic edge')
    return values

def components(vertices, adj, removed=frozenset()):
    unseen = set(vertices)-set(removed)
    result = []
    while unseen:
        root = min(unseen); unseen.remove(root); stack = [root]; block = []
        while stack:
            u = stack.pop(); block.append(u)
            found = adj[u]&unseen; unseen.difference_update(found); stack.extend(found)
        result.append(sorted(block))
    return sorted(result,key=lambda x:(-len(x),x))
