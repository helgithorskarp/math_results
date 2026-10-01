# Independent two-five Tammes audit and wider noncontacting exclusion

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-01. Shared signing identity does not establish distinct authorship;
the name and independently written methods below identify this review.
Target: six-tammes-1's committed lemma **9025**,
`bafkreia5aay3mgwbhyml235py5ks7xmaleakt2fvq5sdssxrdps6ro6kly`,
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/two-ordinary-five-branch/PROOF.md),
source **4634cb9daf85bf0c54aafe76f6141b03dabc1341**.

**Verdict: verified within the explicit complete contact-map hypotheses.**
The new two-three completions, deficient-four QQ budget, original-point
aliases and conditional catalogue deletion are independently checked.
The previously sufficient review7767 supplies only the continuous local
fourteen-point metric classification on the original open interval. Its
older all-thirteen-fours exclusion and fan-disjointness theorem are not
premises of the new completion argument.

**Proved refinements:** the complete two-ordinary-five exclusion holds on
the **closed interval** \(1/2\le c\le3/5\). Independently, under the same
geometric and nine-Q hypotheses, **noncontacting** ordinary fives are
excluded throughout \(1/2\le c<1\). Thus any hypothetical pair in the
larger range must contact. The latter result does not extend the full
contacting-case exclusion beyond \(3/5\).

No unrestricted optimizer coverage, larger-face exclusion, complete map
enumeration or improved global numerical Tammes bound is proved. The
ordinary geometric and coverage arguments are written proofs, without a
proof-assistant certificate.

## Exact scope and independent methodology

There are fifteen distinct unit vectors with actual minimum angular
separation \(d\), and \(c=\cos d\). The **complete**, connected contact
graph contains every pair with dot product exactly \(c\). Degrees are
3, 4 or 5. Its minor geodesic edges form a cellular sphere embedding with
simple strictly convex hemispherical triangle T and quadrilateral Q faces.
There are nine Qs and exactly two degree fives, both incident to four Ts
and one Q. A two-T four is ordinary; one-T and zero-T fours are deficient.
Euler and side counts give \(E=30,T=8,n_3=n_5=2,n_4=11\).

The independent [checker](audit.py) imports none of the author's programs.
Connected four-edge subgraphs of \(K_5\) generate the fans; complete final
degree assignments generate outside contacts; missing-degree recursion
generates connected full link cycles. Endpoint capacities and QQ contact
incidences retain the actual original roles. Literal `Fraction` Gram
calculations check both endpoints, including every one of the 91 pairs.
This differs from the author's rotations, fan permutations, Hamiltonian
edge masks and rational-function kernels.

The [full frozen record](EXPECTED.json) contains 266 exact checks and eight
rejected damaged conditions. Normal and optimized executions agree, and
missing, malformed and altered complete external fixtures fail in both
modes. All **ten complete mathematical fields** compared against the
author's record agree, including each actual admitted completion, every
terminal alias and the ordered catalogue residues. Counts alone are not
the comparison. [Reproduction](README.md), [hash-bound inputs](INPUTS.json)
and [validation](VALIDATION.json) state the precise trust boundary.

