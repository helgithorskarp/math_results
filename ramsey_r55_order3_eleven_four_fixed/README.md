# Ten fixed vertices: universal extension and sharp rigidity

**Every one of the 197 four-triangle cores extends to a Ramsey (5,5)
graph with ten uniform fixed vertices.** For the 118 cores containing
a blue K4, ten is the sharp maximum, and all ten-vertex extensions
have a completely determined signature system with four possible
fixed-edge patterns. The [proof](PROOF.md) is solver-free.

The signatures at equality are the four singletons and six pairs of
the four core triangles, once each. Intersecting signatures have blue
edges. Disjoint signatures have red edges, except that at most one
of the three complementary pair edges may be blue. All four choices
are valid for every core. The other 79 cores admit these constructions
too; their other fixed extensions and maximum sizes are not classified.

This settles the local feasibility question: the core and its ten
fixed vertices alone cannot exclude any of the 197 cases. Further
pruning must use additional full-graph information. **No 43-vertex
graph, full extension verdict, global automorphism exclusion, or
Ramsey lower-bound improvement is claimed.** Both eleven-cycle
internal-color splits remain open.

## Evidence

[result.json](result.json) gives the complete single-fixed-vertex
signature census and the edge counts and SHA256 hashes of four
explicit 22-vertex graphs per core. The allowed-signature counts
11,13,14,15,16 occur in respectively 1,19,42,125,10 cores. Its
input is the preceding [197-class core cover](../ramsey_r55_order3_eleven_four_core).

The producer [construct.py](construct.py) uses red K4 supports to
calculate signatures. The separate [verify.py](verify.py) imports
no producer or inherited classification code. It checks:

* all 3,152 literal one-fixed-vertex graphs;
* all 1,576 complementary-pair template choices, of which 788 are valid;
* all 788 generated edge lists and 182,028 literal action-pair identities;
* the exact signature data and every valid graph's edge hash and size.

The four forbidden template choices have respectively 2,2,2,6 blue
K5s, and no red K5s. Eight malformed-certificate controls are rejected.
An independent integer enumeration of the proved equality inequalities
finds exactly the required singleton/pair multiplicities.

[fixture.edges](fixture.edges) is the 22-vertex construction for core
0 with all complementary pair edges red. Its format is `n m` followed
by the sorted red pairs `u v`, with labels starting at zero. All omitted
pairs are blue. [inspect_fixture.py](inspect_fixture.py) is a standalone
matrix checker that inspects every five-set and needs no catalog,
producer, solver, or omitted file.

## Reproduction

CPython 3.11.2, standard library only. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B construct.py --work /scratch/new-r55-four-fixed/production
cmp result.json /scratch/new-r55-four-fixed/production/result.json
python3 -B verify.py --source /scratch/new-r55-four-fixed/production --report /scratch/new-r55-four-fixed/verification.json
cmp report.json /scratch/new-r55-four-fixed/verification.json
python3 -B controls.py --source /scratch/new-r55-four-fixed/production --report /scratch/new-r55-four-fixed/controls.json
cmp controls_report.json /scratch/new-r55-four-fixed/controls.json
python3 -B inspect_fixture.py fixture.edges
python3 -B -O construct.py --work /scratch/new-r55-four-fixed/production-O
cmp result.json /scratch/new-r55-four-fixed/production-O/result.json
python3 -B -O verify.py --source /scratch/new-r55-four-fixed/production-O --report /scratch/new-r55-four-fixed/verification-O.json
cmp report.json /scratch/new-r55-four-fixed/verification-O.json
python3 -B -O controls.py --source /scratch/new-r55-four-fixed/production-O --report /scratch/new-r55-four-fixed/controls-O.json
cmp controls_report.json /scratch/new-r55-four-fixed/controls-O.json
```

The producer and checker default to the sibling `cover.json`, whose
SHA256 is pinned. Pass `--cover /path/to/cover.json` to use a separate
copy. Normal and optimized runs agree on all reports and all generated
edge-list bytes. The 788 generated graphs and operational scratch
files stay outside Git; the public result is a compact certificate
index, and one standalone edge-list fixture is included.

## Scope and dependencies

The hand proof requires no external Ramsey value and does not rely
on the completeness of the 197-class catalog. Its application to the
entire four-versus-seven branch imports that catalog and its full
normalization bridge. Both the inherited catalog and this new result
await independent review. Internal checker separation does not
constitute an independent reviewer verdict. Exact source bytes,
unformalized arguments, Python/runtime/hardware and SHA256 remain
trust boundaries; no proof-assistant formalization is claimed.

The [earlier three-triangle signature argument](../ramsey_r55_order3_eleven_signature_bound)
used the same red-neighbor incidence mechanism in a different setting.
The present four-triangle theorem includes a universal extension and
a conditional equality classification, and imports none of its full
SAT refutations or external degree assumptions.

Fixture labels put singleton signatures first. They must not be
copied directly into the full parent's sorted eleven-bit fixed rows.
No new full-formula bridge or full extension test is part of this
milestone. No computation remains active after the recorded checks.
