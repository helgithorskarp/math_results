# A quantitative degree barrier for low-noise Gaussian counterexamples

Complete author proof, 27 September 2026; independent review is pending.
This signs complete finite Hankel matrices on a uniform small-noise domain.
It does **not** prove all Gaussian hinges, full majorisation on that domain,
or a new Kneser--Poulsen inequality.

## 1. Statement

Let x_1,...,x_N and y_1,...,y_N be finite configurations in R3, N>=2, with

    |y_i-y_j| <= |x_i-x_j| for all i,j.

Use positive common probabilities w_i summing to one. The y_i are distinct.
Set

    delta = min_(i<j) |y_i-y_j|^2 > 0.

Assume at least one pair (u,v) attaining this minimum has positive loss

    eta = |x_u-x_v|^2-|y_u-y_v|^2 > 0.                 (1)

Other pairs may be tight, including other nearest pairs. Every strictly
contracting finite configuration with distinct targets satisfies (1).
Choose an integer b>=1 with w_i>=2^(-b) for every i.

Let s>0 be the Gaussian variance, C=(2 pi s)^(-3/2), and

    f=sum w_i gamma_s(.-x_i), g=sum w_i gamma_s(.-y_i),
    F=f/C, G=g/C,
    d_m=C integral (G^m-F^m),
    a_j=d_(j+2)/[(j+1)(j+2)].

For an integer D>=1 define

    M=2D+2,
    K_D=8D(D+1)(2D+1),
    L_(D,b)=M b + ceil(log_2(2D)).                      (2)

**Theorem.** If

    eta/s >= 4,       delta/s >= K_D L_(D,b),           (3)

then the full matrix H_D=(a_(i+j))_(0<=i,j<=D) satisfies

    H_D >= (1/2) diag(a_0,a_2,...,a_(2D)) > 0.         (4)

The first inequality is in positive-semidefinite order. In particular,
for every nonzero real polynomial P of degree at most D, the globally
convex energy

    U_P(t)=integral_0^t (t-u) P(u)^2 du,
    V_P(rho)=C U_P(rho/C)

has strictly positive target-minus-source Gaussian internal-energy gap.
Its degree is at most 2D+2. Positive sums of these energies and arbitrary
linear terms have the same comparison. The assertion includes every
polynomial convex on the entire real line, vanishing at zero, of degree
at most 2D+2: a nonnegative univariate polynomial is a sum of two polynomial
squares. We do not assert here the larger class of polynomials whose
curvature is nonnegative only on the attained density interval.

There is no radius bound, covariance assumption, angular symmetry, special
map formula, or paired-rank restriction. The theorem is uniform over all
configurations satisfying the displayed separation, loss and mass bounds.
It applies to rank-six configurations and does not reopen orthocentric flaps.

## 2. Replica bounds from one nearest pair

The classical Gaussian product formula gives

    d_m=m^(-3/2) E[exp(-S_m^y/(2ms))-exp(-S_m^x/(2ms))],
    S_m^z=sum_(r<t) |z_(I_r)-z_(I_t)|^2,              (5)

for iid labels I_r of law w. Every term in the difference is nonnegative.
Tuples with one distinct label cancel exactly.

For counts n_i summing to m with at least two positive entries,

    sum_(i<j) n_i n_j >= m-1.                          (6)

Indeed sum n_i^2 is maximized at the two-entry vector (m-1,1), by transferring
units from smaller nonzero entries to the largest while retaining two
positive entries. Equivalently the maximum is (m-1)^2+1. Hence every
nonconstant target tuple has S_m^y >= (m-1)delta. Writing

    alpha_m=(m-1)/(2m),    c_m=1/[m^(5/2)(m-1)],

and bounding the total probability of nonconstant tuples by one gives

    a_(m-2) <= c_m exp(-alpha_m delta/s).                (7)

For a lower bound keep just the m tuples containing m-1 copies of u and
one copy of v, where (u,v) is the fixed pair in (1). Their total probability
is m w_u^(m-1) w_v, and their source-minus-target scatter loss is
(m-1)eta. Thus

    a_(m-2) >= m w_u^(m-1) w_v c_m
       exp(-alpha_m delta/s) [1-exp(-alpha_m eta/s)].    (8)

This also counts correctly when m=2: the two ordered tuples (u,v),(v,u)
occur once each. We do not add a second orientation to (8).

If 2<=m<=M and eta/s>=4, then alpha_m>=1/4 and
1-exp(-alpha_m eta/s)>=1-e^(-1)>1/2. Also
w_u^(m-1)w_v>=2^(-bm)>=2^(-bM), and m>=2. Consequently

    2^(-bM)c_m exp(-alpha_m delta/s)
      <= a_(m-2) <= c_m exp(-alpha_m delta/s).          (9)

All inequalities concern the actual endpoint moments. No conditional kernel,
unaveraged interpolation time, or numerical exponential is substituted.

## 3. Normalized off-diagonal entries decay uniformly

Set A=2i+2, B=2j+2 and m=i+j+2=(A+B)/2. Arithmetic-geometric mean gives

    c_m <= sqrt(c_A c_B),                              (10)

because m>=sqrt(AB) and m-1>=sqrt((A-1)(B-1)). Using (9), for i!=j,

    0 <= a_(i+j)/sqrt(a_(2i)a_(2j))
      <= 2^(bM) exp[-Gamma_(i,j) delta/s],              (11)

