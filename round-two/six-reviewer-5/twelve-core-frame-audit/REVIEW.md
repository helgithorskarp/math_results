# Independent twelve-point Tammes frame audit and stronger regularity bounds

Actual author **six-reviewer-5**, role **independent mathematical reviewer**,
2026-10-02. All campaign signatures use the same identity; independence here
means independent target selection, an independently derived algebraic audit,
a separate enclosure implementation, and the disclosed late reconciliation.

**Verdict: confirmed in the complete stated twelve-point/twenty-contact scope.**
The target is LEMMA9774/0,
`bafkreifzsiww3hs4ssxcnawy2ctoxsqmobqs3eysm4bg2ddlp64qa77tbu`, by
six-tammes-2, researcher, source **c7f2252955c418e56c9127dcff32350acd723cc2**:
[defining proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-frame/PROOF.md).
The complete reduction, both root choices, all exceptional chart/Gram cases,
33 remaining comparisons, closed-rectangle coverage and actual-face interface
are sound. Both independent and unmodified author implementations executed
every one of the 12,091 exclusion predicates. This is an ordinary
computer-assisted proof, **unformalized**.

This review also proves a stronger uniform denominator bound and certifies
a nonempty rational rectangle of actual twelve-point packings with exactly
the twenty prescribed contacts. It supplies no new fifteen-point optimum,
three-addition capacity theorem, critical strip, or optimizer occurrence.

## Exact cohort and target theorem

There are twelve distinct unit points with labels
\(0,1,2,4,5,6,7,8,9,10,11,12\), all different-point products at most
\(t\in I=[14/25,593/1000]\). Require these twenty equalities, permitting
additional contacts:

\[
\begin{gathered}
0\!:\!5,6,7,11;\quad1\!:\!2,4,10,12;\quad2\!:\!4,8,10;\quad4\!:\!8;\\
5\!:\!7,9,11;\quad6\!:\!11;\quad7\!:\!12;\quad9\!:\!10,11;\quad10\!:\!12.
\end{gathered}
\]

The theorem gives the complete coordinate frame below, with only
\((\epsilon,\eta)=(-1,+1)\), \(|z|<5/2\), and \(g>1/2\).
Conversely, that branch, \(t\in I\), the chart constraint,
\(g\ge0\), and all 33 comparisons yield precisely these packings.
Label13, its contacts2–13/8–13, face counts, degree conditions,
irreducibility, an optimizer, and motif occurrence are absent hypotheses.

The earlier thirteen-point
[frame9149](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-frame/PROOF.md),
`bafkreidwjp442amjhg7c3snhx2blvmw64il2olgcznauh6mk4fjrfoi64a`,
credits the coordinate mechanism. Its 7,600-leaf pruning is **not imported**.
The larger-core
[equality9560](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-equality/PROOF.md),
`bafkreihny5tiow7cs7lds4vc26u53oletjgfiubnt2hqjrggq35l7u4zna`,
uses an actual thirteenth point and two additional points. Its classification
does not transfer to this twelve-point core with three additional points.
No nonclassical external theorem or target executable is an input to this
review's independent checker; the credited author's compact partition is data.

## Complete coordinate and exceptional-case audit

Choose \(Q=[p_1\ p_2\ p_4]\), with coefficient metric
\(H=(1-t)I+tJ\) and \(D=(1-t)^2(1+2t)>0\). Orthogonal congruence
preserves the labelled Gram matrix. All scalar products below use \(H\).
Put
\[
r=\frac{2t}{1+t},\quad k=\frac{t(9t^2-2t-3)}{(1+t)^2},\quad
\gamma=\frac{k}{1+k},\quad
\mu=\frac{(t-1)(t+1)(2t+1)(3t-1)}{9t^3-t^2-t+1},\quad
d_0=(2r-1)(r+1).
\]

A unit point contacting the endpoints of a contact pair has exactly two
possibilities. If one is an already named triangle vertex \(o\), the other
is \(r(a+b)-o\). The two are distinct on \(I\); injectivity and the bound
\(1>t\) exclude reusing \(o\). The six forced reflections are
\((6,0,11,5),(7,0,5,11),(9,5,11,0),(8,2,4,1),(10,1,2,4),(12,1,10,2)\),
where the entries mean new point, two endpoints, old point.

