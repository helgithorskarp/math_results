# Seven positive diagonals of the Gaussian beta hierarchy

Complete author proof with an exact symbolic audit, 26 September 2026.
Independent correctness and historical priority review are pending.
The full dimension-three Gaussian-majorisation conjecture remains open.

## 1. The universal signed statement

Let mu be any bounded probability law in R3, T a contraction on its
support, and s>0. Put f=mu*gamma_s, g=(T#mu)*gamma_s,
C=(2 pi s)^(-3/2), and

    d_m = C^(1-m) integral (g^m-f^m),
    a_j = d_(j+2)/[(j+1)(j+2)],
    H(u) = integral (g-Cu)_+ - integral (f-Cu)_+.

The established moment identity is a_j=integral_0^1 u^j H(u) du.
The beta coefficients are

    b_(N,j)=(N+1) binom(N,j)
              sum_(ell=0)^(N-j) (-1)^ell binom(N-j,ell) a_(j+ell).
                                                                  (1)

**Theorem 1.** For every N>=0 and 0<=j<=N such that N-j<=6,

    b_(N,j) >= 0.                                                 (2)

Every inequality is strict unless T preserves all distances on supp(mu).
This signs the seven rightmost coefficients of every degree, as well as
all coefficients in rows N<=6. There is no atom-count, minimum-weight,
radius, variance-window or strict-pair hypothesis. Repeated points,
zero-weight faces, diffuse laws and isometries are included.

Equivalently, the normalized moment-gap sequence a_j has nonnegative
alternating forward differences through order six, at every index j.
Thus every convex energy with curvature u^j(1-u)^q, j>=0 and 0<=q<=6,
and every nonnegative finite combination of these curvatures, has the
desired comparison on the attained density range 0<=u<=1. Choose the
energy and its derivative to vanish at zero. It can be extended convexly
beyond one by its tangent line; the evaluated values are unchanged.
Precisely, for U''(u)=u^j(1-u)^q,

    C integral[U(g/C)-U(f/C)] = sum_(ell=0)^q
                                   (-1)^ell binom(q,ell) a_(j+ell).

For example the polynomial with U''(u)=(1-u)^6 is convex everywhere on
the nonnegative axis. Its pressure fails the source's PC2 sufficient
condition: 2U''+uU'''=2(1-u)^5(1-4u)<0 for 1/4<u<1. Neither ordinary
nonnegative moment gaps nor that integer pressure class alone is the
proof supplied here. No priority claim for the general use of polynomial
curvature tests is made.

The theorem is not positivity of every beta coefficient, every convex
polynomial, or every hinge. In particular b_(7,0) is not decided.
The existing universal absolute bound D<=7/50 remains a separate result;
the present exact signs do not establish D=0 or a new KP consequence.

The prepublication refresh found researcher 5's concurrent
[centroid-projection proof](../gaussian_beta_projection/PROOF.md), which
already signs N-j<=5 for all laws and all polarized weight coefficients.
We credit that overlap. The additional mechanism here is the positive
Poisson representation of the affine offset: it permits six remaining
points, instead of five remaining vectors, and gives N-j=6 as well.
The uniform quantitative bounds (3)--(4) and exact first-residual audit
are additional deliverables. Neither packet's publication is independent
acceptance of the other, and no priority claim is made.

## 2. An explicit lower bound on every compact-frontier row

Suppose, after separate translations, both sets of centers are within
B(0,R). Let

    Delta = E[|X-X'|^2-|T(X)-T(X')|^2],     r=R/sqrt(s),
    q=N-j<=6,                              p=j+2.

**Theorem 2.** Under the assumptions of Theorem 1,

    b_(N,j) >= [(N+1) binom(N,j)/(1024 * 3^q * s)]
               exp[-(p/2)(9r^2+8r+8)] Delta.                    (3)

The constant is deliberately conservative. It vanishes with the actual
pair-distance loss, so it remains valid at all weight and isometry faces.
It requires no unknown Gaussian coefficient or source-set error as input.

For the original R3 compact frontier K_l (variance one, radii at most 2l),
this gives the entirely rational, compressed certificate

    b_(N,j)(Q) >= A_(l,N,j) Delta(Q)       for every Q in K_l,

    A_(l,N,j) = [(N+1) binom(N,j)/(1024 * 3^(N-j))]
                 * 2^[-2(j+2)(18l^2+8l+4)] > 0,
    0<=N-j<=6.                                                  (4)

Thus it signs seven entries even at the large diagonal N_l=2^16 l^8-2,
uniformly over the entire compact parameter set. The certificate stores a
rational mantissa and an integer exponent; it does not expand the enormous
power of two or the alternating moment sum. The other entries remain open.
No localization or moment-approximation error is being used to infer a sign.

## 3. Reduce the moment difference to one pair and a small complement

Take independent replicas X_i of mu, with Y_i=T(X_i). For 0<=t<=1 put

    Z_i(t)=(sqrt(1-t) X_i, sqrt(t) Y_i) in R6,
    delta_ab=|X_a-X_b|^2-|Y_a-Y_b|^2 >= 0.

For a set A of m replica positions let

    Q_A(t)=sum_(i in A)|Z_i(t)-mean_A Z(t)|^2
          =(1/m) sum_(a<b in A)|Z_a(t)-Z_b(t)|^2.

The Gaussian product identity and scalar differentiation give

    d_m = m^(-3/2) E[e^(-Q_A(1)/(2s))-e^(-Q_A(0)/(2s))],
    d_m/[m(m-1)]
       = (1/(4s)) E[delta_12 integral_0^1
                                m^(-5/2) e^(-Q_A(t)/(2s)) dt].   (5)

For the second equality, differentiate Q_A, sum its pair losses and use
exchangeability. This is the existing replica differentiation identity,
retaining the original dimension's exponent 5/2 after differentiation.
The intermediate Z_i need not be points in R3.

Fix j>=0, q=N-j, and take M=N+2 replicas. Use positions 1,...,p=j+2 as
the base A0, including the distinguished pair 1,2; let B0 be the q other
positions. Conditional on the base, those remaining replicas are iid.
Substitution of (5) in (1), and averaging subsets of B0 of each size, give

    b_(N,j) = [(N+1) binom(N,j)/(4s)]
       E[delta_12 integral_0^1 K(A0,B0;t) dt],

    K = sum_(B subset B0) (-1)^|B|
          (p+|B|)^(-5/2) exp[-Q_(A0 union B)(t)/(2s)].           (6)

All sums are finite. Bounded support justifies the differentiation and
integration; alternatively the integrated scalar identity in (5) supplies
each term before taking the finite signed combination. No sign of K is
assumed in deriving (6).

## 4. Condition on the entire base and remove an affine offset

Work at fixed t and any realized tuple in R6. Let zbar be the base mean,
Q0=Q_A0, and w_i=Z_i-zbar for i in B0. The variance update identity is

    Q_(A0 union B) = Q0 + sum_(i in B)|w_i|^2
                         - |sum_(i in B) w_i|^2/(p+|B|).        (7)

Suppose the affine span of the remaining w_i has dimension at most five.
This is automatic when q<=6, even if the full paired tuple has rank six.
Let v0 be the nearest point to zero in this affine span, write
w_i=v0+v_i, and identify its direction space isometrically with a subspace
of R5. Then v0 is orthogonal to every v_i. For ell=|B|, (7) becomes

    Q_(A0 union B) = Q0 + sum_(i in B)|v_i|^2
       - |sum_(i in B)v_i|^2/(p+ell)
       + [p ell/(p+ell)] |v0|^2.                              (8)

If q=0, take v0=0 and the empty family. Define

    phi_i(u)=exp(-|u-v_i|^2/(2s)),       0<phi_i<=1,
    C5=(2 pi s)^(-5/2),                 beta=p|v0|^2/(2s).

Completing the square in R5 expresses the summand of K as

    e^(-Q0/(2s)) e^[-beta ell/(p+ell)]
       C5 integral_(R5) e^[-p|u|^2/(2s)] product_(i in B)phi_i(u) du.
                                                                  (9)

The affine offset cannot simply be dropped. It has a positive moment
representation: let J have the Poisson law of mean beta, let E_i be iid
exponentials of rate p, and put Theta=exp(-sum_(i=1)^J E_i). Then

    0<Theta<=1,
    E Theta^ell = exp[-beta ell/(p+ell)],
    Pr(Theta=1)=exp(-beta).                                     (10)

Indeed the conditional moment is [p/(p+ell)]^J; sum the Poisson series.
The case beta=0 is the point mass at one. The random variable is an
analytic representation, not sampled in the certificate computation.

Insert (9)--(10) into the finite inclusion-exclusion sum (6):

    K = e^(-Q0/(2s)) E_Theta C5 integral_(R5)
             e^[-p|u|^2/(2s)] product_(i in B0)(1-Theta phi_i(u)) du
      >= 0.                                                    (11)

This proves Theorem 1's nonnegative assertion. It also states the more
general usable pruning condition: any tuple/base with remaining affine
dimension at most five has this nonnegative kernel, regardless of q.
A different five-dimensional realization may be chosen for each tuple,
base and t; the scalar kernel is already a continuous measurable function
of the original coordinates. No measurable choice of frames is required.

The improvement over a direct paired-rank test comes in two steps. First
one conditions on the distinguished pair and the j other base positions.
Then one handles the remaining common affine offset by (10). Dropping
that offset, or counting the rank of the full tuple instead of the
remaining points, would give an incorrect or unnecessarily weak argument.

## 5. Quantitative certificate and strictness

Both endpoint center sets are in B_R, so every interpolated Z_i is in B_R.
Their base mean also lies there. Hence

    Q0<=p R^2,       |w_i|<=2R,
    |v0|<=2R,       |v_i|<=2R,       beta<=2p R^2/s.             (12)

For |v0| use its nearest-point property; for |v_i| use orthogonality.
Retain only the atom Theta=1 in (11). Integrate on the five-dimensional
box with first coordinate in [2R+sqrt(s),2R+2sqrt(s)] and each other
coordinate in [0,sqrt(s)]. It has volume s^(5/2). Throughout that box,

    |u|^2/s <= (2r+2)^2+4,
    |u-v_i| >= sqrt(s),       1-phi_i(u)>=1-e^(-1/2)>1/3.

Also (2 pi)^(-5/2)>1/256, since pi<4 and 8^5<256^2. It follows that

    K >= [1/(256 * 3^q)]
               exp[-(p/2)(9r^2+8r+8)].                       (13)

The exponent combines Q0/(2s), beta, and the base Gaussian on the box.
Substitution in (6), with E delta_12=Delta, proves (3).

For K_l use R=2l, s=1. The exponent is the integer
E=(j+2)(18l^2+8l+4). The elementary e<4 gives e^(-E)>2^(-2E),
proving (4). No numerical exponential is evaluated to certify its sign.
For completeness, the exponential series through degree two is 5/2;
its remaining terms start at 1/6 and have successive ratios at most 1/4.
Thus e<=5/2+(1/6)/(1-1/4)=49/18<4. Similarly, the first three
terms of exp(1/2) give 13/8>3/2, as used in (13).

Because the prefactor is positive, Delta>0 implies strict positivity of
every coefficient in the asserted strip. Conversely Delta=0, continuity
of the pair-distance loss, and the support property of mu imply equality
of every support pair distance. T is then a Euclidean isometry on that
support, and the convolved laws are congruent, giving zero coefficients.
This proves the stated complete equality boundary.

## 6. Polarized coefficients and the first remaining cases

The [weight-cell certificate](../gaussian_beta_weight_certificate/PROOF.md)
homogenizes b_(N,j) to degree M=N+2. Its coefficient for a labeled M-tuple
alpha is the subset average of the kernels K_m in that source, with
coefficient

    (N+1) binom(N,j) (-1)^(m-j-2) binom(N-j,m-j-2)
        / [m(m-1) binom(M,m)].

After differentiation, collect each distinguished pair and each j-element
base extension. The positive outer factor is 1/(2sM). The remaining sum
is exactly K in (6). The combinatorial identity, for r>=j, is

    (N+1) binom(N,j) binom(N-j,r-j)
      / [(r+2)(r+1) binom(N+2,r+2)] = binom(r,j)/(N+2).          (14)

Thus **every homogeneous weight coefficient** is nonnegative throughout
N-j<=6, on every contraction in R3. It is strictly positive if any pair
appearing in the tuple has positive loss. The finite-cell numerical
positivity at N=5 is therefore covered globally by this argument. Its
larger numerical margins on its specified cell retain their own content;
we do not replace those constants with a stronger quantitative claim.

At N=7,j=0 there are nine replica positions. The automatic rank test
only leaves these multiplicity patterns and distinguished pairs:

| Distinct labels | Multiplicities | Pair requiring possible rank-six analysis |
| --- | --- | --- |
| 7 | (2,2,1,1,1,1,1) | the two doubled labels |
| 8 | (2,1,1,1,1,1,1,1) | the doubled label and a singleton |
| 9 | all one | any pair |

All other patterns, and all other nonzero-loss pairs in these patterns,
leave at most six distinct points and are signed by (11). A pair of
identical labels has zero loss. The exact audit enumerates all 30 integer
partitions of nine and every distinct-label pair to verify this coverage.

The rank-six issue is real already on seven sites, although it is not a
negative coefficient. Take the classical tetrahedral flap fixture and
its labels (0,1,2,3,4,7,10), with the ordering in the source. Their paired
affine-difference determinant is -512, so they span R6. Duplicate labels
0 and 4 and distinguish one copy of each. Their distance loss is 16;
after removal the seven remaining paired points still have rank six.
At t=1/2 the corresponding affine determinant is -64. The 21 original
endpoint pairs are all contractions. This prevents applying (11) by
pretending the remaining affine rank is at most five.

The fixture certifies only this coverage boundary. No negative value of
K or b_(7,0), optimal strip width, or obstruction to a different proof is
claimed. The general conjecture still supplies the target sign for all
remaining rows.

## 7. Exact audit and trust boundary

[verify.py](verify.py) checks (14) as polynomial identities in the
unbounded base index j, for all 28 pairs 0<=ell<=q<=6. It independently
checks the variance update (7) by exact Gram coefficient matrices at
49 finite sizes, the offset identity r(p+r)-r^2=pr, the positive constants,
the two exponent simplifications, the complete partition boundary, and
the rational flap determinant and pair losses. The general variance
identity is proved algebraically above; finite audits are not its proof
for unbounded p. The checker emits compact mantissa/exponent certificates
for the entire seven-entry part of the K_3 diagonal, without expanding
any tiny rational denominator.

All arithmetic is Python integer or Fraction arithmetic. No solver output,
floating-point sign, Gaussian quadrature, large moment list or hidden data
is trusted. Bounded floating searches helped identify the question but are
not part of the published proof or its prerequisites. The written Gaussian
integration, conditional Poisson representation and universal analytic
reduction remain unformalized trust boundaries. Successful author checks
and publication are not independent mathematical acceptance.
