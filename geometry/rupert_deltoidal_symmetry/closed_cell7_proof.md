# A whole closed deltoidal receiver cell excludes every source orientation

**six-rupert-1 — researcher — 2026-09-30.**

For the standard deltoidal hexecontahedron, every receiver in the entire
closed cell7 has only the 120 proper relative rotations giving equal
shadows as closed containments at scale at least one. Thus no such receiver
admits a strict Rupert passage, with source direction, rotation, planar
roll, translation and scale unrestricted. All proper body images and
antipodal receiver normals are included.

This completes one whole cell of the twelve-cell reflection chamber.
It has four times the unit-z chart area of the previous certified
half-cell7 triangle and 400 times that of the earlier mix1/20 triangle.
These are chart-area ratios, not spherical area ratios. The global Rupert
problem remains **open** on the complementary receiver directions.

The proof is complete and written, with exact finite hypotheses checked
below. It is unformalized, and independent review is not asserted. The
improvements are the source coefficient **21/8**, a complete physical-area
maximum calculation on each closed triangle, and the actual contact
remainder bound **73/50**. A ten-piece closed cover has a uniform
torque–remainder margin **1/2000**. Two pieces have edge-critical area
maxima; checking only their corners would not establish these bounds.

## 1. Model, dependencies and theorem

Let $K=\operatorname{conv}(V)=-K$, using the 62 ordered original vertices
in [verify.py](verify.py). Write $G$ for its complete proper body group,
of order 60, $P_n$ for projection onto $n^\perp$, and $A(n)$ for the
physical area of $P_nK$. Put $s=\sqrt5$ and

\[
\begin{split}
 M&=((3s-5)/6,(s-1)/6,1),& m&=M/\|M\|,\\
 N_7&=((25-7s)/38,(9-s)/38,1),\\
 N_8&=((5-s)/10,(-5+3s)/10,1),\\
 a_0^2&=(3503950+1491850s)/31581,& a_0&>0.
\end{split}
\]

The [global-area proof](global_area_proof.md), source
5596212ab31932f7dd8b90cf6f1ad73c66afbe16, graph
bafkreigpe3pe5qqrekltisoss3zikl3znyydtso7utxsvag2yu2ykz3tsm at height7378,
establishes the model, twelve closed cells, global minimum $a_0$, and
complete minimum-normal orbit $Gm$, including antipodes. In particular
$m$ is not a proper rotational symmetry axis; its body stabilizer is
trivial. The minimum shadow's proper planar symmetry group is $C_2$.

The [adaptive-area proof](adaptive_area_proof.md), source
2a0eb5428787e69876ac4652f7d8c192c07fa9e2, graph
bafkreiejtc4l7y4ubwokktltjem2nb2rviz3ds3jld4yavourzxaacwc4m at height7410,
supplies the original area/roll framework and actual weak supports.
The [directional-area proof](directional_area_proof.md), source
7d6c787f4760e4038e23256c6a6e396ec73b38ec, graph
bafkreihb55kg5d5tclfow7alxh6zseg7hpjyhanejzjatmlt6vn2cxztau at height7454,
proves the selected transport errors, complete reduced-roll control,
structured full-angle bound, and previous closed half-cell. Its whole
exact computation and both earlier computations are replayed by the new
checker. All parent mathematical hypotheses remain dependencies.

For $u$ in the entire closed triangle

\[
                 \mathcal T_7=\operatorname{conv}(M,N_7,N_8),       \tag{1}
\]

the actual area vector is

\[
 C_7=((5+15s)/11,(10+30s)/33,(20+10s)/3),\qquad
                    A(u/\|u\|)=C_7\cdot u/\|u\|.                 \tag{2}
\]

It has positive dot product with every ray in (1). The four contact
triples $(p,q,j)$ are

\[
                 (43,57,43),\ (57,61,57),\ (57,61,61),\ (45,34,34).
\]

Define

\[
 \mu_j(u)=(V_q-V_p)\times u,\quad T_j(u)=V_j\times\mu_j(u),\quad
                 r_7(u)=\min_{\|z\|=1}\max_j z\cdot T_j(u).        \tag{3}
\]

Indices $j$ in (3) enumerate the four contacts. Repeated original
vertices are retained as different contacts, not merged. Every $\mu_j$
is an actual weak outer support throughout the whole closed cell.

**Theorem.** For every $n=u/\|u\|$ with $u\in\mathcal T_7$, every
$Q\in SO(3)$, every $t\in n^\perp$, and every $\lambda\ge1$,

\[
 \lambda P_nQK+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad Q\in G\cup J_nG,
 \qquad J_n=2nn^T-I.                                             \tag{4}
\]

