#!/usr/bin/env python3
"""Fetch pinned external evidence, rebuild the CNF, independently audit/replay.

The external generator is used only after its hash is checked. Its numeric
edge-variable labels are an untrusted input to the independent C++ checker.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--drat-trim", default=os.environ.get("DRAT_TRIM", "drat-trim"))
    ap.add_argument("--cxx", default=os.environ.get("CXX", "g++"))
    args = ap.parse_args()
    work = args.work.resolve()
    if work == HERE.parent or HERE.parent in work.parents:
        raise ValueError("keep generated files outside the repository")
    work.mkdir(exist_ok=True, parents=True)
    manifest = json.loads((HERE/"result.json").read_text())
    started = time.monotonic()
    for relative, expected in manifest["external_files"].items():
        target = work/"external"/relative
        if not target.exists():
            url = ("https://raw.githubusercontent.com/wustep/maths/" +
                   manifest["external_source_commit"] + "/" + relative)
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read(expected["bytes"]+1)
            if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
                raise RuntimeError(f"download mismatch: {relative}")
            target.parent.mkdir(exist_ok=True, parents=True)
            target.write_bytes(data)
        if target.stat().st_size != expected["bytes"] or sha(target) != expected["sha256"]:
            raise RuntimeError(f"cached input mismatch: {relative}")
    print("PASS all_four_external_inputs_match_pinned_hashes=true", flush=True)
    source = work/"external/problems/ramsey-r55/compute/q2/orbit_sat.py"
    spec = importlib.util.spec_from_file_location("external_orbit_encoder", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    obj = module.OrbitEncoding(43,5,7)
    obj.build(True,3,False,False,True)
    formula = work/"p5_c7_k3.cnf"
    module.write_dimacs(obj, formula)
    if sha(formula) != manifest["cnf_sha256"]:
        raise RuntimeError("regenerated CNF hash mismatch")
    print("PASS regenerated_cnf_sha256=" + sha(formula), flush=True)
    labels = work/"edge_labels.tsv"
    labels.write_text("".join(str(value)+" "+" ".join(map(str,key))+"\n"
        for key,value in sorted(obj.enc.names.items(), key=lambda pair: pair[1])))
    subprocess.run([sys.executable,str(HERE/"audit_reductions.py")],check=True)
    binary = work/"independent_formula"
    subprocess.run([args.cxx,"-O3","-std=c++20","-Wall","-Wextra","-Wpedantic",
                    str(HERE/"independent_formula.cpp"),"-o",str(binary)],check=True)
    subprocess.run([str(binary),str(labels),str(formula)],check=True)
    proof = work/"p5_c7_k3.drat"
    compressed = work/"external/problems/ramsey-r55/compute/q4/certs/proofs/p5_c7_k3.drat.gz"
    with gzip.open(compressed,"rb") as src, proof.open("wb") as out:
        shutil.copyfileobj(src,out)
    if proof.stat().st_size != manifest["proof_bytes"] or sha(proof) != manifest["proof_sha256"]:
        raise RuntimeError("uncompressed proof mismatch")
    replay_log = work/"replay.log"
    with replay_log.open("w") as out:
        replay = subprocess.run([args.drat_trim,str(formula),str(proof)],
                                stdout=out,stderr=subprocess.STDOUT)
    if replay.returncode != 0 or "s VERIFIED" not in replay_log.read_text().splitlines():
        raise RuntimeError("DRAT replay did not verify")
    print("PASS stored_external_DRAT_replay=VERIFIED", flush=True)
    record = {"external_source_commit":manifest["external_source_commit"],
              "cnf_sha256":sha(formula),"proof_sha256":sha(proof),
              "independent_formula_check":True,"DRAT_replay":"VERIFIED",
              "elapsed_seconds":round(time.monotonic()-started,3)}
    (work/"reproduction.json").write_text(json.dumps(record,indent=2)+"\n")
    print("PASS type_1^8_5^7_excluded_external_result_independently_reproduced=true")


if __name__ == "__main__":
    main()
