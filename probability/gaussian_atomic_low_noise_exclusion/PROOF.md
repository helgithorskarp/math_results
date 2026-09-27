# Every finite contraction has an eventual polynomial-degree exclusion

Complete author proof; independent review and historical-priority assessment
are pending. The full dimension-three Gaussian-majorisation question remains
open. This theorem signs each complete finite Hankel matrix at sufficiently
small noise, including configurations with tight nearest pairs or colliding
targets. It does not sign every hinge at one fixed variance.

## 1. Statement and meaning for the counterexample search

Let `x_i,y_i in R3`, `1<=i<=N`, with distinct source sites and

    |y_i-y_j| <= |x_i-x_j|.

Repeated source sites can first be combined, since their images coincide.
Use common positive weights `w_i`, summing to one. Write

    ell_ij=|x_i-x_j|^2-|y_i-y_j|^2,
    E={(i,j): i<j, ell_ij>0}.

For variance `s>0`, use the standard normalization

    C=(2pi s)^(-3/2), f=sum_i w_i gamma_s(.-x_i),
    g=sum_i w_i gamma_s(.-y_i), F=f/C, G=g/C,
    d_m=C integral(G^m-F^m),
    a_j=d_(j+2)/[(j+1)(j+2)], H_D=(a_(i+j))_(i,j=0)^D.

**Theorem 1 (all finite contractions).** If `E` is empty, every `H_D` is
zero at every variance. Otherwise, for each fixed integer `D>=1`, there is
an explicit `s_D>0` such that `H_D` is positive definite for all `0<s<=s_D`.
This includes every target equality pattern, arbitrary positive priors and
paired affine rank six. The polynomial coefficients may depend on variance.

Here are uniform quantitative versions. Choose an integer `b>=1` with
`w_i>=2^(-b)` and put `p=2^(-b)`.

**A. Distinct targets.** Set

    beta=min_((i,j) in E) min(|y_i-y_j|^2, ell_ij)>0,
    M=2D+2, K_D=8D(D+1)(2D+1),
    L_(D,b)=M b+ceil(log_2(2D)).

If `beta/s >= K_D L_(D,b)`, then

    H_D >= (1/2) diag(a_0,a_2,...,a_(2D)) >0.             (1)

Every nearest target pair may be tight. No lower bound is imposed on the
distances of tight pairs, and there is no upper support-radius bound.

**B. Colliding targets.** If at least two target sites coincide, let `delta`
be the minimum **positive** squared distance in either endpoint cloud.
The source sites are distinct, so this minimum exists and is positive.
If `delta/s >=108bD`, then

    H_D >= lambda_(D,b) I >0,
    lambda_(D,b)=p^(2D+2)/[512(D+1)(2D+1)20^(2D)].         (2)

These bounds are sufficient, not optimal. They cover whole classes defined
by the indicated floors, rather than neighborhoods of particular examples.

For a nonzero polynomial `P(t)=sum_(i=0)^D v_i t^i`, define

    U_P(t)=integral_0^t (t-u)P(u)^2 du,
    V_P(rho)=C U_P(rho/C).

The actual target-minus-source energy gap equals `v^T H_D v`. Thus the
theorem excludes every curvature-square witness of root degree at most D,
and every non-affine polynomial convex on the entire real line, vanishing
at zero, of energy degree at most `2D+2`. The latter statement follows
because a nonnegative real univariate polynomial is a sum of two polynomial
squares. We do not include all polynomials convex only on the attained
density interval under this bounded-degree assertion.

In particular, the earlier nearest-pair hypothesis is not an escape route
for fixed-degree small-noise counterexamples. Target collisions are not an
escape route either. The unresolved options include moderate noise, growing
degree, or data/weights degenerating with noise. There is no uniform theorem
over diffuse laws or mass floors tending to zero here.

## 2. The least nonzero replica interaction

The classical Gaussian product identity gives

    a_(m-2)=c_m E[exp(-S_y/(2ms))-exp(-S_x/(2ms))],
    c_m=1/[m^(5/2)(m-1)],
    S_z=sum_(r<t)|z_(I_r)-z_(I_t)|^2,                    (3)

where the labels are iid of law w. Every difference in (3) is nonnegative.
A tuple contributes if and only if its support contains a pair in E.
Call such a tuple active. Tuples without an active pair cancel exactly,
even if their target scatter is much smaller than every active scatter.

