#!/usr/bin/env python3
"""Exact finite diagnostics; does not decide good43. CPython 3.11, stdlib."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import tarfile

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decode(raw):
    raw = raw.rstrip(b"\r\n")
    require(raw and 63 <= raw[0] <= 125, "short graph6 order required")
    n = raw[0] - 63
    pairs = n * (n - 1) // 2
    require(len(raw) == 1 + (pairs + 5) // 6, "graph6 length")
    require(all(63 <= x <= 126 for x in raw), "graph6 byte")
    if pairs % 6:
        require((raw[-1] - 63) % (1 << (6 - pairs % 6)) == 0, "padding")
    adj = [0] * n
    k = 0
    for j in range(1, n):
        for i in range(j):
            if ((raw[1 + k // 6] - 63) >> (5 - k % 6)) & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return adj


def has_clique(adj, k, candidates=None):
    if candidates is None:
        candidates = (1 << len(adj)) - 1
    if k == 0:
        return True
    while candidates.bit_count() >= k:
        bit = candidates & -candidates
        candidates ^= bit
        if has_clique(adj, k - 1, candidates & adj[bit.bit_length() - 1]):
            return True
    return False


def complement(adj):
    full = (1 << len(adj)) - 1
    return [full ^ row ^ (1 << i) for i, row in enumerate(adj)]


def good(adj, clique=5, independent=5):
    return not has_clique(adj, clique) and not has_clique(complement(adj), independent)


def missing_pairs(adj):
    return sum(not (adj[i] & adj[j]) for i, j in itertools.combinations(range(len(adj)), 2))


def check_fixture(record):
    adj = decode(record["graph6"].encode("ascii"))
    n = len(adj)
    require(n == record["n"], "order mismatch")
    e = sum(row.bit_count() for row in adj) // 2
    require(e == record["e"], "edge mismatch")
    require(good(adj, 4, 5), "not a (4,5) graph")
    require(missing_pairs(adj) == 0, "pair-common-neighbor failure")
    independent4 = []
    for vertices in itertools.combinations(range(n), 4):
        mask = sum(1 << v for v in vertices)
        if all(not (adj[v] & mask) for v in vertices):
            independent4.append(mask)
    supports = [adj[h] | (1 << h) for h in range(n)]
    for support in supports:
        require(all(support & row for row in adj), "not total dominating")
        require(all(support & mask for mask in independent4), "misses an I4")
    require(all(x & y for x in supports for y in supports), "support intersection")
    full = (1 << n) - 1
    for support in supports:
        # Original H, red-universal root n, and one outside vertex n+1.
        ext = [row | (1 << n) | ((1 << (n + 1)) if (support >> i) & 1 else 0)
               for i, row in enumerate(adj)] + [full, support]
        require(good(ext), "one-attachment graph is not Ramsey-valid")
    return {"n": n, "e": e, "missing_pairs": 0,
            "independent_four_sets": len(independent4),
            "valid_closed_neighborhood_supports": n,
            "checked_single_attachment_graphs": n}


def check_census(tar_path, catalog24_path):
    expected = json.loads((HERE / "CENSUS.json").read_text())
    archive = Path(tar_path).read_bytes()
    require(hashlib.sha256(archive).hexdigest() == expected["tar_sha256"], "tar hash")
    raw24 = Path(catalog24_path).read_bytes()
    require(hashlib.sha256(raw24).hexdigest() == expected["catalog24_sha256"], "catalog24 hash")
    actual = []
    with tarfile.open(tar_path) as archive:
        for record in expected["records"]:
            n, e = record["n"], record["e"]
            if n < 24:
                raw = archive.extractfile(record["source_member"]).read()
                require(hashlib.sha256(raw).hexdigest() == record["source_sha256"], "member hash")
                lines = raw.splitlines()
            else:
                lines = [line for line in raw24.splitlines()
                         if sum((x - 63).bit_count() for x in line[1:]) == e]
            require(len(lines) == record["records"], "census size")
            for line in lines:
                adj = decode(line)
                require(len(adj) == n and sum(x.bit_count() for x in adj) == 2 * e, "census order/edges")
                require(missing_pairs(adj) == 0, "census P2 failure")
            actual.append({"n": n, "e": e, "records": len(lines), "P2_records": len(lines)})
    return actual


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-tar")
    parser.add_argument("--catalog24")
    parser.add_argument("--record-expected", action="store_true", help="write initial compact output")
    args = parser.parse_args()
    require(bool(args.catalog_tar) == bool(args.catalog24), "supply both catalog paths")
    # Small controls distinguish Ramsey validity from the pair condition.
    c5 = [(1 << ((v - 1) % 5)) | (1 << ((v + 1) % 5)) for v in range(5)]
    require(good(c5, 4, 5) and missing_pairs(c5) == 5, "C5 control")
    k4 = [15 ^ (1 << v) for v in range(4)]
    require(not good(k4, 4, 5) and missing_pairs(k4) == 0, "K4 control")
    rows = [check_fixture(r) for r in json.loads((HERE / "WITNESSES.json").read_text())["records"]]
    result = {"status": "NEGATIVE_METHOD_DIAGNOSTICS_VERIFIED", "witnesses": rows,
              "physical_single_attachments": sum(r["checked_single_attachment_graphs"] for r in rows),
              "good43_constructed": False, "complete_good43_classes_excluded": 0,
              "trial_gate_met": False, "external_review": False}
    expected_path = HERE / "EXPECTED.json"
    if args.record_expected:
        expected_path.write_text(json.dumps(result, indent=2) + "\n")
    else:
        require(result == json.loads(expected_path.read_text()), "expected output mismatch")
        manifest = json.loads((HERE / "MANIFEST.json").read_text())
        for name, digest in manifest.items():
            require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, "manifest " + name)
    if args.catalog_tar:
        result["optional_top_edge_census"] = check_census(args.catalog_tar, args.catalog24)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