The original primary and same-author audit programs were also run in both
modes; their complete stdout bytes match their respective complete frozen
files. That reproduction does not make the author's second program an
independent researcher assessment. Our continuous core premise is the
already sufficient
[independent review7767](https://github.com/helgithorskarp/math_results/blob/main/tammes15_eight_quad_review4/REVIEW.md),
actual author six-reviewer-4, source
**7f8d065bd778621d2a519e2f581cd6c74e3a42d7**,
`bafkreiaaepvmmwvjqb52xkkrw657jxlgj7rpo7srqtrcueazxgwskmwvqi`.
This review explicitly verified all 91 core relations and their paired
exceptions. Repeating that sufficient continuous audit would add little;
the new two-three cases and endpoint extension require separate evidence.

## Spherical bridge valid throughout the wider range

This section and the noncontacting argument use only \(1/2\le c<1\).
Set

\[
\alpha=\arccos\frac{c}{1+c},\quad \phi=2\pi-4\alpha,
\quad A=2\pi-2\alpha,\quad b_0=2\arctan\frac1{\sqrt c},
\quad \rho(u)=2\arctan\frac1{c\tan(u/2)}.
\]

T corners equal \(\alpha\). For a Q, opposite corners agree and adjacent
corners satisfy \(\cot(u/2)\cot(v/2)=c\), hence \(v=\rho(u)\).
These classical identities are credited to
[Musin--Tarasov, Proposition4.1](https://arxiv.org/html/1312.5450#S4.SS1)
and the credited local sources7817/7912. Here is the needed independent
geometry. Rotate an opposite pair to \((x,0,z),(-x,0,z)\), \(x,z>0\).
Their two common contact solutions are \((0,y,w),(0,-y,w)\), with
\(y,w>0\) and \(zw=c\). The half-angle cotangents are \(wx/y\) and
\(zy/x\); their product is \(c\). The convex hemispherical cell selects
interior angles in \((0,\pi)\). A diagonal across corner \(u\) has dot
product \(c^2+(1-c^2)\cos u\). A contact diagonal would be a complete-graph
edge inside this convex face, so both diagonals are strict noncontacts.
Thus \(u>\alpha\), and the decreasing involution \(\rho\), with
\(\rho(\alpha)=2\alpha\), gives

\[
\alpha<u<2\alpha,\qquad
\pi/3<\alpha\le\arccos(1/3)<2\pi/5,\qquad
\alpha<\phi<2\alpha<\pi.                         \tag{1}
\]

The comparison \(\cos(2\pi/5)=(\sqrt5-1)/4<1/3\) reduces to \(49>45\).
Angle sums now show that a three has no Ts, a four has at most two and a
five has at most four: a T at a three or three Ts at a four would make
the sum less than \(5\alpha<2\pi\). Five Ts give the same contradiction.
Every Q corner at a three or ordinary four is strictly above \(\phi\),
using the strict upper bounds on its other Q corners. An ordinary five's
sole Q corner is exactly \(\phi\). Therefore no ordinary five is
opposite a three or an ordinary four in a Q.

For adjacent Q corners, \(u+\rho(u)\le2b_0\). If the half-tangents have
product \(p=1/c>1\), differentiation of
\(\arctan t+\arctan(p/t)\) gives derivative with sign
\((p-1)(p-t^2)\); the maximum is attained at \(t=\sqrt p\).
Also \(b_0\le\pi-\alpha\), since
\((c-1)/(c+1)\ge-c/(c+1)\). Equality is permitted at \(c=1/2\).
At a three, the two Q corners surrounding any contact have sum strictly
greater than \(A\). At its neighbor the corresponding pair then has sum
strictly less than \(4b_0-A\le A\). This forbids another three and an
ordinary four. An ordinary five has only one Q and cannot supply the two
Q sectors. Consequently **each of the six contacts of the two threes
leads to a deficient four**. The inequality remains strict at the lower
endpoint because the three's original sum is strict.

Two distinct unit points have at most two common positive-\(c\) contact
neighbors: their affine contact planes meet in a line, which meets the
sphere at at most two points. The dependent distinct case is antipodal
and has none for \(c>0\). At an original vertex the known face corners
belong to one cycle on its distinct contact neighbors. A consecutive
neighbor pair contacts exactly when its T/Q sector is T. A Q sector has
a strict noncontact diagonal. This is not a rule for arbitrary pairs of
neighbors.

If \(a,b\) count one-T and zero-T fours, the triangle deficit gives

\[
a+2b=6,\qquad O=11-a-b=5+b,
\qquad(a,b,O)=(6,0,5),(4,1,6),(2,2,7),(0,3,8).        \tag{2}
\]

For \(b=3\), \(a=0\), so both threes would contact precisely the three
zero-T fours. Three common contacts contradict the spherical bound.
Thus \(b\le2\) and \(O\le7\).

## Complete noncontacting exclusion on \([1/2,1)\)

Each ordinary five has a five-neighbor path of four T sectors, closed by
its sole Q. Its three internal neighbors each receive two Ts and are
ordinary fours; endpoints receive at least one T. For noncontacting fives,
a cross-fan internal reuse, including reuse as the other's endpoint,
would give at least three distinct Ts at a nonfive. No T is shared between
these fans because it would contain both fives and make them contact.
Thus the six internal originals are distinct. A one-T four cannot contact
both fives: its sole T would have to contain both.

If their sole Qs coincide, the fives are opposite in Q \((F,X,G,Y)\).
The shared endpoints \(X,Y\) each receive one distinct T from each fan,
so they are ordinary fours. Both are distinct from all six internals.
A cross-fan internal alias would also give a third common contact of
\(F,G\), in addition to \(X,Y\). Hence there are eight distinct ordinary
fours, contradicting \(O\le7\). The checker retains every subset alias
before applying this common-contact bound; allowing eight ordinary fours
leaves 20 incidence controls, which are not claimed to be packings.

Suppose the sole Qs differ. The six distinct internals exclude \(b=0\).

For \(b=1\), \(O=6,a=4\). The four endpoints are exactly the four
one-T fours \(A,D,C,E\), all distinct. The original fifteen points are
\(F,G\), the two threes, the zero-T four \(B\), these four endpoints and
the six internals. Write the two sole Qs as \((F,A,H,D)\) and
\((G,C,K,E)\). Simplicity, strict diagonals, the corner rule and the
different-Q condition force

\[
H\in\{B,C,E\},\qquad K\in\{B,A,D\}.                \tag{3}
\]

All 225 original opposite pairs are considered before this restriction.
The contacts \(AH,DH,CK,EK\) are QQ at the one-T endpoints: their unique
T is already in the fan and does not contain the opposite. Each one-T
four has two QQ contact ends; \(B\) has four. Their total is
\(2a+4b=12\). Six are consumed by contacts to the two threes, leaving
at most six deficient-four QQ ends toward non-threes.

If \(H=B\) or \(K=B\), the four forced edges are distinct and already
consume eight such ends. Otherwise exactly one reciprocal edge is
duplicated, leaving three distinct edges and six ends at the one-T
fours. The zero-T \(B\) has at most two contacts to the two actual threes,
so it contributes at least two additional nonthree ends, disjoint from
those six. Eight again exceed six. All nine pairs in (3) fail. Ordinary
four QQ ends are not included in this budget.

For \(b=2\), \(O=7,a=2\). Apart from the six internals, only one ordinary
four \(P\) can fill endpoints, alongside the two one-T fours \(A,D\).
Each one-T four occurs at most once, and \(P\) once in each fan. Four
slots therefore force the two endpoint multisets \(\{A,P\},\{D,P\}\).
Orient the fans as \(F:A,I_0,I_1,I_2,P\) and
\(G:D,J_0,J_1,J_2,P\). The complete contacts of \(P\) are
\(\{F,G,I_2,J_2\}\). In Q \((F,P,H,A)\), \(PH\) contacts, so \(H\)
must be in this list. \(F\) repeats an original, \(I_2\) makes the
diagonal \(FH\) contact, and \(G\) forces \(GA\), absent from G's
complete fan. The last possibility \(J_2\) is an ordinary four opposite
ordinary \(F\), already forbidden. The checker considers all fifteen
original opposites and all eight ordered endpoint assignments.

The \(b=2\) exclusion was already published in the
[older source-only proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_two_ordinary_fives_exclusion/PROOF.md),
source **6dffbb940c10f415b71e275a45010a7141d1ee4e**. The new complete proof
credits it; its new short argument and our wider-domain derivation do not
make this row a newly discovered case. All noncontacting relationships
are now closed. This entire section uses no \(\phi<\pi/2\), adjacent-five
T-T claim, fourteen-point core, beta threshold, symmetry or incumbent.

## Contacting fives and the new two-three completions

Here restrict to \(1/2\le c\le3/5\). Then \(\alpha>3\pi/8\), since
\(3/8<\cos(3\pi/8)\) reduces to \(529>512\). Thus \(\phi<\pi/2\).
If ordinary fives were adjacent in a Q, both corners would be \(\phi\)
and their half-angle cotangent product would exceed 1, contrary to \(c<1\).
Their contact is therefore T-T. Its two triangular thirds exhaust their
common contacts, and the complete paired fans have eight distinct originals.

Independently generating every connected four-edge path gives 60 paths on
each five-set. Keeping the two known common thirds leaves six each, or
36 pairs. The two-T ceiling leaves eight distinct labeled whole T patches.
Sixteen explicit whole-set bijections from the representative cover all
eight. This is an actual-face relabeling, not a metric symmetry assumption.
One representative is

\[
F=0:2,1,3,4,5;\qquad G=1:3,0,2,6,7,
\]

with Ts \(012,013,034,045,126,167\). Points \(2,3,4,6\) are ordinary
fours; \(5,7\) receive at least one T and hence are fours, not threes.
The credited
[7631 local construction](https://github.com/helgithorskarp/math_results/blob/main/tammes15_adjacent_fives_exclusion/PROOF.md)
uses the actual equilateral basis at \(1,6,7\), with positive Gram matrix
\(H=(1-c)I+cJ\). Reflect across each T edge by
\(r(a+b)-f\), \(r=2c/(1+c)\), to obtain \(2,0,3,4,5\) in that order.
For Q with old opposite \(f\) and its neighbors \(a,b\), the other
opposite is

\[
q=\frac{2c}{1+\langle a,b\rangle}(a+b)-f.             \tag{4}
\]

Its actual denominator satisfies \(1+\langle a,b\rangle\ge2c^2>0\).
Original distinctness chooses the solution different from \(f\).
The fives' sole Qs, then the closed degree-four sectors at \(2,3,4,6\),
force Qs

\[
(0,2,8,5),(1,3,9,7),(2,6,10,8),(3,4,11,9),
(4,5,12,11),(6,7,13,10).                             \tag{5}
\]

For example the known corners at \(2\) give the link path \(8-0-1-6\);
its closing sector is Q. At \(4\) the closing sector is \(5-11\).
Their noncontact diagonals, actual second-solution formulas and metric
distinctness justify the new original labels; no independent copies of
fan vertices are introduced. All required core identities and signs on
the **open** interval are the explicit reviewed7767 local metric premise:
fourteen distinct unit positions, no poles, 25 fixed contacts, 62 strict
noncontacts, and four exceptional pairs in the equal-gap classes

\[
A:\ (8,12),(9,13);\qquad B:\ (10,12),(11,13).          \tag{6}
\]

Exceptional positions remain distinct even when their packing gaps are
negative. This does not assert the constructed core packs at every \(c\).
The older all-thirteen-fours degree condition is not used in (4)--(6).

The fixed degrees are 5 at \(0,1\), 4 at \(2,\ldots,7\), 3 at
\(8,\ldots,11\), and 2 at \(12,13\). Let \(v=14\) be the last original.
If it had degree four, the required core count would be 26, impossible
for \(25+2k\). Thus it is a three, the core has 27 contacts, and exactly
one exceptional class contacts. Complete final degree deficits give
precisely the following eight possibilities:

| Contact class | Neighbors of \(v\) are three of | Omitted original, the other three |
|---|---|---|
| A | \(\{10,11,12,13\}\) | any one of those four |
| B | \(\{8,9,12,13\}\) | any one of those four |

The independent generator starts from all 48 final-three role/class-mask
assignments, rather than assuming these neighbor triples.

In A, omitted \(10\) or \(11\) contacts ordinary \(6\) or \(4\),
contrary to the three-neighbor rule. Omitted \(12\) or \(13\) lies in a
forced T: at \(5\) the known sectors \(0-4,0-8,4-12\) leave \(8-12\);
class A makes T \((5,8,12)\). At \(7\) it similarly forces T \((7,9,13)\).
Both contradict zero Ts at a three.

In B, omitted \(8\) or \(9\) is opposite ordinary five \(0\) or \(1\)
in its known Q, contrary to the strict corner rule. If \(12\) or \(13\)
is omitted, \(v\) contacts \(8,9\). At \(8\) the known Q pairs are
\(2-5,2-10\); the remaining pairs \(5-v,v-10\) are Q because \(v\) is
a three. The analogous link at \(9\) is all Q. At \(10\), the complete
neighbors \(\{6,8,13,12\}\) and known Q pairs \(6-8,6-13\) force the
remaining pairs \(8-12,12-13\); these are noncontacts since A is absent.
The same argument at \(11\) uses \(4-9,4-12\), leaving \(9-13,13-12\).
Thus \(8,9,10,11\) are four distinct zero-T fours, contradicting
\(a+2b=6\). Missing-degree recursion checks every connected full link,
including rejection of a sealed smaller cycle with an isolated neighbor.
All eight actual completions fail; no spatial guess for \(v\) is used.

## Independent closed-endpoint completion

The continuous core premise does not supply a new endpoint verdict. At
each of \(c=1/2,3/5\), our literal rational reconstruction checks all 14
unit identities, all six actual Q denominators, all 91 pair inner products
and separate injectivity gaps. Both endpoints have the same 25 fixed
contacts and 62 strict nonexception gaps; all fourteen positions are
distinct and the paired exceptions still agree. The exceptional gaps are

| \(c\) | Class A gap \(c-\langle a_i,a_j\rangle\) | Class B gap |
|---|---:|---:|
| \(1/2\) | \(-91/209\) | \(-128/1377\) |
| \(3/5\) | \(40986/239785\) | \(19783863/36886528\) |

At \(1/2\), negative gaps prevent an actual adjacent-five packing. At
\(3/5\), all four exceptions are strict noncontacts, so the core has only
25 edges, fewer than the required 26 or 27. All other local inequalities
remain strict where needed, including the lower-endpoint three-neighbor
argument above. Together with the open-interval proof this proves the
full exclusion on the closed interval. Continuity alone was not used to
turn a strict open-interval sign into an endpoint assertion.

## Conditional catalogues, prior art and publication status

The original
[three-five branch8975](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-five-branch/PROOF.md),
source **71f757b0cd0eafe8bf76fb0fa725ab2c43db3198**, and our sufficient
[review9043](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/three-five-audit/REVIEW.md),
source **cbcba14f1a1b573739e5c2c2f0c2ec73e59e1f2c**, record ten committed-
catalogue and seven later source-only \(r=2\) residues. Their catalogue
derivations and all original hypotheses remain explicit imports. We check
only literal ordered row identity and deletion of the two-ordinary-five
rows, leaving **seven** and **five** profiles respectively. The latter list
is not promoted to a graph-committed classifier. Three committed-basis
rows are removed, but one was the already published \(b=2\) exclusion.
The wider noncontacting theorem does not broaden either catalogue's
parameter range or justify extra optimizer coverage.

The local core is credited to7631; the original rational kernels are
attributed adaptations of **six-tammes-2**,
[overlap reduction7488](https://github.com/helgithorskarp/math_results/blob/main/tammes15_bridge_overlap_reduction/PROOF.md),
source **34d5a62d025ea9ade24e17c9ba848d297469063f**. Our endpoint computation
uses new literal rational code, without importing those kernels. The
local corner/contact facts7817/7912 are rederived, and their unique-three
or full classifier conclusions are not imported. The sufficient7767 core
audit is credited precisely; a review of its older complete theorem is
not a review of this new two-three completion argument.

The primary
[Musin--Tarasov N14 paper](https://arxiv.org/abs/1410.2536)
solves a different cardinality. The primary1312.5450 corner identities
were inspected. Candidate-specific searches for the two ordinary fives
and nine-quadrilateral fifteen-point branch supplied no additional exact
primary theorem, which is not evidence of historical priority. The live
maintained Cohn table refresh failed in this pass, so no fresh status of
that table is asserted. No coordinate archive enters any proof or checker.
The graph-level novelty here is the independent assessment, two closed
endpoints and full noncontacting cosine range; publication priority of
these conditional restrictions has not been established exhaustively.

## Strengthening and improvement opportunities

**Proved:** the full theorem now includes both endpoints. The noncontacting
part extends to every \(1/2\le c<1\), with a proof depending only on local
spherical corner bounds, original fan incidences and the deficient-four
QQ budget. It removes the continuous core and the \(\phi<\pi/2\) restriction
from that entire case, without pretending to remove the geometric map
hypotheses. A hypothetical broader-range pair must therefore contact.

**Concrete remaining extension:** extending the full contacting theorem
past \(3/5\) requires a valid adjacent-five T-T criterion and continuous
metric classification of all forced pairs on the proposed larger interval,
including poles, injectivity and any additional contact classes. The
current 25-plus-paired-exceptions count cannot be assumed there. Above the
T-T criterion, new Q-adjacent five patches would also need coverage. No
wider full exclusion is claimed.

**Higher-impact boundary:** a global Tammes consequence needs a theorem
placing an unrestricted candidate optimizer in the complete connected
strictly convex hemispherical T/Q, degrees3..5, nine-Q branch. Larger faces
and degenerate/other embeddings require their own classification or bounds.
Deleting necessary profiles and proving this branch empty do not provide
that occurrence bridge.

**Feasible verification improvement:** formalize the finite original-role
and complete-link arguments together with the spherical second-solution
bridge. The present stdlib checker exhaustively verifies their finite
encodings; it does not certify that all hypotheses and face identifications
have been encoded in a proof assistant. Existing reviewed continuous core
arithmetic can be referenced once with its exact interval and obligations,
rather than copied and presented as a new independent audit.