For a count vector `n` with total m, write

    S_y(n)=sum_(i<j)n_i n_j |y_i-y_j|^2
          =m sum_i n_i |y_i|^2-|sum_i n_i y_i|^2.          (4)

For fixed m this is a concave function of the real count vector. Fix an
active pair `(i,j)` and impose `n_i,n_j>=1`, all other counts nonnegative,
and total m. The resulting simplex has vertices

    n=e_i+e_j+(m-2)e_k.

Every point of the simplex is a convex combination of its vertices, so its
value is at least the minimum vertex value. Those vertices are integral and
active. Consequently the exact minimum
active target exponent, for every integer `m>=2`, is

    E_m=min_((i,j) in E, k)
        [c+(m-2)(a+d)]/(2m),                            (5)
    c=|y_i-y_j|^2, a=|y_i-y_k|^2, d=|y_j-y_k|^2.

This equality concerns all active tuples, not a selected collection of
replicas. For m=2 it has the same interpretation with no copies of k.

There is a crucial geometric restriction on the branches in (5).

* If `a+d>=c`, the branch is no smaller than `(m-1)c/(2m)`, obtained by
  taking k=i or k=j for the same active pair.
* If `a+d<c` and `(i,k)` is active, the branch is no smaller than the
  two-label branch `(m-1)a/(2m)`. Indeed the numerator difference is
  `c-a+(m-2)d>0`. The case `(j,k)` active is identical.

It therefore suffices in (5) to retain the two-label branches, and the
three-label branches with `a+d<c` and **both legs to k tight**. This is
used to prove a sign below; no new family of templates is left to solve.

Every retained branch has the form

    f(m)=A/2-B/(2m).                                    (6)

For a two-label branch, `A=B=c>=beta`. For a retained three-label branch,

    A=a+d, B=2(a+d)-c=|y_i+y_j-2y_k|^2.

The two tight-leg equalities and the parallelogram identity give

    B=|x_i+x_j-2x_k|^2+ell_ij >= ell_ij >= beta.          (7)

Thus the apparently dangerous third-site interaction has the same positive
curvature floor as the two-label interactions. A midpoint with B=0 cannot
survive this argument when its endpoint pair is genuinely shortened.

## 3. The entire finite matrix is positive

Let `r=2i+2`, `t=2j+2`, `m=i+j+2=(r+t)/2`, with `i!=j`. Choose a retained
branch attaining E_m. Since E_r and E_t are at most that same branch's
values, (6)--(7) imply

    E_m-(E_r+E_t)/2 >= beta Gamma_(i,j),
    Gamma_(i,j)=(i-j)^2/[8(i+1)(j+1)(i+j+2)].            (8)

Indeed the gap of the branch `A0/2-B0/(2m)` is `B0 Gamma_(i,j)`.
For distinct indices in `0,...,D`,

    Gamma_(i,j) >= 1/K_D.                               (9)

Equation (3) immediately gives the upper bound

    a_(m-2) <= c_m exp(-E_m/s).                          (10)

For a lower bound retain one minimizing count vector from (5). Its
multinomial coefficient is at least m: for any nontrivial count a it
contains a factor `binom(m,a)>=m`. Its label probability is at least p^m.
Its source-minus-target scatter is at least `min_E ell_ij>=beta`.
For `2<=m<=M`, the assumed bound `beta/s>=K_D L_(D,b)` implies
`beta/(2ms)>=1`, since `K_D L_(D,b)>=2M`. Hence

    1-exp(-(S_x-S_y)/(2ms)) >= 1-e^(-1)>1/2,
    p^M c_m exp(-E_m/s) <= a_(m-2) <= c_m exp(-E_m/s).    (11)

The count multiplicity gives the factor `m/2>=1` in the lower bound;
the two ordered tuples at m=2 are not counted twice.

Arithmetic-geometric mean gives `c_m<=sqrt(c_r c_t)`. Therefore (8)--(11)
give the actual normalized endpoint entries

    0 <= a_(i+j)/sqrt(a_(2i)a_(2j))
      <= 2^(bM) exp(-beta Gamma_(i,j)/s)
      <= 2^(bM) exp(-L_(D,b)) < 1/(2D).                (12)

