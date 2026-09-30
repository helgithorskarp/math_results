# The complete four-level degree-nine angular classification

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Status: complete ordinary author proof with an exact rational continuous
domain certificate. Independent review of this extension is pending.

## 1. Statement and credited inputs

For a nonzero balanced real eight-vector, max-normalize to
\(\max|\theta_j|=1\), and use
\[
 \mu_k=\sum\theta_j^k,\quad e=\mathbf1/\sqrt8,\quad P=I-ee^*,
 \quad C=P\operatorname{diag}(\theta)P|_{e^\perp},
 \quad w=\operatorname{diag}(\theta)e,
\]
\[
 \Psi=\sum_{\lambda\text{ distinct}}\|\Pi_\lambda w\|^4,
 \quad J=122\mu_2+\frac{224\mu_4-5760\Psi}{\mu_2},
 \quad K=p_8J/\mu_2,\quad p_8=10985/33554432.                  \tag{1}
\]
Full projections are used at collisions. The functional, its continuity
and polynomial interpretation are credited to the
[angular quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and its
[independent audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md).
Let \(\mathcal F_4\) be the closed set of such normalized vectors with
**at most four distinct coordinate values**. No prescribed multiplicity
pattern or central symmetry is imposed.

Recall the credited value
\[
 j(u)=\frac{2058+21912u-15876u^2+19224u^3+3402u^4}
                   {(3+u)(1+3u)^2},\qquad J_*=j(u_*),          \tag{2}
\]
where \(u_*\in(2/25,9/100)\) is the unique maximizing root of
\[
 26634-231084u-907290u^2+376920u^3
                   +971190u^4+224532u^5+30618u^6=0.
\]
The [complete asymmetric 3+3+1+1 theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_asymmetric_four_block_stability/PROOF.md)
proves its whole-class maximum, equality orbit and unit-direction
stability constant \(7/6\). The scalar value and
\(J_*>j(1/9)=5472/7>780\) come from the
[credited symmetric face](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_symmetric_displacement_face/PROOF.md).
The [complete equal-pair theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_double_displacement/PROOF.md)
proves \(J<615\) throughout \(2+2+2+2\). Those results are inputs;
their scalar optima are not claimed again.

**Theorem 1.** On the whole set \(\mathcal F_4\),
\[
 \boxed{J\le J_*},
\]
with equality exactly at permutations of
\[
 \theta_*=(1,1,1,-1,-1,-1,\sqrt{u_*},-\sqrt{u_*}).             \tag{3}
\]
The new global exclusions are
\[
 J\le780\quad\text{in both }3+2+2+1\text{ and }4+2+1+1,
 \qquad J\le3328/5\quad\text{in }5+1+1+1.                  \tag{4}
\]
All collisions and saturation choices are included. The numbers in (4)
are sufficient bounds, not asserted exact maxima of those three cohorts.
Writing \(\mathcal O_*\) for the unit-normalized orbit in (3),
\[
 \boxed{\operatorname{dist}(\theta/\sqrt{\mu_2},\mathcal O_*)^2
                    \le\frac73(J_*-J).}                    \tag{5}
\]
Thus a near-maximal four-level sequence converges to this orbit. This is
a global support-size classification; no reduction of arbitrary
five-to-eight-level vectors to this class is asserted.

## 2. Moment exclusion and multiplicity completeness

If the actual distinct levels are \(t_1,\ldots,t_k\), group the
coordinates into their equal-level blocks. Within-block difference
spaces are eigenvectors of the diagonal matrix and of its compression;
they are orthogonal to \(w\). The block-constant space is invariant,
and its intersection with \(e^\perp\) has dimension \(k-1\).
Therefore at most \(k-1\le3\) distinct compression modes have positive
\(w\)-weight. Their weights sum to \(\nu=\|w\|^2=\mu_2/8\).
Cauchy--Schwarz and \(\mu_4\le\mu_2\) give
\[
 \Psi\ge\nu^2/3=\mu_2^2/192,\qquad
 J\le92\mu_2+224\mu_4/\mu_2\le92\mu_2+224.                 \tag{6}
\]
In particular, \(\mu_2\le6\) implies \(J\le776\).
This bound remains valid at every collision.

If a level \(b\) has multiplicity \(m\ge5\), balance and normalization
imply \(|b|\le(8-m)/m\), and hence
\[
 \mu_2\le m((8-m)/m)^2+(8-m)=8(8-m)/m\le24/5.
\]
Equation (6) proves \(J\le3328/5<780\), settling the heavy cohort.
An actual binary profile has only one positive-weight mode, so
\[
 \Psi=(\mu_2/8)^2,\qquad
 J=32\mu_2+224\mu_4/\mu_2\le480.                            \tag{7}
\]

There are exactly five positive four-part multiplicity partitions of8:

| Partition | Whole-class bound | Input or new proof |
|---|---:|---|
| 5+1+1+1 | 3328/5 | New moment bound |
| 4+2+1+1 | 780 | New exact weighted-cubic cover |
| 3+3+1+1 | J* | Credited complete asymmetric theorem |
| 3+2+2+1 | 780 | New exact weighted-cubic cover |
| 2+2+2+2 | less than615 | Credited complete equal-pair theorem |

Every vector with fewer than four levels can be represented with four
positive block labels: split an occupied block into two labels without
changing its level, and repeat. Eight coordinates ensure this can
continue until four labels exist. Thus the table covers all of
\(\mathcal F_4\), rather than only profiles with four distinct levels.
Only its \(3+3+1+1\) row can attain \(J_*\), and its credited equality
classification proves (3). For that row, the credited distance estimate
has constant \(7/6\). For every other row, \(J_*-J>12/7\), while the
squared distance between unit vectors is at most4. Since
\((7/3)(12/7)=4\), (5) follows throughout the union.

## 3. Exhaustive saturation polygons and their closed fan covers

Take either new cubic cohort. Some label is saturated in absolute value;
reflect to make it \(-1\), and denote its multiplicity by \(m\).
If \(m=4\), balance forces all four remaining coordinates to equal
\(+1\), already covered by (7). A saturated multiplicity greater than4
is impossible. For each remaining inequivalent choice, order the other
three multiplicities as \(n\ge h\ge l>0\), and use labels
\[
 (-1,x,y,z),\qquad z=(m-nx-hy)/l.                            \tag{8}
\]
No ordering of the **values** is imposed. Their full admissible domain is
the compact rational polygon
\[
 \mathcal P_{mnhl}=\{(x,y):|x|\le1,\ |y|\le1,
                                    |(m-nx-hy)/l|\le1\}.    \tag{9}
\]
Equal-mass labels are interchangeable; fixing which one is saturated
loses no profile. The five required polygons and their certificates are:

| Saturated and remaining masses | Boundary edges/fans | Closed leaf rectangles |
|---|---:|---:|
| 3,2,2,1 | 3 | 7 |
| 2,3,2,1 | 4 | 6 |
| 1,3,2,2 | 5 | 5 |
| 2,4,1,1 | 4 | 6 |
| 1,4,2,1 | 4 | 6 |

The checker constructs every feasible intersection of two of the six
boundary lines in (9), removes duplicates, and sorts the vertices
counterclockwise using rational determinants. Every polygon vertex of
this bounded full-dimensional intersection has two active boundary
constraints, so this construction is exhaustive. It checks that each
successive edge is an original boundary face, all vertices lie on its
inner side, and the center
\[
 c_0=(m/(8-m),m/(8-m))
\]
is strictly on the inner side of every edge. It also reconstructs the
polygon area as the sum of its positive fan triangle areas.

For each boundary edge from \(a\) to \(b\), its triangle with center
\(c_0\) is parameterized by the full unit square:
\[
 (x,y)=c_0+\rho[(1-v)(a-c_0)+v(b-c_0)],\quad0\le\rho,v\le1. \tag{10}
\]
These are convex combinations of admissible points, and every point of
the polygon lies in a fan triangle. A ray from the interior center
meets the boundary, which proves coverage including all edges. The
whole edge \(\rho=0\) maps to the same triple collision.

The compact cover.json supplies only unit-square binary bisection trees;
it supplies no polynomial or sign oracle. Both closed children of every
split are required, both are traversed, and every leaf is checked. The
root square has area1; exact accumulated child areas are verified at
every split. Missing fans, duplicated fans, omitted closed children and
extra domains are rejected. The five saturation choices above and all
their20 fan indices are fixed independently of that input file.

## 4. Exact cubic trace and all zero-discriminant profiles

Let \(t=(-1,x,y,z)\) with positive masses \(m_i\) from (8), and set
\[
 H(\lambda)=\prod_i(\lambda-t_i)^{m_i},\quad
 g(\lambda)=\prod_i(\lambda-t_i),\quad
 R(\lambda)=\prod_i(\lambda-t_i)^{m_i-1},
\]
\[
 Q(\lambda)=\sum_i m_i\prod_{j\ne i}(\lambda-t_j),\qquad H'=RQ.
                                                               \tag{11}
\]
The leading coefficient of \(Q\) is8. Equal-level difference modes have
zero weight. At a simple \(Q\)-root, the secular compression identity
gives
\[
 r_\lambda=\|\Pi_\lambda w\|^2
     =-8H(\lambda)/H''(\lambda)=-8g(\lambda)/Q'(\lambda).     \tag{12}
\]
This follows, for example, from the block determinant decomposition
of the diagonal matrix along \(e\oplus e^\perp\), whose compression
characteristic polynomial is \(H'/8\). At a common simple root of
\(g,Q\), the weight is zero and the last fraction in (12) applies;
the original fraction is not evaluated as \(0/0\).

Write \(Q=8\lambda^3+q_2\lambda^2+q_1\lambda+q_0\) and
\(\Delta=\operatorname{Disc}(Q)\). Its quotient companion matrix is
\[
 M=\begin{pmatrix}0&0&-q_0/8\\1&0&-q_1/8\\0&1&-q_2/8\end{pmatrix},
 \qquad Y=Q'(M),\quad \det Y=-\Delta/8.
\]
For \(\Delta>0\), define \(f(M)=-8g(M)\). Then
\[
 \Psi=\operatorname{tr}(f(M)^2Y^{-2}),
 \quad 64\operatorname{tr}(f(M)^2\operatorname{adj}(Y)^2)
                              =\Delta N_\Psi,
 \quad \Psi=N_\Psi/\Delta.                                  \tag{13}
\]
For each of the five mass charts, the source derives these polynomial
identities over \(\mathbb Q[x,y]\), checks the companion equation,
adjugate relation, exact discriminant division and complete multiplication
back. No cubic radical or floating approximation is used.

The zeros of \(\Delta\) are all actual binary profiles. To see this,
for distinct original levels the secular function
\(\sum m_i/(\lambda-t_i)\) is strictly decreasing between consecutive
levels and has exactly one simple zero in each interval. If one pair of
labels coincides, \(Q\) acquires one simple zero at that label plus two
strictly interlacing active zeros. If the labels coincide in two pairs,
\(Q\) has the two distinct original values as simple zero-weight roots
and one active root strictly between them. A repeated \(Q\)-root thus
occurs only when three labels coincide; then the actual vector has two
levels. Four coincident labels would give the zero vector and cannot
be normalized. This also proves \(\Delta>0\) in every remaining case.
Equation (7) handles every excluded discriminant point directly.

For \(\Delta>0\), the exact angular numerator and denominator are
\[
 N=(122\mu_2^2+224\mu_4)\Delta-5760N_\Psi,
 \quad D=\mu_2\Delta>0,\quad J=N/D.                          \tag{14}
\]
On each fan, exact division removes \(\rho^2\) from both
\(780D-N\) and \(\Delta\), and multiplication back is checked.
The new certificates prove their resulting polynomials nonnegative on
each **trace** leaf. Hence \(J\le780\) for positive discriminant and
\(\rho>0\). At \(\rho=0\), and at any other zero discriminant point,
(7) applies without division. On the eight **low-moment** leaves the
certificate instead proves \(6-\mu_2\ge0\), so (6) gives \(J\le776\).

There are22 trace leaves and8 low-moment leaves. The source recomputes
every one of their **3020** tensor Bernstein sign coefficients:
2178 for the bound,770 for the discriminant,72 for the moment cells.
Every affine change and inverse basis identity is checked. The product
Bernstein basis is nonnegative and sums to one on each closed rectangle;
nonnegative coefficients therefore prove the whole continuous domain.
Sampling is not the sign proof. This establishes both new cubic rows
in (4), with complete saturation and collision coverage.

## 5. Sharp complex phase-class displacement basin

Let \(p(z)=b(z-a)\prod_{j=1}^8(z-z_j)\), \(b\ne0\), have simple real
marked root \(0<a<1\), with \(|z_j|\le1\). Other original roots and
critical points may repeat; critical multiplicities count. Put
\[
 G_a=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16/(1+a),\quad
 \rho_p=\max|z_j+1|,\quad \kappa=(1+a)(a-5/8),\quad d_0=13/8.
\]
For \(\rho_p\le1/2\), write uniquely
\(z_j=-(1-\tau_j)e^{i\phi_j}\), \(\tau_j\ge0\), with small principal
real phases. Require **at most four distinct phase values**, including
collisions and all phases equal. Inward depths may vary independently
within phase blocks; no real-coefficient hypothesis is imposed.
Let \(R_4(a)\) be the supremum of \(r\in[0,1/2]\) such that every
polynomial in this class with \(\rho_p\le r\) satisfies \(G_a\ge0\).
The admissible radii form an initial interval; endpoint admissibility
is not assumed.

**Corollary 2.** This whole class has the sharp leading basin
\[
 \boxed{\lim_{a\downarrow5/8}\frac{R_4(a)^2}{\kappa}
      =B_*=\frac{106496}{5J_*},\qquad27.106707<B_*<27.106708.} \tag{15}
\]
The constant and the matching family are credited. The new conclusion
extends their sharp validity from one multiplicity pattern to every
four-level phase profile. Every squared radius
\((B_*-\varepsilon)\kappa\), \(0<\varepsilon<B_*\), is uniformly
sufficient for small positive \(a-5/8\). Negative sequences with
\(a\downarrow5/8\) and \(\rho_p^2/\kappa\to B_*\)
have total inward depth and squared total phase \(o(E_a^2)\), centered
unit directions tending to \(\mathcal O_*\), and \(G_a/E_a^2\to0\).

The analytic premises are the credited
[all-disk joint expansion](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md)
and [original-root variational reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_displacement_variational_basin/PROOF.md).
With \(T=\sum\tau_j\), \(M=\sum\phi_j\),
\(s=\|\phi-(M/8)\mathbf1\|\), \(\eta=(\phi-(M/8)\mathbf1)/s\),
and \(q_\infty=\max\eta_j^2\), their uniform negative-gap bootstrap
gives \(s>0\), \(T=O(s^4)\), \(M^2=O(s^4)\), \(\kappa=O(s^2)\),
and
\[
 G_a=\kappa E_a+\frac{128}{169}T+\frac{40}{2197}M^2
                          -K(\eta)E_a^2+o(E_a^2),
 \quad\rho_p^2/E_a=d_0^4q_\infty+o(1),
 \quad E_a=\sum|(a-z_j)^{-1}-(1+a)^{-1}|^2.                  \tag{16}
\]
Centering and normalization preserve the number of distinct phase
values. Theorem1 therefore gives
\(K(\eta)/q_\infty=p_8J\le p_8J_*\).
Dropping the nonnegative penalties in (16) rules out negative gaps
at every strictly smaller leading scale, as in the cited reduction.

For the reverse bound, the credited equality direction (3) is still
admissible. Normalize it to \(\eta_*\), fix \(\lambda>1\), and use
the actual boundary-root polynomials
\[
 s^2=\lambda\kappa d_0^4/K(\eta_*),\quad
 p_a(z)=(z-a)\prod_j(z+e^{is\eta_{*,j}}).
\]
They have at most four phases, \(T=M=0\), negative gap for all small
positive \(a-5/8\), and
\(\rho_p^2=\lambda B_*\kappa+O(\kappa^2)\). Taking
\(\lambda\downarrow1\) proves (15). The equality-chain argument in
(16), followed by (5), proves the near-sharp statements.

No effective cutoff, finite-radius crossing uniqueness, two-sided
analytic basin or exact endpoint sign is supplied. The collapse comparison
is \(128/13>8\), so its negative gaps are not first-power counterexamples.
The unrestricted five-to-eight-level maximum, full complex displacement
basin and full degree-nine first-power Tang--Zhang inequality remain
unresolved in this work.

## 6. Verification and trust

The standalone Python3.11 checker derives its own polynomial inputs.
The cover is untrusted domain data validated for complete closed coverage;
expected.json is only a complete regression record. Every sign coefficient
is regenerated. Thirty-seven full8x8 rational commutant projections check
the pinching independently of the weighted-cubic calculation, including
all polygon vertices, the five central collisions, all binary corner
types, varying generic profiles and the credited larger comparison.

Both normal and optimized runs must match. Missing cover/manifest,
omitted fan, missing closed child and altered coefficient/control records
are rejected under optimization. These are author checks, not independent
peer review or formalization. The spectral interpretation, support-count
argument, polygon completeness, cited cohort theorems and joint analytic
asymptotics are written proof bridges. See LITERATURE.md for exact sources
and attribution. No private data, external solver, floating proof input
or large proof corpus is required.
