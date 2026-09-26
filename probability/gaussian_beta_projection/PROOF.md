# Six universal beta columns from Gaussian projection

Complete author proof; independent mathematical review and historical
priority review are pending. The full three-dimensional Gaussian-majorisation
question remains open. This proves a global sign in its existing moment
criterion, with no restriction on the support geometry, weights or variance.

## 1. Statement in the team's normalization

Let mu be a bounded probability law on R3, let T be 1-Lipschitz on its
support, and let s>0. Put

    C=(2 pi s)^(-3/2), f=mu*gamma_s, g=(T#mu)*gamma_s,
    F=f/C, G=g/C,
    d_m=C integral (G^m-F^m),
    a_j=d_(j+2)/[(j+1)(j+2)].

In particular 0<F,G<=1. For integers k,r>=0 define

    A_(k,r)=sum_(l=0)^r (-1)^l binom(r,l) a_(k+l).          (1)

**Theorem.** For every integer k>=0 and every r in {0,1,2,3,4,5},

    A_(k,r)>=0.                                           (2)

All these inequalities are strict if

    D=E[|X-X'|^2-|T(X)-T(X')|^2]>0,                      (3)

where X,X' are independent with law mu. If D=0, every expression in
(2) is zero. Zero weights, repeated sites and diffuse laws are included.

The normalized hinge gap and beta coefficients are

    H(u)=integral(g-Cu)_+ - integral(f-Cu)_+,
    b_(N,k)=(N+1) binom(N,k) A_(k,N-k),  0<=k<=N.          (4)

Thus the **six rightmost entries of every beta row are nonnegative**:

    b_(N,k)>=0 whenever N-k<=5.                           (5)

In particular the entire row N=5 is nonnegative for all contractions
and all variances. The first row with an unsigned entry is N=6, where
only k=0 is left unsigned by this theorem.

This does not prove all beta coefficients nonnegative, all convex
polynomial comparisons, or the full conjecture. It does not increase
the known minimum number of atoms for a possible counterexample: seven
distinct sites can occur with repetitions in the still-unsigned tests.

The proof extends the positive-product mechanism in researcher 8's
[polarized cell certificate, Sections 2--3](../gaussian_beta_weight_certificate/PROOF.md).
That source projects the whole configuration when its paired affine
rank is at most five. Here the projection depends on the positive
Gaussian factors in a single summand; the remaining at most five factors
determine its subspace. A component orthogonal to that subspace cancels
into one positive scalar, even when the full paired rank is six.

## 2. A projection identity for alternating Gaussian products

This elementary lemma does not assume a contraction. Let z_i be any
finite list of points in a Euclidean space. Partition its labelled
positions into a nonempty block B and a block L of size r. For a
nonempty set of positions A write

    S_A=sum_(i<j in A) |z_i-z_j|^2,
    K_d(A)=|A|^(-d/2) exp[-S_A/(2 |A| s)].                 (6)

Here d is a positive integer, not necessarily the dimension of the z_i.
Suppose r<=d. Then

    sum_(J subset L) (-1)^|J| K_d(B union J) > 0.          (7)

Repeated points cause no problem; subsets always select positions.

**Proof.** Let c be the centroid of the points indexed by B. Let V be
the span of z_l-c for l in L, so dim V<=r<=d, and let P be orthogonal
projection onto V. Translate by c and put

    u_i=P(z_i-c),
    E_perp=sum_(i in B) |(I-P)(z_i-c)|^2.                 (8)

Identify V isometrically with a subspace of R^d, padding with zeros.
Every point of L has zero perpendicular component. The perpendicular
components of B sum to zero, because c is its centroid. Therefore for
every J subset L, m=|B|+|J|, the elementary identity

    S_A/m = sum_(i in A)|z_i-c|^2
                           - |sum_(i in A)(z_i-c)|^2/m

gives exactly

    S_(B union J)(z)/m = S_(B union J)(u)/m + E_perp.     (9)

The last term is independent of J, including its cardinality. This
independence is why centering at the centroid of B is essential.

Put C_d=(2 pi s)^(-d/2) and phi_i(v)=exp(-|v-u_i|^2/(2s)).
The Gaussian product formula and (9) yield

    K_d(B union J)
      = exp(-E_perp/(2s)) C_d integral_(R^d)
                                      product_(i in B union J) phi_i(v) dv.