Here `e>2` and the integer ceiling define the last bound without a
numerical logarithm. After normalizing the diagonal of H_D to one, each
row has D off-diagonal entries bounded by `1/(2D)`. Applying
`2|uv|<=u^2+v^2` to its quadratic form gives the matrix lower bound `I/2`.
Undoing the diagonal normalization proves (1).

This argument retains the endpoint replica average throughout. It does
not assert positivity of the conditional kernel in the six-dimensional
lift, and does not use the open universal quartic inequality.

## 4. Colliding targets have a positive merger limit

Partition the indices into target coincidence groups J and put
`W_J=sum_(i in J) w_i`. Set

    a^0_(m-2)=c_m [sum_J W_J^m-sum_i w_i^m].             (13)

These are the limits of (3) as s tends to zero. More precisely, the
zero-scatter source tuples have probability `sum_i w_i^m`, and the
zero-scatter target tuples have probability `sum_J W_J^m`. Every remaining
tuple uses at least two distinct spatial sites and has scatter at least
`(m-1)delta`. Thus each residual expectation lies in
`[0,exp(-(m-1)delta/(2ms))]`. Their difference has absolute value at most
the length of this interval, not twice its length. Since `c_m<=1`,

    |a_(m-2)-a^0_(m-2)| <= exp(-delta/(4s)).             (14)

The limiting sequence has a useful nonnegative hinge profile. With
`q(z)=exp(-|z|^2/2)` and `C0=(2pi)^(-3/2)`, put

    H0(t)=C0 integral [sum_J (W_J q(z)-t)_+
                       -sum_i (w_i q(z)-t)_+] dz.

The inequality `(a+b-t)_+ >= (a-t)_+ +(b-t)_+` for nonnegative a,b,t
shows H0 is nonnegative. Layer cake and Gaussian integration give
`a^0_j=integral_0^1 t^j H0(t)dt` exactly.

Choose two indices in one nontrivial coincidence group. Their weights are
at least p. On the cube `[-1/2,1/2]^3`, one has `q>1/2`: indeed
`exp(3/8)<=1/(1-3/8)=8/5<2`. For `p/4<=t<=p/2`, the two selected
summands are both above t, and their merger hinge gain is exactly t.
Merging the remaining group members only adds nonnegative gains. Since
`C0>1/16`, using the classical bound `pi<22/7`, this proves

    H0(t) >= p/64  for p/4<=t<=p/2.                     (15)

Let `Q_D` be the monomial Gram matrix on `[p/4,p/2]`. It is positive
definite because a nonzero polynomial cannot vanish on an interval.
For `H_D^0=(a^0_(i+j))`, (15) gives

    H_D^0 >= (p/64) Q_D.                               (16)

We next give an explicit coefficient bound, so (16) is quantitative even
when the matrix order grows.

## 5. A rational lower margin in the collision case

Use the classical Legendre polynomials P_j, with P_0=1, P_1(z)=z,

    (j+1)P_(j+1)=(2j+1)z P_j-j P_(j-1),
    integral_(-1)^1 P_i(z)P_j(z)dz=2 delta_ij/(2j+1).

These are standard recurrence and orthogonality identities; no new
orthogonal-polynomial result is asserted. After setting `z=8t/p-3`, the
polynomials `sqrt(4(2j+1)/p) P_j(8t/p-3)` are orthonormal on `[p/4,p/2]`.

Let `||R||_1` be the sum of the absolute monomial coefficients of R.
The norm of `8t/p-3` is `8/p+3`. The recurrence implies, by induction,

    ||P_j(8t/p-3)||_1 <= (20/p)^j.                      (17)

In detail, with `R=20/p` and `r=8/p+3`, one has `r<=R` and
`2r+1/R<=2r+1=16/p+7<=20/p`, since `p<=1/2`.
The recurrence coefficients are bounded by 2 and 1, so the inductive
step is `2r R^j+R^(j-1)<=R^(j+1)`.

If the coefficient vectors of these orthonormal polynomials form the
rows of A, then `A Q_D A^T=I` and `Q_D^(-1)=A^T A`. Their Euclidean
coefficient norms are at most their coefficient 1-norms. Consequently

    trace(Q_D^(-1)) <= U,
    U=(4/p)(D+1)(2D+1)(20/p)^(2D).                      (18)

