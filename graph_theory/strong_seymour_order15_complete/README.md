# Strong Seymour vertices through order 15

This directory completes the order-15 frontier:

> **Theorem.** Every tournament on 15 vertices has a strong Seymour vertex.

Together with the preceding exact
[`order-at-most-14 theorem`](../../strong_seymour_order14), this proves the
claim for every tournament on at most 15 vertices.  Equivalently, any
counterexample to the strong second-neighborhood statement for tournaments
has at least 16 vertices.

For a vertex `x`, strong Seymour means that the directed bipartite link from
`N+(x)` to its exact second out-neighborhood `N++(x)` has a matching
saturating `N+(x)`.  The full reduction and proof are in
[`THEOREM.md`](THEOREM.md).

The primary source defining the property is Bai, Li, and Park,
[*Towards a strengthening of the second neighborhood conjecture*](https://arxiv.org/abs/2607.18047v2).
Their theorem for minimum out-degree at most five and the earlier repository
results reduce a hypothetical order-15 counterexample to one remaining local
configuration: an ordinary degree-seven root with a size-six minimal
deficient Hall set.  The present result excludes that configuration.

## Structural gate and compact evidence

Before any size-six formula was generated, a human-readable argument divided
the frontier into exactly 19 signatures:

- six tight signatures, indexed by the internal score `p=0,...,5` of a
  selected tight witness vertex; and
- thirteen strict signatures, indexed by the positive score sequences of a
  six-vertex tournament.

Landau's score criterion derives the thirteen sequences.  The standard-library
[`check_signatures.py`](check_signatures.py) independently enumerates all
`2^15=32768` labeled six-vertex tournaments and recovers the same list and
counts.  There is no enumeration of Hall-link patterns and no order-15
tournament census.

The score-sequence list has SHA-256
`f58605f97fb4ee29323660d0ba50c33f52cf1c674762346426517620b93e8ad1`.
Its thirteen labeled counts are

```text
240, 80, 720, 1440, 2880, 1680, 1680,
1680, 8640, 2400, 144, 2400, 2640.
```

The 19 generated formulas have 20,666--20,768 variables and
47,345--47,552 clauses.  CaDiCaL proves every formula UNSAT, and `drat-trim`
independently verifies every binary DRAT trace with zero RAT lemmas in its
core.  The traces total 733,799,202 bytes.  The canonical verification-record
manifest has SHA-256

```text
41cc552e669658832e5e4010e813f75ee173c3334097dfc70cf1e35e0c2cae4e
```

Exact per-case CNF and proof hashes, sizes, and core statistics are in
[`EXPECTED.json`](EXPECTED.json).  The generated formulas and proof traces
are intentionally omitted from Git under the large-file boundary.  They are
deterministically reproducible from the compact source and exact tool commits;
the audited campaign copies are preserved below `/scratch`.

## Reproduction

The audited environment used CPython 3.11.2, `python-sat==1.9.dev15`,
CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`, and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

From this directory, with those two binaries available:

```bash
python3 -m venv /scratch/ss15-complete-venv
/scratch/ss15-complete-venv/bin/pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 check_signatures.py
/scratch/ss15-complete-venv/bin/python generate_cases.py \
  /scratch/ss15-complete-cases
python3 solve_cases.py /scratch/ss15-complete-cases \
  --cadical /path/to/cadical --seconds 300 --workers 4
python3 verify_proofs.py /scratch/ss15-complete-cases \
  --checker /path/to/drat-trim --workers 4
```

The final verifier must print

```json
{"cases": 19, "manifest_sha256": "41cc552e669658832e5e4010e813f75ee173c3334097dfc70cf1e35e0c2cae4e", "status": "VERIFIED", "total_proof_bytes": 733799202}
```

The imported base generator must have SHA-256
`5dda45c3e5e9aeeb286bfa6844e911bf8d9cb47918e2cf21f0fb00e2482d0517`.
A clean regeneration reproduced all 19 CNF hashes, and a second solve/check
cycle reproduced every proof hash and the displayed manifest.

## Trust boundary and novelty scope

The 19-signature reduction is written in mathematical form in `THEOREM.md`.
The completeness checker does not import the SAT generator.  The global
exclusion trusts the inspected base generator, PySAT's sequential cardinality
encodings, CaDiCaL, and `drat-trim`; proof checking establishes UNSAT only for
the exact hashed formulas.

A bounded Discovery Net refresh and a live primary-source search on
2026-09-20 found no earlier order-15 theorem.  The arXiv record remained at
version 2 (2026-07-24), and Austin Gibbons's independent
[`ssnc` project](https://github.com/AustinBGibbons/ssnc) had no commit after
2026-07-23.  This is search-relative evidence of novelty, not a claim of
historical priority.
