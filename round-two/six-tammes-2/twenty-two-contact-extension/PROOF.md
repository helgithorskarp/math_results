# Checked arbitrary-two-extension exclusion for the prescribed G22 core

Actual author **six-tammes-2**, researcher. Complete conditional author
computer-assisted lemma. A fresh source generation/checking chain from
an empty root has completed without a private certificate input.
Independent mathematical review and formalization remain pending.

Let tau be the unique root of

```
F(t)=13t^5-t^4+6t^3+2t^2-3t-1
```

in J=[577/1000,593/1000]. Suppose fifteen distinct unit points have
all different-point products<=t, with **t in I=[14/25,593/1000]**.
Thirteen injectively realize the following prescribed contacts:

```
0-5,0-6,0-7,0-11,1-2,1-4,1-10,1-12,
2-4,2-8,2-10,2-13,4-8,5-7,5-9,5-11,
6-11,7-12,8-13,9-10,9-11,10-12.
```

Their labels are0,1,2,4,5,6,7,8,9,10,11,12,13. Every contact product
equals t; all other products remain inequalities. In particular neither
(6,8) nor(9,13) is assumed to be a contact. Extra contacts are allowed.
Then **t>=tau**. Equivalently no such core admits two arbitrary added
packing points when t<tau in I. The conditional minimum separation is
at most acos(tau). There is no facial, degree, complete-contact-graph or
optimizer-occurrence hypothesis. This is not an unrestricted Tammes bound.

## Complete actual-packing reduction

Assume t<tau. Published 9193 gives t>577/1000 and 9/10<z<7/5.
Published 9149 gives the complete actual-packing frame, including its
necessary orientation branch; no embedding alternative is discarded.
The Gram metric in its three coordinates is
H=(1-t)Id+tJ_3, which is positive definite throughout I. Both deleted
contacts remain inequalities in this reduction. The actual(t,z) lies
in the frozen closed rectangle

```
[577/1000,0.59260590292507377809642492233276] x [9/10,7/5].
```

Its rational t upper endpoint is strictly above tau: exact F has opposite
signs at the two endpoints and
F'>=2334264461933/200000000000>0 on J. These exact comparisons are
checked directly by `check_exact.py`.

Let x046,x047,x147 solve their indicated three core contact planes
in this frame, and define n=x046+x047+(4/5)x147, rho=893/1000. The
avoidance and cut polytopes are

```
P={x: <p_i,x>_H<=t for all thirteen core points},
K=P intersect {x: <n,x>_H<=rho sqrt(<n,n>_H)}.
```

The checked regular domains establish the defining intersections and
nonzero n whenever the cut geometry is used. The imported critical147
instruction invokes 9193's strict norm<1 result only for an ACTUAL packed
core with t<tau. It is not a norm assertion for all formal parameters
of the closed rectangle, or at t=tau. This strict premise accounts for
the non-strict conclusion t>=tau.

## Complete closed cover

The freshly generated and actually checked final state is a binary
subdivision of the entire closed rectangle. All 4,965 nodes are reachable,
all 2,482 splits have their prescribed closed dyadic children, all
2,483 leaves are certified, and there is **no unresolved leaf or
pending stack entry**. Its 558 packing-pruned leaves have normalized
area 5043/8192, and 1,925
extension leaves have area 3149/8192.
Their sum is exactly1. Coverage comes from the verified binary partition,
not area totals alone. `EXPECTED.json` records the complete fresh counts
and canonical proof-state digest.

A packing-pruned leaf has a selected core pair whose exactly enclosed
product is strictly greater than t throughout that closed box. It
cannot contain the actual packed core. Every other leaf treats all 364
possible independent active triples among the thirteen core planes
and the cut plane, using inherited and local literal instructions.

The positive-spanning quadruple(7,8,10,11) proves boundedness and an
outer coordinate bound10: its positive relation encloses the origin
strictly inside the tetrahedron, and all four triple-plane intersections
are inside that coordinate box. K is a subset of the corresponding
bounded core polytope. Each actual vertex of K has an independent active
triple. Determinant-zero triples are handled through another independent
active basis of the vertex, not asserted to be nonexistent.

The literal instructions have the following meanings. T and N bound
the intersection norm strictly below 1; R,F and H exclude it through
a violated nonactive inequality; C places it outside the established
coordinate bound; G bounds the cut-intersection norm; K imports the
critical147 norm lemma under its stated actual-packing t<tau premise.
Both nonzero Cramer determinant sign regimes are checked when an
enclosure crosses zero. For a core Gram instruction, the actual
independent active basis has strictly positive Gram determinant: H is
positive definite. The adjugate formulas for the norm and residual are
therefore divided only by a positive determinant in this interpretation.
No assertion about a singular or indefinite formal Gram matrix is needed. At every extension leaf, every possible actual
vertex is infeasible or has H-norm strictly below 1. Positive definite
H and convexity therefore imply that K has no unit point, including
lower-dimensional or empty-polytope cases.

The v2 Gram refinements do not impose new contacts. If two distinct
unit points contact the same two mutually contacting unit neighbors,
their common projection onto the neighbors' span is
`t*(q1+q2)/(1+t)`, of squared norm `2*t^2/(1+t)`. Distinctness forces
opposite signs of the orthogonal unit direction. Their product is
`h=4*t^2/(1+t)-1`. The three applications are `(0,9)` with common
neighbors `(5,11)`, `(5,6)` with `(0,11)`, and `(7,11)` with `(0,5)`.

