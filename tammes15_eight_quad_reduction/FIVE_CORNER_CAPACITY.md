# Ordinary-five corner capacity leaves six Tammes-15 profiles

Author: **six-tammes-1**, role: **researcher**. Date: 2026-09-30.
Status: complete author-audited, unformalized hand proof with exact
identity/incidence checks. Independent mathematical review is pending.

## Statement and scope

Let fifteen distinct unit vectors have minimum geodesic separation d
and put `c=cos(d)`. Assume their **complete** contact graph is connected,
has degrees3..5, and gives a cellular decomposition of S2 into simple
strictly convex triangle and quadrilateral faces, each in an open
hemisphere. Suppose exactly eight faces are quadrilaterals.

**Ordinary-five lemma.** If `1/2<c<3/5` and every degree-five vertex has
four triangle faces and one quadrilateral, then there are **at most two
degree-three vertices**. More precisely, with `p` zero-triangle degree
fours and `s` ordinary degree fours having separated quadrilaterals,

\[
\boxed{2n_5\le n_4-p+s.} \tag{1}
\]

Here an ordinary degree four has two triangle faces and two Q faces.
A one-triangle four has one T and three Qs. These and the zero-triangle
fours exhaust degree-four types in this interval.

**Six-profile corollary.** Under the same graph hypotheses and
`1/2<c<beta`, where beta is the unique root in `(119/200,3/5)` of

\[
1+4c+2c^2-4c^3-11c^4-24c^5,
\]

the necessary cover decreases from seven to **six degree/deficit
profiles**, with eleven global colored auxiliary H types unchanged.
Distribution `(d41,d42,d51)=(4,0,0)` and distribution `(2,1,0)` each
retain `n3=0,1,2`. This includes `1/2<c<=119/200`.

The ordinary-five hypothesis in the first lemma is explicit. Its
application in the corollary uses [FIVE_BOUNDARY.md](FIVE_BOUNDARY.md),
source `14b0fcbf082e2e9b5eff01e2ea2facd5405b9b07`, which establishes
that hypothesis in the beta interval. The corollary also uses the
whole double-zero exclusion in [TWO_ZEROS.md](TWO_ZEROS.md), source
`facf5229d14e35bd0cd6674dfdaff7f71d9f95e5`, and the auxiliary conventions
in [PROOF.md](PROOF.md), source
`2f9b8b2c7125c339a7a350437bc32b8aa40ac7db`.
It refines the seven-profile stage in [TOPOLOGY.md](TOPOLOGY.md), source
`b3995d988480906e6929caf25e465d74c359e734`.
The new proof uses rhombus angles, vertex angle capacity and Q-Q edge
parity. The earlier planar fan-normalization proof remains a separate
unchanged stage.

These are necessary structures, not realized packings or full contact
graphs. The remaining q8 branch, larger faces, global optimizer graph
coverage, global numerical separation bounds and Tammes-15 optimality
remain unresolved. No congruence between distinct arbitrary Qs is
assumed. The Qs incident to ordinary fives have fixed angles because
those vertices have four equilateral triangles.

## 1. Angle facts and an exact comparison

Write

\[
\alpha=\arccos\frac{c}{1+c},\qquad
x=2\pi-4\alpha,\qquad
\rho(t)=2\arctan\frac{1}{c\tan(t/2)},\qquad y=\rho(x).
\]

The equilateral T angle is alpha. Opposite angles of a Q are equal,
adjacent ones are t,rho(t), and every Q corner satisfies
`alpha<t<2alpha`. These are the established spherical-rhombus/packing
facts in [PROOF.md](PROOF.md) and [FIVE_BOUNDARY.md](FIVE_BOUNDARY.md).
The earlier [independent rhombus review](../tammes_15_triangle_quad_exclusion_review1/README.md)
checks those underlying facts; it does not review the later q8 claims.

For the full interval `1/2<c<3/5`, put `h=c/(1+c)`. Then
`1/3<h<3/8<1/2`, so `pi/3<alpha<2pi/5`. For the upper bound, use
`cos(2pi/5)=(sqrt(5)-1)/4<1/3`; `sqrt(5)<7/3` follows from
`5<49/9`. It follows that `alpha<x<pi` and `pi-alpha>x`.
All half-angle tangents below are therefore on their positive branches.

We claim the stronger exact comparison

\[
\boxed{y>\pi-\alpha.} \tag{2}
\]

Set `A=1+2c-c^2>0` and `u=tan(x/2)>0`. Since `x/2=pi-2alpha`,
the double-angle identity gives

\[
u^2=\frac{4c^2(1+2c)}{A^2},\qquad
\cos y=\frac{c^2u^2-1}{c^2u^2+1}.
\]

With positive denominators, `cos y<-c/(1+c)` is equivalent to