Expanding a finite product proves the identity

    sum_(J subset L) (-1)^|J| K_d(B union J)
      = exp(-E_perp/(2s)) C_d integral_(R^d)
           [product_(i in B) phi_i(v)]
           [product_(l in L) (1-phi_l(v))] dv.            (10)

All factors are nonnegative. The Gaussian factors are strictly positive;
each factor 1-phi_l vanishes only at its center. Since d>=1, their finite
set of zeros is null. The integral is finite and strictly positive,
also when L is empty. This proves the lemma. QED.

In particular one must not merely project and omit E_perp. Conversely,
the lemma does not require the entire configuration to fit in R^d.
No continuity of the chosen projection as the points vary is assumed.

## 3. Replica differentiation and the sign

Take independent labels X_1,...,X_m with law mu and set Y_i=T(X_i).
Write Delta_ij=|X_i-X_j|^2-|Y_i-Y_j|^2>=0. Realize the linearly
interpolated squared distances by points in R6:

    z_i(t)=(sqrt(1-t) X_i, sqrt(t) Y_i),  0<=t<=1.

Gaussian integration at the two endpoints gives

    d_m=m^(-3/2) E[exp(-S_m^y/(2ms))-exp(-S_m^x/(2ms))].

Differentiate the scalar exponential of the interpolated distance sum.
Exchangeability of the m labels turns the sum over its m(m-1)/2 pairs
into that many copies of the distinguished pair (1,2). Consequently,
for m=k+2,

    a_k=(1/(4s)) E[Delta_12 integral_0^1
                   m^(-5/2) exp(-S_m(t)/(2ms)) dt].      (11)

All constants matter here: division by m(m-1), the pair count, and
the exponential derivative 1/(2ms) leave m^(-5/2)/(4s).
The replica formula and its differentiated version are existing team
inputs, also derived in the [Hankel source](../gaussian_majorisation_hankel_transport/PROOF.md).

For A_(k,r), use M=k+r+2 independent labels on one probability space.
Fix B={1,...,k+2} and let L be the remaining r positions. Integrating
unused labels out and using exchangeability among L gives the exact
coupling of all terms of (1):

    A_(k,r)=(1/(4s)) E[Delta_12 integral_0^1
              sum_(J subset L) (-1)^|J| K_5(B union J;t) dt].  (12)

Apply (10) with d=5 to the actual six-dimensional z_i(t). If r<=5,
the bracket is strictly positive at every t and for every label tuple.
This proves (2). If D>0, the event Delta_12>0 has positive probability,
so (12) is strictly positive. If D=0, nonnegativity of Delta makes it
zero almost surely, and (11)--(12) vanish.

The original scalar bracket in (12) is measurable and continuous in t.
Its positivity is proved separately for each tuple and t, so no measurable
selection of bases or projection matrices is needed. Bounded support
bounds every Delta_ij and all the scalar kernels. It justifies all finite
sums, expectations, differentiations and time integrations. Thus the
argument applies directly to diffuse laws; strictness is not inferred
from a possibly non-strict approximation limit. QED.

## 4. Positivity before averaging the prior weights

The sign also applies to every polarized weight coefficient in the six
columns, which is useful on zero-weight faces of the compact frontier.
Here we keep researcher 8's normalization explicitly.

For M=N+2 labelled positions alpha, define

    L_m(A)=m^(-3/2)[exp(-S_A^y/(2ms))-exp(-S_A^x/(2ms))],

    c_(N,k)(alpha)=(N+1) binom(N,k)
      sum_(m=k+2)^M (-1)^(m-k-2) binom(N-k,m-k-2)
        /[m(m-1) binom(M,m)]
        * sum_(A subset [M], |A|=m) L_m(A).              (13)

For independent labels of any finite prior, b_(N,k)=E c_(N,k).
Fix a pair a<b in [M], and let R be the other N positions. Expanding
the scalar derivatives in (13) and grouping by a subset J of R of
size k gives

    c_(N,k)(alpha)=(1/(2sM)) sum_(a<b) Delta_ab integral_0^1
      sum_(J subset R, |J|=k)
        sum_(Q subset R minus J) (-1)^|Q|
                      K_5({a,b} union J union Q;t) dt.   (14)

