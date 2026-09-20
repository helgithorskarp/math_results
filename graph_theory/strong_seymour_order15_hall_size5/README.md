# Order-15 strong Seymour vertices: Hall size five excluded

This directory proves the next structural reduction in the unresolved
order-15 strong-Seymour problem:

> At every ordinary Seymour vertex of a hypothetical 15-vertex tournament
> without a strong Seymour vertex, every inclusion-minimal deficient Hall set
> has size exactly six.

The argument is in [`THEOREM.md`](THEOREM.md).  The preceding
[`size-four exclusion`](../strong_seymour_order15_hall_size4) left witness
sizes five and six.  Here a degree argument divides size five into one tight
case and eight strict tournament types; all nine exact cases have
independently checked DRAT proofs.

This does **not** claim that the full order-15 problem is solved.

The primary source for the strong matching condition and the
minimum-out-degree-five theorem is Bai, Li, and Park,
[*Towards a strengthening of the second neighborhood conjecture*](https://arxiv.org/abs/2607.18047).
Austin Gibbons's independent [SSNC project](https://github.com/AustinBGibbons/ssnc)
concerns regular constructions and does not settle this nonregular branch.

## Compact evidence

The strict branch reduces to the eight five-vertex tournament types of
minimum out-degree at least one.  Their labeled orbit sizes are

```text
40, 120, 120, 120, 120, 40, 120, 24,
```

which sum to 704.  `check_tournament_types.py` expands these orbits and
verifies directly that their union is exactly the required labeled set.  Its
union SHA-256 is
`d96a749ce921425cf5644e3369b78c8f9828ac9f7ed99b44e3ef173e673bc299`.

The tight formula has 20,698 variables and 47,404 clauses.  Each of the eight
strict formulas has 20,741 variables and 47,509 clauses.  The nine binary
DRAT traces total 88,525,488 bytes.  `drat-trim` verifies every trace with
zero RAT lemmas in its core.  The canonical verification-record manifest has
SHA-256
`0358a8f0b7280141575039a7a5b6a6827121695ff242f788300ba44bb9034e13`.
Exact CNF and proof hashes, byte counts, and core statistics are in
[`EXPECTED.json`](EXPECTED.json).

The generated CNFs and proof traces are intentionally omitted from Git under
the large-file boundary.  They are deterministically reproducible from the
source and exact tool commits; the campaign copies are preserved under
`/scratch/graph-r2-pass12-ss15/`.

## Reproduction

The audited environment used CPython 3.11.2, `python-sat==1.9.dev15`,
CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`, and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

From this directory, with those two binaries available:

```bash
python3 -m venv /scratch/ss15-s5-venv
/scratch/ss15-s5-venv/bin/pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 check_tournament_types.py
/scratch/ss15-s5-venv/bin/python generate_cases.py /scratch/ss15-s5-cases
python3 solve_cases.py /scratch/ss15-s5-cases \
  --cadical /path/to/cadical --seconds 300 --workers 4
python3 verify_proofs.py /scratch/ss15-s5-cases \
  --checker /path/to/drat-trim --workers 4
```

The final verifier must print

```json
{"cases": 9, "manifest_sha256": "0358a8f0b7280141575039a7a5b6a6827121695ff242f788300ba44bb9034e13", "status": "VERIFIED", "total_proof_bytes": 88525488}
```

The imported base generator must have SHA-256
`5dda45c3e5e9aeeb286bfa6844e911bf8d9cb47918e2cf21f0fb00e2482d0517`.

## Trust boundary and novelty scope

The human proof reduces the size-five frontier to nine cases.  The
standard-library checker independently verifies the tournament-type
classification.  The global exclusion trusts the inspected base generator,
PySAT's cardinality encoding, CaDiCaL, and `drat-trim`; the checked traces
prove UNSAT only for the exact hashed formulas.

A bounded Discovery Net and live primary-source search found no earlier
size-five exclusion at this order.  This is search-relative evidence of
novelty, not a claim of historical priority.
