"""Relabeling and malformed-native-input controls, independent of author tests."""
import argparse
import json
from pathlib import Path
import random
import subprocess
from check import canonical, require
from point_maps import maps, structure


def controls(exact, quotient, executable, work):
    work.mkdir(parents=True, exist_ok=True)
    codes = {r["code_sha256"]: r["blocks"] for r in exact["equality"]}
    rng = random.Random(20261001)
    relabelings = 0
    for cls in quotient["classes"]:
        words = codes[cls["representative"]]
        perm = list(range(18))
        rng.shuffle(perm)
        moved = sorted(sum(1 << perm[i] for i in range(18) if w & (1 << i)) for w in words)
        found, _ = maps(structure(words), structure(moved))
        require(found == [perm], "arbitrary point relabeling/inverse uniqueness")
        relabelings += 1
    rejected = 0
    good = exact["equality"][0]["blocks"]
    paths = []
    for name, content in [("bad-weight", "0\n"), ("duplicate", f"{good[0]} {good[0]}\n"),
                          ("out-of-range", "1048575\n"), ("negative", "-1\n"),
                          ("parse", "invalid\n"), ("oversized", " ".join(map(str, [good[0]] * 257)) + "\n"),
                          ("valid", " ".join(map(str, good)) + "\n")]:
        p = work / (name + ".txt")
        p.write_text(content)
        paths.append(p)
    bad_calls = [["--words", 1, p] for p in paths[:-1]]
    bad_calls += [["--words", 0, paths[-1]], ["--words", 68, paths[-1]],
                  ["--words", 1, work / "absent.txt"], [46, paths[-1]], []]
    for args in bad_calls:
        r = subprocess.run([str(executable), *map(str, args)], capture_output=True, text=True, timeout=5)
        require(r.returncode != 0 and '"status":"COMPLETE"' not in r.stdout, "malformed native input accepted")
        rejected += 1
    return {"status": "COMPLETE", "arbitrary_full_point_relabelings": relabelings,
            "malformed_native_rejections": rejected}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("exact", type=Path)
    parser.add_argument("quotient", type=Path)
    parser.add_argument("--executable", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    obj = controls(json.loads(args.exact.read_text()), json.loads(args.quotient.read_text()),
                   args.executable.resolve(), args.work)
    args.output.write_bytes(canonical(obj))
    print(json.dumps(obj))
