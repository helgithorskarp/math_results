# A concrete marked 20-vertex neighborhood for the proper-signature interface

There exists a graph H on 20 vertices with **92 red edges**, no red K4,
and no blue K5, containing an adjacent distinguished pair u,v with

    d_H(u)=7,  d_H(v)=5,  N_H(u) intersect N_H(v)=empty.

Its remaining vertices split into eight blue to both roots, six red
only to u, and four red only to v. The explicit edge list is
[GRAPH.json](GRAPH.json). This supplies an actual local graph for the
8/6/4 neighborhood requirement left open by the preceding full-visible
pilot. It is not merely a degree or edge-count vector.

This is **not a 43-vertex Ramsey graph**, not a Ramsey bound, not a
whole-profile or signature-family exclusion, and not a proof that this
local graph extends to the target. No novelty is claimed for the existence
of 20-vertex Ramsey(4,5) graphs generally. The useful output is the exact
marked candidate and its reproducible embedding into the current search.

## Direct proof and fixed labels

Local labels are u=0, v=1, X=2..9, A=10..15, B=16..19. Precisely

    N_H(0)={1} union A,    N_H(1)={0} union B.

The checker verifies the simple edge list, all 92 edges, and both exact
neighborhoods. It enumerates all 4,845 four-subsets for red K4s and all
15,504 five-subsets for blue K5s. A second, bitset-intersection enumeration
agrees entry by entry. Both forbidden lists are empty. The degree list is

    7,5,10,8,10,10,8,10,9,9,10,10,9,10,9,9,10,11,11,9.

Appending a new vertex red to every vertex of H gives a 21-vertex graph
with no monochromatic K5: a red K5 through the new vertex would require
a red K4 in H, and a blue K5 cannot contain that vertex. The checker also
tests all 20,349 five-sets of this actual 21-vertex graph directly. This
small rooted graph is the partial object used below, not the target.

Neither SAT soundness nor any graph catalogue or imported Ramsey theorem
is needed for this existence proof. [verify.py](verify.py) imports no
generator, inherited checker, solver, or nonstandard library.

## Exact 43-vertex handoff

The target family has red triangle E={0,1,2}, all three exceptional degrees
20, and forty other degrees 21. Its fixed E-incidence cell sizes, in mask
order 1,2,3,4,5,6, are `(8,8,6,10,4,4)`; masks 0 and 7 are absent. It retains
exceptional profiles `(t_R,t_B)=(92,107)` at each root. These are conditional
search assumptions, not conclusions about every Ramsey(5,5;43) graph.

Embed H as the red neighborhood of global root 0:

| local vertices | global vertices | role |
|---|---|---|
| 0 | 1 | other exceptional root |
| 1 | 2 | other exceptional root |
| 2..9 | 3..10 | signature 001 |
| 10..15 | 19..24 | signature 011 |
| 16..19 | 35..38 | signature 101 |

Bits are indexed by global roots 0,1,2, with root 0 the low bit. The
mapping agrees with every prescribed E incidence. Together with root 0,
it fixes the entire valid 21-vertex rooted graph described above. Vertices
outside that graph have only their three E incidences fixed; thus they
cannot lie in any five-set with all ten edges already fixed.

[HANDOFF.json](HANDOFF.json) contains the exact **153 signed central-edge
units**, with variables 1..780 indexing lexicographically ordered pairs
from 3..42. Red is positive. All these edges are visible in root 0's red
neighborhood. There remain **627** central variables: **503 visible and
124 invisible**. Unlike the old 353-K5 seed, this candidate's fixed
21-vertex core has no monochromatic K5. However, only one of the six full
root-neighborhood tests has been realized; the other five and the two
additional stratum tests are not decided.

There are 138 currently fixed red edges, so an extension with 450 red
edges needs 312 further red edges. Individual residual red degrees are
listed for all 43 vertices. Their sum is 624, and each fits its unassigned
degree box. This is **not a simultaneous degree-feasibility certificate**.

The six profile equations are also recorded as exact remaining edge sums.
For a blue neighborhood of order22, 107 blue edges means 124 red edges.

| root/side | known red edges | remaining red sum | variables in sum |
|---|---:|---:|---:|
| 0/R | 92 | 0 | 0 |
| 0/B | 0 | 124 | 231 |
| 1/R | 19 | 73 | 138 |
| 1/B | 38 | 86 | 165 |
| 2/R | 13 | 79 | 147 |
| 2/B | 48 | 76 | 140 |

These sums overlap. The checker reconstructs every variable list and
right-hand side from the actual partial graph; it does not claim that
the rows can be satisfied together. [handoff.py](handoff.py) regenerates
the units and affine data, while the separate checker builds a symmetric
partial-color matrix and independently reconstructs the entire handoff.

Appending the units to a **complete** target-family formula fixes this
candidate. A refutation would exclude only its extension fiber. Appending
them to the preceding visible-only pilot still leaves a relaxation:
K5s involving invisible edges must not be forgotten. No extension solve
of this new candidate is started in this milestone.