\[
c^2u^2<\frac{1}{1+2c}
\quad\Longleftrightarrow\quad
A^2>4c^4(1+2c)^2.
\]

Factor the difference:

\[
\begin{aligned}
A^2-4c^4(1+2c)^2
&=[A-2c^2(1+2c)][A+2c^2(1+2c)],\\
A-2c^2(1+2c)&=(1+c)(1+c-4c^2),\\
1+c-4c^2&=\frac4{25}+\left(\frac35-c\right)
                       \left(4c+\frac75\right)>0.
\end{aligned}
\]

The second factor `A+2c^2(1+2c)` is positive as well. Thus the cosine
inequality holds. Both y and pi-alpha lie in `(0,pi)`, where cosine
is strictly decreasing, proving (2). In particular `y>x`.
Also `y<2alpha`, because x>alpha, rho is strictly decreasing and
`rho(alpha)=2alpha`. No numerical angle evaluation is used.

## 2. Local vertex and five-corner rules

A degree three cannot have a T: even one T and two Qs have total angle
strictly below5alpha<2pi, and more T faces reduce the upper bound.
Thus all its three sectors are Qs. A degree four cannot have three or
four Ts, for the same bound, so it has zero, one or two Ts.

At a degree four, **at most one incident face angle can equal y**.
If two were y, the other two would be at least alpha, giving total
angle at least `2y+2alpha>2pi` by (2), a contradiction. This includes
one-triangle and ordinary fours and does not depend on their rotation.

Every ordinary five has one Q corner with angle x. Each of its adjacent
Q corners has angle y. Another ordinary five cannot be adjacent in
that Q, because its sole Q angle is x<y. A zero-triangle vertex cannot
be an adjacent corner either: each Q edge at a five has a T on its
other side, which would put a T at the zero-triangle endpoint. Hence
both adjacent Q corners are nonzero-triangle **degree fours**. Call
these vertices W fours; their total number is `n4-p`.

Consequently a Q contains zero, one, or two ordinary fives; two must
be opposite. If it contains two, its other two corners are W fours
with angle y. At each such four, both Q boundary edges meet a five
and have T on the other side. The Q sector is therefore flanked by
two distinct T sectors. A degree four then has exactly two Ts and its
two Q sectors are separated. Thus the two four corners belong to the
s separated ordinary fours. Each can supply this y corner only once.
In particular, different two-five Qs use disjoint pairs of these fours.

These rules involve whole face corners. Two ordinary fives opposite
in one Q supply one y corner occurrence at each neighboring four,
even though each such occurrence is adjacent to both fives.

## 3. Five-corner capacity

Let f1,f2 count Q faces with one or two ordinary-five corners. Each
degree five has exactly one Q occurrence, so

\[
n_5=f_1+2f_2.
\]

There are exactly `2(f1+f2)` y corner occurrences adjacent to those
fives, all at W fours. The one-y-per-four rule makes them occurrences
at distinct W fours. The preceding two-five rule gives

\[
2(f_1+f_2)\le n_4-p,\qquad 2f_2\le s.
\]

Therefore

\[
2n_5=2(f_1+f_2)+2f_2\le n_4-p+s,
\]

which proves (1). The exact checker independently enumerates the
four-corner role patterns and verifies these occurrence counts,
including the distinction between two five incidences and one y corner.

## 4. Degree counts and Q-Q parity force n3<=2

Write `r=n3`. Euler and face-side counting with fifteen vertices and
eight Qs give `E=31,T=10`, so the degree sum is62. Hence

\[
n_5=r+2,\qquad n_4=13-2r.
\]

Let a count one-triangle fours, p zero-triangle fours, and m ordinary
fours. All degree fives are ordinary by hypothesis and all degree
threes have no T. The thirty T corner occurrences give

\[
a+2p=4,\qquad a=4-2p,\qquad p\in\{0,1,2\},\qquad m=9-2r+p.
\]

Capacity (1) becomes `s>=4r+p-9`. But `s<=m=9-2r+p`, so `r<=3`.
At r=3 both bounds coincide and force `s=3+p`.

Now count the ends of Q-Q edges at all vertices. A zero-triangle
degree three contributes3, a zero-triangle four4, a one-T four2,
an ordinary four with adjacent Qs1, one with separated Qs0, and an
ordinary five0. Thus

\[
2E_{QQ}=3r+4p+2a+(m-s)=17+r+p-s.
\]

The right side is even, so `r+p+s` must be odd. At the forced r=3,
s=3+p it equals6+2p, which is even. This contradiction proves

\[
\boxed{n_3\le2.}
\]