These are two disjoint **left** cosets, containing exactly120 proper
rotations. The theorem holds also at each closed edge and corner and
on every $g\mathcal T_7$ and $-g\mathcal T_7$, $g\in G$, after
normalization. Neither a restriction on the original relative angle
nor a restriction on the source normal is imposed.

## 2. A global source-normal coefficient of21/8

The complete chamber has14 distinct unit-z corner rays $u_i$, with
minimum $u_9=M$. Let $q_i=A(u_i/\|u_i\|)^2$, $q_*=a_0^2$, and

\[
 t_i^2=1-{(M\cdot u_i)^2\over\|M\|^2\|u_i\|^2},\qquad
 \kappa=21/8,\quad \gamma=51/50,\quad
                          d_i^2={\gamma^2t_i^2\over\kappa^2}.
\]

For all13 nonminimum corners the checker proves exactly

\[
 q_i-q_*-d_i^2>0,\qquad
               (q_i-q_*-d_i^2)^2>4q_*d_i^2.                       \tag{5}
\]

The positive branch in (5) gives
$A(u_i/\|u_i\|)-a_0>\gamma t_i/\kappa$.
For a whole closed cell, write $u=\sum_i\lambda_i u_i$ with
$\lambda_i\ge0$ and $\sum_i\lambda_i=1$. Set $n_i=u_i/\|u_i\|$,
$n=u/\|u\|$, and $w_i=\lambda_i\|u_i\|/\|u\|$. Then

\[
 n=\sum_iw_in_i,\quad\sum_iw_i\ge1,\quad
 A(n)-a_0=\sum_iw_i(A(n_i)-a_0)+a_0(\sum_iw_i-1).
\]

The area identity uses the actual linear area vector of this cell.
Consequently

\[
             \|P_mn\|\le\sum_iw_it_i
                     \le(\kappa/\gamma)(A(n)-a_0).                \tag{6}
\]

The exact chamber-corner checks also give
$m\cdot n>c=2399/2601$ throughout the closed chamber: extend the
positive dot inequalities by linearity and the norm triangle inequality.
Since $2/(1+c)=\gamma^2$,

\[
        \|n-m\|^2={2\over1+m\cdot n}\|P_mn\|^2
                        \le\gamma^2\|P_mn\|^2.
\]

The case $n=m$ holds directly. Fold an arbitrary unit normal by actual
orthogonal body symmetries into the chamber. Areas are invariant and
the full directed minimum orbit is $Gm$. This proves

\[
                  \operatorname{dist}(k,Gm)\le\kappa(A(k)-a_0)
                  \qquad\text{for every unit }k.                 \tag{7}
\]

No optimality of $\kappa$ is claimed. The smaller coefficient13/5 fails
one of (5); that failure concerns this sufficient corner argument.

## 3. Refined receiver criterion using actual contact remainders

For $n=u/\|u\|$ in (1), put

\[
\begin{split}
 e&=A(n)-a_0,&\delta&=\|n-m\|,&a&=\kappa e,\\
 E_0&=(29/100)(a+\delta)+(23/20)(a^2+\delta^2),\\
 E&=(29/100)a+(141/200)\delta+(23/20)(a^2+\delta^2),\\
 b&=2E,&X&=\sqrt{(a+\delta)^2+b^2},&\Theta&=(1003/1000)X.
\end{split}                                                       \tag{8}
\]

We will verify on every closed piece that

\[
 \delta\le1/20,\quad a\le1/10,\quad E_0\le1/28,\quad b\le1/10,
 \quad X\le3/20,\qquad r_7(u)>B\Theta,\quad B=73/50.              \tag{9}
\]

Here is why (9) implies (4). Central convex symmetry reduces a closed
containment at arbitrary $\lambda\ge1,t$ to centered containment at
scale one. With $k=Q^Tn$, area monotonicity and (7) provide an actual
proper body gauge $h\in G$ such that $\|h^Tk-m\|\le a$. Let
$R_1,R_2$ be the minimal proper rotations carrying $m$ to $h^Tk,n$.
Their operator chords are at most $a,\delta$.

Apply the parent's complete roll argument, with this new source bound.
It uses the unique antipodal maximum-radius pair $V_4=-V_{57}$, the
strict radius gap $R_0-\sqrt5>1/28$, and both signed actual edge probes
$(57,59,57,+1),(41,57,57,-1)$. Its 60 nonmaximum joint radius/height
comparisons and124 support-gap/height comparisons are replayed. They
give a left half-turn gauge and a factorization

\[
                 Q'=J_n^\sigma Qh=R_2WR_1^T,
\]

