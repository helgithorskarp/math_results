# A uniform all-threshold certificate near the finite isometry boundary

Author proof, 27 September 2026. Independent review and formalization are
pending. The unrestricted dimension-three Gaussian-majorisation problem
remains open.

The result is an explicit finite-configuration consequence of the accepted
[Procrustes identity](../gaussian_contraction_rigidity/PROOF.md), Section 6,
and its [independent review](../gaussian_contraction_rigidity_review1/REVIEW.md).
It upgrades a whole sector of small positive losses to **all thresholds and
all variances**, with arbitrary atom weights. The mechanism is a certified
straight contracting motion after rigid alignment. Continuous-contraction
comparison itself is prior work, not a new geometric principle.

## 1. Exact certificate

Let x_1,...,x_n be distinct points in R3 and let y_1,...,y_n satisfy

```
Delta_ij = |x_i-x_j|^2-|y_i-y_j|^2 >= 0.
```

Center each point list at its **unweighted** mean, and let A,B be the
n-by-3 matrices with the centered points as rows. Define

```
S=A^T A,    F=||AA^T-BB^T||_F^2,
delta=min_(i<j) Delta_ij.
```

**Theorem 1.** Suppose k>0 is a certified lower bound `S>=k I_3` and

```
                         k delta >= 4F.                    (1)
```

Then, after a rigid motion of the target list, straight interpolation is
a contracting motion in R3. Consequently, for **every** probability vector
`p_i>=0`, every Gaussian variance s>0 and every density threshold h>=0,

```
integral (sum_i p_i gamma_s(z-y_i)-h)_+ dz
 >= integral (sum_i p_i gamma_s(z-x_i)-h)_+ dz.             (2)
```

The weights need not have a positive lower bound and need not be specified
to the certificate. The same geometry also has the classical union and
intersection Kneser--Poulsen comparisons for arbitrary individual ball
radii. These are consequences of the known motion theorems.

If F=0, the lists are congruent and (2) is equality, even when S is singular.
Otherwise a failed guard, or a singular source, is **UNRESOLVED** here. No
negative hinge is inferred. Singular sources and many other failed inputs
have separate positive theorems that this narrowly scoped checker does not
attempt to reproduce.

### Proof

Choose an orthogonal Q so that `A^T BQ` is symmetric positive semidefinite,
by polar/SVD alignment, and put C=BQ, U=A+C, V=A-C. Orthogonal alignment
preserves `BB^T`. Direct expansion gives the accepted identity

```
F = (1/2) tr(U^T U V^T V) + (1/2) tr((U^T V)^2).         (3)
```

Here `U^T V=A^T A-C^T C` is symmetric, so the second term is nonnegative.
Furthermore

```
U^T U=A^T A+C^T C+2A^T C >= S >= k I.
```

Thus, writing v_i for the rows of V,

```
sum_i |v_i|^2 <= 2F/k,
|v_i-v_j|^2 <= 2(|v_i|^2+|v_j|^2) <= 4F/k <= Delta_ij.  (4)
```

This is where retaining the squared Gram error, rather than replacing it
by a first loss moment, is useful. For a pair put a=A_i-A_j and b=C_i-C_j.
Along straight interpolation its squared distance is
`d(t)=|(1-t)a+tb|^2`. Its derivative increases with t, and

```
d'(1)=|a-b|^2-(|a|^2-|b|^2) <= 0.                      (5)
```

It follows that d'(t)<=0 throughout [0,1]. This proves the simultaneous
motion, not merely endpoint contraction. Distinct source points cannot
collide before the last time: monotonicity would force their distance to
remain zero thereafter, contrary to its nonzero initial value and its
quadratic polynomial form.