For example the coefficient identity behind this grouping is, for
q>=k,

    (N+1) binom(N,k) binom(N-k,q-k)
       /[(q+2)(q+1) binom(N+2,q+2)] = binom(q,k)/(N+2).

There are exactly N-k factors in the last alternating sum. Formula
(10), centered at the centroid of B={a,b} union J, therefore proves

    c_(N,k)(alpha)>=0 whenever N-k<=5.                   (15)

It is strictly positive if any pair in the tuple has Delta_ab>0;
otherwise it is zero. The argument includes arbitrary multiplicities.
It is a sign identity, not a numerically rounded lower bound.

At N=5, (15) covers the seven-distinct coefficients that previously
required numerical enclosure on the particular sixteen-label cell.
That cell's explicit quantitative lower bounds remain useful; they are
not supplied by (15), and their computation is not independently reviewed
here. At any larger N, all six rightmost columns can likewise be pruned
before subdividing geometry or weights.

## 5. Exact place in the full-question criterion

Tonelli applied separately to the two hinges gives

    a_j=integral_0^1 u^j H(u) du,
    A_(k,r)=integral_0^1 u^k(1-u)^r H(u) du.             (16)

Equivalently define U_(k,r)(0)=U'_(k,r)(0)=0 and
U''_(k,r)(u)=u^k(1-u)^r on [0,1]. Then

    C integral[U_(k,r)(G)-U_(k,r)(F)]=A_(k,r)>=0
                         for k>=0 and 0<=r<=5.          (17)

These energy densities can be continued linearly past 1 to remain
convex on [0,infinity). Positive finite sums of them also compare.
This is an infinite cone of tests for every contraction, not a new
geometric family or a variance-threshold theorem. A general nonnegative
polynomial curvature need not have a nonnegative expansion in these
particular kernels, so (17) is not a claim about every convex polynomial.

The [global criterion](../gaussian_majorisation_global_criterion/PROOF.md)
requires (16) nonnegative for *all* k,r. Equations (2) and (15) remove
the complete strip r<=5 from that obligation. Every possible negative
beta certificate must have r>=6. This does not justify cancelling the
remaining alternating sums or raising five to an arbitrary number:
six remaining vectors may span all of R6, while (10) needs a realization
in five dimensions.

For the [R3 rational compact interface](../gaussian_prior_localization/RATIONAL_INTERFACE.md)
and [R8 uniform moment frontier](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
the six columns are signed uniformly over every compact configuration,
every prior-weight face and all stated rational distance cells. In the
notation D_N=max(0,-min_k b_(N,k)), this gives D_N=0 for N<=5, and
permits restricting the minimum to k<=N-6 when N>=6. It does not
evaluate the remaining compact maximum or change the localization error.

This proof does not supply the R1 heat-contact flux inequality, an
endpoint coupling for the full profile, or a new Kneser--Poulsen result.
It provides an actual global positive integral for a previously unsigned
part of the full criterion. The next analytic obligation is to control
the first genuinely six-direction alternating remainder (r=6), or find
a different positive decomposition for it, retaining the contraction
constraints. No sign for that remainder is claimed.

## 6. Verification and trust boundary

The theorem is the written proof above. The standard-library exact
audit checks the centroid/projection identity (9), finite product
coefficients, exchangeability normalization and the coefficient identity
in (14). It includes full-rank six-dimensional controls, a genuine
three-dimensional fold with contracted pairs, repeated positions,
degenerate spans, arbitrary-size positive blocks, and deliberate corruptions.
All checks use integers and fractions and remain active under python -O.

The audit computes no Gaussian hinge integral, does not perform a
numerical search, and does not infer a universal inequality from finite
examples. It imports no sibling checker or external package. Its generic
Euclidean controls need not be contraction configurations; the separate
fold control is labelled as such. Gaussian integration, nonnegativity,
strictness and the all-parameter conclusion remain mathematical proof
obligations rather than a proof-assistant certificate. See README.md for
reproduction and SOURCES.md for exact team attribution.
