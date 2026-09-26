# Ordered Gaussian weights and unequal-radius square-cone unions

Exact computer-assisted author proof, 26 September 2026. Independent
mathematical review and formalization are pending. This annex adds an
unbounded weight cone to the original [orbit theorem](PROOF.md), with a
new certificate. It yields every Gaussian hinge, bounded radial laws, and
a Kneser--Poulsen union class with strictly unequal radii. The unrestricted
dimension-three problem remains open.

## 1. The positive class

Keep the following **ordered** lists of directions, indexed from zero:

\[
\begin{split}
A&=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),\\
B&=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)).
\end{split}                                                    \tag{O1}
\]

The support map fixes zero and every positive A ray, and sends
\(-tB_j\) to \(tB_j\) for \(t>0\). It is a contraction since it is
an isometry within each cluster and

\[
 |rA_i+tB_j|^2-|rA_i-tB_j|^2=4rt A_i\cdot B_j\ge0,
 \qquad A_i\cdot B_j\in\{0,2\}.                              \tag{O2}
\]

A global 1-Lipschitz extension exists by Kirszbraun's theorem.

**Theorem O1 (ordered weights, all variances).** Let

\[
\mu=p_0\delta_0+\sum_{i=0}^3 a_i\delta_{A_i}
                    +\sum_{j=0}^3 b_j\delta_{-B_j},
\qquad \nu=T_\#\mu,
\]

where the coefficients are nonnegative, sum to one, and

\[
 \boxed{a_0\ge a_1\ge a_2\ge a_3\ge0,
 \qquad b_0\ge b_1\ge b_2\ge b_3\ge0.}                       \tag{O3}
\]

For every \(s>0\), with \(f_s=\mu*\gamma_s\),
\(g_s=\nu*\gamma_s\), and Gaussian covariance \(sI_3\),

\[
 \int(f_s-h)_+\,dx\le\int(g_s-h)_+\,dx\qquad(h>0).           \tag{O4}
\]

There is no bound on the weight ratios. The cone has nonempty interior in
the probability simplex. Zero weights and all equalities in (O3) are allowed.
No relationship between the total A mass and total B mass is required.

**Theorem O2 (bounded radial measures).** Let \(\alpha_i,\beta_i\) be
finite nonnegative measures on \((0,L]\), for some finite \(L>0\), with

\[
 \alpha_0\ge\alpha_1\ge\alpha_2\ge\alpha_3,
 \qquad \beta_0\ge\beta_1\ge\beta_2\ge\beta_3,                \tag{O5}
\]

where inequalities mean that the differences are nonnegative measures.
Replace the atoms in O1 by the measures obtained under
\(r\mapsto rA_i\) and \(t\mapsto-tB_j\), keep arbitrary mass at zero,
and normalize the total mass to one. Then (O4) still holds for all \(s,h>0\).
Equivalently, the four directional densities with respect to a common radial
reference measure are ordered almost everywhere within each cluster.
The two clusters can use different reference measures. This includes
arbitrarily many shells and nonatomic radial laws.

In fact a stronger finite statement holds. Let \(G\) be the group of 48
signed coordinate permutations. For every \(x\in\mathbb R^3\), \(s>0\),
and real \(h\),

\[
 \sum_{g\in G}(f_s(gx)-h)_+
 \le \sum_{g\in G}(g_s(gx)-h)_+,
 \qquad \sum_{g\in G}f_s(gx)=\sum_{g\in G}g_s(gx).           \tag{O6}
\]

The sums count group labels, including repetitions at points with a
nontrivial stabilizer. This finite majorisation is the bridge to geometry.

## 2. A finite certificate for the entire ordered cone

For \(C=A\) or \(B\), put \(F_C^q(x)=\sum_{i=0}^3q_i e^{C_i\cdot x}\).
Every G orbit meets the chamber \(x_1\ge x_2\ge x_3\ge0\).
Use

\[
 e^{x_1}=uvw,\quad e^{x_2}=vw,\quad e^{x_3}=w,
 \qquad u=1+U,\ v=1+V,\ w=1+W\quad(U,V,W\ge0).
\]

For each label \(g\), let \(c_{C,g,i,k}\) be the coefficient at monomial
position \(k\) of \(uv^2w^3 e^{C_i\cdot gx}\). If \(e=g^TC_i\),
the polynomial before shifting is

\[
 u^{1+e_1}v^{2+e_1+e_2}w^{3+e_1+e_2+e_3}.                  \tag{O7}
\]

All exponents lie in the box \((2,4,6)\), giving 105 positions. Define
\(g\preceq_C h\) exactly when, for every \(k\) and \(r=0,1,2,3\),

