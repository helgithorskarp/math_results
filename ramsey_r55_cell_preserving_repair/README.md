# Cell-preserving graph repair reaches a certified descent barrier

Twelve explicit four-edge switches reduce the central local-cap error of the
[previous 43-vertex realization](../ramsey_r55_triple_graph_realization) from
143 to 83. They preserve every individual degree, every signature-cell edge
total, all exceptional local counts, all mixed-K5 constraints, and all 884
pointwise root bounds. The new graph still has **492 monochromatic K5s** and
29 central local-cap failures: it is **not a Ramsey (5,5;43) graph**.

The exact endpoint audit proves a useful limitation: among all 11,453
four-edge central edits preserving degrees and cell-edge quotas, no admissible
edit strictly improves the local-cap objective. Four neutral edits remain;
their supports are exposed for a possible next bounded plateau investigation.
No neutral walk or larger-edit search is included in this milestone.

This is graph-level repair and a precisely delimited local barrier, not a
new aggregate census, a whole-profile exclusion, or an improvement to a
Ramsey-number bound. The 66-profile/271-split hard frontier is unchanged.

## Invariant-preserving mechanism

Let E be the exceptional set, let C be its complement, and group central
vertices by their red neighborhood X in E. For distinct a,b,c,d in C with
`X_a=X_b`, switch red ac,bd to blue and blue ad,bc to red. This preserves
degrees, all signature-cell edge quotas and exceptional local edge counts.
Of the pointwise root-degree rows, only those at a,b can change.

The actual red-triangle change at any outside vertex u is
`(x_ua-x_ub)(x_ud-x_uc)`. Corresponding endpoint formulas give an exact
linear-time score update. Newly forbidden mixed K5s can be found by inspecting
same-color triangles around the four changed edges. These are implementation
shortcuts with proved hypotheses; they are not assumed by the independent audit.

[PROOF.md](PROOF.md) proves these assertions and shows that this switch form
covers every four-edge central degree/quota-preserving edit. The standard
restricted-switch idea is not claimed new. Connectivity of this additionally
constrained realization space is not asserted.

## Exact input, path and endpoint

E=`{0,1,2}` is a red triangle of degree-20 vertices; C=`3..42` consists of
degree-21 vertices. Signature multiplicities in mask order 0..7 are
`(0,8,8,6,10,4,4,0)`. All exceptional local profiles remain `(92,107)`.

For a central vertex of signature X, the degree identity gives
`t_R+t_B=201-|X|`. Therefore the required hard-branch caps `t_R,t_B<=100`
are equivalent to `101-|X|<=t_R<=100`. Phi is the sum of the integer distances
from these intervals. The verified path has scores

```text
143,133,125,118,112,108,102,98,95,92,89,86,83.
```

[PATH.json](PATH.json) gives the twelve moves and discovery records.
[GRAPH.json](GRAPH.json) is the endpoint's 43 hexadecimal red-adjacency rows,
SHA256 `7a832f229bb3fd97f5c3e5dceb060988fb5c5d2df074d1cb37ddbb1dcd5fc8a6`.
It retains the original graph's 450 red edges and all cell-pair quotas.

| Literal graph property | Input | Endpoint |
|---|---:|---:|
| Central local-cap error Phi | 143 | 83 |
| Central vertices failing local caps | 39 | 29 |
| Red K5s | 327 | 240 |
| Blue K5s | 245 | 252 |
| Monochromatic K5s meeting E | 0 | 0 |

All 492 remaining K5s lie inside C. The endpoint still fails the full
exceptional-neighborhood conditions: its red neighborhoods at roots 0,1,2
contain respectively 11,6,5 blue K5s, and its blue neighborhoods contain
36,25,28 red K5s. Counts for different roots may overlap.

## Complete endpoint repair classification

The verifier enumerates all 91,390 central four-sets and all pairs of perfect
matchings on each. Literal degree/quota preservation leaves exactly 11,453
distinct four-edge edits. Their complete support set agrees entry for entry
with the search's opposite-same-cell-pair generator.

Of these edits, 2,855 lower Phi algebraically. Of those, 618 fail a pointwise
bound; all remaining 2,237 create a mixed K5. Thus none is a permitted strict
improvement. Among ALL edits, 1,640 fail the pointwise gate and another 9,620
fail the mixed gate, leaving 193 admissible neighbors: four neutral and 189
uphill. This is a pointwise-first partition, not disjointness of the underlying
failure properties. [report.json](report.json) gives the full score histogram
and all four neutral supports.