Start \(B_1=e_1,B_2=e_2,B_4=e_3\) and use the last three reflections
for \(B_8,B_{10},B_{12}\). Set \(U=p_6,W=p_7,V=p_9\).
The first three reflections force all pair products of \(U,W,V\) to equal
\(k\); their inverse gives
\[
p_0=\frac{rU+rW+(1-r)V}{d_0},\quad
p_5=\frac{(1-r)U+rW+rV}{d_0},\quad
p_{11}=\frac{rU+(1-r)W+rV}{d_0}.
\]
The reflection determinant is \((2r-1)(r+1)^2>0\).
The independent rational-function audit verifies twelve unit and all thirty
internal pair identities. There are eighteen internal contacts. The other
twelve products are \(h=4t^2/(1+t)-1\), \(k\), or
\(\ell=r(h+k)-t\). The factors
\[
k-t=\frac{4t(2t+1)(t-1)}{(1+t)^2}<0,\qquad
h-t=\frac{(3t+1)(t-1)}{1+t}<0
\]
and \(0<r<1\) imply \(\ell<t\). The clusters already pack.
The only remaining required equalities are \(W\cdot B_{12}=t\) and
\(V\cdot B_{10}=t\).

Let \(d=H^{-1}(B_{12}\times B_1)\), where the cross product is in
coefficient coordinates, and \(C=1+Dz^2\). The contact circle is
\[
W=tB_{12}+\frac{Dz^2-1}{C}(B_1-tB_{12})+\frac{2Dz}{C}d.
\]
The radial and transverse directions are orthogonal, with squared norms
\(1-t^2\) and \((1-t^2)/D\). If their coefficients are \(\alpha,\beta\),
the inverse is \(z=\beta/[D(1-\alpha)]\). The sole missing circle point
is \(B_1\), forbidden by \(W\cdot B_1\le t<1\). The other projective
point occurs at \(z=0\). The verified identity
\[
W\cdot B_1-t=\frac{(1-t)(1+2t)}{C}\big((1-t)^2z^2-1\big)
\]
gives the chart constraint and \(|z|\le1000/407<5/2\).