\[
 \sum_{i=0}^r(c_{C,h,i,k}-c_{C,g,i,k})\ge0.                  \tag{O8}
\]

For any ordered \(q\), the coefficient difference is nonnegative because

\[
 \sum_{i=0}^3 q_i d_i
 =(q_0-q_1)d_0+(q_1-q_2)(d_0+d_1)
  +(q_2-q_3)(d_0+d_1+d_2)+q_3\sum_{i=0}^3d_i.                \tag{O9}
\]

Thus \(F_C^q(gx)\le F_C^q(hx)\) throughout the chamber whenever
\(g\preceq_C h\). This argument is uniform in all weight ratios.
Equivalently, we check the four prefix generators
\((1,0,0,0),(1,1,0,0),(1,1,1,0),(1,1,1,1)\) of the entire cone.

**Certificate lemma.** The relations in (O8) are partial orders. For every
A-upper set \(S\) and B-upper set \(U\),

\[
                  |S\cap U|\ge |S\cap(-U)|.                 \tag{O10}
\]

Here \(-U=\{-g:g\in U\}\). The complete exact records are:

| Quantity | A | B |
|---|---:|---:|
| Comparable ordered pairs, including equality | 750 | 742 |
| Upper sets, including empty and full | 5294 | 5783 |

The first verifier constructs every coefficient by binomial products,
regenerates (O8), and enumerates A-upper sets by disjoint include-successors
or exclude-predecessors branching. For every such S it verifies a bijection
from \((-S)\setminus S\) to \(S\setminus(-S)\) along increasing B-order
edges. There are 5292 nonempty matchings and 87056 matched edges in total.
For a B-upper U, membership of a negative endpoint in U forces membership
of its matched positive endpoint; this proves (O10).

The second verifier imports neither constructor. It builds explicit signed
matrices, expands (O7) by repeated polynomial multiplication, and reconstructs
**all 4608 entries** of the two order relations, comparing each with the
certificate. It enumerates each order's upper sets by adding a vertex only
after its strict successors. Every upper set has such an ordering, so this
enumeration is complete. It then checks **all 30,615,202 pairs** in (O10)
by direct integer intersection counts. The minimum is zero. The sorted
all-pair gap list, with 48 added to each gap and one byte per entry, has hash

```text
3e699553bee5618a0f0bcffb360a8b81e84359a3c96a85825b4eeb88d281e148
```

The compact [ORDERED_CERTIFICATE.json](ORDERED_CERTIFICATE.json), consisting
principally of two 48-row bit-mask relations, has SHA256

```text
9301619c92908a0aeacd2a928e037453d4fd6600aa3d571c8332484222c27044
```

The constructor rejects a reversed B order; the other verifier rejects a
corrupted cyclic comparison. The hashes identify reproducible results and
do not replace execution of the checks. The original fixed-base certificate
and its results are unchanged.

## 3. From the finite lemma to every Gaussian hinge

We recall the elementary identity behind [PROOF.md, Section 2](PROOF.md).
For \(u,v\ge0\) and \(h>0\),

\[
 (u+v-h)_+-(u-h)_+-(v-h)_+
 =\int_0^h\mathbf1_{\{u>t\}}\mathbf1_{\{v>h-t\}}\,dt.         \tag{O11}
\]

If arrays \(a_g,b_g\) are nonnegative and increasing for their respective
orders, their strict superlevel sets are upper. Summing (O11) and using
(O10), while the individual a and b terms cancel under \(g\mapsto-g\), gives

\[
 \sum_g(a_g+b_g-h)_+\ge\sum_g(a_g+b_{-g}-h)_+.               \tag{O12}
\]

For \(h\le0\) the sums are equal by linearity. A common additive constant
or nonnegative multiplicative factor can be absorbed into h.

For a chamber point x, write \(c_s(x)=(2\pi s)^{-3/2}e^{-|x|^2/(2s)}\).
The radial version of the Gaussian expansion is

\[
\begin{split}
 f_s(gx)&=c_s(x)[p_0+a_g+b_{-g}],\\
 g_s(gx)&=c_s(x)[p_0+a_g+b_g],\\
 a_g&=\sum_i\int e^{-r^2/s}e^{rA_i\cdot gx/s}\,d\alpha_i(r),\\
 b_g&=\sum_j\int e^{-3t^2/(2s)}e^{tB_j\cdot gx/s}\,d\beta_j(t).
\end{split}                                                   \tag{O13}
\]

Take a common dominating measure within each cluster. Condition (O5)
makes its four Radon--Nikodym densities ordered almost everywhere.
For every positive r, \(rx/s\) remains in the chamber. Equations
(O8)--(O9) and the positive radial factors in (O13) show that the integrated
arrays are increasing for the same finite orders. Bounded support makes
each integral finite. Thus (O12) proves (O6) in the chamber, and the group
property extends it to every x by relabelling the orbit. Its equal-sum
assertion follows directly from central negation permuting G.

