# Complete exclusion of a zero-free rank-four cut family

No good43 admits a20+23 cut with all15 nonzero F2^4 types on each side,
five distinct types doubled on the20 side, and the eight types in an affine
hyperplane doubled on the23 side, when cross edges are dot products.
All443 internal edges are arbitrary; no full graph symmetry is imposed.

The [proof and coverage argument](PROOF.md) reduce3003 normalized type
placements and their pair colors to32 global branches. Each branch has a
necessary23-side CNF with a checked UNSAT proof. This closes the complete
43-vertex class. These cuts have ranksfour andfive in the two colors and
no zero types, so they survived the preceding zero-pair filter. Other
rank-four families and good43 existence remain open; no Ramsey bound improves.

## Reproduce

Tested with CPython3.11.2 on Debian Linux amd64. Choose fresh directories
outside the source repository. `bootstrap.py` needs `dpkg-deb`; it downloads
and hashes two small pinned packages and extracts them without system installation.

```sh
python3 -B bootstrap.py /tmp/r55-affine-tools
python3 -B reproduce.py /tmp/r55-affine-replay \
  --cadical /tmp/r55-affine-tools/cadical/usr/bin/cadical \
  --drat-trim /tmp/r55-affine-tools/drat-trim/usr/bin/drat-trim
```

Expected final status: `COMPLETE_AFFINE_DUPLICATION_FAMILY_EXCLUDED`, with
32 physical proofs checked. The replay takes several minutes and generates
roughly300 MB of CNFs and proofs. SAT, UNKNOWN, missing proof bytes or checker
failure stop it without a completeness verdict. No cap escalation or
alternative solver is part of this replay.

Recheck an existing complete run and exercise adverse evidence controls:

```sh
python3 -B verify.py /tmp/r55-affine-replay \
  --drat-trim /tmp/r55-affine-tools/drat-trim/usr/bin/drat-trim
python3 -B controls.py /tmp/r55-affine-replay /tmp/r55-affine-controls \
  --drat-trim /tmp/r55-affine-tools/drat-trim/usr/bin/drat-trim
```

The verifier reads all proof bytes and executes the checker again; it does
not accept saved status records. Controls also check every one of443 internal
coordinates and460 cross coordinates, and reject forged completion metadata,
empty/truncated proofs, stale success logs and missing formula clauses.

`expected_cases.json` records all32 first-run input and proof hashes and
sizes. `expected_audit.json` contains the independent geometric and formula
audit. `VALIDATION.json` records fresh public replay and adverse controls.
Large traces remain in the private reproducible checkpoint; GitHub contains
source and compact evidence. A fresh replay generates every required proof,
so omitted private traces are not external input dependencies.

## Physical family interface

`model.py` accepts a JSON object with `doubled_rows`, five sorted distinct
integers1..15, and `internal_hex`,443 bits in111 lowercase hex digits.
Bits enumerate within-part pairs lexicographically, least significant first.
Output `n:43,red_hex` uses903 lexicographic pair bits in226 hex digits.
The affine hyperplane is normalized to odd column types; the proof covers
every other defining nonzero vector by factor-basis change and relabeling.

```sh
python3 -B model.py fixture_parameters.json
```

The fixture is intentionally non-Ramsey. The generator represents every
internal assignment, including those ruled out by the derived pair-color
constraints. Family membership is never reported as Ramsey feasibility.

The only imported mathematical computation is
[McKay and Radziszowski's R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf),
used for global degree bounds. Small Ramsey facts and symmetry/projection
reductions are proved here. The checker is
[drat-trim](https://github.com/marijnheule/drat-trim) and the producer is
[CaDiCaL](https://github.com/arminbiere/cadical); exact tested package URLs
and executable hashes are in `tools.json`.

The [rank-width theorem](../ramsey_r55_rank_width_four/PROOF.md) and
[zero-pair reduction](../ramsey_r55_rank4_cut_search_reduction/PROOF.md)
were independently accepted at h3751. They motivate this survivor class and
are not logical premises of its exclusion. External review of this package
is pending. No priority or decision of the remaining rank-four search is claimed.
