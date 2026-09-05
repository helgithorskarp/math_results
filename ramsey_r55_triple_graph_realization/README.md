# A degree-exact graph realizes the mixed-clique and exceptional-root filters

[GRAPH.json](GRAPH.json) is an explicit simple graph on 43 vertices with
degrees `20^3 21^40`. It realizes one surviving signature pattern of the
[470-case aggregate filter](../ramsey_r55_external_root_lifting), and passes
the following **joint** conditions on actual individual edges:

- all 43 prescribed degrees and all fixed exceptional incidences;
- all exceptional local **edge-count** caps;
- every forbidden monochromatic five-set that meets the exceptional set E;
- all exceptional-root union bounds and all **pointwise** external-root
  lifting inequalities, not just their sums over signature cells.

This is **not a Ramsey (5,5;43) graph**. It contains 327 red K5s and 245
blue K5s, all entirely among the forty central vertices. Furthermore,
39 central vertices violate their required hard-branch local edge caps.
The graph also fails the *opposite-color* five-clique requirements inside
the exceptional neighborhoods. Those failures are explicitly counted below.

Thus the mixed-clique/degree/lifting layer has a genuine simple-graph
realization, but does not force a target graph or even genuine local Ramsey
neighborhoods. No whole profile is excluded; the campaign counts remain
66 profiles / 271 anchored splits. No census of the other retained cases
was performed.

## 1. Exact graph and prescribed data

Vertices E=`{0,1,2}` form a red triangle and have degree 20. Vertices C=`3..42`
all have degree 21. There are exactly 450 red edges. Every central signature
X is its red neighborhood within E. Its mask is `sum_(i in X) 2^i`.
The signature vector in mask order `0..7` is

```text
(0,8,8,6,10,4,4,0).
```

Central vertices are ordered by increasing mask. The six cells occupy
`3..10`, `11..18`, `19..24`, `25..34`, `35..38`, `39..42`, respectively.
This is a fixed input from the parent finite census, not an automorphism
assumption on the graph. The input parent certificate and its surviving
record are pinned and checked; the remaining parent census is not rerun.

The 898-byte graph certificate lists 43 hexadecimal adjacency bitmasks. Bit v
of row u is one exactly when uv is red. Its SHA256 is

```text
a57fc26ea50196d82537220cf057c659860f9842dd35351d33445781f019eae5
```

At each exceptional vertex, the actual local profile is `(t_R,t_B)=(92,107)`.
Here t_R counts red edges induced by red neighbors; t_B counts blue edges
induced by blue neighbors. The hard-branch scalar requirements are
`t_R<=93, t_B<=107` at E and `t_R,t_B<=100` at C. Only the E requirements
are satisfied. The degree identity `t_R+t_B=201-|X|` at C explains why
singleton cells would need exactly `(100,100)` and pair cells would need
`(99,100)` or `(100,99)` in a genuine hard-branch graph.

## 2. What the graph actually verifies

The checker exhausts all 962,598 five-sets by their ten literal edge colors.
A separate recursive bitset clique extension enumerates monochromatic
five-sets; the complete lists agree. None of the 304,590 five-sets meeting E
is monochromatic.

For every disjoint red clique A and blue clique B in E, with A or B nonempty,
let S be the vertices outside the roots that are red to A and blue to B.
There are 19 valid root pairs. For every u outside the roots, the graph obeys

```text
u red to A  => d_R(u,S) <= U(4-|A|,5-|B|)-1,
u blue to B => d_B(u,S) <= U(5-|A|,4-|B|)-1.
```

U is the elementary parity-refined Ramsey recurrence used in the parent.
There are 884 verified pointwise inequalities, including 410 with u outside S;
minimum slack is zero. Fixed exceptional vertices and central vertices are
both checked. All 19 union capacities also hold. The six one-way side sizes
are `12,12,14,14,14,14`, so the order-15/16 density bounds are **vacuous here**.

Summing pointwise inequalities over cells recovers the parent's aggregate
lifting rows. Individual degrees give its cell-degree equations, and the
local profiles give its exceptional edge intervals. Integer cell-edge counts
are obtained from actual edges and satisfy the simple-graph boxes. Together
with the vacuous density rows this verifies all retained aggregate stages for
this graph, not merely a separate, possibly incompatible aggregate primal.

The source also computes the precise gaps beyond this layer:

| Root | Blue K5s inside its red neighborhood | Red K5s inside its blue neighborhood |
|---:|---:|---:|
| 0 | 11 | 38 |
| 1 | 6 | 25 |
| 2 | 5 | 26 |

There is no red K4 inside a root's red neighborhood and no blue K4 inside
its blue neighborhood: each would already make a monochromatic K5 meeting E.
But avoiding those K4s and satisfying local **edge counts** is not the same
as having full `(4,5)` or `(5,4)` Ramsey neighborhoods. The table records the
missing opposite-color K5 condition. Overlap between roots is allowed, so
the table entries are not counts of distinct global obstructions.

