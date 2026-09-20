# Order-15 strong Seymour vertices: exclusion of small Hall witnesses

This directory proves a structural narrowing of the only unresolved
order-15 regime for tournaments without a strong Seymour vertex:

> At every ordinary Seymour vertex, every inclusion-minimal deficient Hall
> witness has size 4, 5, or 6.

The proof is in [`THEOREM.md`](THEOREM.md).  Witness sizes one and two are
excluded by direct propagation to an ordinary vertex of out-degree six.
Size three either does the same or has one rigid local signature: a directed
triangle whose vertices all dominate both Hall neighbors.  A small DRAT
certificate excludes that final signature.

The result depends on the earlier
[`strong_seymour_order15`](../../strong_seymour_order15) frontier theorem,
which proves that a hypothetical order-15 counterexample is nonregular, has
minimum out-degree six, and has no ordinary Seymour vertex of out-degree six.
It does **not** claim that the full order-15 problem is solved.

The primary source for the strong matching condition and the
minimum-out-degree-five theorem is Bai, Li, and Park,
[*Towards a strengthening of the second neighborhood conjecture*](https://arxiv.org/abs/2607.18047).
Austin Gibbons's independent [SSNC project](https://github.com/AustinBGibbons/ssnc)
constructs regular tournaments with exactly nine strong vertices; it does
not settle this nonregular order-15 branch.

## Exact evidence

The local checker exhausts all labeled orientations internal to a minimal
Hall witness of size at most three and all arcs from that witness to its Hall
neighbor set.  Its expected output is:

```json
{"size_1": {"degree_six_patterns": 1, "locally_feasible": 1, "patterns": 1, "record_sha256": "eb090ab70f24f4f1168a9436aaa26636b5b6b5c59db1421fc216c71c37aaa113", "rigid_patterns": 0}, "size_2": {"degree_six_patterns": 2, "locally_feasible": 2, "patterns": 8, "record_sha256": "668163400b0e275f560affbfda5c879ef515c6d8780f28fa384a79d8ac7a4624", "rigid_patterns": 0}, "size_3": {"degree_six_patterns": 72, "locally_feasible": 74, "patterns": 512, "record_sha256": "fc86fc316f2945390b8bdc2a2123a6349249898c864d856f840ceaa1a759084e", "rigid_patterns": 2}, "status": "VERIFIED"}
```

The exact rigid-residue instance and proof data are:

| item | value |
|---|---|
| variables | 20,666 |
| clauses | 47,347 |
| CNF bytes | 1,068,047 |
| CNF SHA-256 | `a3b59a14d2a7b086bc02343d0f1b5199be8351f30a9c4dcfbe87190ba12061bb` |
| binary DRAT bytes | 2,527,866 |
| binary DRAT SHA-256 | `ca4f4bbbc37d0c069427752cc95f3eaf5c6f13668f9a7bb35c41d5d41d0085e9` |
| clauses in checked core | 5,893 |
| lemmas in checked core | 17,300 |
| resolution steps | 331,692 |
| RAT lemmas in core | 0 |

The generated CNF and DRAT trace are intentionally omitted from Git: they
are deterministically reproducible generated evidence.  They are preserved
under `/scratch/graph-r2-pass10-ss15/` in the campaign workspace.

## Reproduction

The audited environment used CPython 3.11.2, `python-sat==1.9.dev15`,
CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`, and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

From this directory:

```bash
python3 -m venv /scratch/ss15-small-hall-venv
/scratch/ss15-small-hall-venv/bin/pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 check_reduction.py
/scratch/ss15-small-hall-venv/bin/python generate_reduced_cnf.py \
  /scratch/ss15-d7-s3-rigid.cnf
cadical /scratch/ss15-d7-s3-rigid.cnf \
  /scratch/ss15-d7-s3-rigid.drat
drat-trim /scratch/ss15-d7-s3-rigid.cnf \
  /scratch/ss15-d7-s3-rigid.drat
sha256sum /scratch/ss15-d7-s3-rigid.cnf \
  /scratch/ss15-d7-s3-rigid.drat
```

`generate_reduced_cnf.py` also reports the SHA-256 of the imported base
generator.  In the audited commit it is
`5dda45c3e5e9aeeb286bfa6844e911bf8d9cb47918e2cf21f0fb00e2482d0517`.
`drat-trim` must end with `s VERIFIED`.

## Trust boundary and novelty scope

The local reductions are written in full and checked by the standard-library
enumerator.  The rigid finite exclusion trusts the inspected base generator,
PySAT's sequential-counter encodings, CaDiCaL, and `drat-trim`.  Proof
checking establishes UNSAT only for the exact hashed formula.

A bounded Discovery Net and live-source search found no earlier exclusion of
these order-15 witness sizes.  The novelty statement is search-relative, not
a claim of historical priority.