Apply Aishwarya--Li [Theorem 1.4](https://arxiv.org/html/2609.07041v2)
to the finite measure and this analytic motion. Hinges are convex energy
densities, so (2) follows. Gaussian hinges are unchanged by the separate
translations and the orthogonal Q, including a reflection. We do not assert
that undoing a reflection is a motion in R3; it is unnecessary for the
comparison. The ball-volume conclusions likewise follow from the
classical [Bezdek--Connelly motion theorem](https://arxiv.org/abs/math/0108098)
by embedding the motion in R5, reversing it for expansion, and using
isometry invariance. Repeated target centers and zero radii are covered by
the usual endpoint limit; source duplicates can first be merged.

## 2. Uniform parameter families and quadratic localization

Let `epsilon=max_(i<j) Delta_ij`. The centering projection
`J=I-11^T/n` gives

```
AA^T-BB^T=-(1/2) J Delta J,
4F <= sum_(i,j) Delta_ij^2 <= n^2 epsilon^2.              (6)
```

Both sums here are over **ordered** pairs, including zero diagonal terms.
It is harmless to use n^2 instead of n(n-1).

**Corollary 2 (uniform finite cover).** Fix n, k>0 and 0<rho<=1.
Every real configuration pair satisfying

```
S>=k I,   rho epsilon<=Delta_ij<=epsilon for i!=j,
                         epsilon <= rho k/n^2             (7)
```

has (2) at every variance and threshold, for every probability vector.
For an unweighted covariance bound `S/n>=kappa I`, the last condition is
`epsilon<=rho kappa/n`. No enumeration of coordinates or weights is needed:
(6) proves (1) for the entire parameter domain (7). At epsilon=0 use
congruence. The conclusion includes positive losses tending to zero.

Equivalently, any failure of full Gaussian majorisation on a finite pair
with `S>=k I` must satisfy

```
       delta < 4F/k <= n^2 epsilon^2/k.                    (8)
```

This is a necessary condition on a hypothetical counterexample, not an
existence claim. At fixed n and positive scatter floor, as epsilon tends
to zero an unresolved adverse configuration must approach a partially
tight distance face **quadratically**: its smallest loss cannot stay a
fixed positive fraction of its largest loss. The formula locates the
remaining boundary; it does not sign that boundary.

## 3. The R3/R8 normalized small-loss sector

The geometric weights above are unweighted. To connect them to the spine,
let p_i>0 be the actual atom probabilities, and assume

```
|x_i-E_p X|<=R,    Cov_p(X)>=kappa I_3,
D=sum_(i,j) p_i p_j Delta_ij,
delta>=rho epsilon,    0<rho<=1.
```

For any direction v, minimizing a scalar quadratic over its center gives

```
v^T S v = min_a sum_i (v.x_i-a)^2
        >= min_a sum_i p_i(v.x_i-a)^2
        = v^T Cov_p(X) v.                                (9)
```

Hence k=kappa is valid, with **no atom-weight floor**. Also

```
3kappa <= tr Cov_p(X)
        = (1/2) sum_(i,j) p_i p_j |x_i-x_j|^2
        <= 2R^2 (1-sum_i p_i^2),
D >= rho epsilon (1-sum_i p_i^2)
  >= (3rho kappa/(2R^2)) epsilon.                       (10)
```

It follows from Corollary 2 that the sufficient mean-loss condition is

```
                D <= 3rho^2 kappa^2/(2R^2 n^2).           (11)
```

This is a theorem about all configurations and weights in the stated
parameter family, not an estimate from finite samples.

**Corollary 3 (a concrete shared frontier).** For at most 19 active atoms,

```
R<=1/2,  Cov_p(X)>=2^-15 I,  D<=2^-40,
Delta_ij >= (1/4) max_(a<b) Delta_ab  for every i<j        (12)
```

imply (2) for all thresholds **and all variances**. The zero-loss case is
included. The constant check reduces to `8*19^2<=3*2^10`, i.e.
`2888<=3072`. It is not claimed optimal. The argument applies after any
common rescaling, and once the geometric premise has been certified the
motion is independent of Gaussian variance.

The accepted R3 moving window has a tiny-loss remainder below its signed
thresholds. Condition (12) removes that whole remainder in this balanced
finite sector; it does not try to join the exposed-cloud tail formulas
whose failure was proved at graph6478. The balanced-loss hypothesis is a
material added premise. Neither the 19-atom number nor preservation of
source moments by a cubature says that arbitrary-law hinges have been
preserved. No conclusion for arbitrary diffuse laws or an atom budget
independent of approximation error is inferred.

## 4. A uniform full paired-rank control

The theorem is not restricted to the paired-rank-at-most-five cases. To
make the exact certificate interface nonvacuous, take the eight points

```
x=(u,v,w)/4,  (u,v,w) in {-1,1}^3,
z=(vw,uw,uv)/8,
y_t=(1-t)x+t z,             0<t<=1/128.                 (13)
```

Separate translations, rotations, reflections and common positive scales
may be added. This is a calibration of the certificate, not a claim of a
new geometric example or an exclusion from older motion classes.

Here S=I/2. Direct polynomial expansion yields

```
delta=t(4-3t)/8,
F=(27/8)t^2-(15/4)t^3+(75/64)t^4,
k delta-4F = t(4-219t+240t^2-75t^3)/16.                 (14)
```

The last factor is positive on [0,1/128]; for instance discard its positive
quadratic term and bound the two negative terms at 1/128. The checker also
reconstructs all 28 loss polynomials, their lower envelope, F, and the
positive Bernstein coefficients of the entire final interval. It does
not infer (14) or its sign from samples.

The six distinct Walsh characters `u,v,w,vw,uw,uv` are orthogonal on the
eight sign vectors. Thus the paired coordinates `(x,y_t)` have affine
rank six for every t>0. For uniform actual weights,
`D=3t/4-15t^2/32`, tending to zero with t. Arbitrary actual weights remain
covered by the motion. The guard also accepts independent endpoint frames:
the stored rational input reflects the first target coordinate and adds
an unrelated translation. Interpolation in those raw coordinates need not
contract; the proved alignment cannot be omitted.

## 5. Exact finite reduction and trust boundary

For rational sites, the entire guard consists of rational arithmetic:
all pair distances, the centered 3-by-3 scatter, seven principal minors of
`S-kI`, F, and the scalar inequality (1). A user can supply rational k>0;
the default `det(S)/tr(S)^2` is positive when S is positive definite and is
at most its least eigenvalue. The certificate verifies this lower bound
again, so the default formula is not an unchecked numerical estimate.

The producer uses centered coordinate Gram products. The separate record
checker uses doubly centered **distance losses** for F and ordered point
differences for S, and tests positive semidefiniteness by exact elimination.
Its supplied-record mode does not import the producer. Either implementation
uses O(n^2) rational operations; the producer streams Gram entries, while
the independent checker stores distance matrices and uses O(n^2) memory.
Rational bit complexity is not bounded uniformly. No solver, angular
quadrature, transcendental enclosure or private input is required.

The ordinary mathematical trust boundary is polar alignment, the trace
identity (3), matrix norm contraction by J, the derivative argument (5),
and the cited Gaussian/ball motion theorems. The exact program checks the
finite hypotheses and polynomial controls; it does not formalize those
analytic implications or constitute independent review. There is no
search-completeness claim beyond this sufficient guard and the explicitly
covered parameter domains. Unbalanced losses, unbounded atom count,
degenerating scatter and the unrestricted problem remain open here.