The full 572 central five-cliques and 39 failed central local caps ensure
that this is a limitation witness, not a construction claim. No priority
claim is made for the standard idea of realizing partial Ramsey constraints.

## 3. One bounded full-neighborhood decision checkpoint

A second formula adds exactly 104,336 distinct ten-literal clauses: forbid a
blue central K5 inside any red exceptional neighborhood, and forbid a red
central K5 inside any blue exceptional neighborhood. Together with the
mixed-five-set clauses, these would make each exceptional neighborhood a
genuine Ramsey `(4,5)` or `(5,4)` graph. They do not impose every central
local profile or every remaining central K5 condition.

Both models fix this one core/signature record. Each has 780 primary edge
variables and 52,901 total variables. The mixed model has 236,260 clauses;
the full-neighborhood model has 340,596. Both impose all individual degrees
and the exceptional local edge intervals. Neither SAT formula explicitly
includes the external-root inequalities; the positive graph is separately
verified against all of them. A future SAT output must pass that audit too.

The full-neighborhood solver returned **UNKNOWN** at its 60-second bound.
There is no SAT/UNSAT verdict or proof certificate. The source reproduces
its exact formula, SHA256
`1480325fd9f354642e4aae4d836723c77a5349e0e721f41a7e3284844e344093`.
See [neighborhood_checkpoint.json](neighborhood_checkpoint.json). No time
limit was extended, no other signature case was started afterward, and no
background solver remains.

The encoding uses unary prefix counters `s[i,j] <=> count(first i)>=j`.
The recurrence `s[i,j] <=> s[i-1,j] OR (x_i AND s[i-1,j-1])` gives four
clauses and proves the counter semantics inductively. It is tested on all
16,894 input/bound combinations through seven inputs. The mixed primary
clauses are independently reconstructed from literal five-sets; the added
family is reconstructed by enumerating each exceptional neighborhood.
The entire counter suffix is unchanged between the two formulas. These
audits do not manufacture a conclusion for the stopped stronger search.

## 4. Reproduction, provenance, and handoff

Proof verification uses CPython 3.11.2 and its standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --report /tmp/triple-graph.json
cmp report.json /tmp/triple-graph.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py --report /tmp/triple-graph-O.json
cmp report.json /tmp/triple-graph-O.json
python3 audit_encoding.py --report /tmp/triple-encoding.json
cmp encoding_report.json /tmp/triple-encoding.json
sha256sum -c SHA256SUMS
```

The graph checker imports no generator or solver. It verifies every claimed
graph property directly, compares complete clique lists, checks all 1,024
five-vertex colorings, and rejects malformed graph data, altered individual
degrees, and an attempted full-Ramsey claim for this very witness. Normal
and optimized reports agree. [report.json](report.json) includes all local
profiles and actual cell-edge counts.

Optional bounded regeneration uses Kissat 4.0.4, source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`:

```bash
python3 generate.py --work /tmp/triple-mixed-fresh \
  --kissat /path/to/kissat/build/kissat --seconds 60
python3 verify.py --graph /tmp/triple-mixed-fresh/graph.json
python3 generate.py --work /tmp/triple-neighborhood-fresh \
  --full-neighborhoods --emit-only
```

Work directories must be new. Omitting `--emit-only` with `--kissat` starts
one bounded stronger solve; that is a new research decision, not part of
replaying the present certificate. Generated formulas and logs stay outside
Git. The generic root-clique encoder in the preceding M=216 template package
is reused with its source hash pinned. The positive proof does not rely on
that encoder or on the SAT cardinality construction.

Fresh production regeneration returned the same actual graph as the initial
probe, taking 6.783 seconds with 72,680 KiB largest child peak RSS. Solver
and formula hashes are in [discovery_report.json](discovery_report.json).
An unchecked SAT exit is not evidence until its graph passes `verify.py`.

During this pass, Discovery Net height 2731 independently published a
[different M=216 pointwise realization](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m216_signature_cut_transfer)
that avoids the earlier seven-root template cut. Its committed report was
read; its source was not rerun here. That result does not claim all mixed
five-set constraints. The present work stays on the distinct `20^3 21^40`
frontier, adds all such mixed constraints, and records the next full-neighborhood
boundary without taking over the M=216 continuation.

Remaining trust lies in the explicit graph, exact Python checker, unformalized
definitions and implication arguments, Python/standard-library semantics,
SHA256 for provenance, and ordinary hardware. There is no new independent
peer-review claim. The positive result needs no solver verdict, proof trace,
floating-point computation, or catalog. The graph fails the campaign target,
which remains open. The next natural direction is genuinely pointed-neighborhood
or central-profile compatibility, not another isolated aggregate count.
