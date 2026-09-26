# The first unsigned Gaussian beta obligation is nonnegative

Author computer-assisted proof, 26 September 2026. Independent mathematical
review and formalization are pending. The unrestricted dimension-three
Gaussian-majorisation question remains open.

## 1. Statement and normalization

Let mu be a bounded probability measure on R3, T a 1-Lipschitz map on its
support, s>0, f=mu*gamma_s, g=(T#mu)*gamma_s, and C=(2 pi s)^(-3/2).
Use the existing moment and beta normalizations

    d_m=C^(1-m) integral(g^m-f^m),
    a_j=d_(j+2)/[(j+1)(j+2)],
    b_(N,j)=(N+1) binom(N,j) sum_(ell=0)^(N-j)
                             (-1)^ell binom(N-j,ell) a_(j+ell).

**Theorem.** For every j>=0, b_(j+7,j)>=0. In particular, the first
previously unresolved universal coefficient b_(7,0) is nonnegative.
The inequality is strict unless T preserves every distance on supp(mu).
Together with [R2's theorem](../gaussian_beta_pair_conditioning/PROOF.md),
this signs every entry in every row N<=7 and all entries with N-j<=7.
There are no atom-count, weight, radius-window or variance restrictions.

Here is an explicit loss bound. After separate translations suppose both
endpoint supports lie in B_R, put r=R/sqrt(s), p=j+2, and define

    Delta=E[|X-X'|^2-|T(X)-T(X')|^2].

Then

    b_(j+7,j) >= [(j+8) binom(j+7,j)/(4s)] (5/2)_7
                  (p+7)^(-19/2) exp[-(p+28)r^2/2] Delta.       (1)

The rising factorial (5/2)_7 equals11486475/128. This also signs every
homogeneous polarized weight coefficient in this diagonal: a coefficient
is positive if its tuple contains a pair of positive distance loss.

Equivalently, every convex energy whose normalized curvature is
u^j(1-u)^7 on [0,1] compares in the desired direction. Its value and first
derivative may be set to zero at zero, and its convex extension beyond one
does not affect the evaluated densities. In particular

    U(u)=((1-u)^9-1+9u)/72,     0<=u<=1,

has U''=(1-u)^7 and b_(7,0)=8C integral[U(g/C)-U(f/C)]. This energy is
not covered directly by the primary paper's PC2 sufficient condition:
2U''+uU'''=(1-u)^6(2-9u) is negative for 2/9<u<1.
No conclusion for every convex energy, every hinge, the next unresolved
beta row, or Kneser--Poulsen volumes follows from the present theorem.

## 2. The conditional kernel and its exact derivative

We use R2's pair-conditioned identity, reproduced here to fix its scope.
For independent replicas X_i, set Y_i=T(X_i),

    Z_i(t)=(sqrt(1-t)X_i,sqrt(t)Y_i) in R6,
    delta_12=|X_1-X_2|^2-|Y_1-Y_2|^2,
    Q_A(t)=sum_(i in A)|Z_i(t)-mean_A Z(t)|^2.

Take a base A0 of p=j+2 positions, including1,2, and seven further
positions B0. Differentiation of the Gaussian product formula and
exchangeability give

    b_(j+7,j)=[(j+8) binom(j+7,j)/(4s)]
                   E[delta_12 integral_0^1 K(t) dt],           (2)

    K(t)=sum_(B subset B0) (-1)^|B|
                     (p+|B|)^(-5/2) exp[-Q_(A0 union B)(t)/(2s)].

The pair loss is nonnegative. We will sign every conditional kernel,
including those whose seven remaining points have affine rank six.
Let Q0=Q_A0(t), zbar=mean_A0 Z(t), and w_i=(Z_i(t)-zbar)/sqrt(s).
Completing a square gives

    K(t)=exp[-Q0/(2s)] K_p(w),
    K_p(w)=sum_(S subset [7]) (-1)^|S| F_p(1_S),
    F_p(x)=(p+sum x_i)^(-alpha)
       exp[-(sum x_i |w_i|^2-|sum x_i w_i|^2/(p+sum x_i))/2],
    alpha=5/2.                                                (3)

The following argument works for seven vectors in any finite Euclidean
dimension and every real p>0. At x>=0 define

    A=p+sum x_i,   m=(sum x_i w_i)/A,   c_i=sqrt(A)(w_i-m).

An exact completion of the square, with h near zero and u=h/A, gives

    F_p(x+h)/F_p(x)
      =(1+sum u_i)^(-alpha)
        exp[-sum u_i |c_i|^2/2
                 +|sum u_i c_i|^2/(2(1+sum u_i))].             (4)

The base p has a fixed center at zero. Including its contribution when
recentering is essential; (4) follows by expanding both sides, not by
discarding that base. Only a neighborhood of h=0 is needed for derivatives.

Let G_ij=c_i.c_j, a_i=G_ii/2. For a matching M on the seven labels, write
m_M=|M| and U_M for its unmatched labels. Define the polynomial

    L_7(G)=sum_M product_(ij in M)G_ij
                  sum_(S subset U_M) (alpha+m_M)_(|S|)
                                         product_(i in U_M\S)a_i.       (5)

This matching formula was already derived by R2 as a large-p asymptotic;
we credit that discovery. Its exact finite-p use here follows from (4).
In the square-free coefficient of product_i u_i, the quadratic exponential
selects disjoint edges, with one factor G_ij/(1+sum u_i) per edge. The
linear exponential supplies the a_i factors; the remaining power series
supplies the rising factorial. Thus

    (-1)^7 partial_1 ... partial_7 F_p(x)
                      =F_p(x) A^(-7) L_7(G(x)).              (6)

All derivatives are ordinary analytic derivatives on a neighborhood of
the nonnegative orthant. Seven applications of the fundamental theorem
of calculus now give the **exact**, positive-weight integral identity

    K_p(w)=integral_[0,1]^7 F_p(x) A^(-7) L_7(G(x)) dx.        (7)

There is no asymptotic limit, inverse transform or numerical quadrature
in this step. It remains to prove L_7>= (alpha)_7 on every PSD Gram matrix.

## 3. Reduce the Gram polynomial to three homogeneous forms

For 0<=k<=7 let

    S_k(G)=sum_M [product_(ij in M)G_ij/(alpha)_(|M|)]
                       e_(k-|M|)((a_i)_(i in U_M)),            (8)

where an elementary symmetric polynomial outside its degree range is
zero. Sorting (5) by Gram degree gives

    L_7(G)=sum_(k=0)^7 (alpha)_(7-k) S_k(G).                 (9)

Indeed a term with m edges and k-m diagonal factors leaves7-k-m scalar
positions, and (alpha+m)_(7-k-m)=(alpha)_(7-k)/(alpha)_m.

We have S_0=1. Also

    S_1=(1-1/alpha)sum_i a_i + |sum_i c_i|^2/(2alpha)>=0.    (10)

When every a_i>0 replace c_i by c_i/a_i, obtaining a Gram matrix G'.
Termwise complementation of the unmatched diagonal labels gives

    S_(7-k)(G)=(product_i a_i) S_k(G'),                       (11)

for every k. Zero vectors are handled by continuity (or approximation
of a PSD G by G+epsilon I). Consequently nonnegativity of S_2 and S_3
for every PSD7x7 matrix suffices for all seven forms. The next section
provides exact finite PSD certificates for these two universal forms.

## 4. An integer-matrix certificate for S_2 and S_3

For k=2,3 let I_k be the set of ordered k-tuples of distinct labels in
{0,...,6}; its size is42 or210. Let H_k(G) be the corresponding principal
submatrix of G tensor ... tensor G (k factors):

    H_k(G)_(x,y)=product_(r=1)^k G_(x_r,y_r).

It is PSD whenever G is PSD. Call (x,y) **aligned** if every label shared
by the two tuples occurs in the same coordinate. Define C_k by

    (C_k)_(x,y)=1/(alpha)_m  if aligned and m=#{r:x_r!=y_r},
                  0         otherwise.                       (12)

Direct counting gives

    S_k(G)=trace(C_k H_k(G))/(2^k k!).                        (13)

A monomial with m edges is represented by2^m k! orientations and orders.
Its coefficient in (8) is1/[2^(k-m)(alpha)_m], agreeing with (13).

Define B_2=35 C_2. Its nonzero aligned entries for m=0,1,2 are35,14,4.
The exact matrix certificate verifies

    (B_2-7I)(B_2-15I)(B_2-45I)(B_2-105I)(B_2-255I)=0.       (14)

Since B_2 is real symmetric, all its eigenvalues are positive. Thus

    S_2(G)=trace(B_2 H_2(G))/280>=0.                          (15)

For C_3 use a correction with an explicitly nonnegative polynomial
evaluation. On the six permutations of
each unordered three-element set, let P_sym and P_alt be the orthogonal
projections onto the symmetric and alternating vectors; off these blocks
their entries vanish. Set

    B_3=315 C_3 +63(P_alt-P_sym).                             (16)

Equivalently start with aligned entries315,126,36,8 for m=0,1,2,3, and
subtract21 when x,y are odd relative permutations of the same three-set.
This is a completely specified210x210 symmetric integer matrix.
The exact certificate verifies

    product_(lambda in E) (B_3-lambda I)=0,
    E={0,42,45,117,132,522,585,882,1755,3252}.                 (17)

Every possible eigenvalue is nonnegative, so B_3 is PSD. On each three-set
A, the traces of P_sym H_3 and P_alt H_3 are respectively per(G_A) and
det(G_A). Hence (13)--(16) give the polynomial identity

    S_3(G)=[trace(B_3 H_3(G))
                   +63 sum_(|A|=3)(per(G_A)-det(G_A))]/15120. (18)

For a symmetric3x3 matrix,

    per(G_A)-det(G_A)=2 sum_(i in A) G_ii G_jk^2,
                         {j,k}=A\{i}.                       (19)

This is nonnegative when the diagonal is nonnegative. The other term in
(18) is nonnegative because it is the trace of a product of PSD matrices.
This proves S_3>=0. Equations (9)--(11) prove

    L_7(G)>=(5/2)_7=11486475/128>0                            (20)

for every PSD7x7 real matrix, with no rank restriction.

### Exact computational obligation

The finite proof obligations are precisely (14), (17), and the explicitly
counted identities (13), (18). [certificate.py](certificate.py) constructs
the full matrices and applies each annihilating polynomial to **every**
standard basis vector, in Python integer arithmetic. No orbit sampling or
floating eigenvalue is used as evidence.

[verify.py](verify.py) constructs the matrices a second way, from their
edge/loop monomials. It verifies the231 and665 coefficient identities
against a separate diagonal-first matching enumeration. It then verifies
PSD by fraction-free symmetric elimination, independently of the spectral
roots: all nonzero pivots are positive, all divisions exact, and the final
zero-diagonal block is zero. The ranks are42 and190. At each elimination,
the residual is a positive scalar multiple of the Schur complement, so
these checks imply PSD including its singular boundary. The spectral and
elimination matrix hashes agree. These are two author checks, not two
independent mathematical reviews.

## 5. Return to Gaussian signs and the compact frontier

In (7), A<=p+7 and

    F_p(x)>=(p+7)^(-5/2) exp[-sum_i |w_i|^2/2].

Combining with (20) yields the strict conditional estimate

    K_p(w)>=(5/2)_7 (p+7)^(-19/2)
                              exp[-sum_i |w_i|^2/2]>0.       (21)

The seven-dimensional cube has volume one. There is no issue from zero
vectors, coincident sites, a singular Gram matrix, or any base p>0.

For bounded endpoint supports in B_R, every Z_i(t) lies in B_R,
Q0<=pR^2, and |w_i|<=2r. Thus (21) and (2) give (1). For Delta=0,
continuity and the support property force every support-pair loss to be
zero; the restriction of T is then the restriction of a Euclidean
isometry. The convolved laws are congruent and every beta gap is zero.
For Delta>0, (1) is strict. All expectations and derivatives are justified
by bounded support and finite sums; diffuse probability laws are included.

For polarized coefficients, use R2's exact pair/base collection identity

    (N+1)binom(N,j)binom(N-j,r-j)
      /[(r+2)(r+1)binom(N+2,r+2)]=binom(r,j)/(N+2).

For a fixed labeled tuple, its coefficient is a positive multiple of a
sum of pair losses times precisely the kernels just signed. This proves
the stated coefficient sign, including every weight face. In particular,
all three formerly unresolved nine-replica multiplicity patterns are
covered globally, not only in the earlier certified flap cells.

At variance one and radius R=2l, the rational compressed bound

    b_(j+7,j) >= A_(l,j) Delta,
    A_(l,j)=[(j+8)binom(j+7,j)*11486475/(512(p+7)^10)]
                                         *2^[-4(p+28)l^2]    (22)

follows from (1), (p+7)^(-19/2)>=(p+7)^(-10), and e<4. This can be
used directly on R3's compact family, regardless of its atom budget or
chosen large row. For a given row N>=7, put j=N-7. It supplies an exact
positive coefficient bound without expanding high powers or taking
differences of nearly cancelling moments. The corresponding rational
radius3l family requires inserting R=3l in (1), not reusing (22).

This is a closure of the first unsigned universal beta obligation. It
does not turn the accepted global defect bound7/50 into zero and does
not sign all of R3's required rows. The all-threshold orthocentric-flap
and local rigid-hull theorems have different scopes; see [SOURCES.md](SOURCES.md).

## 6. Evidence boundary

The universal analytic reductions, the Gram/trace argument and the stated
normalizations are written mathematical premises. The two finite matrix
PSD assertions have exact computer-assisted certificates. The additional
[audit_recentring.py](audit_recentring.py) checks42 rational derivative
identities by independent square-free power-series arithmetic,42 exact
homogenization controls, all1850 integer matching terms after scaling
L_7 by128, and R2's regular-simplex polynomial. Those finite derivative
checks are controls; the general identity is proved in (4)--(7).

No solver correctness, floating sign, quadrature, external dataset,
unstated rank assumption or omitted large certificate is a premise.
The Python interpreter and arbitrary-precision integer/Fraction operations
remain computational trust boundaries. Neither publication nor matching
checks constitute external peer review or a proof-assistant formalization.
