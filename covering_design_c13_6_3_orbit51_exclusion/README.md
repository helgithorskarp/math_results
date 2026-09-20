# Orbit-51 exclusion in the exceptional `C(13,6,3)` profile

This directory supports the following exact computer-assisted theorem.

> In a hypothetical 20-block `(13,6,3)` covering with point-degree profile
> `(12,9^12)`, three blocks through the degree-12 point cannot share a low
> triple and have three disjoint residual pairs (`3K2`, orbit 51).

Consequently only the support-five `P3+K2` type (orbit 52) remains among the
five `h=7` heavy-triple types: the earlier support lemma excludes types
53--55. This does **not** exclude the whole `(12,9^12)` profile and does not
determine `C(13,6,3)`.

## Structural reduction

Normalize the degree-12 point as `12`, the common triple as `Q={0,1,2}`, and
the residual matching as `34,56,78`; put `R={9,10,11}`. The 12 blocks
through point 12 become 5-subsets of the low points. After deleting the
three fixed residues `01234,01256,01278`, the remaining nine through rows
have column sums

```text
(2,2,2,4,4,4,4,4,4,5,5,5).
```

The eight away 6-subsets have every column sum four. Thus the whole extension
is represented by only a `9 x 12` through matrix and an `8 x 12` away matrix.
Pair and triple coverage become exact two-way and three-way row-intersection
conditions.

Only six incidences of the remaining through rows meet `Q`, so some row is
`Q`-free. The automorphism group of `Q + 3K2 + R` has seven orbits on such
5-sets. Their orbit sizes are `6,36,9,24,36,12,3` (sum 126).

For `i,j in Q`, the three fixed blocks contribute codegree three. Covering
the triples with `R` forces one further occurrence, while the imported
optimal-link theorem bounds the total by five. Hence the three residual
codegrees have, up to `S3(Q)`, pattern `111`, `211`, `221`, or `222`.

In patterns `221` and `222`, let `T_i` be the two remaining through rows
containing `i`. The orbit of `(T_0,T_1,T_2)` is determined by its three pair
intersections and triple intersection. The corresponding away columns are
4-subsets of eight rows with forced pair intersections. Their eight Venn
cell sizes are linear functions of one triple-intersection number.
Nonnegativity leaves only four joint types for `221` and seven for `222`.
This is the dual Venn reduction used by the certificates.

The final exact frontier is therefore:

- 14 cases for the seven `Q`-free types crossed with `111` and `211`;
- 77 cases for the seven `Q`-free types crossed with the 11 feasible joint
  Venn types for `221` and `222`.

All 91 cases are UNSAT. See [PROOF.md](PROOF.md) for completeness and
encoding details.

## Reproduction

Requirements used for the recorded run:

- CPython 3.11.2 (generator and audit use only the standard library);
- CaDiCaL 3.0.1, commit `c60730422e758ef1cebe7aeddf2dda31c996bf04`;
- `drat-trim`, commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

Run in a scratch directory because the generated CNFs and proofs are large:

```bash
JOBS=10 ./run_and_check.sh /scratch/orbit51-run /path/to/cadical /path/to/drat-trim
```

The recorded run generated 91 CNFs (113,188,593 bytes total) and binary DRAT
traces (569,850,222 bytes total). These bulky generated artifacts are not
committed. [EXPECTED.json](EXPECTED.json) records every instance and proof
hash; [EXPECTED_AUDIT.json](EXPECTED_AUDIT.json) records 91 byte-identical CNF
regenerations, 2,531 primitive truth-table checks, and the orbit enumerations.
Every trace was independently
accepted by `drat-trim` with `s VERIFIED`.

## Files

- `generate_dual_cnf.py`: exact CNF generator and the three structural orbit
  decompositions;
- `audit_encoding.py`: independent small-formula audits, orbit coverage, Venn
  coverage, and regeneration of every recorded CNF hash;
- `collect_results.py`: validates solver/checker outcomes and collects compact
  hashes;
- `run_and_check.sh`: deterministic end-to-end runner;
- `EXPECTED.json`: compact 91-case certificate manifest;
- `PROOF.md`: mathematical reduction, CNF semantics, and scope.

The [La Jolla Coverings Repository version 1.2](https://zenodo.org/records/19735294)
records a 21-block construction, while its current covering table records the
unresolved global bound `20 <= C(13,6,3) <= 21`. General context
is in Gordon, Kuperberg, and Patashnik,
[*New constructions for covering designs*](https://arxiv.org/abs/math/9502238).
No claim of historical priority is made for this search-relative orbit
exclusion.