The argument is uniform in all three p values and needs no enumeration
of the zero-triangle graph or its embedding types. In the beta interval
the earlier double-zero exclusion removes p=2. The remaining p=0,1
each have r=0,1,2, giving six degree/deficit profiles. The eleven earlier
global colored H codes remain a necessary cover; realization of any
code is a separate matter. The only newly removed profile from the
seven-profile stage is `(d41,d42,d51,n3)=(4,0,0,3)`, degrees(3,7,5).

## 5. Further incidence restrictions

**No Q at a degree three contains an ordinary five.** Each Q corner
at a degree three is strictly greater than x: its other two Q angles
are strictly below2alpha and all three sum to2pi. It cannot be adjacent
to a five by the zero-triangle edge rule. It cannot be opposite to a
five because opposite angles would force it to equal x.

**An ordinary four is incident to at most one Q containing a five.**
Its two Q angles sum to `A0=2pi-2alpha`. A Q containing a five has
angle x or y at that four. The three possible two-face sums satisfy

\[
2x<A_0\quad(\alpha>\pi/3),\qquad
x+y<A_0\quad(y<2\alpha),\qquad
2y>A_0\quad(y>\pi-\alpha).
\]

None equals A0. These restrictions may help apply exact forbidden
contact motifs to the remaining six profiles; they do not establish
their occurrence. For the mixed r=2,s=0 case, (1) is tight: eight W
fours supply eight distinct y corners for four single-five Qs. This is
a precise next equality frontier, not an additional exclusion here.

## 6. Reproduction and trust boundary

[check_five_corner_capacity.py](check_five_corner_capacity.py) checks
the exact rational polynomial identities by two coefficient
representations, the positive endpoint margin4/25, the finite cyclic
T/Q and five-corner masks, the degree equations, parity and capacity
for all nonnegative integer degree/face allocations. It independently
counts y corners from masks and compares the six retained profiles
entry by entry with degree-sum generation. It audits the strict linear
angle identities used above; it does not evaluate approximate angles.
All preceding proof/checker/certificate/expected files remain unchanged.

```sh
python3 -B tammes15_eight_quad_reduction/check_five_corner_capacity.py | cmp - tammes15_eight_quad_reduction/EXPECTED_five_corner_capacity.json
python3 -B -O tammes15_eight_quad_reduction/check_five_corner_capacity.py | cmp - tammes15_eight_quad_reduction/EXPECTED_five_corner_capacity.json
python3 -B tammes15_eight_quad_reduction/check_five_corner_capacity.py --selftest
(cd tammes15_eight_quad_reduction && sha256sum -c SHA256SUMS)
```

CPython>=3.11, standard library only, one thread, no solver or downloaded
proof input. The trigonometric branches, cosine-to-angle comparison,
local-to-global corner interpretation and earlier rhombus/packing facts
are unformalized hand proofs. Exact checker output is supporting
bookkeeping, not proof-assistant certification or a complete spherical
embedding enumeration. Independent review is pending. No incomplete
run, timeout, UNKNOWN or resource kill would establish nonexistence.

The [Cohn table](https://cohn.mit.edu/spherical-codes/) still lists the
unstarred N15 cosine0.59260590292507377809642492233276 and quintic
13c^5-c^4+6c^3+2c^2-3c-1. The
[coordinate file](https://spherical-codes.org/data/3/15) remains unchanged,
SHA2561b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805.
[Musin–Tarasov](https://arxiv.org/abs/1410.2536) proves N14. Bounded
current primary searches found no N15 solution or identical corner
capacity restriction; no historical-priority or new-packing-record claim.

The complementary [pentagon-bridge lemma](../tammes15_pentagon_bridge_exclusion/PROOF.md)
by **six-tammes-2**, role **researcher**, source
`f567d7c76db9bb9beb754d12f42d3a4e5aed2868`, graph
`bafkreibspdhbe6gb26b32wupxemx4d3cfqazcrplhwjybu7idl6mkwwvaa`,h7400,
excludes94 prescribed ten-/eleven-label motifs. Its source/committed
body and current checkpoint were read; its checker was not replayed
here and independent review remains pending. It is cited context,
not a premise or a forced-occurrence theorem. The corner restrictions
above supply geometric filters for future justified motif analysis.

The newer [contact-pair closure classification](../tammes15_contact_pair_closure/PROOF.md)
by **six-tammes-2**, role **researcher**, source
`d0e9574dd3699f4ab6fc636f84f43070d49903f7`, graph
`bafkreiglj3fpqibmepcmkilp6ykjz2qknysdepz3zlcrpi3hx7lry3nvmm`, h7430,
proves closure through seven vertices with one eight-vertex exception.
Its corollary removes the old-neighbor requirement from the small bridge
exclusions. The full written proof, committed body and latest checkpoint
were read; its checker was not replayed here and independent review is
pending. It is complementary cited context. A forced occurrence of
disjoint patches on original labels is still needed before using it to
exclude a surviving profile.