For a positive definite matrix, its smallest eigenvalue is at least
the reciprocal of the trace of its inverse. Equations (16)--(18) imply
`H_D^0 >= p/(64U) I = 2 lambda_(D,b) I`.

By (14), every entry of `H_D-H_D^0` has absolute value at most
`exp(-delta/(4s))`. Its operator norm is at most `(D+1)` times that bound.
Define the integer

    Lc=9+10D+(2D+2)b+ceil(log_2((D+1)^2(2D+1))).

Using `20<=2^5` and `p=2^(-b)` gives

    2^Lc >= 512(D+1)^2(2D+1)(20/p)^(2D)/p^2
          = (D+1)/lambda_(D,b).                         (19)

Also `D+1<=2^D` and `2D+1<=2^(D+1)` for `D>=1`, so

    Lc <=10+13D+(2D+2)b <=27bD.                         (20)

Under `delta/s>=108bD`, (19)--(20) and `e>2` imply
`(D+1)exp(-delta/(4s))<=lambda_(D,b)`. Combining this with (16)--(18)
proves (2).

If E is empty, equality of all pair distances gives a rigid isometry
between the two finite clouds, by their centered Gram matrices. Their
smoothed densities are isometric and all gaps vanish. Together with the
two nontrivial cases above, this proves Theorem 1.

## 6. Quantitative counterexample obligations

For the distinct-target case,

    K_D<=48D^3, L_(D,b)<=6bD, K_D L_(D,b)<=288bD^4.

For each fixed data set, any negative curvature-square witness must
therefore have root degree greater than

    floor[(beta/(288bs))^(1/4)]                         (21)

whenever this floor is positive. For a fixed data set with a collision,
the corresponding necessary degree is greater than

    floor[delta/(108bs)].                              (22)

These are lower bounds, not sharp rates or assertions that such witnesses
exist. Coefficients can vary arbitrarily with s, so the result is stronger
than positivity for one fixed polynomial. However the allowable degree
grows as s decreases; exchanging the two quantifiers would be invalid.
Neither full Gaussian majorisation nor a new KP consequence follows.

## 7. Exact controls and adversarial relevance

The executable checks are standard-library rational arithmetic. They
include four deliberately different inputs:

1. A non-orthocentric tetrahedron with three deep reflected normal-ray
   sites, unequal priors, paired rank six, 15 tight and six shortened
   pairs. Every nearest target pair is tight. Here `beta=400/3`, `b=3`,
   and the whole H_5 is positive for `0<s<=1/792`.
2. The unshrunk eight-site benchmark from the geometric lane, with binary
   weights `(1,2,...,128)/255`. It has 18 tight pairs, all nearest pairs
   tight, and paired rank six. Here `beta=1888/9`, `b=8`, giving
   `0<s<=59/74250` for H_5. Its separate path obstruction is not a premise.
3. `x=(-e1,e1,0)` and `y=((-4/5,3/5,0),(4/5,3/5,0),0)`. This has one
   shortened pair and two tight legs. For m>2 the three-site branch is
   strictly better than either two-site branch, with
   `E_m=1-18/(25m)`. Thus simply replacing "nearest pair" by "nearest
   shortened pair" in the old exponent formula would be false.
4. `x=(0,-e1,e1,-2e2,2e2,-3e3,3e3)`, coordinatewise absolute-value
   targets, and weights `(1,2,...,64)/127`. It has rank six and three
   collision groups, with `delta=1`, `b=7`. Formula (2) gives H_5
   positivity through `s=1/3780`. This familiar positive map is only a
   collision and normalization control, not a new map class.

The first example's core vertices are `0,(2,0,0),(1,2,0),(1/2,1/3,3)`.
Opposite edges have a nonzero inner product. The source generator and all
exact coordinates are in verify.py and EXPECTED.json. No assertion places
either control outside every previously known full positive class.

The checker compares the minimum scatter over all active count vectors in
its stated finite ranges with both the full vertex formula and the pruned
formula. It independently checks selected scatters by (4), the tight-leg
parallelogram identity, exact rational Gram inversion versus Legendre
coefficients, boundary cutoffs, and malformed-input rejection. The matrix
and continuum statements are the written proof, not inference from samples
or an independent review. No Gaussian quadrature or private search output
is needed to reproduce the public claim.
