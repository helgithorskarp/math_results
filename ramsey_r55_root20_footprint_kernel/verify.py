#!/usr/bin/env python3
"""No producer imports: literal cliques, upward closure and triangle-free DFS."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def check(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def upper_closure(seeds):
    bad = bytearray(1 << 20)
    full = (1 << 20) - 1
    for seed in seeds:
        remaining = full ^ seed
        subset = remaining
        while True:
            bad[seed | subset] = 1
            if subset == 0:
                break
            subset = (subset - 1) & remaining
    return bad


def compare_file(path, domains):
    with path.open() as source:
        for t, masks in domains.items():
            for s in masks:
                check(source.readline() == f"{t} {s:05x}\n", "domain entry mismatch")
        check(source.read() == "", "domain trailing content")


def audit(work):
    graph_bytes = (HERE / "GRAPH.json").read_bytes()
    check(sha(graph_bytes) == "8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf", "input identity")
    doc = json.loads(graph_bytes)
    red = set(tuple(e) for e in doc["red_edges"])
    check(doc["n"] == 20 and len(red) == len(doc["red_edges"]) == 92, "graph dimensions")
    check(all(type(u) is int and type(v) is int and 0 <= u < v < 20 for u,v in red), "edge encoding")
    masks = {}
    for color, k in ((True,3),(False,3),(True,4),(False,4),(False,5)):
        masks[color,k] = [sum(1 << v for v in q) for q in combinations(range(20),k)
                          if all((e in red) == color for e in combinations(q,2))]
    check(not masks[True,4] and not masks[False,5], "core Ramsey conditions")
    # Exact increasing-vertex recursion visits every red-triangle-free set once.
    free_sets = []
    def visit(chosen, start):
        s = sum(1 << i for i in chosen)
        check(any(s & q == 0 for q in masks[False,4]), "a Ramsey(4,5) extension exists")
        free_sets.append(s)
        for v in range(start,20):
            neighbors = [u for u in chosen if (u,v) in red]
            if not any((u,w) in red for u,w in combinations(neighbors,2)):
                visit(chosen + (v,), v+1)
    visit((),0)
    # Different algorithm from the producer: mark literal forbidden supersets.
    b4, b3 = upper_closure(masks[False,4]), upper_closure(masks[False,3])
    full = (1 << 20) - 1
    domains = {t: [s for s in range(t,1 << 20,4) if not b4[full ^ s]] for t in (1,2,3)}
    minimal = {}
    for t, ds in domains.items():
        pool = set(ds)
        minimal[t] = [s for s in ds if all((s ^ (1 << i)) not in pool
                       for i in range(2,20) if s >> i & 1)]
    compare_file(work / "domains.txt", domains)
    compare_file(work / "minimal.txt", minimal)
    report = json.loads((work / "analysis.json").read_text())
    expected = {"graph_sha256":sha(graph_bytes), "n":20, "red_edges":92,
                "red_triangles":len(masks[True,3]), "blue_triangles":len(masks[False,3]),
                "blue_four_cliques":len(masks[False,4]), "subsets_checked":1 << 20,
                "ramsey45_extension_masks":[], "domain_sizes":{str(t):len(ds) for t,ds in domains.items()},
                "minimal_domain_sizes":{str(t):len(ds) for t,ds in minimal.items()},
                "domain_size_histograms":{str(t):{str(k):v for k,v in sorted(Counter(s.bit_count() for s in ds).items())} for t,ds in domains.items()},
                "identical_footprint_blue_allowed":{str(t):sum(not b3[full ^ s] for s in ds) for t,ds in domains.items()},
                "identical_footprint_red_allowed":{str(t):0 for t in domains},
                "claim":"H20 has no Ramsey(4,5;21) vertex extension; exact one/two-outside-vertex interface only",
                "full_43_extension_decided":False}
    for name in ("domains.txt", "minimal.txt"):
        expected[name + "_sha256"] = sha((work / name).read_bytes())
    check(report == expected, "analysis report mismatch")
    result = {"status":"VERIFIED_LOCAL_NONEXTENSION_AND_EXACT_DOMAINS_NOT_43_EXTENSION",
              "triangle_free_subsets_exhausted":len(free_sets),
              "triangle_free_subsets_sha256":sha("".join(f"{s:05x}\n" for s in sorted(free_sets)).encode()),
              "domain_entries_compared":sum(map(len,domains.values())),
              "minimal_entries_compared":sum(map(len,minimal.values())),
              "analysis_sha256":sha((work / "analysis.json").read_bytes())}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work",type=Path,required=True)
    parser.add_argument("--report",type=Path,required=True)
    args = parser.parse_args()
    result = audit(args.work)
    args.report.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()
