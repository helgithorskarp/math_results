#!/usr/bin/env python3
"""Rebuild and independently verify all 238 compact UP refutations."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
INPUT = (HERE.parent / "ramsey_r55_cyclic43_q13_boundary_certificate" /
         "objective-twelve-component-fast.json")
INPUT_SHA256 = "4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(command, check=True):
    return subprocess.run(command, check=check, capture_output=True, text=True)


def reject(command, message):
    result = run(command, check=False)
    need(result.returncode != 0, message)


def reproduce(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    need(sha256(INPUT) == INPUT_SHA256, "pinned cyclic input")
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in manifest.items():
        need(sha256(HERE / name) == digest, "source identity " + name)
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    versions = json.loads((HERE / "VERSIONS.json").read_text())
    compiler = run(["g++", "--version"]).stdout.splitlines()[0]
    need(compiler == versions["compiler"], "compiler version")

    common = ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", "-Wconversion",
              "-Wshadow", "-Werror", "-pthread"]
    release = destination / "classify_up"
    sanitized = destination / "classify_up_san"
    run(["g++", *common, "-O3", "-DNDEBUG", str(HERE / "classify_up.cpp"),
         "-o", str(release)])
    run(["g++", *common, "-O1", "-g", "-fsanitize=address,undefined",
         "-fno-omit-frame-pointer", str(HERE / "classify_up.cpp"),
         "-o", str(sanitized)])

    generated = {}
    generator_outputs = {}
    for label, program in (("release", release), ("sanitized", sanitized)):
        census = destination / f"{label}-census.tsv"
        proof = destination / f"{label}-proof.tsv"
        result = run([str(program), str(INPUT), str(census), str(proof)])
        need(census.read_bytes() == (HERE / "CENSUS.tsv").read_bytes(),
             label + " census")
        need(proof.read_bytes() == (HERE / "PROOF.tsv").read_bytes(),
             label + " proof")
        generated[label] = (census, proof)
        generator_outputs[label] = result.stdout.strip()

    verification = {}
    for label, flags in (("normal", []), ("optimized", ["-O"])):
        result = run([sys.executable, *flags, "-B", str(HERE / "verify.py"),
                      str(INPUT), *map(str, generated["release"])])
        receipt = json.loads(result.stdout)
        need(receipt == expected["verification"], label + " verification")
        verification[label] = receipt

    bad_census = destination / "bad-census.tsv"
    lines = (HERE / "CENSUS.tsv").read_text().splitlines()
    fields = lines[1].split("\t")
    fields[4] = str(int(fields[4]) + 1)
    lines[1] = "\t".join(fields)
    bad_census.write_text("\n".join(lines) + "\n")
    reject([sys.executable, "-B", str(HERE / "verify.py"), str(INPUT),
            str(bad_census), str(HERE / "PROOF.tsv")],
           "altered census accepted")

    bad_witness = destination / "bad-witness.tsv"
    lines = (HERE / "PROOF.tsv").read_text().splitlines()
    fields = lines[1].split("\t")
    fields[-1] = "43"
    lines[1] = "\t".join(fields)
    bad_witness.write_text("\n".join(lines) + "\n")
    reject([sys.executable, "-B", str(HERE / "verify.py"), str(INPUT),
            str(HERE / "CENSUS.tsv"), str(bad_witness)],
           "altered witness accepted")

    missing_conflict = destination / "missing-conflict.tsv"
    lines = (HERE / "PROOF.tsv").read_text().splitlines()
    need(lines[-1].split("\t")[2] == "CONFLICT", "proof final row")
    missing_conflict.write_text("\n".join(lines[:-1]) + "\n")
    reject([sys.executable, "-B", str(HERE / "verify.py"), str(INPUT),
            str(HERE / "CENSUS.tsv"), str(missing_conflict)],
           "missing terminal conflict accepted")

    answer = {
        "status": "REPRODUCED_ALL_238_DEFECT_SUPPORT_FAMILIES_UP_UNSAT",
        "source_representatives": 238,
        "families_closed": 238,
        "families_open": 0,
        "generator_outputs": generator_outputs,
        "normal_and_optimized_verification": verification,
        "release_and_sanitized_outputs_identical": True,
        "deliberate_corruptions_rejected": 3,
        "compiler": compiler,
        "python": sys.version,
    }
    (destination / "RECEIPT.json").write_text(
        json.dumps(answer, indent=2, sort_keys=True) + "\n")
    print(json.dumps(answer, sort_keys=True))
    return answer


if __name__ == "__main__":
    need(len(sys.argv) == 2, "usage: reproduce.py FRESH_OUTPUT_DIRECTORY")
    reproduce(sys.argv[1])