where the exact curvature of alpha is

    Gamma_(i,j)=alpha_m-(alpha_A+alpha_B)/2
      = (A-B)^2/[4AB(A+B)]
      = (i-j)^2/[8(i+1)(j+1)(i+j+2)].                 (12)

For distinct indices in {0,...,D}, one of i+1,j+1 is at most D, the other
at most D+1, and i+j+2<=2D+1. Therefore

    Gamma_(i,j) >= 1/K_D.                              (13)

Under (3), the right side of (11) is at most

    2^(bM) exp(-L_(D,b)) < 2^(bM-L_(D,b)) <= 1/(2D).  (14)

Here e>2 follows already from the first three terms of its positive series;
the ceiling in (2) is an integer condition, not a floating logarithm.

Normalize H_D by its positive diagonal. Its diagonal entries are one and
each of its D off-diagonal entries per row has absolute value at most
1/(2D). For any vector z,

    z^T R z >= sum_i z_i^2
                 - sum_(i<j) |R_ij|(z_i^2+z_j^2)
              >= (1/2) sum_i z_i^2.

This direct diagonal-dominance estimate proves (4). Finally expanding P^2
and integrating twice gives

    integral [V_P(g)-V_P(f)]=sum_(i,j) P_i P_j a_(i+j),

which proves the energy statement. These integrals are finite because the
normalized densities lie in [0,1] and the energies vanish at zero. QED.

## 4. Uniform region and degree obstruction

For every fixed b, delta_0>0, eta_0>0 and D, the entire class with
weights >=2^(-b), target separation squared >=delta_0, and a nearest target
pair shortened by squared loss at least eta_0 obeys the theorem whenever

    0<s<=min(eta_0/4, delta_0/[K_D L_(D,b)]).           (15)

For example, all such laws with weights >=1/8, delta_0=1/4 and eta_0=1
satisfy H_5>0 and all the stated degree-twelve comparisons for

    0<s<=1/422400.                                     (16)

This is coverage of a whole separated finite-law class, not sampling of
coordinates or a numerical neighborhood of the example below.

The existing complete Hankel criterion says every genuine Gaussian
majorisation failure has a finite globally convex curvature-square witness.
For data satisfying (1), a negative witness P must therefore have degree
strictly above every D passing (3). For fixed b, delta and eta, this lower
bound diverges as s tends to zero. Indeed K_D<=48D^3 and
L_(D,b)<=6bD, so the simpler condition delta/s>=288bD^4 suffices.
Once s<=eta/4, every negative curvature-square witness must have degree
greater than floor[(delta/(288bs))^(1/4)], whenever that floor is positive.
Its energy degree is correspondingly greater than twice that floor plus two.
This is a sufficient exclusion scale, not an optimal asymptotic rate.

It follows that searching any fixed polynomial degree at ever smaller
variance cannot find a counterexample in this class. This is the durable
obligation for an adversarial or certification lane: increase degree, leave
the certified noise range, or address a configuration whose nearest target
pairs are all tight. No fixed degree proves all hinges. Degree and noise
cannot be interchanged in the quantifiers.

If all nearest target pairs are tight, (8) with positive eta is unavailable,
even when many farther pairs contract. We make no statement excluding a
counterexample there. This boundary matters for configurations with a rigid
core; a positive total or average loss cannot replace a verified nearest
pair loss. Target collisions, vanishing masses and diffuse laws are also
outside the uniform statement as written.

## 5. Rational non-orthocentric rank-six fixture

The exact checker includes seven sites built from the oblique tetrahedron
with vertices 0,(2,0,0),(1,2,0),(1/2,1/3,3). Add the three points p+r n,
where p is the centroid of the face opposite vertex 0,1,2, n is its outward
cross-product normal divided by six, and r is respectively 2,3,4. Reflect
them to p-r n, fix the four vertices, then multiply all targets by 3/4.
This comes from the contraction (3/4)(2P_C-I), but the checker verifies
every pair directly over rational numbers.

Use weights (1/8,1/8,1/8,1/8,1/4,1/8,1/8). The target separation squared
is 245/576, attained at labels 0,4; its source squared loss is 84659/5184.
Every pair is strict, with minimum squared loss 7/4, and the paired affine
rank is six. The fixture passes (15)--(16). These assertions are exact
input checks; no moment quadrature is used to certify the theorem's region.
We make no assertion that this fixture is outside every other positive
Gaussian class, or that the reflected-projection family is Gaussian-negative.

## 6. Provenance and verification boundary

The replica formula, complete Hankel criterion, elementary nearest-distance
count, arithmetic-geometric mean and diagonal dominance are existing
ingredients. The contribution is their quantitative combination into a
low-noise degree obstruction for actual Gaussian endpoint tests. Priority
is provisional; targeted searches found no matching statement.

`verify.py` uses only standard-library integers and Fraction. It checks the
rank-six input, every pair and probability, the exact integer cutoff and
boundary rejections, finite composition counts, and the rational curvature
identity and its minimum. It produces EXPECTED.json identically under normal
and optimized Python. These finite controls do not formalize the universal
proof, which is the written argument above. No floating-point eigenvalue,
interval library, private search, omitted certificate stream or source from
another workspace is a proof input. See SOURCES.md for dependencies and the
distinction from high-noise and peak-pruning results.
