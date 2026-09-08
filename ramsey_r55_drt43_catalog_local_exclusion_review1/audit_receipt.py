#!/usr/bin/env python3
"""Definition-level audit of the h3989 independent result receipt."""

from hashlib import sha256
import argparse
import json
from pathlib import Path


CATALOG_SHA256 = "fde36db6e2e4e07e9c1ec5df32ffc0eb262705393be686fc41a7f31bdc149d6d"
SOURCE_RESULT_SHA256 = "b7043fe5ea23b70277b916b00a226e675499d7d095adbd2167a883000ac3d333"
INDEPENDENT_RESULT_SHA256 = "b70aac40f58e54d5d0995eb015f44be5d73a0cfe04ab7f85e88810f578027402"
RECORDS = 2178
N = 43
RECORD_BITS = N * (N - 1) // 2
SELECTOR_CLAUSES_PER_RECORD = N * (1 + 21 * 20)


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read_catalog(path):
    raw = path.read_bytes()
    need(len(raw) == 1_968_912 and digest(path) == CATALOG_SHA256,
         "catalog byte identity")
    records = raw.decode("ascii").splitlines()
    need(len(records) == len(set(records)) == RECORDS,
         "catalog record coverage")
    for record in records:
        need(len(record) == RECORD_BITS and set(record) <= {"0", "1"},
             "catalog bit record")
        out = [0] * N
        offset = 0
        for first in range(N):
            for second in range(first + 1, N):
                if record[offset] == "1":
                    out[first] |= 1 << second
                else:
                    out[second] |= 1 << first
                offset += 1
        need(all(mask.bit_count() == 21 for mask in out),
             "catalog regularity")
        need(all((out[first] & out[second]).bit_count() == 10
                 for first in range(N) for second in range(first + 1, N)),
             "catalog double regularity")
    return records


def parse_source(path):
    need(digest(path) == SOURCE_RESULT_SHA256, "source result identity")
    lines = path.read_text().splitlines()
    need(lines[0] == "record\troots\tunsat\tclauses\tproof_bytes",
         "source header")
    rows = []
    for index, line in enumerate(lines[1:-1]):
        fields = tuple(map(int, line.split("\t")))
        need(len(fields) == 5 and fields[:3] == (index, N, N),
             "source row")
        rows.append(fields)
    need(len(rows) == RECORDS, "source row count")
    totals = tuple(sum(row[column] for row in rows)
                   for column in range(1, 5))
    need(lines[-1] == "TOTAL\t" + "\t".join(map(str, totals)),
         "source total row")
    need(totals == (93_654, 93_654, 548_087_198, 2_482_356_972),
         "source expected totals")
    return rows


def parse_independent(path, source_rows):
    need(digest(path) == INDEPENDENT_RESULT_SHA256,
         "independent result identity")
    lines = path.read_text().splitlines()
    need(lines[0] == ("record\troots\tbranches_unsat\tbase_clauses\t"
                      "source_clauses\tsource_reported_proof_bytes"),
         "independent header")
    rows = []
    for index, line in enumerate(lines[1:-1]):
        fields = tuple(map(int, line.split("\t")))
        need(len(fields) == 6 and fields[:3] == (index, N, N * 21),
             "independent row coverage")
        source = source_rows[index]
        need(fields[3] + SELECTOR_CLAUSES_PER_RECORD == fields[4]
             == source[3], "per-record clause reconstruction")
        need(fields[5] == source[4], "reported proof-byte transcription")
        rows.append(fields)
    need(len(rows) == RECORDS, "independent row count")
    totals = tuple(sum(row[column] for row in rows)
                   for column in range(1, 6))
    need(lines[-1] == "TOTAL\t" + "\t".join(map(str, totals)),
         "independent total row")
    need(totals == (93_654, 1_966_734, 508_658_864,
                    548_087_198, 2_482_356_972),
         "independent expected totals")
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("source_result", type=Path)
    parser.add_argument("independent_result", type=Path)
    args = parser.parse_args()
    records = read_catalog(args.catalog)
    source_rows = parse_source(args.source_result)
    rows = parse_independent(args.independent_result, source_rows)
    print(json.dumps({
        "base_clauses": sum(row[3] for row in rows),
        "catalog_records": len(records),
        "catalog_sha256": CATALOG_SHA256,
        "first_position_branches_unsat": sum(row[2] for row in rows),
        "independent_result_sha256": INDEPENDENT_RESULT_SHA256,
        "root_formulas_unsat": sum(row[1] for row in rows),
        "source_clauses_reconstructed": sum(row[4] for row in rows),
        "source_reported_proof_bytes": sum(row[5] for row in rows),
        "source_result_sha256": SOURCE_RESULT_SHA256,
        "status": "AUDITED_INDEPENDENT_ACCEPT_H3989",
        "target_good43_found": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