## Verification and reproduction

CPython 3.11.2 standard library suffices for the complete positive proof
and the handoff checks. From this directory, choose new output paths:

```sh
sha256sum -c SHA256SUMS
python3 -B handoff.py --output /scratch/new-root20-handoff.json
cmp HANDOFF.json /scratch/new-root20-handoff.json
python3 -B verify.py --report /scratch/new-root20-check.json
cmp verification.json /scratch/new-root20-check.json
python3 -B controls.py --report /scratch/new-root20-controls.json
cmp controls_report.json /scratch/new-root20-controls.json
```

Repeat with `python3 -B -O` and distinct paths, then compare outputs.
Normal and optimized handoffs and reports agree byte for byte. Thirteen
corruptions are rejected, including wrong root incidences, a red K4 and
a blue K5 introduced while preserving all 92 edges and root incidences,
wrong unit signs/coverage, wrong embedding, residual degrees, profile
right-hand sides, variable lists and remaining-variable counts.

GRAPH.json SHA256:
`8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf`.
HANDOFF.json SHA256:
`898de74eadcd57f3953d72506b95638d60c171fa63f55b2b1a858db9265356f4`.

### Optional discovery replay

The graph was found in one `Kissat --time=120` call, exit10, in 91.702187
seconds including construction, peak child RSS27,760 KiB. The complete
SAT assignment and the decoded graph were checked. [discovery.json](discovery.json)
records the run and its provenance. No UNSAT outcome or proof trace is
used as evidence. The large discovery trace and log stay outside Git.

The published generator reproduces the original formula byte for byte,
including under optimized Python:

```sh
python3 -B generate.py --work /scratch/new-root20-formula --emit-only
sha256sum /scratch/new-root20-formula/case.cnf
python3 -B generate.py --work /scratch/new-root20-search \
  --kissat /path/to/kissat --seconds 120
python3 -B verify.py --graph /scratch/new-root20-search/graph.json \
  --handoff HANDOFF.json --report /scratch/new-root20-discovery-check.json
```

The last command checks against the **published** handoff and therefore
expects the same marked graph. If a rerun finds a different graph, first
regenerate its handoff with `handoff.py --graph NEW_GRAPH --output NEW_HANDOFF`
and verify those two files together. Bounded solver behavior is host-dependent;
a timeout is UNKNOWN and does not invalidate the existing graph certificate.

The discovery formula has153 primary variables,9,618 total variables and
51,170 clauses, of which13,078 are distinct direct Ramsey clauses. It
fixes all37 edges incident with the two local roots;11 are red, so the
153 remaining edges must contain exactly81 red edges. The exact threshold
counter is imported from the byte-pinned
[earlier generator](../ramsey_r55_triple_graph_realization/generate.py),
SHA256 `0cf0264142d89472cb93358bc8f4ecf33d13b8996aba03672dd401133257e898`.
Within each of X,A,B, adjacent rows are lex ordered, omitting the mutual
entry. This is safe relabeling normalization: a global lex-minimum edge
vector under within-cell permutations satisfies every such comparison.
It imposes no graph automorphism. None of these discovery-encoding claims
is required by the direct positive witness proof.

Formula SHA256:
`90739bbfc9ad1fa298d6d1fa9b05c33c121ad34292998e989ae6f7034300d482`.
Kissat4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
binary SHA256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.

## Context, trust and stopping boundary

The [two-stratum interface](../ramsey_r55_two_stratum_kernel) identified
the remaining fully visible constraints for proper signatures. The next
monolithic visible-skeleton pilot returned UNKNOWN after180seconds; its
source and audited formula were preserved locally, not published as a
mathematical finding. This pass changes scale to an actual root
neighborhood and provides a positive, directly checked object.

The new external [convex barrier](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_anchor_convex_barrier),
Discovery Net `bafkreigymf3xqhcm27sn3lyszkwxevkwdcjxvgjv35fwx4gxyi3nq5pjsi`
at height2951, concerns a different d=22 slice including empty/full
signatures. It reinforces the need for joint Boolean graph structure,
but supplies no premise or exclusion for this certificate. Its body was
read; its source was not replayed. No orbit-averaging or symmetry search
is duplicated here. The teammate's independently accepted34-case residual
symmetry review is recorded in the local campaign checkpoint, not used
as a proof input.

The trust base for the positive result is the explicit small edge list,
simple set/bitset enumeration, the displayed embedding and equations,
Python/runtime/hardware, and SHA256 for file identity. There is no
independent peer review or proof-assistant formalization. Internal
algorithmic separation is not represented as either.

The coherent milestone ends with this local graph and exact handoff.
The full 627-variable extension remains open. The next bounded direction
is to test this **specific** marked graph's visible lift with all remaining
root/stratum tests and exact degrees/profiles, followed by the complete
invisible-edge constraints if a visible skeleton is found. No such lift,
another local graph search, or extended timeout is begun here.
