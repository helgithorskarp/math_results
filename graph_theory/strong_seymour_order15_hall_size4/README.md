# Order-15 strong Seymour vertices: Hall size four excluded

This directory proves the next structural reduction in the unresolved
order-15 strong-Seymour problem:

> At every ordinary Seymour vertex of a hypothetical 15-vertex tournament
> without a strong Seymour vertex, every inclusion-minimal deficient Hall set
> has size five or six.

The complete argument is in [`THEOREM.md`](THEOREM.md).  The preceding
[`small-Hall theorem`](../strong_seymour_order15_small_hall) reduced the
possibilities to sizes four, five, and six.  Here the size-four local data are
classified into ten relabeling orbits, and each orbit is excluded by an
independently checked DRAT proof.

This does **not** claim that the full order-15 problem is solved.

The primary source for the strong matching condition and the
minimum-out-degree-five theorem is Bai, Li, and Park,
[*Towards a strengthening of the second neighborhood conjecture*](https://arxiv.org/abs/2607.18047).
Austin Gibbons's independent [SSNC project](https://github.com/AustinBGibbons/ssnc)
constructs regular tournaments with exactly nine strong vertices; it does
not settle this nonregular order-15 branch.

## Compact evidence

The local classification has the following exact counts:

| quantity | value |
|---|---:|
| all labeled local patterns | 262,144 |
| degree-feasible, double-covered patterns | 22,368 |
| patterns forcing an ordinary degree-six vertex | 21,896 |
| surviving labeled patterns | 472 |
| `S_4 x S_3` orbits | 10 |

The ten orbit sizes are

```text
24, 8, 72, 144, 72, 72, 24, 24, 24, 8.
```

Their expanded-union SHA-256 is
`ecf26ea337d8d00a8d0118bc3ca3350174bcdc819f1d1802cf52b0c387d539d5`.
The independent checker uses orbit expansion rather than the production
canonical-minimum calculation.

Every SAT case has 20,666 variables and 47,354 clauses.  The ten binary DRAT
traces total 22,674,389 bytes.  `drat-trim` verifies all ten; the canonical
verification-record manifest has SHA-256
`4bdfd9d33ecac18c36224720177c391d2153a38c0d328d81771b173da804a829`.
Exact CNF and proof hashes, byte counts, and core statistics are in
[`EXPECTED.json`](EXPECTED.json).

The generated CNFs and proof traces are intentionally omitted from Git under
the large-file boundary.  They are deterministically reproducible from the
source and exact tool commits, and the campaign copies are preserved under
`/scratch/graph-r2-pass11-ss15/`.

## Reproduction

The audited environment used CPython 3.11.2, `python-sat==1.9.dev15`,
CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`, and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

From this directory, with those two binaries available:

```bash
python3 -m venv /scratch/ss15-s4-venv
/scratch/ss15-s4-venv/bin/pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 check_signatures.py
/scratch/ss15-s4-venv/bin/python enumerate_and_generate.py \
  /scratch/ss15-s4-cases
python3 solve_cases.py /scratch/ss15-s4-cases \
  --cadical /path/to/cadical --seconds 300 --workers 4
python3 verify_proofs.py /scratch/ss15-s4-cases \
  --checker /path/to/drat-trim
```

The final two concise outputs must end respectively with `"status": "UNSAT"`
and equal

```json
{"cases": 10, "manifest_sha256": "4bdfd9d33ecac18c36224720177c391d2153a38c0d328d81771b173da804a829", "status": "VERIFIED", "total_proof_bytes": 22674389}
```

The imported base generator must have SHA-256
`5dda45c3e5e9aeeb286bfa6844e911bf8d9cb47918e2cf21f0fb00e2482d0517`.

## Trust boundary and novelty scope

The human proof reduces the local frontier to ten cases.  The standard-library
checker independently verifies their exhaustive orbit union.  The global
exclusion trusts the inspected base generator, PySAT's cardinality encoding,
CaDiCaL, and `drat-trim`; the checked traces prove UNSAT only for the exact
hashed formulas.

A bounded Discovery Net and live-source search found no earlier exclusion of
Hall-witness size four at this order.  This is search-relative evidence of
novelty, not a claim of historical priority.
