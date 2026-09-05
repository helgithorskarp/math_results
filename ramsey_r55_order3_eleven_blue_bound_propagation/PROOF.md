# Propagating the first empty vertex's attachment bound into full extensions

Fix the order-three action `1^10 3^11` on a hypothetical 43-vertex
Ramsey(5,5) graph. The moving triangles C0,...,C3 are internally red;
C4,...,C10 are internally blue; fixed vertices are 33,...,42. Use the
complete parent normalization without any change. The independently
accepted forced-empty theorem makes the first fixed vertex e=33 blue to
all twelve red-core vertices in the listed residual cores.

Let b be the number of blue moving triangles to which e is blue, and h its
number of red neighbors among the other nine fixed vertices. Then

```
d_red(e)=3(7-b)+h,  d_blue(e)=21+3b-h.
```

The inherited window 18<=d_red(e),d_blue(e)<=24 implies b<=4. Equality
b=4 forces h=9 and degrees (18,24). The previous
[complete maximal-branch test](../ramsey_r55_order3_eleven_empty_blue4)
refuted this entire equality branch, including every labeled choice of
four blue triangles, in precisely these 19 core classes:

```
92,97,109,114,118,119,122,154,164,167,177,182,185,186,188,190,191,192,193.
```

Those imported full DRAT proofs were each replayed twice. During this pass,
reviewer-1 independently accepted all nineteen branch exclusions in
[the maximal-attachment review](../ramsey_r55_order3_eleven_empty_blue4_review1),
source `cd6eb0daf6e1e0d75367e3941c345c29decd512a`. Conditional on the
accepted encoding and checked refutations,
every normalized full extension of one of these cores satisfies b<=3.
Six other cores, 124,155,159,168,180,194, have no such established bound
and are excluded from this pass's tests. The statement concerns e=33 in
the existing canonical representation, not every empty fixed vertex.

## The full-extension reduction

Let F_c be the complete unrestricted formula for core c in
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation).
It contains the accepted r=4 parent, all 18 core units, intrinsic-anchor
consequences, the four first-fixed empty-prefix units, and 1,440 sharp
singleton/pair cuts. It already retains every Ramsey, degree,
common-neighborhood, deficit, and normalization constraint of the parent.

The seven primary variables 215,...,221 mean that e is red to C4,...,C10.
Append, for every four-subset S of these variables, the positive clause

```
OR_{v in S} v.                                              (1)
```

The 35 clauses (1) assert that no four of these bits are simultaneously
blue. They are equivalent to b<=3, or at least four red links. Thus a
full graph with core c satisfying the inherited hypotheses gives a model
of F_c plus (1). Refuting this strengthened formula excludes the **whole
core**, using the imported b=4 exclusion for the other side of the split.
A timeout gives no such conclusion.

All fixed edges remain subject to F_c only: no extra fixed-edge unit is
added. The number of red moving links is not fixed to four; all counts
four through seven are allowed when consistent with F_c. The six cases
without an imported b=4 exclusion receive no new clause or solver test.
No permutation, arbitrary attachment choice, or stronger fixed-vertex
normalization is introduced.

Crucially, F_c is the **unrestricted base**, not the preceding maximal
branch formula. The latter imposes exactly three red moving links and
nine fixed red edges. Appending (1) to that branch formula would yield an
irrelevant contradiction. The generator and independent auditor match
unrestricted base hashes from the earlier full-extension result and
explicitly reject maximal-branch formula identities.

| Complementary blue-triangle-free anchors g | Tested cores | Base clauses | New clauses | Variables |
|---|---:|---:|---:|---:|
| 1 | 6 | 617,432 | 35 | 34,290 |
| 2 | 13 | 617,482 | 35 | 34,300 |

No auxiliary variable is introduced. Final clause counts are 617,467
and 617,517 respectively.

## Reproduction and checking

The source contract pins the imported branch result, verification and
boundary, as well as the transitive generator/checker sources. Preparation
reconstructs all 25 current unrestricted bases through the previous
complete preparation, matches that published preparation entry by entry,
and checks every base hash. It selects only the 19 imported exclusions.

The new auditor imports no producer code. It enumerates literal edge
orbits of the action on 43 vertices, recovers the 320 primary variables,
and independently generates (1). For every tested formula it compares
the full unrestricted prefix, exact header, exact tail, and EOF. It checks
all 128 moving assignments and all 65,536 moving/fixed incidence
assignments. Exactly 64 moving patterns satisfy the new bound. All 17,728
incidence assignments satisfying the inherited degree window and b<=3
satisfy the new tail; the tail contains no fixed-edge variable. Thirteen
malformed inputs, including branch/base confusion and an unproved case,
are rejected. Normal and optimized Python reports must agree.

The bounded decision test uses two workers and a 20-second Kissat cap per
case. An UNSAT result is accepted only after full DRAT replay, including
RAT steps. Fresh verification reconstructs all 25 unrestricted bases and
all 19 new formulas again, and replays every new complete proof a second
time. A SAT claim would require an explicit 43-vertex edge list and an
independent literal check of all five-sets. UNKNOWN traces are not proofs
or saved solver states. The reports state the actual outcome.

## Imported trust and scope

The full parent, 197-core cover, intrinsic-anchor strengthening,
forced-empty theorem, and core123 exclusion have accepted independent
reviews. Older empty-signature-specific whole-core closures remain an
explicit inherited review boundary for the cumulative 25-core starting
count. The 19 maximal-attachment branch exclusions imported here received an
accepted independent review during the final publication refresh. It
reconstructed all 25 formulas and regenerated the exact nineteen proofs
with a distinct Kissat binary before full sequential DRAT replay. Its
60-second safety cap does not certify the original 20-second runtime.
The new full-extension propagation and seven new proofs await review.

The degree window imports R(4,5)=25 through the parent; its original
computation is not repeated. Ordinary unformalized reductions, exact
source, interpreter/compiler/hardware, SHA-256 identity and the full DRAT
checker remain trusted. Internal reconstruction and second replay do not
constitute independent peer review or proof-assistant formalization.
Large formulas, proofs, logs and binaries remain external. Compact hashes
and result reports alone are not refutations. This bounded pass does not
claim a target graph, a Ramsey lower-bound improvement, or exclusion of
the whole eleven-cycle action.
