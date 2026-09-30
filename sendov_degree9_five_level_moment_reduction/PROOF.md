# Five-level multiplicity reduction by an active-compression moment bound

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Complete ordinary author proof with exact rational continuous-domain
certificates; independent review of this extension is pending.

## 1. Statements and attribution

For a real eight-vector with sum theta=0 and max|theta|=1, put
\[
 \mu_k=\sum\theta_j^k,\quad e=\mathbf1/\sqrt8,\quad P=I-ee^*,
 \quad C=P\operatorname{diag}(\theta)P|_{e^\perp},
 \quad w=\operatorname{diag}(\theta)e,
\]
\[
 \Psi=\sum_{\lambda\text{ distinct}}\|\Pi_\lambda w\|^4,
 \qquad J=122\mu_2+(224\mu_4-5760\Psi)/\mu_2.                 \tag{1}
\]
Full projections are used at collisions. The functional, polynomial
interpretation and continuity are credited to the
[angular theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and its [independent audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md).
Let M_m denote the closed class admitting constant positive blocks of
sizes m_i, allowing equal-valued labels and coordinate permutations.

**Theorem 1.** Throughout the entire classes,
\[
 \boxed{J\le750\text{ on }M_{2,2,2,1,1},\qquad
        J\le650\text{ on }M_{4,1,1,1,1}.}                     \tag{2}
\]
These are sufficient bounds, not exact cohort maxima. Arbitrary
asymmetry, saturation choices and all collisions are included.

**Corollary 2.** For the whole balanced max-normalized class F5 with
at most five actual levels,
\[
 \boxed{\sup_{F5}J=\sup_{M_{3,2,1,1,1}}J.}                  \tag{3}
\]
Every member of F5 with J>750 admits the remaining3+2+1+1+1
representation. The remaining value is not proved here. No reduction
of arbitrary six-to-eight-level vectors is asserted. Credited continuity
also gives maxima on the compact normalized sets; the supremum equality
itself does not require continuity.

This improves three collision rows of the
[complete four-level classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_level_displacement/PROOF.md):
\[
 J\le750\text{ in }3+2+2+1,\qquad
 J\le650\text{ in }4+2+1+1\text{ and }5+1+1+1.               \tag{4}
\]
The scalar optimizer and its value retain their earlier attribution.

## 2. Uniform active-block moment lemma

Represent theta with positive masses m_i summing8 and levels t_i, even
when labels coincide. Let S_B project orthogonally onto the block-constant
space and U=S_B-ee* onto its balanced part. Extend C=PDP by zero on e,
where D=diag(theta). Then U commutes with C, Uw=w, and Z=U-C^2U is
symmetric and commutes with C. Define
\[
 A=\mu_2^2+8\mu_2-8\mu_4,
\]
\[
 B=\mu_2^2-48\mu_2+16\mu_4+224
                       -32\sum_i(m_i-1)(1-t_i^2)^2.           \tag{5}
\]
Then
\[
 \boxed{B>0,\qquad\Psi\ge A^2/(128B),\qquad
 J\le122\mu_2+224\mu_4/\mu_2-45A^2/(\mu_2B).}              \tag{6}
\]

Indeed, the within-block difference spaces have eigenvalue t_i and
zero w-weight. The rank-one projection expansion gives
\[
 \operatorname{tr}C^2=3\mu_2/4,\qquad
 \operatorname{tr}C^4=\mu_4/2+\mu_2^2/32.                    \tag{7}
\]
Before imposing mu1=0, the fourth trace is
\[
 \mu_4/2+\mu_1\mu_3/16+\mu_2^2/32
                  -\mu_1^2\mu_2/128+\mu_1^4/4096.
\]
Expand the four factors D(I-ee*): every selection of rank-one factors
contributes a product of the cyclic gap moments. The checker derives
all word coefficients and verifies (7) separately through full8x8
polynomial compression. Subtracting the known difference spaces from
tr(P-C^2)^2 yields
\[
 \operatorname{tr}Z^2=7-3\mu_2/2+\mu_4/2+\mu_2^2/32
                -\sum_i(m_i-1)(1-t_i^2)^2=B/32.              \tag{8}
\]
Additional zero-weight modes may remain inside U at collisions; leaving
them in the denominator preserves the inequality.

Since w is perpendicular to e,
\[
 \|w\|^2=\mu_2/8,\qquad
 \|Cw\|^2=\|PD^2e\|^2=\mu_4/8-\mu_2^2/64,
 \qquad\operatorname{tr}(ww^*Z)=A/64>0.                     \tag{9}
\]
The sign follows from mu4<=mu2 and mu2>0. Thus Z is nonzero and B>0
even at collisions. Let T=sum Pi_lambda ww* Pi_lambda be spectral
pinching. Each block is rank one, so ||T||_F^2=Psi. Commutation implies
tr(TZ)=tr(ww*Z). Frobenius Cauchy--Schwarz gives
Psi>=(A/64)^2/(B/32), and substituting in (1) proves (6).
No secular discriminant or singular spectral division is needed.
The tools are classical; the specific cohort bounds and reduction are
the present application.

For target c it remains to prove the polynomial inequality
\[
 F_c=(c\mu_2-122\mu_2^2-224\mu_4)B+45A^2\ge0,              \tag{10}
\]
whose denominator mu2 B is strictly positive.

## 3. Exhaustive closed cube charts

Reflection and coordinate permutations preserve J. Only equal-mass
labels are ordered. Reflect a saturated label to-1.

For a saturated double in2+2+2+1+1, order the other doubles a>=b and
singles d>=f. Set s=a+b, h=a-b, v=(d-f)/2. Balance gives their single
mean1-s. The full constraints are exactly
\[
 0\le s\le2,\quad0\le h\le2-s,\quad
                            0\le v\le\min(s,2-s).           \tag{11}
\]
On two full cubes (r,u,q) in[0,1]^3 with i=0,1, use
\[
 s=r+i,\ h=(2-s)u,\quad
 v=sq\ (i=0),\quad v=(2-s)q\ (i=1),
\]
\[
 a=(s+h)/2,\ b=(s-h)/2,\ d=1-s+v,\ f=1-s-v.               \tag{12}
\]
These include s=0,1,2 and all collisions. The inverse uses u=h/(2-s)
and q=v/min(s,2-s) for positive widths; a zero-width coordinate can be
set to zero. These constraints follow from the largest double and both
single bounds and conversely imply every level lies in[-1,1].

For a saturated single, order the three doubles a>=b>=d. With the
remaining single f, set s=a+b+d=(1-f)/2 in[0,1]. The exact constraints are
\[
 s/3\le a\le1,\quad (s-a)/2\le b\le\min(a,s-a+1),\quad d=s-a-b.\tag{13}
\]
The upper endpoint for b changes at a=(s+1)/2. Two full cubes give
\[
 a=s/3+(s+3)u/6,\quad b=(s-a)/2+(3a-s)q/2                  \tag{14a}
\]
and
\[
 a=(s+1)/2+(1-s)u/2,\quad b=(s-a)/2+(s-a+2)q/2.            \tag{14b}
\]
In both d=s-a-b and f=1-2s. Every ordered section in (13) is covered.
When widths vanish their inverse coordinates can be zero; this includes
the equal-triple face and the s=1 collapsed second interval. All four
closed cubes are required.

In4+1+1+1+1, a saturated mass4 forces the four singles to the opposite
value. Thus a saturated singleton can always be chosen and reflected
to-1. The other three single levels x,y,z range independently over[-1,1],
with heavy level
\[
 b=(1-x-y-z)/4\in[-1/2,1].                                 \tag{15}
\]
Using x=2r-1,y=2u-1,z=2q-1 gives one full cube. Its corner includes the
saturated-heavy binary profile. No separate missing face is excluded.

## 4. Exact continuous certificates

The standalone source derives (10) from three raw affine balance charts
over Q[x,y,z]. On each mapped cube it checks balance and substitution.
It regenerates238 nonnegative Bernstein coefficients for every \(1\pm t_i\)
and applicable equal-mass ordering difference. This validates the images;
the section argument above proves exhaustive coverage.

Each bound polynomial has degree at most8 in each cube variable. Its
complete closed bisection tree has these leaves and coefficients:

| Chart | Target | Closed leaves | Bound coefficients |
|---|---:|---:|---:|
| double0 | 750 | 2 | 1458 |
| double1 | 750 | 2 | 1458 |
| singleton0 | 750 | 1 | 729 |
| singleton1 | 750 | 2 | 1458 |
| heavy4 | 650 | 4 | 2916 |

All8019 coefficients are regenerated and nonnegative. The tensor
Bernstein basis is nonnegative and sums to one, proving (10) on every
continuous closed leaf. Each affine and inverse basis reconstruction is
checked. Cover data supplies only bisection trees: all five hardcoded
charts, both closed children of every split, and total volume1 are
required. Missing/extra cubes and omitted children reject.

Three raw full8x8 polynomial compressions check the projectors, block
invariance, second/fourth traces and both test-matrix traces. Twenty-four
distinct normalized cohort profiles, including all cube corners and
generic profiles, use exact Frobenius projection of ww* onto the full
symmetric commutant. This is a different route from the moment minorant.
A25th profile is the credited larger comparison below. Fifty-five closed
inverse-chart round trips include every corner and vanishing-width face.
Permutation-equivalent profiles share their defining pinching computation;
all references and distinct weighted denominators remain in the record.
These controls supplement the continuous proof and its written bridges.

## 5. The reduction and collision rows

The three positive five-part partitions of8 are4+1+1+1+1,3+2+1+1+1,
and2+2+2+1+1. Every lower-support vector can be represented by five
positive labels, splitting occupied blocks without changing their value.
Eight coordinates ensure this can continue until five labels exist.
Thus these closed classes exhaust F5.

The credited comparison theta=(1,1,1,-1,-1,-1,1/3,-1/3) admits
3+2+1+1+1 labels. Its active weights at0,+-1/sqrt3 are1/3,2/9,2/9,
so Psi=17/81 and J=5472/7>750, as in the
[credited scalar face](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_symmetric_displacement_face/PROOF.md).
The source reproduces its defining pinching and value. Neither excluded
cohort can contribute to the full supremum or a sequence tending to it,
proving (3). No global value follows for the remaining class.

Merging2+1 in2+2+2+1+1 produces3+2+2+1. In4+1+1+1+1,
merging two singletons produces4+2+1+1 and merging a singleton with the
heavy block produces5+1+1+1. The collision-inclusive theorem proves (4).

## 6. Complex original-phase displacement lower basins

For complex degree-nine disk-root polynomials with simple marked real
root0<a<1, write z_j=-(1-tau_j) exp(i phi_j) near-1. Require phase
blocks of sizes m, allowing equal phase labels and independent inward
depths within every block. Let
\[
 G=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16/(1+a),\quad
 \rho=\max|z_j+1|\le1/2,\quad\kappa=(1+a)(a-5/8).
\]
Critical multiplicities count; arbitrary complex coefficients and repeated
other roots are allowed. A radius r is sufficient when G>=0 for every
admissible polynomial in this class with rho<=r. Define R_m(a) as the
supremum of these universal sufficient radii in[0,1/2].
The credited [joint expansion](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md)
and [variational reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_displacement_variational_basin/PROOF.md)
give on negative-gap sequences, for centered unit phase direction eta,
q_infinity=max eta_j^2 and p8=10985/33554432,
\[
 G=\kappa E+(128/169)T+(40/2197)M^2-K(\eta)E^2+o(E^2),
 \quad\rho^2/E=(13/8)^4q_\infty+o(1),\quad
 K(\eta)/q_\infty=p_8J.
\]
Here E=sum|(a-z_j)^-1-(1+a)^-1|^2, T=sum tau_j, M=sum phi_j.
Their uniform bootstrap includes moving directions and collisions.
Centering and normalization preserve the phase-block representation.
Theorem1 and the nonnegative penalties therefore give
\[
 \boxed{\liminf_{a\downarrow5/8}R_{2,2,2,1,1}(a)^2/\kappa
                     \ge53248/1875,\qquad
 \liminf_{a\downarrow5/8}R_{4,1,1,1,1}(a)^2/\kappa
                     \ge4096/125.}                         \tag{16}
\]
The normalization is(13/8)^4/p8=106496/5. To see uniform sufficiency,
suppose negative gaps occurred along a sequence with rho^2<=beta kappa,
where beta is strictly less than106496/(5c) and c is the corresponding
bound750 or650. The cited negative-gap bootstrap gives E>0 and
kappa/E<=K(eta)+o(1). Its displacement identity and q_infinity>=1/8
give a positive lower bound for kappa/E along this sequence. Consequently
rho^2/kappa>=(13/8)^4/(p8 c)+o(1), contradicting its assumed strict
upper scale. Every strictly smaller leading squared radius is therefore
uniformly sufficient. These are lower bounds, not sharp constants or matching
failures. No effective cutoff, endpoint admissibility or finite-radius
crossing statement is supplied. Since the collapse comparison128/13>8,
negativeG is not a first-power counterexample. The remaining five-level
maximum, unrestricted displacement optimum and full first-power endpoint
remain unproved here.

## 7. Trust

The source uses CPython3.11 exact rational arithmetic. The cover supplies
no polynomial or sign oracle; expected.json is regenerated regression
data. Normal and optimized runs must agree; omitted/malformed cubes,
missing children and absent required files reject. The projection
inequality, exhaustive section charts, label-splitting argument and cited
analytic asymptotics remain written proofs outside a formal kernel.
Author checks are not independent review. See README.md for commands and
LITERATURE.md for precise attribution and complementary scopes.
