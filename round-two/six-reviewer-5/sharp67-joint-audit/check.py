"""six-reviewer-5: cold independent sharp-67 audit; Python standard library only.

The reviewed 46-type classification is an explicit mathematical premise.
No author module, native executable, private carrier or execution seal is loaded.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import resource
import subprocess
import time

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def canonical(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def decode(word):
    require(type(word) is int and 0 <= word < 2**18, "word domain")
    result = frozenset(i for i in range(18) if word & (1 << i))
    require(len(result) == 5, "word weight")
    return result


def packing(words, length, degrees=None):
    require(len(words) == length and len(set(words)) == length, "word count/duplicate")
    points = [decode(w) for w in words]
    triples = [t for block in points for t in combinations(sorted(block), 3)]
    require(len(triples) == len(set(triples)) == 10 * length, "repeated triple")
    deg = [sum(v in block for block in points) for v in range(18)]
    pair = [sum({a, b} <= block for block in points) for a, b in [(17, 15), (17, 16), (15, 16)]]
    if degrees is not None:
        require([deg[i] for i in (17, 15, 16)] == degrees, "center degree")
        require(pair == [5, 5, 4], "center pair multiplicity")
        require((15, 16, 17) not in set(triples), "covered center triple")
    return {"degree_histogram": dict(sorted(Counter(deg).items())), "triples": len(triples), "pair": pair}


def stars(census):
    """Reconstruct private x quadruples as injections, not a clique helper.

    Four distinct rows are chosen, then four distinct column images.
    Keep injections whose four cells exist, and sort their literal point tuples.
    """
    output = []
    for model_id, model in enumerate(census["models"]):
        lengths = model["cycle_half_lengths"]
        require(lengths in ([5], [2, 3]), "anchor form")
        missing = set()
        offset = 0
        for length in lengths:
            for row in range(length):
                missing.add((offset + row, offset + row))
                missing.add((offset + row, offset + (row + 1) % length))
            offset += length
        cells = [(a, b) for a in range(5) for b in range(5) if (a, b) not in missing]
        require(len(cells) == 15, "cell count")
        labels = {p: i for i, p in enumerate(cells)}
        rows = [sum(1 << i for i, (a, b) in enumerate(cells) if a == r) for r in range(5)]
        cols = [sum(1 << i for i, (a, b) in enumerate(cells) if b == r) for r in range(5)]
        tuples = set()
        for rr in combinations(range(5), 4):
            for cc in permutations(range(5), 4):
                pairs = tuple(zip(rr, cc))
                if all(pair in labels for pair in pairs):
                    tuples.add(tuple(sorted(labels[pair] for pair in pairs)))
        quad = [sum(1 << i for i in q) for q in sorted(tuples)]
        direct = [sum(1 << i for i in q) for q in combinations(range(15), 4)
                  if len({cells[i][0] for i in q}) == len({cells[i][1] for i in q}) == 4]
        require(quad == direct and len(quad) == model["candidate_count"], "input decoding")
        for mark, rep in enumerate(model["marked_classes"]):
            require(len(rep["clique"]) == len(set(rep["clique"])) == 9, "marked representative")
            private = [quad[i] for i in rep["clique"]]
            words = sorted([r | 1 << 15 | 1 << 17 for r in rows] +
                           [r | 1 << 16 | 1 << 17 for r in cols] +
                           [r | 1 << 17 for r in private])
            packing(words, 19)
            links = [decode(w) - {17} for w in words]
            rho = {i: sum(i in q for q in links) for i in range(17)}
            saturated = [i for i, d in rho.items() if d == 5]
            m = sum(not any({i, j} <= q for q in links) for i, j in combinations(saturated, 2))
            require(m == rep["low_low_pairs"], "marked leave statistic")
            require(rho[15] == rho[16] == 5 and not any({15, 16} <= q for q in links), "eligible mark")
            output.append({"case": len(output), "model": model_id, "marked": mark, "m": m, "words": words})
    require(len(output) == 46, "all marked input cases")
    return output


def run(executable, args, timeout):
    p = subprocess.run([str(executable), *map(str, args)], capture_output=True, text=True, timeout=timeout)
    require(p.returncode == 0, "INCOMPLETE native child: " + p.stderr[:400])
    obj = json.loads(p.stdout)
    require(obj.get("status") == "COMPLETE", "native incomplete output")
    return obj


def residual(core, cert):
    require(digest(core) == cert["core_sha256"], "core/certificate binding")
    packing(core, 45, [19, 20, 20])
    occupied = {t for word in core for t in combinations(sorted(decode(word)), 3)}
    points = [frozenset(q) for q in combinations(range(15), 5)
              if not any(t in occupied for t in combinations(q, 3))]
    # Independent definition-level cross-check of the entire universe.
    literal = [frozenset(q) for q in combinations(range(15), 5)
               if all(len(frozenset(q) & decode(w)) <= 2 for w in core)]
    require(points == literal, "residual universe mismatch")
    candidates = [sum(1 << i for i in q) for q in points]
    tuples = [sorted(q) for q in points]
    require(len(candidates) == cert["candidate_count"] and digest(tuples) == cert["candidate_sha256"], "residual candidate binding")
    require(cert["tree"]["kind"] == "color", "expected proper-color certificate")
    colors = cert["tree"]["colors"]
    limit = cert["limit"]
    require(type(limit) is int and 1 <= limit <= 22 and len(colors) == len(points), "color count")
    require(all(type(c) is int and 0 <= c < limit for c in colors), "color domain")
    require(set(colors) == set(range(limit)), "unused color convention")
    edges = 0
    for i, j in combinations(range(len(points)), 2):
        if len(points[i] & points[j]) <= 2:
            require(colors[i] != colors[j], "improper color")
            edges += 1
    return candidates, {"core_sha256": digest(core), "candidate_sha256": digest(tuples),
                        "candidate_count": len(candidates), "edges": edges, "limit": limit}


def corruptions(cores, certs, witness):
    failures = 0
    def reject(action):
        nonlocal failures
        try:
            action()
        except (ValueError, KeyError, IndexError, TypeError):
            failures += 1
            return
        raise ValueError("damaged evidence accepted")
    cert = copy.deepcopy(certs[0]); core = cores[cert["core_sha256"]]
    for changed in ["hash", "count", "short", "domain", "conflict"]:
        bad = copy.deepcopy(cert)
        if changed == "hash": bad["candidate_sha256"] = "0" * 64
        elif changed == "count": bad["candidate_count"] += 1
        elif changed == "short": bad["tree"]["colors"].pop()
        elif changed == "domain": bad["tree"]["colors"][0] = bad["limit"]
        else: bad["tree"]["colors"] = [0] * bad["candidate_count"]
        reject(lambda: residual(core, bad))
    for changed in ["duplicate", "weight", "triple", "degree"]:
        words = list(witness["blocks"])
        if changed == "duplicate": words[0] = words[1]
        elif changed == "weight": words[0] = 0
        elif changed == "triple": words[0] = (1 << 15) | (1 << 16) | (1 << 17) | 3
        else: words = [((w & ~(1 << 17) & ~(1 << 15)) | ((w >> 17 & 1) << 15) | ((w >> 15 & 1) << 17)) for w in words]
        reject(lambda: packing(words, 67, [19, 20, 20]))
    return failures


def audit(work, executable, reuse=False):
    begun = time.monotonic()
    work.mkdir(parents=True, exist_ok=True)
    input_manifest = json.loads((HERE / "INPUTS.json").read_text())
    for rec in input_manifest["files"]:
        require(hashlib.sha256((HERE / rec["local"]).read_bytes()).hexdigest() == rec["sha256"], "source input hash")
    expected = json.loads((HERE / "expected.json").read_text())
    cases = stars(json.loads((HERE / "census.json").read_text()))
    controls = run(executable, ["--controls"], 20)
    results, all_cores, compact = [], [], []
    for case in cases:
        k = case["case"]
        source = work / f"input-{k}.txt"
        source.write_text(" ".join(map(str, case["words"])) + "\n")
        output = work / f"case-{k}.json"
        # Reuse is only a local ancillary-stage convenience. The default is cold.
        if reuse:
            obj = json.loads(output.read_text())
        else:
            obj = run(executable, [k, source], 65)
            output.write_bytes(canonical(obj))
        ref = expected["cases"][k]
        require(obj["status"] == "COMPLETE" and obj["case"] == k, "case completion")
        require(obj["triples"] == ref["triples"] and obj["covers"] == ref["covers"], "tail coverage")
        require(obj["y_eleven"] == ref["counts"]["y_eleven"] and obj["z_eleven"] == ref["counts"]["z_eleven"], "complete center counts")
        require(obj["carrier_sha256"] == ref["carrier_sha256"], "entrywise candidate/solution transcript mismatch")
        require(len(obj["cores"]) == ref["joint_count"] and digest(obj["cores"]) == ref["joints_sha256"], "literal joint output mismatch")
        for core in obj["cores"]:
            require(digest(core["blocks"]) == core["core_sha256"], "core digest")
            packing(core["blocks"], 45, [19, 20, 20])
        all_cores.extend(obj["cores"])
        results.append(obj)
        compact.append({**{a: obj[a] for a in ("case", "covers", "triples", "y_eleven", "z_eleven", "y_nodes", "z_nodes", "peak_query_nodes", "carrier_sha256")},
                        "model": case["model"], "marked": case["marked"], "m": case["m"], "joints_sha256": digest(obj["cores"])})
        print(json.dumps({"case": k, "status": "COMPLETE", "seconds": obj["seconds"], "cores": len(obj["cores"])}), flush=True)
    require(len(all_cores) == 77 and len({r["core_sha256"] for r in all_cores}) == 77, "all distinct cores")
    cores = {r["core_sha256"]: r["blocks"] for r in all_cores}
    certs = json.loads((HERE / "residual.json").read_text())["certificates"]
    require(len(certs) == 77 and {r["core_sha256"] for r in certs} == set(cores), "exact certificate coverage")
    residuals, equality = [], []
    for cert in certs:
        core = cores[cert["core_sha256"]]
        candidates, rec = residual(core, cert)
        residuals.append(rec)
        if cert["limit"] == 22:
            path = work / (cert["core_sha256"] + "-residual.txt")
            path.write_text(" ".join(map(str, candidates)) + "\n")
            obj = run(executable, ["--words", 22, path], 25)
            for choice in obj["solutions"]:
                require(len(choice) == len(set(choice)) == 22 and all(type(i) is int and 0 <= i < len(candidates) for i in choice), "extremal indices")
                words = sorted(core + [candidates[i] for i in choice])
                stat = packing(words, 67, [19, 20, 20])
                equality.append({"core_sha256": cert["core_sha256"], "residual_indices": choice, "blocks": words,
                                 "code_sha256": digest(words), **stat})
    witness = json.loads((HERE / "witness67.json").read_text())
    require(digest(witness["core_blocks"]) == witness["core_sha256"] and witness["core_sha256"] in cores, "witness core binding")
    require(witness["core_blocks"] == cores[witness["core_sha256"]], "witness census equality")
    stat = packing(witness["blocks"], 67, [19, 20, 20])
    require(any(r["blocks"] == witness["blocks"] for r in equality), "witness is enumerated equality case")
    require(set(witness["core_blocks"]) <= set(witness["blocks"]), "witness extension")
    rejections = corruptions(cores, certs, witness)
    result = {"status": "COMPLETE", "reviewer": "six-reviewer-5", "role": "independent mathematical reviewer",
              "cases": compact, "totals": {k: sum(o[k] for o in results) for k in ("covers", "y_eleven", "z_eleven", "y_nodes", "z_nodes")},
              "distinct_cores": len(cores), "residuals": residuals, "capacity_histogram": dict(sorted(Counter(r["limit"] for r in residuals).items())),
              "equality": equality, "equality_count": len(equality), "equality_distinct_codes": len({r["code_sha256"] for r in equality}),
              "witness": stat, "controls": controls, "damaged_evidence_rejections": rejections}
    (work / "exact.json").write_bytes(canonical(result))
    measurement = {"seconds": time.monotonic() - begun, "reuse_census": reuse,
                   "peak_child_RSS_KiB": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   "exact_sha256": digest(result)}
    (work / "measurement.json").write_bytes(canonical(measurement))
    print(json.dumps({"status": "COMPLETE", "totals": result["totals"], "equality_count": len(equality), **measurement}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--executable", required=True, type=Path)
    parser.add_argument("--reuse-census", action="store_true")
    args = parser.parse_args()
    audit(args.work, args.executable.resolve(), args.reuse_census)