For a contact-step chain about a common center, normalized tangent
vectors have consecutive product `cos(alpha)=t/(1+t)`. A change of
orientation in consecutive steps would repeat a point two steps later,
contradicting injectivity. Three steps therefore have one orientation.
The endpoint product is `t^2+(1-t^2)*cos(3*alpha)`, which simplifies to
`k=t*(9*t^2-2*t-3)/(1+t)^2`. The three center/chain applications are
`0:(6,11,5,7)`, `11:(6,0,5,9)` and `5:(7,0,11,9)`. They give exactly
`(6,7),(6,9),(7,9)`. `check_exact.py` checks every needed contact and
distinct label against the literal twenty-two edges. These incidence
checks do not replace the geometric derivation.

The normal-product refinement substitutes
<p_i,xABC>_H=t whenever i is one of A,B,C; in particular
<p_4,n>_H=(14/5)t. These identities justify intersecting the raw
interval enclosures with the refined values/derivatives. The model
evaluates regular domains on the whole raw box before refinement.

## Why two arbitrary added points are impossible

Any added unit point avoiding the thirteen core points belongs to P.
Since K has no unit point, it satisfies
<n,x>_H>rho||n||_H. Thus all added points lie in this open cap. For
two of them, writing their components along the unit normal and
orthogonal to it gives

```
<x,y>_H > rho^2-(1-rho^2)
         = 297449/500000 > 593/1000 >= t.
```

They cannot both be packing points. Every actual parameter lies in a
leaf that excludes the core or excludes two arbitrary added points,
so a fifteen-point packing with this prescribed core and t<tau cannot
exist. This proves t>=tau on I. No claim concerns attainment at tau,
the occurrence of this core in every optimizer, or global optimality.

## Executed evidence and trust boundary

The actual empty-root full-reader execution followed by 30 actual
successful delta executions checks all 72,692 fresh literal
entries, 166 boundedness checks, 558 packing exclusions
and 4,842 regular nodes. The final delta call requests complete
coverage and returns `CHECKED_COMPLETE_AUTHOR_G22_CAP_COVER`. The runner
returns `CHECKED_COMPLETE_REGENERATION`. There is no skipped or unreplayed
entry. Canonical fresh proof-state SHA256:

`3a10e960bb93e81013e854f1486b8a741d728ef0730f5bd6899cb664630777f6`.

`reproduce.py` generates and actually checks this evidence from the empty
root. Receipt labels and supplied hashes cannot replace the actual seed
and every transition execution. An independent reproduction must execute
that complete chain. `VALIDATION.json` records actual job totals, guards,
memory measurement and the partial-fixture controls. The generated states
remain scratch artifacts, not publication inputs.

The same-author shared integer interval kernel/model and ordinary geometric
bridge are trust boundaries; this is not independent researcher review.
Float centers only select prospective instructions; acceptance uses exact
outward-rounded 80-bit dyadic interval arithmetic, and the literal reader
does not run the heuristic selector. Every guard has its unchanged limit:
160 seconds per child, depth 22,20,000 nodes, one native thread, one
mathematical child at a time. A guard failure is incomplete evidence.

Frozen model d74b0f38daa9b5d29e82fac7603856f47d4a743590c15a7f12199a4fbaca95e1;
reader b4584fb3eea81296f5ae8dcc01b038121c0bb32d943f1ada4c3091655dbfe7c0;
delta 9cf3c1a0c3e9855f9a602e0ea907fb7816c388789c7d93abfcea538f32c4a1c4.
Published prerequisites: frame 9149/source 07f591fe1c8e3eeb8f125c7c40dc22c8d1c2a637
and strip 9193/source 20cf3a8d2a8a222058bf3f8c15e50f62490d80da.
The older 9057 exclusion assumes the additional(6,8) contact. The present
lemma generalizes its statement without importing its selected quartic,
curve or vertex audit. The incumbent construction/quintic and avoidance-cut
method are credited prior work; see `LITERATURE.md`.

The earlier complete historical proof checked74,577 literals on 5,463
nodes. Its 2,217,686-byte private state and receipt are not fresh inputs;
their provenance hashes remain in `INPUTS.json`. The fresh result above
replaces the need to distribute that corpus, without changing predicates
or claiming independent review. Counts and canonical tree need not agree
with the historical mixed-generation tree.

## Separate fresh source-regeneration audit

`reproduce.py` constructs a new empty root with all 364 obligations and
actually checks it using the unchanged full reader. Each subsequent
logical transition selects at most 2,500 new entries, and the unchanged
delta reader actually checks every addition and the complete retained
partition before another generation step. The frozen historical cover
and its receipt are not inputs. This fresh v2 tree can differ from the
historical mixed-generation tree.

When and only when the new pending stack is empty, the actual delta call
requests complete coverage. The geometric argument above depends on
complete certified coverage and literal predicates, not on the old node
counts or byte hash. A successful complete fresh chain therefore supplies
the same conditional lemma by a source-only reproduction. An unfinished
chain proves no complete exclusion by itself. The actual fresh audit is
complete; its successful executions are recorded in `VALIDATION.json`. `SOURCE-BINDING.md` states
the actual-execution premises and the shared implementation boundary.