where $W$ fixes $m$, its reduced roll lies in the **complete** interval
$[-\pi/2,\pi/2]$, and its chord is at most $b$. The remote-roll step
uses $E_0\le1/28$ to force roll chord below1/5 before applying the
signed support estimate. Thus no small-roll premise is being assumed.
The errors $E_0,E$ concern selected probes; they are not full-shadow
Hausdorff bounds.

The axes of $R_1^T,R_2$ are perpendicular to $m$, and that of $W$ is $m$.
The structured composition lemma gives $\|Q'-I\|\le X$. The parent's
exact four-variable identity and positive quaternion branch are
replayed. For $X\le3/20$, differentiating $2\arcsin(x/2)$ gives
the full principal rotation angle $\theta\le\Theta$, because

\[
                (1003/1000)^2\bigl(1-(3/20)^2/4\bigr)>1.          \tag{10}
\]

This is the same composition mechanism credited to six-rupert-3,
[ORTHOGONAL_COMPOSITION_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
source4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph
bafkreigmk5cetignwl2kdcdsks5mbnwajuamd4znhr5iorjgol7wzmf26y at height7414.
Its perpendicular-axis hypotheses hold in this exact factorization;
no other solid's geometric constants are imported.

For each of the four contacts at each of the three **whole-cell** corners,
the checker verifies

\[
              {\|V_j\|^2\|\mu_j(u)\|^2\over4}<B^2.              \tag{11}
\]

Since $\mu_j$ is linear in $u$ and its norm is convex, (11) extends
throughout (1). This keeps the actual support normal rather than
bounding it by edge length times $\|u\|$. All744 weak-support
comparisons at the three corners also pass; linearity extends those
supports to the entire cell, including every tie on its boundary.

If $\theta>0$ and $v$ is the full rotation vector of $Q'$, some contact
has $v\cdot T_j(u)\ge\theta r_7(u)$. The integral rotation remainder
$\|Q'V_j-V_j-v\times V_j\|\le\|V_j\|\theta^2/2$ gives

\[
            \mu_j(u)\cdot(Q'V_j-V_j)
                    \ge\theta r_7(u)-B\theta^2>0,                \tag{12}
\]

contradicting centered closed containment. Hence $Q'=I$, which gives
$Q\in G\cup J_nG$. Conversely these rotations give equal shadows by
body symmetry and $K=-K$. Equal positive areas force $\lambda=1$,
and the support inequalities force $t=0$.

The parent proves
$\min_{g\in G}\|J_m-g\|_F^2=(106-36s)/29>8(1/20)^2$.
Since $\|J_n-J_m\|_F^2\le8\delta^2$, $J_n\notin G$ under (9).
Thus the two left cosets in (4) are disjoint and have120 elements.
Conjugation and antipodal invariance prove the stated receiver images.

## 4. Complete physical-area maxima on closed triangles

Consider any nondegenerate closed unit-z triangle with vertices
$a,b,c$ and positive $C_7\cdot u$ throughout. Its normalized rays are
the unit vectors in the positive cone of $a,b,c$. The maximum of
$C_7\cdot n$ exists. At a maximizer in the relative interior of a
spherical face, the tangential derivative vanishes.

There are exactly these strata to inspect:

1. A corner $a$, with squared value $(C_7\cdot a)^2/\|a\|^2$.
2. An open edge cone spanned by distinct rays $a,b$. Its only positive
   critical direction is proportional to the orthogonal projection of
   $C_7$ onto $\operatorname{span}(a,b)$. Write that projection
   $p=\alpha a+\beta b$. The Gram determinant is strictly positive, and
   \[
   \alpha={(C_7\cdot a)\|b\|^2-(C_7\cdot b)(a\cdot b)\over
                 \|a\|^2\|b\|^2-(a\cdot b)^2},\quad
   \beta={(C_7\cdot b)\|a\|^2-(C_7\cdot a)(a\cdot b)\over
                 \|a\|^2\|b\|^2-(a\cdot b)^2}.
   \]
   Include the candidate $\|p\|^2$ exactly when $\alpha,\beta>0$.
   A zero coefficient lies at a previously included corner.
3. The open interior, where the only positive critical direction is
   proportional to $C_7$. Include $\|C_7\|^2$ exactly when
   $C_7/(C_7)_z$ lies strictly inside the chart triangle, checked by
   all three oriented edge signs. Here $(C_7)_z>0$. Boundary critical
   points have already been included in a lower-dimensional stratum.

The negative critical directions have negative dot product and cannot
be maxima, since $C_7\cdot n>0$. These cases exhaust every stratum,
so the largest included squared value $q_{\mathcal P}$ is the actual
maximum throughout the whole closed triangle $\mathcal P$.

All calculations are in $\mathbb Q(\sqrt5)$, with exact signs. In the
actual cover, pieces110 and112 have edge1 maxima. The checker also
tests a simple corner trap: on
$\operatorname{conv}((0,0,1),(1,0,1),(0,1,1))$ with $C=(1,1,1)$,
the squared maximum is8/3 at the middle of the opposite spherical edge,
whereas every corner squared value is at most2. Interior and corner
examples, and reversal of the triangle orientation, are checked too.

## 5. Outward enclosures and closed coverage

Every positive upper enclosure is a rational multiple of $10^{-6}$.
A bounded binary search chooses the first grid point passing a strict
exact comparison and checks the previous positive grid point as well.
No ordinary floating-point approximation enters a proof decision.

For the physical area excess, find $e_{\mathcal P}>0$ with
$\sqrt{q_{\mathcal P}}-\sqrt{q_*}<e_{\mathcal P}$. The exact test is

\[
 L=q_{\mathcal P}-q_*-e_{\mathcal P}^2;\qquad
     L\le0\ \text{or}\ L^2<4e_{\mathcal P}^2q_* .                \tag{13}
\]

If $L\le0$, positivity of $q_*,e_{\mathcal P}$ proves the strict
inequality directly. Otherwise (13) squares only positive quantities.
The search cap is1/10 and is itself tested.

At each of the three corners, find a chord bound $d>0$ by checking

\[
 M\cdot u>0,\qquad
      (M\cdot u)^2>(1-d^2/2)^2\|M\|^2\|u\|^2.                  \tag{14}
\]

The tested cap is1/20, so $1-d^2/2>0$. Taking the largest corner bound
$\delta_{\mathcal P}$ extends to the whole triangle: the corresponding
positive spherical cap is closed under positive combinations, by
linearity of $m\cdot u$ and the norm triangle inequality.

Substitute these upper bounds in (8). All expressions are monotone for
nonnegative $e,\delta$. Check every gate in (9) and find an outward
rational $\theta_{\mathcal P}$ with
$(1003/1000)^2((a_{\mathcal P}+\delta_{\mathcal P})^2+b_{\mathcal P}^2)
<\theta_{\mathcal P}^2$. Set

\[
               \rho_{\mathcal P}=B\theta_{\mathcal P}+1/2000.     \tag{15}
\]

The fixed closed subdivision has leaves

\[
                 0,\ 10,\ 110,\ 111,\ 112,\ 113,\ 12,\ 13,\ 2,\ 3.
\]

For an ordered triangle $(a,b,c)$, put $ab=(a+b)/2$, $bc=(b+c)/2$,
$ca=(c+a)/2$, and label its four children

\[
 0=(a,ab,ca),\quad1=(ab,b,bc),\quad2=(ca,bc,c),\quad3=(ab,bc,ca).
\]

This is an exact closed cover: if a barycentric coordinate is at least
1/2 the point lies in its corner child; if all three are at most1/2
it lies in the central child. Each child's oriented chart area is one
quarter of its parent's. Internal paths are exactly the root,1 and11;
every internal node has all four children. The prefix tree is reconstructed,
all paths are checked, and the leaf chart-area fractions sum exactly to1.
No inference of coverage from sampled points or area alone is made.

The largest certified piece bounds are

\[
 e_{\mathcal P}\le8597/500000,\qquad
 \delta_{\mathcal P}\le43149/1000000,\qquad
 \theta_{\mathcal P}\le523/4000.
\]

These are upper enclosures, not asserted exact global extrema. The
per-piece values and coefficient hashes are in
[expected_closed_cell7.json](expected_closed_cell7.json).

## 6. Polynomial ball certificates throughout every closed piece

On a piece with chart corners $u_0,u_1,u_2$, write
$u=\sum_{k=0}^2\lambda_ku_k$, $\lambda_k\ge0$, $\sum_k\lambda_k=1$.
The four actual torque vectors $T_j(u)$ are linear in $\lambda$.
Their signed homogeneous cubic cofactors

\[
                 w_j=-(-1)^j\det(T_0,\ldots,\widehat T_j,\ldots,T_3)
\]

have all40 monomial coefficients strictly positive. The checker also
verifies identically, as polynomials in all three coordinates,
$\sum_jw_jT_j=0$. Thus the four vertices are affinely independent,
and the origin lies strictly inside their tetrahedron even on the
closed boundary: positive weights give a dependence, nonzero minors
give rank3, and $\sum_jw_j>0$ excludes an affine dependence.

For a facet opposite contact $j$, let $N_j$ be the cross product of
the two facet edge vectors, and let $H_j=N_j\cdot T_a$ for one of
its vertices. The checker verifies the exact cofactor identity for
$H_j$. Every one of the28 monomial coefficients of

\[
 H_j^2-\rho_{\mathcal P}^2\|N_j\|^2(\lambda_0+\lambda_1+\lambda_2)^2
\]

is strictly positive. On the nonnegative simplex this proves each
facet distance strictly exceeds $\rho_{\mathcal P}$. The origin is
interior, so its ball of that radius lies in the tetrahedron and

\[
                r_7(u)>\rho_{\mathcal P}
                   >B\Theta(u)+1/2000
                   \qquad(u\in\mathcal P).                       \tag{16}
\]

The strict second inequality follows from the outward angle enclosure.
Corner and barycenter direct evaluations audit the polynomial formulas;
coverage and positivity throughout the continuum follow from the
coefficient proof. Across ten leaves there are400 positive cubic and
1120 positive degree-six coefficients,30 identically zero balance
coordinates, and320 direct evaluation audits. No hidden polynomial
corpus is needed: all coefficients are regenerated from the62 vertices,
four contacts and ten paths. The hashes summarize the reconstructed
coefficients. Equations (9),(12),(16) prove the theorem.

## 7. Reproduction, literature and remaining frontier

Run from this directory, using Python3.11+ and its standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B closed_cell7_certificate.py --self-test > closed-cell7-result.json
python3 - <<'PY'
import json
assert json.load(open('closed-cell7-result.json')) == json.load(open('expected_closed_cell7.json'))
print('all fields match')
PY
```

The parent expected directional file is pinned by SHA256
`e0ee007750c6dcb08d15d1222344ed22f59a13523f822c79f31ee09da8fed34c`.
Its complete derivation and pinned earlier parents are replayed before
the new finite checks. Eight malformed controls reject a false source
coefficient, remainder and angle factor, missing/overlapping/duplicate
cover leaves, a reversed weak support and an unsupported margin.
Five definition-level area/grid controls pass. Optimized Python is refused
because assertions are part of the checker. There are no solvers, external
numeric libraries, hidden inputs or floating-point proof decisions.
The trust boundary is the stated continuous geometry, the earlier
unformalized proofs, Python/Fraction and the exact ordered-field code.

The primary status source remains Raj Gosain and Benjamin Grimmer,
[Some New Insights from Highly Optimized Polyhedral Passages](https://arxiv.org/abs/2509.08190),
especially Tables3–4. The named deltoidal and pentagonal hexecontahedra
remain open in the primary literature inspected through2026-09-30.
[2604.26531](https://arxiv.org/html/2604.26531) proposes the
rhombicosidodecahedron as a non-Rupert conjecture, not an established
counterexample. [2508.18475](https://arxiv.org/abs/2508.18475) constructs
a different non-Rupert body. None resolves this named solid.

The local phase was already closed by six-rupert-1's uniform strict
small-angle result, source58ec651cdd077243b556287369b6f56132735f6d,
graph bafkreifnp5u7bnnjoxqysdxep55lhl6ohvvro6jmagbdw4wacpdae2eryy
at height7322. Its gap is existential and supplies no numerical
global angle cover. This whole-cell theorem advances the all-source
receiver domain instead; it does not settle global non-Rupertness.

Complementary work read for this pass includes six-rupert-2's
[J77 signed-region classification](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_sharp_region_gap/PROOF.md),
source2def43a003a2a692571ae654c543517b1cb20e6b, graph
bafkreieoes3bbhpwp53w22xek5ky7mrwmhcdxnb37fex5c2gox4zalouua at height7438,
and six-rupert-3's
[balanced RID support proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/BALANCED_SUPPORT_PROOF.md),
sourcea28d2c5b3ceeaee468843f42fef97d3a6efafad8, graph
bafkreih3x3gcblkb75wdttiaemyogphqiwcptjd3qjunsbjydn6qozyzxa at height7468.
The latter requires
threefold-covariant endpoints with a common signed height to cancel
first-order source tilt. Those hypotheses do not follow from our
minimum shadow's $C_2$ symmetry or from antipodal vertices. Neither
peer's solid-specific constants or conclusions are used in this proof.
These are precise source credits, not independent reviews of this theorem.

The next frontier is the remainder of the closed reflection chamber.
The new coefficient and physical-area maximum routine can be reused on
adjacent receiver pieces, but the gates in (9), actual support persistence
and torque bounds must all be established there. No conclusion about
the complementary receiver sphere follows from a failed sufficient
certificate or a floating-point passage search.
