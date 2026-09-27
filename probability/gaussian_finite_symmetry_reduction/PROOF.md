# Finite symmetry preserves the unrestricted Gaussian defect

27 September 2026. Complete author proof; independent review pending.
No adverse Gaussian input is supplied. This is a reduction of the actual
finite-variance question, not a sign theorem or a motion obstruction.

Let gamma_s be the probability Gaussian of covariance s I_3, and write

    H_f(h) = integral (f-h)_+,
    D_s(mu,T) = sup_(h>=0) [H_(mu*gamma_s)(h)
                              -H_((T#mu)*gamma_s)(h)]_+.

Here mu has compact support and T is short (1-Lipschitz) on that support.
The adverse sign is positive in this convention. Let D_s^all be the
supremum over these pairs. It lies in [0,1]. Hinges characterize the
majorisation question in Aishwarya--Li. Spatial rescaling gives
D_s^all=D_1^all for every s>0.

## 1. The reduced class has exactly the same supremal defect

Let W be the 48 signed coordinate permutation matrices in R3. Restrict
the supremum to pairs for which

* mu and T#mu are W-invariant;
* T has a global short extension satisfying T(w x)=w T(x) for every w in W;
* both means vanish and both covariance matrices are positive scalar
  multiples of I_3, with each squared support radius at most four times
  its own scalar covariance.

**Theorem.** The restricted supremum equals D_s^all at each fixed s>0.
The equality still holds if the restricted laws are finite and have
rational centres and weights, at s=1. In particular the full conjecture
is equivalent to its assertion on this symmetric class at variance one.

**Compact isotropic version.** Equivalently, it suffices to consider all
positive variances with W-invariant source laws satisfying Cov(mu)=I_3
and supp(mu) contained in B(0,2), and global equivariant short maps. The
targets can additionally have covariance alpha I_3, 0<alpha<1, and support
in B(0,2sqrt(alpha)). The supremal defect over this compact isotropic
class and all positive variances still equals D_1^all. Covariance and
radius are now fixed; the variance is not bounded away from zero.

The assertion is about arbitrary equivariant contractions, not about
aligning the oriented halves of an orbit or preserving individual radii.
Within-orbit weights are equal; the representative points and the weights
between different orbits remain unrestricted. No finite atom bound is
asserted. The fixed-variance version has no fixed radius bound. This does not reduce the number
of free representative coordinates or furnish a finite cover.

More precisely, after independent translations put both supports of any
given pair in B(0,R), R>=1. The translations preserve every hinge and
every labelled contraction inequality. For any L>=16R the construction
below gives a restricted pair (mu_L,T_L) such that, simultaneously for
every h>=0,

    | H_(mu_L*gamma_s)(h/48)-H_((T_L#mu_L)*gamma_s)(h/48)
          - H_(mu*gamma_s)(h)+H_((T#mu)*gamma_s)(h) |
       <= E_L := 47 exp[-(L/2-2R)^2/(8s)].                    (1)

Consequently

    |D_s(mu_L,T_L)-D_s(mu,T)| <= E_L.                        (2)

There is no factor 1/48 multiplying the old defect. All 48 copies carry
the old sign and their masses add to one. This lossless-in-the-limit
defect comparison, rather than only an existence implication, is the
useful reduction.

## 2. Explicit construction and all cross-pair inequalities

Set v=(1,2,3). Its W-orbit has 48 distinct points and

    min_(w!=z) |w v-z v|^2 = 2.                              (3)

Indeed equal coordinate sign patterns with a nontrivial permutation
change at least two integer coordinates, whereas any changed sign
changes a nonzero integer coordinate by at least two. Swapping the first
two entries attains 2. We use only the weaker separation >=1.

For x in supp(mu), and w in W, define

    P_w(x)=w(Lv+x),      Q_w(x)=w((L/2)v+T(x)),
    mu_L=(1/48) sum_w (P_w)#mu,
    T_L(P_w(x))=Q_w(x).                                    (4)

The source blocks are disjoint because their centre separation is at
least L and each has radius R. Within each block the given contraction
applies. For two different blocks put d=|w v-z v|>=1. Triangle inequalities
give

    |P_w(x)-P_z(y)| >= Ld-2R,
    |Q_w(x)-Q_z(y)| <= (L/2)d+2R.

Their length difference is therefore at least

    (L/2)d-4R >= L/4 > 0,                                  (5)

using L>=16R. Thus all cross-block pairs strictly contract, uniformly
over the entire two compact supports, not just their sampled atoms.
Target blocks are also disjoint, with centre separation at least L/2.

Equation (4) is equivariant on its source support. Kirszbraun gives a
global short extension F. Averaging it as

    F_W(x)=(1/48) sum_(w in W) w^(-1) F(w x)                 (6)

gives another short extension, which is W-equivariant. Each summand in
(6) equals T_L(x) on the prescribed support. For z in W, substituting
w'=wz in (6) gives F_W(zx)=z F_W(x). No averaging of the prescribed
endpoint law or change of its map values is involved.

Both endpoint laws in (4) are W-invariant. Their means vanish by the
sign changes. A covariance commuting with every coordinate sign change
is diagonal, and commuting with every permutation makes its diagonal
constant. Explicitly, the two scalar covariance factors are

    lambda_P = (1/3) integral |Lv+x|^2 dmu(x),
    lambda_Q = (1/3) integral |(L/2)v+T(x)|^2 dmu(x).         (7)

They are positive. In fact lambda_P>lambda_Q because the mean ordered
distance loss is positive by (5) and both means are zero. The two
covariances are not required to equal each other or I_3. Since -I is
in W, the extension is odd and fixes zero.

Both laws have a uniform radius-to-covariance guard. Write c=L or L/2
for the relevant endpoint. Then c>=8R, |v|^2=14 and |v|<4 imply

    sup |cv+x|^2 <= 14c^2+8cR+R^2 <= (961/64)c^2,
    lambda >= (14c^2-8cR)/3 >= (13/3)c^2.

It follows that

    (squared support radius)/lambda <= 2883/832 < 4.       (7a)

Apply the same spatial scale lambda_P^(-1/2) to both endpoints. This
preserves shortness, equivariance and the hinge defect, provided the
variance is changed from s to s/lambda_P. The source then has covariance
I_3 and radius less than 2; the target has covariance alpha I_3, where
alpha=lambda_Q/lambda_P is in (0,1), and radius less than 2sqrt(alpha).
The Gaussian threshold is multiplied by lambda_P^(3/2) under this scale.
This proves the compact isotropic version once (2) is established. The
rescaling need not retain rational coordinates; rationality is asserted
only for the preceding fixed-variance scalar-covariance version.

## 3. Uniform hinge error from separated components

For nonnegative u_1,...,u_m and h>=0 define

    I_h(u)=(sum_i u_i-h)_+ - sum_i(u_i-h)_+.

Then

    0 <= I_h(u) <= sum_(i<j) min(u_i,u_j).                  (8)

For the lower bound, if there are active terms their sum subtracts h
at least as many times as the combined term does; with no active terms
the conclusion is immediate. For the upper bound choose a largest term
u_j. If u_j>=h, I_h<=sum_(i!=j)u_i. If u_j<h, the same bound follows
from (sum u_i-h)_+<=sum u_i-u_j. The pairs containing j alone already
sum to sum_(i!=j)u_i on the right of (8).

Now let rho_i,rho_j be any probability Gaussian convolutions at variance
s whose centre laws are supported in B(c_i,R), B(c_j,R), with
D=|c_i-c_j|>2R. Splitting space by the midpoint perpendicular plane and
integrating the less favorable density on each side gives

    integral min(rho_i/m,rho_j/m)
       <= (2/m) Q((D-2R)/(2sqrt(s)))
       <= (2/m) exp[-(D-2R)^2/(8s)],                       (9)

where Q(t)=Pr{N(0,1)>=t}. The first inequality holds for arbitrary
diffuse centre laws by integration over the labels. The second is the
elementary Gaussian Chernoff bound: apply Markov to exp(tZ), whose mean
is exp(t^2/2). No spatial quadrature is used.

Write f=mu*gamma_s, g=(T#mu)*gamma_s. Orthogonal invariance of gamma_s
makes each smoothed block a translated, rotated copy of f/48 or g/48.
Consequently the sum of their separate hinge integrals at h/48 is
exactly H_f(h), respectively H_g(h). From (8)--(9), the two integrated
interaction terms obey

    0<=I_P(h)<=E_L,       0<=I_Q(h)<=E_L,                   (10)

because there are binom(48,2) pairs and the smaller endpoint centre
separation is at least L/2. The factor is
binom(48,2)*(2/48)=47. Thus |I_P-I_Q|<=E_L, proving (1).
Taking positive parts and suprema, and observing that h->h/48 ranges
over all nonnegative thresholds, proves (2).

Every constructed pair belongs to the unrestricted class. Conversely,
given any pair and any error eta>0, take L large enough that E_L<eta.
Equation (2) implies that the restricted supremum is at least every
unrestricted defect minus eta. Let eta decrease to zero. This proves
the asserted equality of suprema, including when that supremum is zero
or is not attained.

## 4. Exact finite margin and rational witnesses

Suppose an actual input has a certified adverse hinge

    H_f(h_*)-H_g(h_*) >= delta > 0.                         (11)

This is a conditional premise; no such input accompanies this packet.
Choose integer k>=1 with 47*2^(-k)<=delta/2 and choose an integer L with

    L>=16R,             (L-4R)^2>=32 s k.                  (12)

Then E_L<=47 exp(-k)<47*2^(-k), because e>2. Equations (1) and (11)
give a symmetric adverse hinge at h_*/48 of size at least delta/2.
For a prescribed approximation error eta, replace delta/2 by eta in
the choice of k. This retains the same variance; no low-noise limit,
eventual-variance theorem, or changing-prior asymptotic is used.

For finite rational input at variance one, all output centres and
weights in (4) are rational. Each old weight is divided by 48. The
signed permutation matrices, v and L are rational, and the cross-pair
guard has rational exact checks. No search for the global extension
(6) is needed to determine the endpoint laws or their Gaussian hinges.

For completeness finite rational pairs suffice for the unrestricted
supremum. Quantize a compact supported law on its actual support and
use the same target labels. Translated Gaussian kernels are uniformly
L1-continuous in their centres, so both densities converge in L1; every
hinge changes by at most that L1 error, uniformly in its threshold.
Finite priors can be rationally approximated with the same bound.

To rationalize centres without losing shortness, first merge coincident
source points (their target values coincide). For a finite distinct
source list, replace each target q_i by (1-epsilon)q_i. Every pair then
has strictly positive squared loss: originally equal target points
already had strict loss, and all other target distances strictly shrink.
Take epsilon sufficiently small to preserve any desired defect error.
The finitely many strict inequalities persist under sufficiently small
independent rational centre perturbations. Gaussian L1 continuity
controls the additional error. Rational thresholds can also approximate
a positive adverse threshold by continuity, but are not needed for the
supremal equality. Now apply (4) to the resulting rational pair.

These are existence reductions; no universal finite cardinality or
coordinate denominator is inferred. Existing effective localization
results retain their own budgets and hypotheses.

## 5. Consequences and boundaries for the shared question

An improved universal defect bound proved only for the reduced symmetric
class would be the same improved bound for all bounded R3 contractions.
Zero defect on that class would settle the full conjecture. A certified
adverse original input transfers with (12), and any adverse reduced input
is already an actual counterexample. No hypothetical sign is promoted
to an observed one.

The compact isotropic version makes simultaneous covariance collapse
unnecessary for an existential counterexample at some variance. It
does not supply a positive lower variance or a uniform effective search
budget. In the fixed-variance construction the covariance grows with
L; in the compact normalization the variance may tend to zero. The
new all-radius localization theorem can consume actual radius and
covariance guards, but its unsigned modulus does not sign these inputs.

The earlier Coxeter result aligns the two oriented halves of reflection
orbits while retaining their representatives. It does not compare
arbitrary changes of those representatives. Here both endpoint densities
are invariant under the whole reflection group, so their alternating
character components vanish separately. Their invariant components
generally differ. The existing alignment argument therefore supplies
no sign for this class. Full finite symmetry is weaker than spherical
invariance; these laws need not be radial, single-radius, or norm
preserving under their map.

The construction has well separated components and nonnegative
cross-component hinge errors, but the component endpoint deficit is
preserved. Separation cannot turn an unsigned local comparison into
a sign. It also does not make an unknown adverse defect easier to
find inside an individual representative block. The support radius
grows with L, the mean distance loss grows, and normalized
defect-to-loss ratios are not preserved. Claims needing those
quantifiers do not follow from (2).

This is a broad finite-variance counterexample-space reduction. It is
not a new positive class, a Kneser--Poulsen theorem, a finite cover, a
numerical census, or an obstruction to all other proof methods. The
Gaussian overlap and separated-copy arguments are elementary; no
historical priority is asserted. The compact checker supports the
algebra and bounds, not the existence of a violating Gaussian pair.