Integrating (O6) over Lebesgue measure and changing variables by each
orthogonal g proves (O4). The hinge integrals are finite, bounded by one.
No interchange of an uncontrolled tail expansion or infinite replica series
is used. Theorem O1 is the single-shell case of O2.

## 4. Unequal-radius ball unions, even for invariant measures

Choose finitely many positive A shell parameters \(r_k\) and B shell
parameters \(t_l\). Put centers at all four \(r_k A_i\) and all four
\(-t_l B_j\), with targets \(r_k A_i\), \(t_l B_j\). At each shell choose
independently ordered radii

\[
 R^A_{k,0}\ge R^A_{k,1}\ge R^A_{k,2}\ge R^A_{k,3}\ge0,
 \qquad
 R^B_{l,0}\ge R^B_{l,1}\ge R^B_{l,2}\ge R^B_{l,3}\ge0.       \tag{O14}
\]

An origin ball of any radius can be included or omitted. Let \(U_X,U_Y\)
be the respective finite unions of **closed** balls with these individual
radii. Empty unions are trivial.

**Theorem O3.** For every \(x\in\mathbb R^3\),

\[
 \boxed{\sum_{g\in G}\mathbf1_{U_X}(gx)
       \ge\sum_{g\in G}\mathbf1_{U_Y}(gx).}                 \tag{O15}
\]

Consequently, for every locally finite G-invariant Borel measure m,

\[
                       m(U_Y)\le m(U_X).                    \tag{O16}
\]

This includes ordinary three-dimensional volume, any radial density, and
surface measure on any sphere centered at the origin. Common translations,
orthogonal transformations and dilations give corresponding versions with
the conjugated symmetry group; the Lebesgue-volume assertion is invariant
under all these changes.

**Proof.** Index the individual balls by v, with centers \(x_v,y_v\)
and radii \(R_v\). For each s>0 set

\[
 q_v(s)=e^{R_v^2/(2s)},\quad Z_s=\sum_vq_v(s),\quad
 p_v(s)=q_v(s)/Z_s,\quad h_s=(2\pi s)^{-3/2}/Z_s.             \tag{O17}
\]

At each shell these coefficients satisfy (O3), no matter how different
the radii are. The finite-shell instance of O2 therefore applies at that
same variance s. For the resulting densities,

\[
 \frac{f_s(z)}{h_s}
 =\sum_v\exp\!\left(\frac{R_v^2-|z-x_v|^2}{2s}\right),       \tag{O18}
\]

and similarly with y for g. The equal orbit sums in (O6), together with
\(\min(u,1)=u-(u-1)_+\), give

\[
 \sum_g\min(f_s(gx)/h_s,1)
 \ge\sum_g\min(g_s(gx)/h_s,1).                              \tag{O19}
\]

For each fixed z the left summand in (O19) tends to \(\mathbf1_{U_X}(z)\):
inside a closed ball a term of (O18) is at least one, while outside all
balls every term tends to zero. This also proves the assertion at ball
boundaries and for radius-zero balls. Taking the limit of the finite sums
proves (O15). Integrating it against m and using G invariance proves (O16).
The unions are bounded, so local finiteness suffices. This strengthens the
Lebesgue small-variance transfer in the team's
[geometric endpoint annex](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md)
for this certified orbit class. It does not require a uniform tail estimate.

## 5. A strict, all-distinct fixture and the rematching boundary

Take the single-shell nine-point configurations \(X=(0,A,-B)\),
\(Y=(0,A,B)\), and assign radii in that order by

\[
       (R_0,R_{A,0},\ldots,R_{A,3},R_{B,0},\ldots,R_{B,3})
       ={1\over40}(32,52,51,50,49,44,43,42,41).                \tag{O20}
\]

At \(x_*=(1,0,1)\), the source union contains all 48 group-labelled
points and the target contains 32. The smallest absolute difference between
a squared distance and the corresponding squared radius, over both
configurations and all these tests, is \(81/1600\). If
\(|x-x_*|<\varepsilon=1/1000\), every such squared distance changes by
less than \(8\varepsilon+\varepsilon^2=8001/10^6<81/1600\), since
\(|gx_*-c|\le\sqrt2+\sqrt3<4\) for each center c. Thus the orbit-count
gap is 16 on this open ball. Globally it is nonnegative by O3, yielding

\[
                 |U_X|-|U_Y|\ge {4\pi\over9\cdot10^9}>0.     \tag{O21}
\]

This explicit lower bound only certifies strictness; it is not an optimized
volume computation. [ordered_geometry.py](ordered_geometry.py) checks all
these finite assertions with rational arithmetic.

