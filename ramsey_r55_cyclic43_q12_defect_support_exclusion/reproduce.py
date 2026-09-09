#!/usr/bin/env python3
"""Rebuild the complete census, family formula, and compact physical core."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
INPUT = (HERE.parent / "ramsey_r55_cyclic43_q13_boundary_certificate" /
         "objective-twelve-component-fast.json")


def need(test, message):
    if not test:
        raise ValueError(message)


def run(command, check=True):
    return subprocess.run(command, check=check, capture_output=True, text=True)


def same(left, right, message):
    need(Path(left).read_bytes() == Path(right).read_bytes(), message)


def reproduce(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, expected in manifest.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        need(actual == expected, "source identity " + name)
    versions = json.loads((HERE / "VERSIONS.json").read_text())
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    compiler = run(["g++", "--version"]).stdout.splitlines()[0]
    need(compiler == versions["compiler"], "compiler version")

    common = ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", "-Wconversion",
              "-Wshadow", "-Werror", "-pthread"]
    programs = {}
    for stem in ("select_support", "verify_support_selection"):
        release = destination / stem
        sanitized = destination / (stem + "_san")
        run(["g++", *common, "-O3", "-DNDEBUG", str(HERE / (stem + ".cpp")),
             "-o", str(release)])
        run(["g++", *common, "-O1", "-g", "-fsanitize=address,undefined",
             "-fno-omit-frame-pointer", str(HERE / (stem + ".cpp")),
             "-o", str(sanitized)])
        programs[stem] = (release, sanitized)

    primary_census = destination / "support-census.tsv"
    primary = run([str(programs["select_support"][0]), str(INPUT),
                   str(primary_census)])
    same(primary_census, HERE / "SUPPORT_CENSUS.tsv", "release census")
    census_rows = list(csv.DictReader(primary_census.open(), delimiter="\t"))
    support_histogram = Counter(int(row["support_edges"]) for row in census_rows)
    need({str(k): support_histogram[k] for k in sorted(support_histogram)} ==
         expected["support_histogram"], "support histogram")
    independent = run([str(programs["verify_support_selection"][0]), str(INPUT),
                       str(primary_census)])
    sanitized_census = destination / "support-census-sanitized.tsv"
    sanitized_primary = run([str(programs["select_support"][1]), str(INPUT),
                             str(sanitized_census)])
    same(sanitized_census, HERE / "SUPPORT_CENSUS.tsv", "sanitized census")
    sanitized_independent = run([str(programs["verify_support_selection"][1]),
                                 str(INPUT), str(sanitized_census)])

    expected_outputs = ["family.cnf", "core.cnf", "certificate.json", "family.json"]
    python_receipts = {}
    for label, flags in (("normal", []), ("optimized", ["-O"])):
        out = destination / label
        out.mkdir()
        paths = [out / name for name in expected_outputs]
        built = run([sys.executable, *flags, "-B", str(HERE / "build_family.py"),
                     str(INPUT), *map(str, paths)])
        for name, path in zip(expected_outputs, paths):
            same(path, HERE / name, label + " output " + name)
        checked = run([sys.executable, *flags, "-B", str(HERE / "verify.py"),
                       str(INPUT), str(primary_census), *map(str, paths)])
        built_json = json.loads(built.stdout)
        checked_json = json.loads(checked.stdout)
        for key, value in expected["family"].items():
            need(built_json[key] == value, label + " family field " + key)
        need(checked_json == expected["verification"], label + " verification")
        python_receipts[label] = {
            "builder": {key: built_json[key] for key in expected["family"]},
            "checker": checked_json,
        }

    bad_certificate = json.loads((HERE / "certificate.json").read_text())
    bad_certificate["forced_red_edges"][0]["blue_five_witness"] = [0, 1, 2, 3, 4]
    bad_path = destination / "bad-certificate.json"
    bad_path.write_text(json.dumps(bad_certificate) + "\n")
    rejected = run([sys.executable, "-B", str(HERE / "verify.py"), str(INPUT),
                    str(primary_census), str(HERE / "family.cnf"),
                    str(HERE / "core.cnf"), str(bad_path),
                    str(HERE / "family.json")], check=False)
    need(rejected.returncode != 0, "certificate corruption accepted")

    bad_census = destination / "bad-census.tsv"
    lines = (HERE / "SUPPORT_CENSUS.tsv").read_text().splitlines()
    columns = lines[52].split("\t")
    need(columns[0] == "51" and columns[-1] == "60", "census control row")
    columns[-1] = "61"
    lines[52] = "\t".join(columns)
    bad_census.write_text("\n".join(lines) + "\n")
    rejected_census = run([str(programs["verify_support_selection"][0]), str(INPUT),
                           str(bad_census)], check=False)
    need(rejected_census.returncode != 0, "census corruption accepted")

    answer = {
        "status": "REPRODUCED_CYCLIC_Q12_DEFECT_SUPPORT_FAMILY_EXCLUSION",
        "source_representatives": 238,
        "selected_source": 51,
        "support_edges": 60,
        "assignments_excluded": 1 << 60,
        "physical_core_clauses": 61,
        "solver_calls": 0,
        "release_primary": primary.stdout.strip(),
        "release_independent": independent.stdout.strip(),
        "sanitized_primary": sanitized_primary.stdout.strip(),
        "sanitized_independent": sanitized_independent.stdout.strip(),
        "normal_and_optimized_python": python_receipts,
        "deliberate_corruptions_rejected": 2,
        "python": sys.version,
        "compiler": compiler,
    }
    (destination / "RECEIPT.json").write_text(
        json.dumps(answer, indent=2, sort_keys=True) + "\n")
    print(json.dumps(answer, sort_keys=True))
    return answer


if __name__ == "__main__":
    need(len(sys.argv) == 2, "usage: reproduce.py FRESH_OUTPUT_DIRECTORY")
    reproduce(sys.argv[1])
