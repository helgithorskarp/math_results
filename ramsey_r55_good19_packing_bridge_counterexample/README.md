# A good19 graph with monochromatic four-clique packing number one

This package certifies a counterexample to the proposed bridge
“every good19 contains two vertex-disjoint monochromatic K4s.” Here
**good n** means a red/blue coloring of the complete graph on n vertices
with no monochromatic K5. Red edges can equivalently be viewed as a graph;
blue cliques are its independent sets.

The explicit graph has **19 vertices, 86 red edges, 24 red K4s and 12 blue
K4s**. It has no red or blue K5. Every pair among its 36 monochromatic K4s
intersects. Its monochromatic K4 packing number is therefore exactly one.

This is a failed global-forcing route checkpoint. It produces no good43,
does not exclude a good43 branch, and does not refute the conjecture that
every good43 has eight disjoint monochromatic K4s. No historical novelty or
Ramsey-bound improvement is claimed. The existing unconditional 60-branch
cover remains valid.

## Explicit witness and independent verification

[`graph.json`](graph.json) stores 171 physical edge bits. Bit k of
`red_hex` is the color of the kth pair in lexicographic order
`(0,1), (0,2), ..., (17,18)`, starting with bit zero. A set bit means red.
The hexadecimal representation has exactly 43 lowercase characters and
its unused high bit is zero:

```
596fe341a9d18792f570ae8cc3330c04b7834ff30cf
```

The equivalent standard graph6 record in [`graph.g6`](graph.g6) is:

```
R~xbEqxHYFCtPsvAVQGIz?my[fKuLg
```

[`CERTIFICATE.json`](CERTIFICATE.json) lists every monochromatic K4.
Among the 630 unordered pairs, 372 intersect in one vertex, 174 in two,
and 84 in three. None are disjoint.

Two separate checkers establish the certificate:

- [`verify.py`](verify.py) uses recursive bitset clique enumeration.
- [`check_literal.py`](check_literal.py) uses a set of physical red edges,
  enumerates all 3,876 four-subsets and 11,628 five-subsets, and checks all
  four-clique pairs by literal set intersection. It imports no producer or
  other checker.

[`reproduce.py`](reproduce.py) requires both results to equal the complete
certificate, checks agreement with graph6, checks the complement, and
requires both checkers to reject five invalid inputs. It compares the
result with [`EXPECTED.json`](EXPECTED.json). From the repository root:

```sh
python3 -B ramsey_r55_good19_packing_bridge_counterexample/reproduce.py
python3 -O -B ramsey_r55_good19_packing_bridge_counterexample/reproduce.py
```

Both runs return `VERIFIED_NEGATIVE_GOOD19_PACKING_BRIDGE`. Python 3.11.2
with only the standard library was used. There are no assertions whose
removal changes the verification. No solver, external graph catalog,
private file, network access, or imported Ramsey theorem is needed to
verify the counterexample. This is an executable finite certificate, not
a proof-assistant formalization.

## Why this was a global R(5,5) route

The predeclared target was to exclude the complete class of good43 graphs
with no packing of eight monochromatic K4s. If the bridge were true, the
following argument would supply the forcing result. In a good43, greedily
remove five red K4s at residual orders 43, 39, 35, 31, 27, using
R(4,5) <= 25 and the absence of a blue K5. From the remaining 23 vertices,
remove another monochromatic K4 using R(4,4) <= 18. The proposed good19
bridge would supply two more disjoint K4s, leaving eleven vertices.

The standard bounds in this hypothetical argument are documented by
[McKay and Radziszowski's R(4,5) paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
and [McKay's Ramsey graph catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
They are not premises of the counterexample verification.

A complete finite bridge decision could fix a red K4 (complementing the
whole graph if necessary). Its 15-vertex remainder must have no
monochromatic K4; otherwise there is already a disjoint pair. The planned
search used all 640 cataloged Ramsey(4,4,15) cores, four new vertices forming
a red K4, and all 60 cross-edge decisions. The encoding forbids all
monochromatic five-sets and all pairs of disjoint monochromatic four-sets.

The run stopped at the first SAT instance, catalog index **379** (zero
based), which produced the witness above. The preceding 379 cores had
independently audited formulas and checked DRAT refutations. Those results
are discovery history, not a complete catalog exclusion or a global
good43 reduction. The other 260 cores were not run. The SAT trace is not a
refutation. [`PROVENANCE.json`](PROVENANCE.json) records the exact discovery
case and frozen run limits; [`BOUNDARY.json`](BOUNDARY.json) records the
failed gate.

The initially incorrect parsing of core 0's redirected status was fixed
without repeating its solver call: the already saved UNSAT result and
proof were audited and checked before continuing. No cap, backend, or
mathematical encoding changed. All instance files and checked proof streams
are retained in the researcher's private checkpoint; they are unnecessary
for this small public certificate.

The unrelated unrestricted packing-threshold investigation in the
[unrefereed z20-cochromatic project](https://github.com/ipitchford/z20-cochromatic/blob/master/applications/vr2-k4/README.md)
motivated checking the good19 specialization. Its 19-vertex Paley-twin
example contains monochromatic five-sets. Its claimed upper-bound proofs
were neither imported nor rerun here.

## Relation to the standing target interface

The earlier [unconditional 60-branch cover](../ramsey_r55_global_clique_packing/README.md)
at source `3f06352ae0735101a04afa1ba7b055736e7300f7` has received
[independent acceptance](../ramsey_r55_global_clique_packing_review1/README.md)
at source `daec8e19799d254263f916c9ad4dd9b71464b403`.
The present counterexample changes none of that cover's constraints or
counts. The good19 augmentation bridge is parked. The stronger good43
packing conjecture remains undecided; extending this saved 19-vertex graph
is not part of this checkpoint.

Discovery Net context: original cover h3835
`bafkreifgyycgvem6uqlasgdwwbluvuvomk4km2n7rzaxg6sgudgzgrj2sq`, accepted by h3845
`bafkreiem4hg5qakgtvnf55vjyhtc7ephwgxczimdvdw43w7taocbnvubuq`.
The new negative certificate has not yet received independent external
review. File integrity is recorded in [`SHA256SUMS`](SHA256SUMS).