The endpoint is a local minimum **allowing ties**, not a strict local minimum,
an isolated graph or a global minimum. The result does not exclude another
descent path, a neutral/uphill escape, a larger simultaneous edit, or a graph
with different cell quotas. In particular it does not settle the previous
UNKNOWN central-profile or full-neighborhood formulas.

## Reproduction and independent checks

CPython 3.11.2, standard library only. From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --report /tmp/r55-switch-report.json
cmp report.json /tmp/r55-switch-report.json
PYTHONDONTWRITEBYTECODE=1 python3 controls.py --report /tmp/r55-switch-controls.json
cmp controls_report.json /tmp/r55-switch-controls.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py --report /tmp/r55-switch-report-O.json
cmp report.json /tmp/r55-switch-report-O.json
PYTHONDONTWRITEBYTECODE=1 python3 -O controls.py --report /tmp/r55-switch-controls-O.json
cmp controls_report.json /tmp/r55-switch-controls-O.json
sha256sum -c SHA256SUMS
```

The mathematical verifier imports no search code. It replays all twelve
switches, recomputes local triangles literally, checks every path invariant,
and enumerates the complete endpoint neighborhood via four-set matchings.
It classifies rejected moves using an explicit violated root inequality or
an actual monochromatic five-set. The full classification is regenerated,
not committed as a large enumeration dump. Its SHA256 is
`3b7c7ad0819528559b444f64e4e31d4019ae99a8a0ac4fadca13234cf8c54846`.

The pinned predecessor graph checker verifies all 962,598 literal five-sets
and compares complete K5 lists with a separate recursive bitset enumeration.
Its previous finite signature census is not rerun. No SAT verdict, solver
trace, floating-point library or graph-isomorphism package is used here.

Controls exhaust 2,048 six-vertex switch completions for the triangle update
and all 256 assignments of four partition labels for the quota criterion.
The mixed-clique gate is tested on all 131,072 seven-vertex completions;
129,664 are initially mixed-free, and 784 of those introduce a mixed K5 that
the gate correctly rejects. Seven vertices are important: the six-vertex
K5 switch test would be vacuous. Four malformed-path/endpoint controls fail
as required. Normal and optimized reports match byte for byte.

Measured fresh verification took 14.052 seconds with peak RSS 21,656 KiB;
the full controls took 10.680 seconds with peak RSS 30,256 KiB. These two
measurements ran concurrently on the research host, so their wall times are
not isolated-performance benchmarks.

Optional deterministic search reproduction, using a fresh directory outside Git:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 search.py --work /tmp/r55-switch-fresh
cmp GRAPH.json /tmp/r55-switch-fresh/GRAPH.json
python3 verify.py --path /tmp/r55-switch-fresh/result.json \
  --graph /tmp/r55-switch-fresh/GRAPH.json --report /tmp/r55-switch-fresh/audit.json
cmp report.json /tmp/r55-switch-fresh/audit.json
```

The discovery run took 4.933 seconds with peak RSS 56,128 KiB. It has no
timer-dependent outcome: each accepted step strictly lowers a nonnegative
integer, and each step's finite neighborhood is fully scanned. Fresh production
reproduced the exploratory graph and all path scores. PATH.json's resource
fields need not reproduce exactly; its actual moves are independently checked.

## Shared context and trust boundary

The [external guarded deletion cuts](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_local_deletion_cuts)
at Discovery Net height 2751 were read as external, unreviewed infrastructure.
Their derivation is not duplicated, and their rows are not used or certified
for this path. They remain a possible stronger constraint layer; passing the
present gates is not claimed to imply passing them. The external M=214
codegree-nine pair-root quotient at height 2755 concerns a different profile.
Neither changes this fixed graph's local switch classification.

The teammate's independently accepted eleven-cycle split restriction and new
three-minority-core handoff remain in the separate symmetry lane. No symmetry
assumption, catalog-neighborhood search, closed order-five branch, or previous
whole-profile closure was reopened.

Remaining trust lies in the displayed unformalized arguments, the explicit
graph and path, exact Python source/runtime, SHA256 provenance and ordinary
hardware. The inherited interpretation of the hard-branch cap uses the earlier
Ramsey-extremal catalog boundary. The direct graph and local-minimum statements
do not depend on that catalog's completeness. Different algorithms and controls
are internal validation, not an independent peer-review verdict.

At this completed boundary no computation is running. The best next bounded
test is the four exposed neutral directions, with the stronger global Ramsey
conditions still visible; that test has not begun here.