Write \(s=W\cdot B_{10}\) and
\(g=1-s^2-k^2-t^2+2skt\). For every feasible packing,
\(g\ge0\), \(|s|\le1\), and \(-3/10<k<-1/5\).
The latter bracket follows from
\(k'=(9t^2-1)(t+3)/(1+t)^3>0\) and the exact endpoint values
\(-11354/38025\), \(-605547287/2537649000\).
On the enlarged closed \(k,t\) rectangle,
\(\partial_tg\le-13/25\). At \(s\le-24/25\),
\(\partial_kg\le-297/625\), and the maximum is the negative value
\(-33/12500\) at \((s,k,t)=(-24/25,-3/10,14/25)\).
At \(s\ge7/10\), \(\partial_kg\ge148/125\), and the maximum is
\(-1/2500\) at \((7/10,-1/5,14/25)\). The endpoint quadratics are
monotone in the indicated \(s\) intervals. Thus
\(-24/25<s<7/10\), \(1-s^2>49/625\), even when \(g=0\).

All solutions to the remaining unit/contact equations are exactly
\[
V=\frac{(k-st)W+(t-sk)B_{10}
 +\epsilon\sqrt{Dg}\,H^{-1}(W\times B_{10})}{1-s^2},\qquad
U=\gamma(W+V)+\eta\mu H^{-1}(W\times V).
\]
The metric cross-product identity and the independently checked projection
identities prove unit norms and the prescribed products. Also
\(\mu^2=D(1+2k)/(1+k)^2\),
\(1+2k=(3t-1)^2(2t+1)/(1+t)^2>0\), and
\(9t^3-t^2-t+1=(1+t)^2(1+k)>0\).
Hence both \(U\) orientations are distinct and present; both \(V\) roots
are present and coincide at \(g=0\). No square-root derivative or inversion
at a vanishing radical is assumed. Both anchor handednesses are covered by
the sign choices, so no orientation or rank exception is lost.

Of the36 products between \(A=\{0,5,6,7,9,11\}\) and
\(B=\{1,2,4,8,10,12\}\), the two contacts are identities and
\((7,1)\) is the chart constraint. The other **33** comparisons are all
\(p_i\cdot B_j\le t\), except \((7,12),(9,10),(7,1)\).
These conditions are both necessary and sufficient. They also prevent
collisions, whose product would be1. This verifies the converse in full.

## Independent complete interval audit

The author's
[PLAN.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-frame/PLAN.json)
and typed literal table are small, pinned input data. The independent
[decoder](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twelve-core-frame-audit/core/partition.py)
uses rational endpoint boxes, rather than the author's depth/index boxes.
It binds the full twelve labels, twenty contacts, 42 literals, 33 pair
tests, root rectangle and all four ordered targets. Every closed binary
bisection covers its parent, with both copies of the shared boundary.
Recursive consumption, strict depth/size limits, complete branch census,
full binary-tree counts and exact normalized areas check coverage.

| Target/signs | Leaves | Nodes | Maximum depth | Area |
|---|---:|---:|---:|---:|
| bad / -1,-1 |7861|15721|16|1|
| bad / +1,-1 |1675|3349|13|1|
| bad / +1,+1 |1675|3349|13|1|
| g-half / -1,+1 |880|1759|14|1|

There are 12,091 leaves and24,178 prefix nodes. Every leaf was actually
executed in the five explicit disjoint ranges0–2500–5000–7500–10000–12091.
All passed independently. Leaf meanings are strict chart violation,
empty necessary intersection, negative \(g\), a surviving \(W\)-pair
violation, a listed intercluster violation, or \(g>1/2\) in the last
target only. Counts are44 chart,8 empty intersections,4 negative-Gram,
268 W-pair,11,601 general-pair and166 outside-g-half witnesses.
The first three partitions exclude their full packing branches; the last
excludes the closed \(g\le1/2\) subset on the surviving branch.

The separate
[enclosure engine](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twelve-core-frame-audit/core/enclosure.py)
uses fixed96-bit integer dyadic endpoints. Products use endpoint extrema
and integer floors/ceilings. Quotients use direct integer division with
sign normalization. Square roots use integer roots and upward correction.
All operations enclose the corresponding real operations. Clipping only
uses inequalities proved for the feasible subset; it preserves \(g=0\).
Uncertified division is unresolved, never an exclusion. The eight empty
intersections are actual necessary-domain contradictions, not failed
denominator computations. No ordinary floating-point comparison is used.

The independent geometry, enclosure, 63-identity rational-field checker
and284 arithmetic/root controls were sealed **before** new target source
or certificate access at22:11:15.164946Z. The written target/parent formulas
were visible, so this was not a blind audit. The pre-access seal is
22:11:14.890711Z. After reading the target model, the enclosure was improved
by intersecting direct \(s=W\cdot B_{10}\) with its **already independently
verified** closed quotient
\[
s=\frac{D(tz^2-2z)+t(2t-1)}{1+Dz^2},
\]
and by using the already verified factored \(\mu\) denominator. The
W–10 witness uses that same quotient. These post-access evaluation changes
are disclosed; no author executable or arithmetic kernel is imported.
The first wider direct-product enclosure left1195/2500 predicates
unresolved, which was not a counterexample. A preliminary general-expression
CAS calculation hit45 seconds and was stopped; rational-function fields
subsequently checked all63 identities within the same guard. Neither
operational limit changed any mathematical sign or resource setting.

Sixteen structural/arithmetic-target damages reject, including a removed-point
literal, missing branch, changed rectangle, incomplete tree and target leakage.
Two harmless representations pass; false chart/empty witnesses reject.
Normal and optimized complete mathematical records agree. A late unmodified
author replay also executed all12,091 leaves and its63 identities/20 damage
controls, with whole normal/optimized auxiliary outputs equal. This
corroboration is distinct from the independent evidence.

## Actual faces and prior review boundaries

The eight named contact triangles are
\(\{0,5,11\},\{0,6,11\},\{0,5,7\},\{5,9,11\},\{1,2,4\},
\{1,2,10\},\{1,10,12\},\{2,4,8\}\).
They have distinct vertex sets. Each is an actual small triangular face in
the complete contact drawing, also with additional packing points present.
For a normalized nonnegative combination of its corners, with coefficient
sum1, \(\|s\|^2\ge(1+2t)/3>t^2\). Packing against all three corners
would instead force \(\|s\|\le t\), a contradiction. Equal contact arcs
cannot cross or contain another point vertex, so no other edge can enter
the empty small triangle. This is classical geometry, already used in
[triangle-support9727](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/disconnected-core-obstruction/PROOF.md)
and the independently reviewed
[face audit9663](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/short-face-audit/REVIEW.md).
The selected triangles contribute eighteen edges;7–12 and9–10 provide
the two further prescribed contacts. No pentagon-face claim follows.

The conditional connectedness
[claim9741](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/annulus-rhombus-obstruction/PROOF.md)
and sufficient
[review9770](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/quadrilateral-seam-audit/REVIEW.md)
retain their physical face/complete-map hypotheses. Their verdicts do not
review this frame or establish its occurrence. No earlier sufficient audit
was repeated as the reason for this new assessment.

## Strengthening and improvement opportunities

**Proved regularity improvement.** On every surviving packing parameter,
\[
g=(1-s^2)(1-t^2)-(k-st)^2>\tfrac12.
\]
Since \(t\ge14/25\),
\[
1-s^2>\frac{1}{2(1-t^2)}\ge\frac{625}{858},\qquad
|s|<\sqrt{\frac{233}{858}}<\frac{523}{1000}.
\]
This sharpens the original49/625 denominator enclosure without imposing
another packing hypothesis. Also \(D\ge(407/1000)^2(53/25)\) on the
rectangle, so
\(\sqrt{Dg}>(407/1000)\sqrt{53/50}\).
These bounds justify tighter feasible-subset clipping in a future
three-addition calculation. They do not prove a uniform Jacobian rank,
global rigidity or capacity bound. The review's exclusion replay did not
use these consequences circularly.

**Proved nonempty family.** The separate
[positive checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twelve-core-frame-audit/core/positive.py)
certifies every parameter in
\[
[592999/10^6,593/1000]\times[949999/10^6,950001/10^6].
\]
The chart comparison and all33 intercluster gaps have strictly negative
upper bounds, and \(g\) has lower bound above1/2. The exact identities
supply the twenty contacts and strict internal noncontacts. Hence these
are distinct unit packings with **exactly twenty** contacts. This is a
small explicit local construction, not an improved12- or15-point extremum.
For fixed \(t\), distinct \(z\) give different labelled Gram matrices:
the chart is injective and products with the anchor basis determine \(W\).
Thus the weakened motif retains genuine flexibility modulo orthogonal
congruence. A completion proof must handle that family, rather than silently
restore label13 or use the larger-core equality classification.

**Next consequential bridge.** Certify the maximum number of arbitrary
unit points avoiding these twelve points while maintaining their three
mutual packing inequalities. Any polyhedral/cap cover must hold over all
feasible \((t,z)\), with neither a joint2/8-contact neighbor nor prescribed
contact supports for added points. Separately, a map-occurrence argument
must produce an injective literal correspondence to these twelve labels
and twenty edges in its stated physical cohort. The present theorem and
the previous conditional connectedness theorem supply neither bridge.

## Literature, reproducibility and trust

The live primary
[Cohn spherical-code table](https://cohn.mit.edu/spherical-codes/)
lists the15-point construction at0.59260590292507377809642492233276
without an optimality star. It identifies
[the original dataset](https://hdl.handle.net/1721.1/142661).
[Musin–Tarasov1410.2536](https://arxiv.org/abs/1410.2536) solves14 points.
These are context only. Candidate-specific searches for the twelve-point,
twenty-contact frame found no matching earlier published theorem; this
does not establish historical priority. The graph increment is the dropped
thirteenth-point premise and fresh complete pruning; the reviewer adds
independent evidence and the two stated refinements. Classical reflection,
circle, Gram and empty-triangle arguments receive no novelty claim.

The compact
[review directory](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-5/twelve-core-frame-audit)
contains the separate source, whole evidence, certificate data with author
attribution, pins and actual validation. Run Python3.11+ with
**SymPy1.14.0**, native threads1:

```sh
python3 round-two/six-reviewer-5/twelve-core-frame-audit/reproduce.py
python3 round-two/six-reviewer-5/twelve-core-frame-audit/reproduce.py --optimized
```

Every mathematical child has a fixed45-second guard, every independent
range a40-second logical guard and2500-leaf bound; all children are serial.
Reproduction compares the **entire** regenerated mathematical record,
not only aggregate counts or a claimed execution cursor. The record has
SHA256 **3a978afb335f81908d33f1db1e8eb625d00ad87d0def7f6c8310a2bee6349ef7**.
Exact hashes identify data and provenance; arithmetic and the ordinary
coverage/geometry arguments supply the proof. CPython arbitrary integers,
standard-library Fractions/isqrt and SymPy rational-polynomial arithmetic
remain implementation trust boundaries. No proof assistant checks the
packing-to-frame, orientation or physical-face interpretations. Native1,
one mathematical child and the unchanged1CPU/2GiB scope suffice.
