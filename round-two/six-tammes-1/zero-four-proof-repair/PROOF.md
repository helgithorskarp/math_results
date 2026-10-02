# Repairing a zero-four source-proof step with three faces

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.
This is an author correction and a smaller explicit reduction for a
published source proof. Independent mathematical review and formalization
remain pending. The common-positive-contact fact used below is established
prior work; no priority claim is made for that fact or for the old row
exclusion.

## 1. The three-face certificate

Let a finite set of distinct unit points in R^3 have contact cosine
**0<c<1**. A contact means inner product exactly c. Suppose F,B,U,X,S are
five distinct actual points, and G,V are actual points for which the
following simple contact faces occur, in the displayed boundary order:

```text
T(F,G,S), Q(U,F,X,B), Q(V,G,S,B).
```

This is impossible. Here G,V need not be fresh points or distinct from
all five named points beyond what simplicity requires. The proof uses
only F,B and the three distinct contacts U,X,S. In the two source
applications all seven displayed names are distinct originals.

In Q(U,F,X,B), the opposite points F,B contact both U and X. The triangle
supplies the contact FS, and Q(V,G,S,B) supplies BS. Thus F,B have three
**distinct** common contacts U,X,S.

Two distinct unit points p,q have at most two common positive-c contacts.
If q=-p, the two equations p dot w=c and q dot w=c contradict c>0. Otherwise
p,q are linearly independent and their two affine contact planes meet in
a line. The equation ||w||^2=1 on a nonconstant line is a quadratic with
positive leading coefficient, so has at most two distinct solutions.
This proves the contradiction. The fact is already stated in the
[published odd-degree reduction](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source d6547391ae745a70087f067568047c8dbba0e099, graph7817, and
[fan reduction](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf, graph7912.

No degree-five quota, angle inequality, beta threshold, N=15 count,
connectedness or completion of the contact map is needed once these
three faces are known. In fact the six witness contacts and five-point
distinctness suffice; faciality is only how the applications supply them.
No additional unknown-face inference is part of this certificate.

The exception c=0 matters: opposite poles can have any number of common
zero contacts on their equator. The checkers verify the five exact unit
vectors (0,0,1),(0,0,-1),(1,0,0),(0,1,0),(-1,0,0). This is a control for
the linear-algebra fact, not a claim that these vectors realize the
three displayed faces. The lemma is applied only for positive c.

## 2. The published source step being repaired

The [two-one-T-four source proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_two_one_triangle_fours_exclusion/PROOF.md),
original source71535b1c836995acfe9b6f6bef3727b97af82c09, excludes
`(r,a,b,f0,f1,f2,O)=(2,2,1,0,2,0,8)` on OPEN1/2<c<3/5 in its stated
complete connected cellular degree3/4/5, simple strictly convex
hemispherical T/Q, nine-Q/eight-T class. F,G are three-T fives; U,V are
zero-T threes; A,D are one-T fours; B is a zero-T four. Eight fours are
ordinary. That row statement is prior art and is not claimed as new here.

Its Section6 C5 has N(U)=ABF, N(V)=ABG and a shared one-T A. Section7 C7
has N(U)=ABF, N(V)=BDG and only B in their common-contact intersection.
The source closes a C7 subcase by reusing the final-B-Q argument of
Section6. That particular face transition does not follow verbatim:
the zero-four cyclic links in these two cases are different.

Here is the exact distinction. In the subcase, B has the four complete
contacts U,V,X,S; the known Q corners pair U with X and V with S. Up to
reversal there are two possible cyclic links:

```text
U V S X    (UV and XS are corners),
U X V S    (UV and XS are opposite).
```

In C5, the one-T A contacting U,V forces Q(U,A,V,B), so UV is a corner
at B and the first link is the appropriate one. In C7, U,V share only B.
If they were adjacent in B's link, their Q would supply another common
contact, contradicting the complete triples. Thus only the second link
is possible. In particular there is no XS corner at B in C7. An assumed
final face Q(B,X,K,S) would use an XS corner; it is not a valid transfer
of the C5 link argument.

These are comparisons of necessary cyclic incidences, not counterexamples
realized by a spherical packing. The whole zero-side prefix is impossible
for the independent metric reason of Section1, so no packing is asserted.

## 3. Replacement paragraph for C7 and shorter C5 closure

In the Section7 C7 subcase where G's endpoint S is on the zero-B side,
the actual faces already include

```text
T(F,G,S), Q(U,F,X,B), Q(V,G,S,B).
```

U differs from S because U has no triangle while S occurs in the known T;
X,S are distinct contacts in F's actual fan. F,B are distinct roles.
Section1 gives the three-common-contact contradiction immediately. This
replaces the incorrect transfer of a final XS face. The other subcase,
where S is on the one-D side, retains its separate source proof; no
blanket verdict on that remaining proof is asserted here.

The same three faces appear in Section6 C5 once S is identified as G's
zero-B endpoint. They already close that branch. Its later ordinary quotas,
B's fourth Q and the two possible final opposites F/G are unnecessary for
this closure. The new certificate therefore reduces both applications
to three named faces and the same six original contact edges.

The old [check.py](https://github.com/helgithorskarp/math_results/blob/main/tammes15_two_one_triangle_fours_exclusion/check.py)
already contains a global common-neighbor cap in its `possible` predicate.
That predicate can reject this prefix. Successful tests of more strongly
assumed face frames do not themselves justify that the additional faces
were forced. The correction explicitly supplies the missing written
bridge and exposes the smaller valid prefix. It introduces no new general
sphere contact theorem.

## 4. Small exact checks and their limits

[certificate.json](certificate.json) gives the two actual source
applications, three faces, original-role order and witness F,B with U,X,S.
[check.py](check.py) regenerates contacts using sets; [audit.py](audit.py)
imports no primary code and reconstructs them with integer edge/neighborhood
masks. The audit enumerates four-vertex links as degree-two edge sets,
whereas the checker enumerates anchored cyclic orders. Both retain every
entry of the two relevant links, rather than comparing only counts.

Both programs compare all **384** boundary-preserving presentations of the
three faces, from6 triangle and8 orientations for each Q. All full records
agree, including the contact edges and three distinct witnesses. Their
canonical record SHA256 is
`9ce793fedd3fd98f312007bf1460b85179ded597a10d20bf5874cfacaa0f027a`.
This small orientation check validates the encoding; it is not an
exhaustive packing/contact-map enumeration or the reason the geometric
lemma is true. The handwritten affine-plane argument supplies that proof.

Deleting any one of the three faces removes the overfull common pair
from the known graph. Deleting each of the six witness edges leaves only
two common contacts. Collapsing S=U or S=X also leaves two; a repeated
name is never counted as three originals. These are nonempty necessary
incidence controls, not spherical packings. The exact zero-cosine control
records the excluded degenerate plane case. All checks use Python's
arbitrary-precision integers and standard library, with no floating-point
metric, solver, network or prior executable as a runtime proof input.

The complete identical stdout is2850 bytes SHA256
`eeef59ee48cbc78d9cc9f7c46d2316d6bf2ec459d2e5a1193e7bb484f08e8e5e`;
see [EXPECTED.json](EXPECTED.json). [VALIDATION.json](VALIDATION.json)
records all four normal/-O runs and conservative child-memory bounds.
Written geometry, source-case interpretation and code encoding remain
ordinary unformalized trust boundaries. Same-author audit does not count
as independent researcher review.

## 5. Catalogue and global status

The older source-only b=1 row statements are prior art. Their main
intervals are wider than the inherited classifier, whose stronger32-profile
cover needs OPEN1/2<c<beta and its small-corner H argument. This correction
certifies precisely the C7 zero-side branch and shortens C5; it does not
newly certify every old branch, r=0 exclusion or catalogue dependency.

The [recent F3T/D2T row proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-two-triangle-fives-row/PROOF.md),
source e97fcedd410c9b063872f89b2c52aff900334487, graph9301, motivated the
source-only dependency audit. Its optional empty source-only deletion table
retains all old classifier hypotheses and imports their derivations.
A complete-nine-Q theorem remains pending that audit, and an unrestricted
optimizer occurrence/larger-face bridge remains absent. No numerical
Tammes-15 bound, global optimum, or new row-priority claim follows here.

The current [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[coordinate table](https://spherical-codes.org/data/3/15) retain the
unstarred fifteen-point incumbent cosine0.59260590292507377809642492233276.
The primary [Musin--Tarasov paper](https://arxiv.org/abs/1410.2536) solves
N14; it is context, not a theorem resolving N15. Primary literature and
source-reader verification remain distinct from this local proof.
