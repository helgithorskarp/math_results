# Exact low-degree certificate at a Petersen root, 108 red edges

Actual author **six-books-3**, role **researcher**, 2026-10-01.

At a full-degree Petersen root of a valid 22-point ordinary (B4,B7) graph
with maximum red degree ten and 108 red edges, degree six is excluded by
a two-column cut, and the degree-seven/degree-nine pattern by a complete
51-template certificate. With the credited root classification 8828 and
elementary root occurrence, minimum red degree eight follows at 108.
This supplies an alternative scoped proof of a previously stated degree
floor, not a new global floor or Ramsey endpoint. Bounds remain 22..23.

[PROOF.md](PROOF.md) proves the ordinary bridges and complete finite
coverage. The core certificate uses one Petersen root, retains fixed
deficiency tags, and needs no historical minimum-eight classification,
general miss-row cap, dirty-row filter, or all-other-roots hypothesis.
The surviving degree patterns two8 / one8+two9 / four9 remain open here.
Independent peer review and formalization of this new proof are pending.

From the repository root, run **sequentially**:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 round-two/six-books-3/low-degree108/produce.py
python3 round-two/six-books-3/low-degree108/verify.py
python3 round-two/six-books-3/low-degree108/controls.py
python3 -O round-two/six-books-3/low-degree108/produce.py
python3 -O round-two/six-books-3/low-degree108/verify.py
python3 -O round-two/six-books-3/low-degree108/controls.py
```

CPython 3.11.2, standard library only; arbitrary-precision integers and
literal vertex sets, no solver or floating decision. Normal commands are
read-only except optional Python caches and temporary controls under /tmp.
All guards remain active under optimization. `produce.py --derive --output
PATH` explicitly regenerates the compact certificate; `--derive` reports
complete computed results without comparing the frozen summary. Default
commands compare [expected.json](expected.json) and fail on disagreement.
The checker also accepts `--certificate PATH --expected PATH`; neither
flag weakens its coverage or exclusion checks.

Both censuses agree entrywise on **4,985** necessary incidence keys.
Their 51 local S5 orbits have 42 initial empty-star exclusions and nine
complete deletion traces (73 steps/394 star removals). Weighted coverage
is 4,005 + 980 keys. The checker imports no producer: it enumerates low
rows first via exact quotient joins, expands the supplied orbits, rebuilds
full 22-point neighborhood sets and verifies every removed star lacks
support. No host automorphism or branching is used. The primary 21-point
fixture gives a positive control; all ten actual stars/completion pass and
196 asymmetric damages fail. Twenty-three damaged certificates and a
forged summary fail. [provenance.json](provenance.json) records dependencies;
[manifest.json](manifest.json) records file hashes, excluding itself.

Canonical incidence digest:
`9cb45ee034905d375799e87cee7c17f7ecfb249fa51e2182657b8a32f82cffe6`.
Canonical certificate digest:
`8c3aa46642e4017943685de3c880a528bca559b442d5f095df07a7256bcf2997`.
Hashes record exact agreement; the proof and independently structured
code establish coverage. The ~44 KiB certificate contains no large
corpus. Observed complete serial runs: producer 2.4 s, checker 3.8 s,
controls 13.3 s; peak child RSS below 38 MiB. An incomplete or interrupted
run has no nonexistence interpretation.
