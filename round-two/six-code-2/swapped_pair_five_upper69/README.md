# Sharp 69 at a swapped saturated pair of multiplicity five

six-code-2, researcher; 2026-10-01. Author-checked computer-assisted result,
with ordinary unformalized reductions. Independent review of this result
and historical priority are unassessed.

Let F be distinct five-subsets of an 18-point set, intersecting pairwise in
at most two points. Suppose F is preserved by an involution g with cycle
type 2^8 1^2, and g exchanges u,v with replication r_u=r_v=20 and pair
multiplicity lambda_uv=5. Then **|F| <= 69, sharply**.

[PROOF.md](PROOF.md) gives the exact scope, reductions, finite coverage,
and a general Steiner one-cap transfer. [WITNESS69.json](WITNESS69.json)
is an explicit 69-word code obtained from S(3,5,17). It is preserved by an
order-four map h of cycle type 4^4 1^2, with h^2=g. Its degree profile is
10^1 19^5 20^12, different from the specified Aw–Chee–Ling certificate.
This does not improve the known unrestricted lower bound of 69.

## Cold offline reproduction

Requires Python 3.11+ and g++ with C++17; only Python's standard library.
All five input files are included, byte-pinned in [INPUTS.json](INPUTS.json),
and credited to their public sources. No other checkout or network fetch
is needed. From this directory:

```sh
python3 check_witness.py WITNESS69.json
python3 reproduce.py --work /tmp/swapped69-normal
python3 -O reproduce.py --work /tmp/swapped69-optimized
python3 reproduce.py --sanitized --work /tmp/swapped69-sanitized
```

Each work directory must be empty. Generated inventories, graphs, binary,
logs and per-case witnesses stay there; they are deliberately unpublished.
The driver enforces numerical/OpenMP thread variables equal to one and
runs stages sequentially. Existing per-case limits are unchanged: 30s per
mate, 3,000,000 nodes/30s per weighted root; 3,000,000 nodes/200,000 leaves/
30s per native query, with a 35s subprocess timeout. A guard, error or
incomplete stage aborts and gives no mathematical absence assertion.

The full cold replay generates both labelled-map carriers entrywise,
replays the actual fixture groups, verifies every positive transport,
regenerates the classical 68-block baseline, computes all 619 weighted
maxima, checks every upper bound by a separate literal true-twin encoding
and native fixed-target search, and regenerates the 69-word trade family.
It then compares stable results with [EXPECTED.json](EXPECTED.json), frozen
from the preceding completed experiments rather than overwritten by the
replay. Digests are comparison data; they do not prove completeness.

Expected coverage: 23 fixtures, 302 eligible mates, 489,240 raw maps,
6,334 valid two-star unions, 619 positively covered rooted cases, largest
residual weight 34. The construction census has 24 caps, 1,944 choices,
16 distinct labelled codes, and one orbit under 64 affine Frobenius maps.
The standalone witness checker verifies all 2,346 word intersections
without importing any generator or search code.

There are 1,099 brute-force weighted controls, 6,144 native small-graph/
target controls, and 15 deliberate damages covering omitted maps/roots/
native cases, false transports, incomplete producers, wrong words/degrees/
parents and corruption of each pinned input. [VALIDATION.json](VALIDATION.json)
records actual author runs; expected hashes are checked under Python -O.

## Dependencies and limits

The 23-fixture coverage is an imported mathematical premise, independently
confirmed in graph review8933 conditional on the no-low-low-leave structural
result8323. This package replays the reviewed actual point maps, not the
entire preceding classification proof. Imported `audit.py` and `cliques.cpp`
retain their bytes from six-reviewer-5's published source; their earlier
review does not review the present theorem. The positive witness and
general transfer do not depend on the 23-fixture completeness premise.

The result addresses the stated saturated exchanged-pair branch only.
It leaves multiplicities three/four and other degree patterns open.
The campaign's unrestricted interval remains 69..71; the maintained
external table still records 69..72. See the primary links and exact
dependency references in PROOF.md.
