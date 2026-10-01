# Complete five-level angular optimizer and sharp complex phase basin

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact rational continuous-domain
certificates; unformalized, independent review of this extension pending.

## 1. Statement and credited optimizer

For a balanced nonzero real eight-vector, max-normalize to
\(\max|\theta_j|=1\) and put
\[
 \mu_k=\sum_j\theta_j^k,\quad e=\mathbf1/\sqrt8,\quad P=I-ee^*,
 \quad C=P\operatorname{diag}(\theta)P|_{e^\perp},
 \quad w=\operatorname{diag}(\theta)e,
\]
\[
 \Psi=\sum_{\lambda\ {\rm distinct}}\|\Pi_\lambda w\|^4,\qquad
 J=122\mu_2+(224\mu_4-5760\Psi)/\mu_2.                     \tag{1}
\]
Use full eigenspace projections at collisions. The functional and its
polynomial interpretation are credited to the
[angular theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and its [independent audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md).
Let \(\mathcal F_5\) be the whole normalized class with at most five
actual coordinate values. Let \(M_m\) be the class admitting five positive
constant block labels of masses \(m_i\), allowing their values to coincide.

The [credited scalar theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_symmetric_displacement_face/PROOF.md)
defines
\[
 j(u)=\frac{2058+21912u-15876u^2+19224u^3+3402u^4}
                 {(3+u)(1+3u)^2},\qquad J_*=j(u_*),
\]
where \(u_*\in(2/25,9/100)\) is the unique global maximizing root of
\[
 26634-231084u-907290u^2+376920u^3
                    +971190u^4+224532u^5+30618u^6=0.       \tag{2}
\]
The actual vector
\[
 \theta_*=(1,1,1,-1,-1,-1,\sqrt{u_*},-\sqrt{u_*})           \tag{3}
\]
has \(J=J_*=785.7538723\ldots\). These values and the exact
[four-level classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_level_displacement/PROOF.md)
retain credit.

**Theorem 1.** Throughout \(\mathcal F_5\),
\[
 \boxed{J\le J_*},
\]
with equality exactly at permutations of (3). If \(\mathcal O_*\) is
the permutation orbit of \(\theta_*/\sqrt{6+2u_*}\), then
\[
 \boxed{\operatorname{dist}(\theta/\sqrt{\mu_2},\mathcal O_*)^2
                                         \le5000(J_*-J).} \tag{4}
\]
The constant 5000 is conservative. The stronger earlier four-level
stability estimate remains credited. No support-size reduction for
six-to-eight-level vectors is asserted.

The new statement closes the entire \(M_{3,2,1,1,1}\) class by a strict
rational/local cover. The
[preceding five-level multiplicity reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_five_level_moment_reduction/PROOF.md)
supplies
\[
 J\le750\text{ on }M_{2,2,2,1,1},\qquad
 J\le650\text{ on }M_{4,1,1,1,1}.                          \tag{5}
\]
These are exactly the other two positive five-part partitions of 8.
Every vector with fewer actual levels admits five positive labels by
splitting occupied blocks without changing their values. Thus all
collisions and the whole support-size class are covered by these
three patterns. The candidate (3) belongs to the remaining pattern
after splitting one triple into a double and a singleton.

## 2. Imported local theorem and strict rational target

The [unrestricted local theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_unrestricted_local_displacement/PROOF.md),
source 7445cf7e90a84b0405deec226b5e21d90b842ee5, graph7823, is an explicit
mathematical input. For a relabelled vector write
\[
 S=\sum_{i=1}^3(1-\theta_i)+
                      \sum_{i=4}^6(1+\theta_i),\qquad
 x=(\theta_7-\theta_8)/2,\qquad r=x^2.
\]
Its hypotheses are balance, max norm 1,
\[
 0\le S\le1/100000,\qquad x\ge0,\qquad 2/25\le r\le9/100,
                                                               \tag{6}
\]
without any coordinate equality or multiplicity assumption. It proves
\[
 J_*-J\ge200S+450(r-u_*)^2,\qquad
 \operatorname{dist}(\theta/\sqrt{\mu_2},\mathcal O_*)^2
                                           \le(J_*-J)/90. \tag{7}
\]
Equality \(J=J_*\) forces (3) in that chart. We do not claim the
local theorem again; its source gives the analytic upper support,
full-gradient identity and explicit Hessian bound.

Use the rational strict threshold
\[
 c=785753/1000.
\]
An exact comparison from the credited scalar formula is
\[
 j(87/1000)=\frac{642838752906487}{818117254500},\qquad
 j(87/1000)-c=\frac{1331662697}{1636234509000}>\frac1{1250}.
                                                               \tag{8}
\]
Since \(J_*\ge j(87/1000)\), (8) proves \(c<J_*\) and supplies the
strict margin needed in (4). No approximate algebraic-root value or
floating rounding is a sign premise.

The new certificate proves \(J\le c\) on every region except eight
closed boxes. Section4 proves that every one of those boxes belongs to
(6). This supplies the complete global bridge missing from local
strictness alone.

## 3. Gram inequalities and exhaustive charts

The [preceding active-Gram theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_five_level_displacement_bound/PROOF.md),
source 74b263681ab01976993d64bafe3733caf62f7b5b, graph8084, supplies
the following spectral and geometric mechanism. We repeat the main
identities to specify exactly what the new source certifies.

The balanced labeled block space \(A\) has dimension 4 and contains w.
Within-block difference spaces outside A have zero w-weight. Let
\[
 s_0=4,\quad s_r=\operatorname{tr}C_A^r
            =\operatorname{tr}C^r-\sum_i(m_i-1)t_i^r\quad(r\ge1),
\]
\[
 b=(\mu_2/8,\ \mu_3/8,\ \mu_4/8-\mu_2^2/64,\
                         \mu_5/8-\mu_2\mu_3/32).
\]
For \(k=3,4\) form \(G_k=(s_{i+j})_{0\le i,j<k}\),
\(D_k=\det G_k\), \(N_k=b^T\operatorname{adj}(G_k)b\), truncating b
for k=3. Frobenius projection onto \(I_A,C_A,\ldots,C_A^{k-1}\) gives
\(\Psi\ge N_k/D_k\) when \(D_k>0\). For k=4 and four distinct active
eigenvalues it is equality. The exact polynomial targets are
\[
 F_k=(c\mu_2-122\mu_2^2-224\mu_4)D_k+5760N_k.              \tag{9}
\]
The dimension bound \(\Psi\ge\mu_2^2/256\) gives the alternative
\[
 J\le199\mu_2/2+224,\qquad
                       2(c-224)-199\mu_2\ge0.             \tag{10}
\]

The active characteristic is \(Q/8\), where
\[
 H=\prod_i(\lambda-t_i)^{m_i},\quad
 R=\prod_i(\lambda-t_i)^{m_i-1},\quad
 Q=\sum_i m_i\prod_{j\ne i}(\lambda-t_j),\quad H'=RQ.
\]
Strict secular interlacing gives \(D_4,D_3>0\) when the five labels
are distinct. The determinant \(D_4\) is conceptually
\(\operatorname{Disc}(Q)/8^6\); no separate computed discriminant
formula is claimed. Trace words through 6, b through 3, Newton
recurrences, adjugates and (9) are regenerated exactly by verify.py.

For clarity the six complete cube charts use \(X,Y,Z\in[0,1]\).
Reflection makes a saturated label \(-1\). Only equal-mass labels
are ordered. Three saturation masses 3,2,1 exhaust the cohort.

For triple and double saturation, write the three singleton levels
as \(1-\beta_i\), with \(0\le\beta_1\le\beta_2\le\beta_3\le2\).
Define
\[
 C_s=(s/3)^3,\quad A_s=(0,0,s),\quad B_s=(0,s/2,s/2),
\]
\[
 D_s=((s-2)/2,(s-2)/2,2),\quad E_s=(0,s-2,2),
\quad \beta=C_s+Y[(1-Z)U+ZV-C_s].                         \tag{11}
\]
The notation \((s/3)^3\) means three repeated coordinates.
For \(0\le s\le2\) the entire ordered section is triangle C,A,B.
For \(2\le s\le4\) it is quadrilateral C,D,E,B, covered by
triangles C,D,E and C,E,B, including degenerate sections at the ends.
The previous source proves these sections and closed inverses.

| Chart | Masses | Parameters and labels |
|---|---|---|
| triple | 3,2,1,1,1 | s=2X, U=A,V=B; (-1,X,1-beta1,1-beta2,1-beta3) |
| double0 | 2,3,1,1,1 | s=2X, U=A,V=B; (-1,(s-1)/3,1-beta1,1-beta2,1-beta3) |
| double1 | 2,3,1,1,1 | s=2+2X, U=D,V=E; same double labels |
| double2 | 2,3,1,1,1 | s=2+2X, U=E,V=B; same double labels |
| singleton0 | 1,3,2,1,1 | (-1,(-3+2X+4Y)/3,1-2Y,1-X+XZ,1-X-XZ) |
| singleton1 | 1,3,2,1,1 | (-1,(1-2X+(2+2X)Y)/3,1-(1+X)Y,-1+X(1+Z),-1+X(1-Z)) |

For singleton saturation q=3t1+2t2 lies in [-1,3], t1 lies between
(q-2)/3 and min(1,(q+2)/3), and the remaining singleton difference
half-width lies in [0,1-|1-q|/2]. Splitting at q=1 yields its two
listed full cubes. These identities and the closed inverses retain
their earlier proof and are checked in the new standalone source.
Every pairwise level difference is a nonzero polynomial, so generic
five-distinct-label profiles are dense in each cube.

## 4. Eight exact local relabelings and the complete strict cover

Write the chart levels as \(t_0=-1,t_1,t_2,t_3,t_4\). The following
explicit permutations put the four relevant charts into the local
coordinates of Section2:

| Chart | Canonical eight-vector, before evaluation | S | x |
|---|---|---|---|
| triple | (t1,t1,t2,-1,-1,-1,t3,t4) | 2(1-X)+(2X/3)(1-Y) | XY(1-Z) |
| double1 | (t1,t1,t1,-1,-1,t4,t2,t3) | 2(1-X)+((4-2X)/3)(1-Y) | XYZ |
| singleton0 | (t1,t1,t1,-1,t2,t2,t3,t4) | 2(1-X)+8(1-Y) | XZ |
| singleton1 | same canonical pattern | 2(1-X)+4(1+X)(1-Y) | XZ |

The source checks the polynomial multiset permutation with full
multiplicities and both S/x identities exactly. Balance, max norm 1,
nonnegative normal deficits and x>=0 follow from the whole physical
cube and equal-mass ordering. They do not depend on testing sample points.

The eight local leaves have common \(X\in[1-2^{-19},1]\).
In triple/double1 they have \(Y\in[1-2^{-17},1]\); in singleton0/1
they have \(Y\in[1-2^{-21},1]\). Each row has two adjacent Z intervals:

| Chart | First Z interval | Second Z interval | Certified S upper bound |
|---|---|---|---|
| triple | [45/64,361/512] | [361/512,723/1024] | 7/786432 |
| double1 | [301/1024,151/512] | [151/512,19/64] | 305835/34359738368 |
| singleton0 | [301/1024,151/512] | [151/512,19/64] | 1/131072 |
| singleton1 | [301/1024,151/512] | [151/512,19/64] | 1/131072 |

All S bounds are at most 1/100000. Exact endpoint products give
\(2/25\le x^2\le9/100\) on every entire box. For example, on triple,
with coordinate endpoints \(X_l,X_h,Y_l,Y_h,Z_l,Z_h\), use
\[
 S\le2(1-X_l)+(2X_h/3)(1-Y_l),\quad
 (X_lY_l(1-Z_h))^2\le r\le(X_hY_h(1-Z_l))^2.
\]
The other rows use the corresponding nonnegative factors in the table.
Every complete bound is stored in expected.json and recomputed.
Thus all eight boxes satisfy every hypothesis in (6), including their
closed faces. This is a universal relabeling/domain-membership proof.

The complete cover has the following closed leaves:

| Chart | Four-moment | Three-moment | Dimension/moment | Local | Total |
|---|---:|---:|---:|---:|---:|
| triple | 54 | 16 | 5 | 2 | 77 |
| double0 | 0 | 0 | 1 | 0 | 1 |
| double1 | 55 | 13 | 4 | 2 | 74 |
| double2 | 1 | 0 | 1 | 0 | 2 |
| singleton0 | 54 | 20 | 8 | 2 | 84 |
| singleton1 | 54 | 20 | 7 | 2 | 83 |
| Total | 218 | 69 | 26 | 8 | 321 |

On four-moment leaves, the chart pullbacks of F4,D4 are both divisible
by X²Y² (triple/double0), Y² (double1/2), X² (singleton1),
or no factor (singleton0). Divisibility and multiplication back are
checked. Nonnegative reduced F4 implies original F4>=0 without
evaluating a singular quotient. Three-moment leaves use full F3;
dimension leaves use (10).

Every tensor Bernstein coefficient on each **closed** leaf is
nonnegative, checked with exact rational arithmetic. Their total is
877,791. The full physical/order certificates add 320 entries.
Binary midpoint splitting includes both closed children at every
node; all child volumes sum exactly to the parent volume. All six
charts are independently required. The maximum depth is 50.
The source regenerates all initial polynomial arrays, verifies inverse
Bernstein conversion, 147 subdivision basis identities, and 15 whole
leaf arrays via separate direct affine substitution.

For distinct labels, positive Gram determinants imply J<=c by
(9) or (10). The spectral collision bridge is the one proved in the
preceding Gram source: if Hermitian matrices and vectors converge,
split spectral-cluster weights obey sum weight²<=(sum weight)² and
the total projections converge. Therefore limsupPsi_n<=Psi_limit,
and J_limit<=liminfJ_n. Applying this to dense generic profiles
in every closed strict leaf extends J<=c to all its collisions.
Local leaves use (7) directly and already allow every collision.
No determinant is divided by at zero. Consequently every cube
profile either has J<=c or lies in the proved local chart.

This proves J<=J* on the entire remaining labeled class. Equations
(5) and positive five-part completeness prove it throughout F5.
Equality can occur only in a local leaf, where (7) forces (3).
The candidate attains it, so this is an exact maximum.

For (4), on strict leaves and the two excluded cohorts, (8) gives
J*-J>1/1250, while the squared distance between unit vectors is
at most4. Hence dist²<5000(J*-J). Local leaves have the stronger
bound 1/90 in (7). This proves the global estimate.

## 5. Sharp complex five-phase displacement basin

Let \(p(z)=b(z-a)\prod_{j=1}^8(z-z_j)\), \(b\ne0\), have simple
marked real root \(0<a<1\) and \(|z_j|\le1\). All other original
and critical multiplicities are allowed and counted. Put
\[
 G_a=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16/(1+a),\quad
 \rho_p=\max_j|z_j+1|,\quad \kappa=(1+a)(a-5/8),\quad d_0=13/8.
\]
For \(\rho_p\le1/2\), uniquely write
\(z_j=-(1-\tau_j)e^{i\phi_j}\), \(\tau_j\ge0\), with small
principal real phases. Require **at most five original phase values**.
The depths vary independently even within phase blocks; coefficients
may be complex. Let R5(a) be the supremum of radii r in [0,1/2]
such that every polynomial in this class with rho<=r has G_a>=0.
Endpoint admissibility is not assumed.

**Corollary 2.** The entire class has the sharp leading basin
\[
 \boxed{\lim_{a\downarrow5/8}\frac{R_5(a)^2}{\kappa}
                  =B_*=\frac{106496}{5J_*},\qquad
                        27.106707<B_*<27.106708.}         \tag{12}
\]
The scalar constant and four-phase matching family are credited.
The new conclusion is their sharp validity across every five-phase
multiplicity pattern and arbitrary inward depths.

The analytic inputs are the
[joint all-disk bootstrap/expansion](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md)
and the
[original-root variational reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_displacement_variational_basin/PROOF.md).
Set
\[
 T=\sum\tau_j,\ M=\sum\phi_j,\ s=\|\phi-(M/8)\mathbf1\|,\
 \eta=(\phi-(M/8)\mathbf1)/s,\ q=\max\eta_j^2,\ p_8=10985/33554432.
\]
They give, uniformly on negative-gap sequences with a decreasing
to 5/8 and rho tending to zero,
\[
 s>0,\quad T=O(s^4),\quad M^2=O(s^4),\quad\kappa=O(s^2),
\]
\[
 G_a=\kappa E+\frac{128}{169}T+\frac{40}{2197}M^2
                           -K(\eta)E^2+o(E^2),\qquad
 E=\sum|(a-z_j)^{-1}-(1+a)^{-1}|^2,
\]
\[
 \rho_p^2/E=d_0^4q+o(1),\quad K(\eta)/q=p_8J(\eta/\sqrt q),
 \quad q\ge1/8,\quad d_0^4/p_8=106496/5.                  \tag{13}
\]
Centering and normalization preserve phase support size. Theorem1
therefore bounds K/q by p8J*. Dropping the nonnegative penalties
in (13) rules out negative gaps at every squared radius
\((B_*-\epsilon)\kappa\), with \(0<\epsilon<B_*\), for sufficiently
small positive a-5/8. This proves the liminf bound exactly as in the
credited metric reduction. Displacement zero has G=0.

For the limsup, the four-phase class is contained in this class,
so R5<=R4. The credited sharp four-phase limit in the complete
four-level source proves the reverse bound. Equivalently its actual
boundary-root ray in the unit-normalized direction (3), with
\(s^2=\lambda\kappa d_0^4/K(\eta_*)\), \(\lambda>1\), has
negative G and squared displacement \(\lambda B_*\kappa+o(\kappa)\).
It still has at most five phases. Taking lambda down to1 proves (12).

**Corollary 3.** On negative-gap sequences in this five-phase class
with \(a\downarrow5/8\) and \(\rho_p^2/\kappa\to B_*\),
\[
 T/E^2\to0,\quad M^2/E^2\to0,\quad
 \operatorname{dist}(\eta,\mathcal O_*)\to0,\quad G_a/E^2\to0.
                                                               \tag{14}
\]
Indeed the normalized expansion becomes
\[
 G_a/E^2=p_8q(J_*-J(\eta/\sqrt q))+
               \frac{128}{169}T/E^2+\frac{40}{2197}M^2/E^2+o(1).
\]
Every displayed term is nonnegative. Negativity forces all to zero;
q>=1/8 and (4) give the direction conclusion. This proves (14).
The geometry uses the new whole-five-level classification rather
than assuming every near-sharp sequence has four phase levels.

No effective cutoff, finite-radius crossing theorem or endpoint
sign is supplied. The collapsed comparison is 128/13>8 at the
threshold, so these negative gaps are not first-power counterexamples.
Six-to-eight-level displacement optimization and the unrestricted
degree-nine first-power Tang--Zhang endpoint remain unresolved here.

## 6. Exact source and trust boundary

The standalone standard-library checker regenerates every polynomial
and sign. It validates the new complete trees and all imported-local
hypotheses, then compares a compact record that hashes every complete
leaf record and coefficient array. All expected counts and hashes are
in [README.md](README.md). Physical-domain completeness, Frobenius
projection, collision semicontinuity, the prior two-cohort exclusions,
the imported local theorem and uniform analytic basin statements
are ordinary mathematics outside a formal proof kernel.

Source code openly adapts the preceding Gram kernel. Full8x8 symbolic
trace/b identities, all Newton recurrences, exact adjugates, 19 distinct
full defining-commutant profiles, nine raw quotient controls and 60
closed inverse round trips are author checks; they do not constitute
independent review. Floating exploration only proposed the trees.
All accepted coefficients and whole-box local guards use exact
fractions. No private input, campaign import, numerical proof premise,
external solver or large coefficient corpus is needed. Exact source
commits, graph references and precise review boundaries are recorded
in [LITERATURE.md](LITERATURE.md).
