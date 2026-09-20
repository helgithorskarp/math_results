# Orbit-52 exclusion for `C(13,6,3)`

This directory supports an exact computer-assisted theorem about the last
open `h=7` heavy-triple type in the exceptional point-degree profile.

> Let `B` be a 20-block `(13,6,3)` covering with point-degree profile
> `(12,9^12)`, and let `h` be its degree-12 point. Three blocks through `h`
> cannot share a low triple `Q` while their three residual pairs form
> `P3+K2`.

Normalize the three residues after deleting `h` as

```text
01234, 01245, 01267.
```

The theorem excludes orbit 52. Together with the published orbit-51
exclusion and the sharp support lemma excluding orbits 53--55, it follows
that **no three blocks through `h` have three low points in common**. This
closes the five-type `h=7` subfrontier. It does not exclude the entire
`(12,9^12)` profile and does not determine `C(13,6,3)`.

## Exact reduction

The link classification for optimal `(12,5,2)` covers forces every low point
to occur five times through `h` and four times away from `h`. After removing
the three fixed rows, the remaining incidence matrices have sizes `9 x 12`
and `8 x 12`, row sums five and six, and column sums

```text
through: (2,2,2,4,3,4,4,4,5,5,5,5)
away:    (4,4,4,4,4,4,4,4,4,4,4,4).
```

The nine remaining through rows contain only six incidences with
`Q={0,1,2}`, so at least one row is `Q`-free. Under
`Aut(P3+K2) x S4`, the 126 possible `Q`-free 5-sets split into 17 orbits.
Their sizes are

```text
2,4,2,16,12,4,12,4,1,8,6,8,24,8,6,8,1.
```

Every pair in `Q` has total codegree four or five. Up to `S3(Q)`, the three
residual codegrees have pattern `111`, `211`, `221`, or `222`. A dual Venn
classification gives four joint through/away types for `221` and seven for
`222`. Hence the complete frontier has

```text
17 * (1 + 1 + 4 + 7) = 221
```

cases. All 221 CNFs are UNSAT. Every CaDiCaL binary DRAT trace was accepted
by `drat-trim`. See [PROOF.md](PROOF.md) for the completeness and encoding
arguments.

## Reproduction

The recorded run used:

- CPython 3.11.2, standard library only;
- CaDiCaL 3.0.1 at commit
  `c60730422e758ef1cebe7aeddf2dda31c996bf04`;
- `drat-trim` at commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

Run the compact definition/orbit audit:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_encoding.py --expected EXPECTED.json \
  | diff -u EXPECTED_AUDIT.json -
```

Regenerate, solve, and independently proof-check every case in a scratch
directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 run_and_check.py \
  /scratch/orbit52-run /path/to/cadical /path/to/drat-trim --jobs 12
```

The recorded run generated 221 CNFs totaling 275,677,984 bytes and 221 DRAT
traces totaling 460,621,219 bytes. `EXPECTED.json` pins every CNF and proof
hash. The generated instances, proofs, and logs are intentionally excluded
from Git.

## Files

- `generate_orbit52_cnf.py`: exact generator and normalization;
- `audit_encoding.py`: primitive truth tables, direct orbit enumerations,
  Venn coverage, and all 221 CNF regenerations;
- `run_and_check.py`: deterministic parallel solver/checker driver;
- `EXPECTED.json`: entry-level CNF and DRAT manifest;
- `EXPECTED_AUDIT.json`: pinned compact audit output;
- `PROOF.md`: mathematical reduction, certificate semantics, and scope;
- `SOURCES.md`: primary sources and graph dependencies.

The live La Jolla Covering Repository still records
`20 <= C(13,6,3) <= 21`. The contribution is therefore a structural finite
reduction, not a resolution of the covering number. No historical-priority
claim is made.
