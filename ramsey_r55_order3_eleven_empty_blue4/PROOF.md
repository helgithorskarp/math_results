# The maximal blue-moving-neighbor branch of the first empty fixed vertex

Let G be a hypothetical Ramsey `(5,5;43)` graph invariant under an
order-three action `1^10 3^11`, in the four-red-triangle/seven-blue-triangle
split. Use the accepted full-parent convention: red moving triangles
C0,...,C3, blue moving triangles C4,...,C10, and fixed vertices 33,...,42.
The complete inherited boundary contains 25 possible red-core classes.

The [forced-empty theorem](../ramsey_r55_order3_eleven_noempty_rigidity/PROOF.md),
now independently accepted for the explicit residual cores, and the existing
lexicographic fixed-row order force vertex e=33 to be blue to all twelve
vertices of the four red triangles. This pass studies one complete branch:
**e is also blue to exactly four of the seven blue moving triangles.**
No other empty fixed vertex is selected or reordered.

## The degree boundary

Let b count blue moving triangles to which e is blue, and let h count its
red neighbors among the nine other fixed vertices. Uniformity gives

```text
d_red(e)  = 3(7-b) + h,
d_blue(e) = 12 + 3b + (9-h) = 21+3b-h.
```

The inherited degree window is 18<=d_red(e),d_blue(e)<=24. It follows
that b<=4, since h<=9. If b=4, the twelve red-core vertices and twelve
vertices in blue moving triangles already provide 24 blue neighbors.
Therefore every other fixed vertex is red to e, h=9, and

```text
(d_red(e),d_blue(e)) = (18,24).                         (1)
```

The seven blue-moving links thus have exactly three red bits, and all nine
fixed edges from e are red. Conversely, these assignments give b=4 and
(1). They describe the whole maximal branch, without choosing which four
moving triangles are blue to e. All `C(7,4)=35` labeled choices are kept.

The blue neighborhood in this branch consists of 24 moving vertices,
invariant under eight 3-cycles: four internally red and four internally
blue. It contains neither a red K5 nor a blue K4, since a blue K4 would
complete a blue K5 with e. This explains why the saturated neighborhood is
a useful frontier. The production formulas nevertheless retain all 43
vertices and every original Ramsey, degree, common-neighborhood, deficit,
and normalization constraint; they do not replace the problem by a
24-vertex relaxation.

## Exact complete formula

The full base for each current core is imported from
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation).
It already contains the four units making e's red-core signature empty,
the sharp singleton/pair cuts, all earlier intrinsic anchor constraints,
the eighteen core units, and the complete accepted r=4 parent.

Positive primary variables mean red edges. The moving attachment L(e,j)
for j=4,...,10 is 211+j, namely 215,...,221. Exactly three of those seven
bits are red. Encode at least three by every positive five-subset clause
(21 clauses), and at most three by every negative four-subset clause
(35 clauses). Equation (1) gives the nine positive fixed-edge units
166,...,174. Thus each full base receives exactly **65 clauses and no new
variable**. No clause or normalizer is removed.

| Applicable complementary anchors g | Tested cores | Final variables | Final clauses |
|---|---:|---:|---:|
| 1 | 6 | 34,290 | 617,497 |
| 2 | 18 | 34,300 | 617,547 |
| 4 | 1 | 34,320 | 617,647 |

The pair-orbit convention and the existing fixed-row ordering are unchanged.
We impose neither an arbitrary first-four choice of blue moving triangles
nor a new permutation of fixed vertices. Consequently the tested branch
is specifically about the first fixed vertex in a normalized complete
representation. If this branch is excluded for a core, then that
representation must have b<=3, and in particular the graph has an empty
fixed vertex with at most three blue moving-triangle neighbors. This does
**not** assert that every empty fixed vertex has that property. An excluded
b=4 branch alone does not exclude the whole core: its b<=3 extensions remain.

## Independent checking and bounded decision

`cube.py` pins the previous complete result, verification, and boundary,
and obtains all and only its 25 unresolved full-core cases. `rebuild.py`
uses an isolated module namespace to regenerate the preceding entire
preparation, compare it against the published preparation entry by entry,
and reconstruct all 25 current complete bases with their exact hashes.
The preceding full-parent C++ audit, intrinsic-anchor checks, no-empty
arithmetic/local certificates, signature truth tables, and mutation
controls all run in this chain. A compact hash of the matched preparation
is recorded instead of embedding another copy of the transitive report.

The new `audit.py` imports no producer. It independently recovers the 320
primary edge-orbit meanings from the literal action on the 43 vertices.
It compares the whole inherited base, independently generates the exact
cardinality clauses and nine fixed edges, and checks dimensions and EOF.
Every one of the 128 seven-bit assignments is checked against “exactly
three red,” with the accepted assignments matched to all 35 labeled
four-blue choices. It also enumerates all 128*512=65,536 assignments of
moving and fixed incidences of e. Every degree-valid assignment has b<=4;
exactly 35 degree-valid assignments have b=4, and each has h=9 and degrees
(18,24). Three malformed case records and nine malformed formulas are
rejected; normal and optimized-Python control reports agree.

The complete bounded run uses two workers and 20-second Kissat caps.
An UNSAT exit is accepted only after full DRAT replay against its exact
complete branch formula. A separate fresh verification regenerates every
base and child and replays every completed refutation a second time.
RAT steps are permitted and checked. UNKNOWN is inconclusive; a partial
trace is neither a refutation nor a resumable solver state. A SAT answer
would be decoded into an explicit 43-vertex edge list and inspected over
all five-sets before a target coloring claim.

The resulting branch exclusions and unresolved cases are reported in
`README.md`, `result.json`, `verification.json`, and `boundary.json`.
The full-core count is preserved separately from the b=4 branch count.
This milestone stops after the complete b=4 test and its verification;
it does not open the complementary b<=3 phase.

## Dependencies and scope

The complete parent, 197-core cover, abstract signature lemma, two-empty
anchor theorem, intrinsic-anchor propagation, and forced-empty theorem
have accepted independent reviews. The previous core123 full exclusion now also has an
[accepted independent review](../ramsey_r55_order3_eleven_empty_propagation_review1).
Older empty-signature-specific closures remain inherited review boundaries
for the starting 25-core bookkeeping. The degree window uses
the parent's external R(4,5)=25 theorem; its original computation is not
repeated here. The new branch encoding and any refutations await independent
review. Ordinary unformalized reductions, source/runtime/compiler/hardware,
SHA-256 identity, and the external full DRAT checker remain trust boundaries.
Internal independent reconstruction and second replay are not independent
peer review or proof-assistant formalization. No Ramsey lower-bound
improvement or complete eleven-cycle exclusion is inferred from a branch
closure. Large formulas, proofs, and logs remain outside Git; hashes and
compact reports alone are not refutations.