The origin ball intersects the interior of every other ball at both
endpoints: \(|c_i|^2<(R_0+R_i)^2\) for all eight other centers.
It cannot be discarded as an isolated common component. This matters
because without the origin the single-shell target centers are coplanar.

The old fixed-base cones force three of the four finite logarithmic rates
in each cluster to agree. In particular their ball limits have
\(R_{A,0}=R_{A,2}\), permitting the coordinate-reflection rematching proved
in the [endpoint annex, Section 4](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md).
Condition (O14) permits all four rates to be strictly ordered; (O20) breaks
both opposite-radius equalities in **both** clusters.

There is a stronger finite check here than simply observing unequal labels:
every ball in (O20) has an exposed open sphere patch in each endpoint union.
Use the outward normal \((0,0,-1)\) for the origin ball, the horizontal
cardinal normals for A, and
\((3B_{j,1}/5,4B_{j,2}/5,0)\) for target B, with their negatives for source
\(-B\). At \(c+Rn\) the corresponding sphere is outside every other ball.
All squared clearances are positive; the smallest over both endpoints is
\(83/100\). The complete rational witnesses are in
[ORDERED_GEOMETRY_EXPECTED.json](ORDERED_GEOMETRY_EXPECTED.json).

If a union of finitely many balls equals either of these endpoint unions,
each exposed sphere patch lies in the union of their boundary spheres.
Finitely many distinct spheres cannot cover a relatively open patch of a
different sphere. Hence one ball has the same center and radius for each
of the nine patches. With nine balls, every ball is forced. Since all nine
radii are distinct, an endpoint rematching carrying radii with the balls
must be the prescribed labelled map T. In particular the old equality-based
rematching cannot establish this fixture. This does not exclude arbitrary
auxiliary constructions or constitute a classification of all known methods.

The [nine-point geometric obstruction](../gaussian_simplicial_cone_reflections/PROOF.md),
Theorem D, says this prescribed T has no continuous contracting motion in
R5; its conclusion is independent of the radii. Thus the established
five-dimensional-motion route, including the team's simplicial and axial
motion classes, does not supply the fixture by its prescribed matching or
by a radius-preserving rematching of its endpoint balls. The positive
result here comes from density-value correlation.

For completeness, the team's existing
[finite-composition theorem](../gaussian_axial_cone_rotations/COMPOSITIONS.md),
Theorem C1, also excludes every finite chain of strong coordinatewise
contractions in R3 with arbitrary rigid alignments at the successive steps.
Indeed \(A^*=\operatorname{cone}(B)\) and
\(B^*=\operatorname{cone}(A)\). The matrix \(H=\operatorname{diag}(-1,-1,1)\)
has negative trace, but \(u^THv\ge0\) for every \(u\in A^*,v\in B^*\):
on the displayed generators its values are zero or two, as checked in
the geometry program. Thus \(I_3\) is outside the rank-one cone required
by that theorem. This applies to the same prescribed matching; the exposed
patch argument again excludes a distinct endpoint radius rematching. It is
a scope application of the existing team lemma, not a new negative route.

## 6. Reproduction, dependencies, and limits

CPython >=3.11, standard library only, with arbitrary-precision integers and
fractions. From this directory:

```bash
python3 verify_ordered_weights.py --check
python3 independent_ordered_check.py --check
python3 ordered_geometry.py --check
sha256sum -c SHA256SUMS
```

The first program shares the original constructor's elementary group,
polynomial and matching routines; the second imports none of them and
checks every relation entry and every upper-set pair. All checks use explicit
exceptions and remain enabled under `python3 -O`. The supplementary geometry
program uses no Gaussian quadrature. Compact expected outputs are supplied;
the large list of individual count differences is recomputed, not stored.
On the recorded CPython 3.11.2 run, the primary calculation took about five
seconds and the direct all-pairs calculation 45 seconds with about 17 MiB
peak resident memory. No optimization or parallel partition is needed.

This is an author proof with exact computational premises, **not** an
independently reviewed or formally verified theorem. The written
cone-to-polynomial, hinge, radial-measure, and geometric arguments are
unformalized trust boundaries. See [ORDERED_SOURCES.md](ORDERED_SOURCES.md)
for primary literature and exact durable team dependencies.

The new cone and the original fixed-base neighborhood are complementary;
neither theorem is asserted to contain the other's entire weight class.
The result answers the endpoint annex's positive obligation for these rays.
It does not settle arbitrary weights on them, arbitrary bounded R3 laws,
unordered individual radii, or intersections of balls. It does not infer
the old covariance obstruction for the new ordered weights. No historical
priority guarantee follows from the bounded literature search.
