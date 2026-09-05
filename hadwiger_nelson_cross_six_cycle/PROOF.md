# A cross six-cycle forces preservation of the source field

Let `F` be any subfield of the real numbers and put

\[
K=F(\alpha),\qquad \alpha=i\sqrt3.
\]

Thus `K=F+alpha F`, its real subfield is `F`, and complex conjugation
preserves `K`. Write `N(z)=z conjugate(z)` and
`Tr(z)=z+conjugate(z)`. For points of `K`, squared distances lie in `F`.

**Theorem.** Let `P,Q subset K`, and let `g` be any Euclidean isometry.
Suppose there are three points of `P` and three points of `g(Q)`, all six
distinct as plane points, that form an alternating unit six-cycle. Then
`g(K)=K`.

The cycle need not be induced. There are no connectedness, cardinality,
denominator or additional-overlap hypotheses.

For the Hadwiger--Nelson application take
`F=Q(sqrt(33))`, so `K=E=Q(i sqrt(3),i sqrt(11))`.
The prior [field colouring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
then four-colours the entire strict unit-distance graph on `P union g(Q)`.
Four-colourability is asserted here for this particular `E`, not for every
field `K` in the geometric theorem.

In particular, every placement of the fixed alternative `B292/V214` pair
that contains a cross six-cycle is four-colourable. This includes every
disjoint 506-vertex such placement and is a uniform exclusion, not a
finite angle census. No five-chromatic graph is constructed.

## 1. Circle intersections and their quadratic fields

We first record two elementary facts, including their exceptional cases.

If a plane point is at unit distance from three distinct points of `K`,
then it belongs to `K`. Three distinct points on a circle are noncollinear.
Writing coordinates as `x+alpha y` and subtracting the three distance
equations gives a nonsingular linear system over `F` for the two real
coordinates of the centre. Its solution is in `F^2`.

For distinct `a,b in K`, write `d=b-a`, `n=N(d)` and `m=(a+b)/2`.
Whenever the two unit circles intersect, `0<n<=4`, and their intersection
points are

\[
m\pm\frac{\alpha d}{2}\sqrt{D},\qquad
D=\frac{4-n}{3n}\in F,\qquad D\geq0. \tag{1}
\]

At `n=4` this is the single tangent point `m in K`. At `n<4`, either the
positive square root belongs to `F`, and both centres lie in `K`, or a
centre outside `K` generates the quadratic field `K(sqrt(D))`. A real
square root in `K` would belong to `F`, so these alternatives are exact.

**Shared-vertex lemma.** Suppose two different pairs of points of `K`
share exactly one point. Choose a unit-circle intersection centre for
each pair, both outside `K`, and call them `z_1,z_2`. If
`N(z_1-z_2) in F`, then `K(z_1)=K(z_2)`.

To prove this, write (1) as

\[
z_1=m_1+b_1\sqrt{D_1},\qquad
z_2=m_2+b_2\sqrt{D_2},
\]

where `b_1,b_2` are nonzero elements of `K` and `D_1,D_2` are positive.
If the two quadratic fields were different, the four elements
`1,sqrt(D_1),sqrt(D_2),sqrt(D_1 D_2)` would be linearly independent over
`K`. Conjugation fixes the two real square roots. Expanding the norm of
the difference, its three nonconstant coefficients would give

\[
\operatorname{Tr}(\overline{m_1-m_2}b_1)=0,\qquad
\operatorname{Tr}(\overline{m_1-m_2}b_2)=0,\qquad
\operatorname{Tr}(\overline{b_1}b_2)=0. \tag{2}
\]

The last equality says that the two nonzero plane vectors `b_1,b_2` are
perpendicular. The first two make `m_1-m_2` perpendicular to both, so
`m_1=m_2`. But the midpoints of two pairs sharing exactly one point are
different. This contradiction proves the lemma. It also explains why
one must not drop the shared-point or distinct-midpoint condition.

## 2. The six-cycle puts the isometry in one quadratic extension

Conjugating `Q` absorbs orientation reversal, so write `g(z)=u z+h`,
where `|u|=1`. Denote the selected fixed points by `p_0,p_1,p_2` and the
selected moving points by `z_j=g(q_j)`. Label the six-cycle so each `z_j`
has two of the three `p_i` as neighbours, with different omitted points.
The three neighbour pairs are the three pairs of the fixed triple.

Each `z_j` is therefore either in `K` or in a quadratic extension given
by (1). Also

\[
N(z_i-z_j)=N(q_i-q_j)\in F.
\]

Any two moving points outside `K` generate the same quadratic extension
by the shared-vertex lemma. If at least two `z_j` are in `K`, subtraction
and division show `u in K`, and then `h in K`; the theorem already follows.

Otherwise at least two of the three moving points are outside `K`.
They generate a common quadratic extension `L/K`, and the third belongs
to `L` as well, whether or not it is in `K`. Differences of two moving
points show `u in L`, and then `h in L`.

We now rule out both ways the isometry could still fail to preserve `K`.

## 3. A base-field rotation with an external translation has no cycle

Suppose `u in K` but `h not in K`. For every cross unit edge `p,g(q)`,
the point `v=p-u q` belongs to `K` and satisfies `|h-v|=1`.
There are at most two distinct such offsets `v`, by the three-centre
fact in Section 1. At a fixed vertex, edges to distinct opposite vertices
have distinct offsets, since `u!=0`.

Consequently a cross six-cycle would alternate its two offset values
`v_1,v_2`. Summing alternate edge equations around the cycle yields
`3(v_1-v_2)=0`. Characteristic zero gives `v_1=v_2`, a contradiction.
In fact this branch has no finite simple cross cycle of any length.

## 4. A non-base quadratic rotation puts the cycle on two lines

Suppose instead `u not in K`, so `L=K(u)`. Write the translation uniquely
as `h=m-u n`, with `m,n in K`. Thus

\[
g(q)=m+u(q-n).
\]

The point `m=g(n)` is the unique point of `K intersection g(K)`:
another one would express `u` as a quotient of nonzero elements of `K`.
Let the minimal polynomial of `u` be

\[
u^2-Tu+J=0,\qquad T,J\in K.
\]

For a cross edge put `x=p-m`, `y=q-n`, `c=conjugate(x)y` and
`S=N(x)+N(y)-1`. Multiplying its distance equation by `u`, using
`conjugate(u)=1/u`, gives

\[
c u^2-Su+\overline c=0.
\]

Reduction by the minimal polynomial and independence of `1,u` give

\[
cT=S,\qquad \overline c=Jc. \tag{3}
\]

In particular, any two nonzero values of `c` on cross edges have real
ratio, since conjugating their ratio leaves it unchanged. For two edges
sharing a nonzero centred vertex, this makes the opposite centred
vertices real multiples of one another. Along a path containing no
zero centred vertex, all fixed vertices therefore lie on one line
through `m`, and all moving vertices lie on a second line through `m`.

The selected six plane points are distinct. At most one is `m`, so
removing it if present leaves a path of five nonzero vertices; otherwise
the cycle itself is nonzero. Propagation along this path puts all the
cycle's fixed vertices on one line and all its moving vertices on the
other. A removed vertex `m` belongs to both lines. This argument works
also when `T=0` and does not divide by `c` on an edge incident to `m`.

## 5. A unit six-cycle on two lines has a cube-root multiplier

If the two lines coincide, a simple unit cycle is impossible: the largest
coordinate among its finitely many distinct vertices has at most one
unit neighbour among them. Hence the lines are distinct.

Choose unit directions `a,b` along them. Write the two triples as
`m+r_i a` and `m+s_i b`, with distinct real `r_i` and distinct real `s_i`.
Relabel the triples so the six-cycle uses exactly the pairs `i!=j`.
Set `t=Re(conjugate(a)b)`, so `|t|<1`. The six edge equations are

\[
r_i^2+s_j^2-2t r_i s_j=1\qquad(i\ne j).
\]

For each `i`, its two distinct neighbour coordinates `s_j` are the two
roots of `s^2-2t r_i s+r_i^2-1`. With `R=sum r_i`, `S_0=sum s_i`, the
root sums on both sides give

\[
S_0-s_i=2t r_i,\qquad R-r_i=2t s_i. \tag{4}
\]

Summing shows `S_0=tR` and `R=tS_0`, hence `R=S_0=0` because `|t|<1`.
Substitution in (4) gives `(1-4t^2)r_i=0` for all `i`. Not all the
distinct `r_i` vanish, so

\[
t=\pm\tfrac12,\qquad s_i=-2t r_i.
\]

The unit ratio `b/a` has real part `t` and imaginary part `+/-sqrt(3)/2`.
Thus

\[
\lambda=-2t\frac ba\in\left\{
\frac{-1+\alpha}{2},\frac{-1-\alpha}{2}\right\}\subset K,
\qquad m+s_i b=m+\lambda(r_i a). \tag{5}
\]

Since `m` and every fixed cycle point belong to `K`, (5) puts every
moving cycle point in `K`. Two of them again force `u,h in K`, contradicting
the current branch. All non-preserving branches have now been excluded.
This proves the theorem.

## 6. Scope, sharpness controls, and the remaining construction family

The inclusion of `i sqrt(3)` in `K` is substantive. For example, put

\[
P=Q=\{3/7,5/7,-8/7\},\qquad
g(z)=\frac{-1+i\sqrt3}{2}z.
\]

All six points are distinct. For different source labels the squared
distance is `r_i^2+r_i r_j+r_j^2=1`, so the cross graph is a six-cycle.
The source points even lie in `Q`, but this isometry does not preserve
`Q(i)`. It does preserve `Q(i sqrt(3))`, exactly as the theorem requires.

A four-cycle does not force field preservation in our `E`. Take
`P={+/-alpha/4}`, `Q={+/-(1+2alpha)/4}` and
`u=(1-2alpha)/sqrt(13)`. Then `|u|=1`, `u not in E`, and
`uQ={+/-sqrt(13)/4}`. Every cross distance is one. This is consistent with
the earlier [four-cycle gluing theorem](../hadwiger_nelson_cross_four_cycle_gluing/PROOF.md),
whose conclusion is four-colourability, not field preservation.

The proof above is independent of that four-cycle theorem. Combining the
two results for the connected fixed `B292/V214` sources excludes cross
cycles of lengths four and six in any non-four-colourable disjoint
placement. Combining also the [single-hub theorem](../hadwiger_nelson_mixed506_single_hub_reduction/PROOF.md)
leaves at most one cross-degree-at-least-three vertex, of degree at most
ten. Without a hub, the nontrivial cross components are paths or even
cycles of length at least eight. No assertion about those remaining
cycles, forests, or quadratic angle families is made here.

`identities.py` expands the polynomial identities used in the proof using
a sparse rational polynomial ring. `examples.py` checks the exact small
geometry and boundary examples in a generic complex multiquadratic
algebra, including a pair of distinct quadratic centres with coincident
midpoints, and a labelled six-cycle that collapses to five plane points.
The latter is rejected by the theorem's six-distinct-points condition.
These checks substantiate the algebra and examples; the field, linear
independence and geometry bridges remain the unformalized proof above.

The input [gadget provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
and [fixed inner union](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are unchanged. Parts' primary construction source is
[Graph minimization](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, retains the 509-vertex benchmark. This structural
exclusion is not a record improvement. No priority claim is made for the
elementary circle, quadratic-field, or two-line mechanisms.
