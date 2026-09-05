# Complete extensions with the forced empty prefix and sharp pair cuts

Let G be a hypothetical Ramsey `(5,5;43)` graph with an order-three
automorphism of cycle type `1^10 3^11`. Work in the four-versus-seven
internal-color split: cycles C0,C1,C2,C3 are red triangles; the other seven
moving triangles are blue. The ten fixed vertices are 33 through 42.
A fixed vertex is uniform to every moving triangle. Its four-bit signature
S is the subset of the red triangles to which it is red.

The inherited complete boundary has 26 four-triangle action classes,
covering 16,605 labeled cores. All have an empty-signature requirement by
the [preceding rigidity theorem](../ramsey_r55_order3_eleven_noempty_rigidity/PROOF.md).
The current milestone tests their **complete 43-vertex extensions** with
that requirement and the sharp pair-signature bound below. It introduces
no restricted fixed graph, selected degree profile, blue attachment,
additional automorphism, or edit radius.

## The two necessary consequences

First, some fixed vertex has signature empty. The accepted complete parent
orders all ten fixed vertices lexicographically by their eleven uniform
attachment bits, with the four red-triangle bits first. Hence the first
fixed vertex has four-bit prefix 0000. This gives four negative primary
units, and leaves its seven blue-triangle bits and nine fixed edges free.
This uses the existing ordering, with no new normalization.

Second, for distinct i,j, let x_i count signatures {i} and y_ij count
signatures {i,j}. Then

```text
x_i + y_ij <= 2.                                         (1)
```

Three such vertices would all be red to Ci. Each pair must consequently
be blue, or that pair and Ci would give a red K5. They are also blue to
both red triangles Ck,Cl outside {i,j}. Some cross-edge between Ck and Cl
is blue, because otherwise their six vertices form a red K6. That edge
and the three fixed vertices would form a blue K5. This proves (1).

This argument applies whether empty signatures exist or not. The omitted
coordinate j is unrestricted. No fixed vertex with empty signature is
counted in (1). The proof uses the four red triangles and absence of
monochromatic K5, without a degree bound or a blue moving triangle.
For each of the 26 literal cores and each of the twelve ordered i,j
choices, the independent auditor supplies an actual blue cross-edge,
checking all 312 local applications of this argument.

The [previous hand proof](../ramsey_r55_order3_eleven_noempty_rigidity/PROOF.md)
already established (1) and used it to close its last no-empty profile.
The new mathematical question here is what happens when this consequence
and the forced empty prefix are propagated into **all 26 full extensions**.
No priority claim is made for the elementary clique-completion argument.

## Exact clause bridge

The primary variable l(f,i) for a fixed vertex f and moving triangle i is

```text
l(f,i) = 211 + 11(f-33) + i.
```

Positive literals mean red edges. The four new units are

```text
-211, -212, -213, -214.
```

For every unordered triple T of fixed vertices and ordered distinct i,j
in {0,1,2,3}, let k<l be the remaining two red-triangle indices. Append

```text
OR over f in T of (-l(f,i) OR l(f,k) OR l(f,l)).            (2)
```

This nine-literal clause is false precisely when all three signatures
belong to {{i},{i,j}}, independently of their j bits. It is therefore
exactly a forbidden-three encoding of (1). There are
`C(10,3)*4*3 = 1,440` such clauses. With the four units the complete
new tail has 1,444 clauses and no new variable.

The parent is the full accepted r=4 formula, with 34,280 variables and
615,920 clauses, followed by the eighteen units for the selected core.
The inherited [intrinsic anchor propagation](../ramsey_r55_order3_eleven_anchor_propagation)
also retains every applicable `z+x_i>=2` condition, where z counts empty
four-bit signatures. With g applicable complementary anchors, that
strengthened base has

```text
34,280+10g variables,       615,938+50g clauses.
```

Every byte of its body is retained. The new final dimensions are

| g | Number of tested cores | Variables | Clauses |
|---|---:|---:|---:|
| 1 | 7 | 34,290 | 617,432 |
| 2 | 18 | 34,300 | 617,482 |
| 4 | 1 | 34,320 | 617,582 |

No parent clause, normalization, core unit, or earlier anchor condition
is removed. The new empty-prefix units use the entire preceding no-empty
closure, rather than treating the earlier UNKNOWN runs as evidence.

## Auditing and proof interpretation

The deterministic producer pins the preceding complete result, the
no-empty boundary and classification, its hand proof, and its compact
local obstructions. `rebuild.py` uses an isolated module namespace to
regenerate the complete parent, run its separate C++ clause audit,
reconstruct all 26 strengthened bases, and compare them against the
published full-base hashes. It also runs the prior normalization and
anchor controls. No old solver search is repeated in this preparation.

The new `audit.py` imports no producer module. It checks every case and
its inherited hash entry, reconstructs each twelve-vertex core as a
literal graph, and verifies all local five-sets and the 312 blue
cross-edge witnesses. It independently recovers the 320 primary
variable meanings from unordered-edge orbits of the actual action on
43 vertices. It compares the entire base prefix, the four first-row
units, and every one of the 1,440 cuts, along with dimensions and EOF.

For every ordered i,j it examines all 16^3 assignments of complete
four-bit signatures to three vertices: 49,152 truth assignments in total.
The logical falsity of (2) agrees exactly with the three signatures all
being {i} or {i,j}. This includes both possibilities of the unrestricted
coordinate j, all empty signatures, and every other signature size.
Four malformed case records and eight malformed formulas must be rejected.
Normal and optimized-Python control reports agree. The inherited no-empty
arithmetic classification and its solver-free local certificates are
also rechecked during both production and fresh verification.

Each of the 26 complete cases has a fixed 20-second Kissat cap. An UNSAT
exit is accepted only after a full DRAT proof replay against that exact
full formula. A fresh verification reconstructs all bases and children
again and replays each complete refutation a second time. UNKNOWN remains
inconclusive, and its partial trace is neither a proof nor a solver state.
A SAT output would require decoding a compact 43-vertex red edge list
and independent literal inspection of all five-sets before a target claim.

The finite result and remaining whole-core boundary are in `README.md`,
`result.json`, `verification.json`, and `boundary.json`. The current
milestone adds only the proved constraints above and finishes the complete
bounded test; it does not start an empty-multiplicity split or another
moving-cycle count.

The no-empty theorem and its new use here await independent review.
The complete parent, 197-class cover, abstract signature lemma, universal
anchor theorem, and previous eight intrinsic-anchor whole-core exclusions
have accepted independent reviews. The cumulative starting 171/26 count
additionally imports older empty-signature-specific exclusions that remain
review boundaries. The externally established R(4,5)=25 degree window is
inherited from the complete parent, not recomputed here. The unformalized
reduction, exact source/runtime/compiler/hardware, hash identity, and full
DRAT checker remain trust boundaries. Internal independent implementations
and second replays are not peer review or proof-assistant formalization.
