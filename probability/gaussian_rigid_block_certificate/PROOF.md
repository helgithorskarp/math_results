# A contracting-motion certificate on partially tight distance faces

Author proof, 27 September 2026. Independent acceptance, formalization and
historical priority are pending. The unrestricted three-dimensional
Gaussian-majorisation question remains open.

The balanced-loss certificate at graph6504 requires every distinct pair to
have positive loss. Here arbitrarily many distances may be preserved: each
preserved group moves rigidly, and only distances **between** groups need a
positive budget. The result is a uniform finite-configuration cover at such
faces, with every atom weight, Gaussian variance and threshold allowed.
It constructs an actual motion in R3. No new cap or flap class is used.

## 1. Endpoint-only hypotheses

Let x_1,...,x_n be distinct points of R3 and y_1,...,y_n satisfy

    Delta_ij = |x_i-x_j|^2 - |y_i-y_j|^2 >= 0.

Partition the labels into at least two nonempty blocks. Require
`Delta_ij=0` whenever i,j belong to the same block. Thus each block has
congruent source and target configurations; it can have affine dimension
one, two or three, and singleton blocks are allowed.

Write c_b for a source block's unweighted mean, and set

    S_b = sum_(i in b) (x_i-c_b)(x_i-c_b)^T.

Choose kappa>0 no larger than the smallest **positive** eigenvalue of each
nonsingleton S_b. There is no condition on its zero eigenvalues. For a
singleton the condition is empty. Set

    d^2 = max_(i<j) |x_i-x_j|^2,
    E = sum_i |y_i-x_i|^2,
    C = 8 + 2d^2/kappa,
    delta_cross = min_(i,j in different blocks) Delta_ij.

**Theorem 1 (a displayed-frame certificate).** If

    E <= kappa,                 delta_cross >= C E,             (1)

then there is a real-analytic simultaneous contracting motion in R3 from
the displayed source to target. A zero value of E is the identity case.

Consequently, for every probability vector p_i>=0, every s>0 and h>=0,

    integral (sum_i p_i gamma_s(z-y_i)-h)_+ dz
      >= integral (sum_i p_i gamma_s(z-x_i)-h)_+ dz.             (2)

The union of balls cannot increase in volume and the intersection cannot
decrease, with arbitrary individual radii. These consequences are the
known Gaussian and Kneser--Poulsen motion theorems, credited in
[SOURCES.md](SOURCES.md). No priority claim is made for those implications.

**Corollary 2 (independent endpoint frames).** Center both full lists at
their unweighted means, giving n-by-3 row matrices A,B. Suppose

    A^T A >= k I_3,    k>0,
    F = ||AA^T-BB^T||_F^2,     H = 2F/k.

Then the entirely frame-invariant guard

    H <= kappa,                 delta_cross >= C H             (3)

implies (2) and both ball-volume signs. A rigidly aligned target admits the
motion of Theorem 1. If F=0, congruence gives equality without the scatter
or partition hypotheses. A single congruent block also gives equality.

The constants are sufficient and are not optimized. Failure of a guard is
UNRESOLVED, not a Gaussian counterexample. This certificate is used together
with, rather than replacing, the sharper balanced guard6504.

## 2. Small rigid blocks have quadratically small acceleration

Let d_b be a target block mean, u_b=d_b-c_b and r_i=x_i-c_b.
Congruence supplies an orthogonal extension O_b with

    y_i = d_b + O_b r_i,
    E_b = sum_(i in b) |y_i-x_i|^2
        = |b| |u_b|^2 + sum_(i in b) |(O_b-I)r_i|^2.          (4)

The extensions can be chosen in SO(3) so that

    ||O_b-I||_F^2 <= 2E_b/kappa.                              (5)

Here is the dimension check. For rank three the extension is unique. The
scatter bound gives `kappa||O_b-I||_F^2<=E_b`. An improper orthogonal
matrix in dimension three has eigenvalue -1, so its squared distance from
I is at least4. This contradicts `E_b<=E<=kappa`; hence it is proper.

For rank two, extend the plane isometry by sending its oriented normal to
the oriented target normal. This gives a proper rotation of angle theta.
If P is projection onto the source plane, then

    ||(O_b-I)P||_F^2 >= 4 sin^2(theta/2)
                     = (1/2)||O_b-I||_F^2.

Indeed `(O_b-I)^T(O_b-I)` is `4 sin^2(theta/2)` times projection onto
the two-dimensional plane perpendicular to the rotation axis; its trace
against a rank-two projection is at least that scalar. The scatter bound
now proves (5). For rank one choose the shortest rotation sending a unit
source direction to its target direction. Its Frobenius squared
displacement is twice the squared displacement of that unit vector, which
again proves (5). For a singleton choose O_b=I. These arguments cover all
block dimensions; there is no unproved choice of a nearly aligned frame.

Take the skew matrix L_b of the shortest rotation, `exp(L_b)=O_b`.
The scalar inequality

    theta/(2 sin(theta/2)) <= pi/2,     pi^2 < 10

on [0,pi], with its continuous value at zero, gives

    |L_b r|^2 <= (5/2)|(O_b-I)r|^2,
    ||L_b||_op^2 <= (5/4)||O_b-I||_F^2
                  <= (5/2)E_b/kappa.                         (6)

Define, for all blocks using the same time parameter,

    z_i(t) = c_b + t u_b + exp(t L_b) r_i,     0<=t<=1.       (7)

All within-block distances are constant. Because the r_i sum to zero in
each block, the translation/rotation cross terms in total kinetic energy
cancel. Equations (4)--(6) give

    sum_i |z_i'(t)|^2 <= (5/2) E,
    |z_i''(t)| <= (5/2)E_b/sqrt(kappa).                      (8)

The second estimate follows from `|L_b^2 r_i|<=||L_b||_op|L_b r_i|`
and `|(O_b-I)r_i|^2<=E_b`. Rotation preserves all norms in these bounds.
For two different blocks and Z=z_i-z_j, therefore,

    |Z'|^2 <= 5E,             |Z''| <= M := 5E/(2sqrt(kappa)). (9)

This is the useful quadratic effect: E is a **squared** endpoint error,
so the acceleration of the correction to straight interpolation is of
second order in the displacement. Keeping the preserved pairs rigid is
essential; straight interpolation shortens and then re-expands them.

## 3. Every cross distance decreases

For any twice differentiable vector path Z with `|Z''|<=M`, its deviation
from its endpoint chord is at most `M t(1-t)/2<=M/8`. This follows by
integrating the Dirichlet Green kernel for the second derivative; the
integral of its absolute value is t(1-t)/2. Both endpoint norms here are
at most d, by endpoint contraction. Thus `|Z(t)|<=d+M/8`.

For f(t)=|Z(t)|^2, (9) gives

    |f''(t)| <= 2[5E + (d+M/8)M] =: L.

Since `integral_0^1 f'(v)dv=-Delta_ij`,

    f'(t) <= -Delta_ij + L integral_0^1 |t-v|dv
          <= -Delta_ij + L/2.                              (10)

For E<=kappa, put q=d/sqrt(kappa). Then

    L/2 <= E[185/32 + (5/2)q]
         <= E[8+2q^2] = C E.                               (11)

The last difference is exactly

    8+2q^2 - 185/32 - (5/2)q
       = 2(q-5/8)^2 + 23/16 > 0.                          (12)

The cross budget (1) and (10)--(11) prove nonincrease of every cross
distance. This proves the simultaneous motion (7), and Theorem1 follows
from the known motion comparison. There is no discretization in time,
threshold, variance or weight in the proof.

For Corollary2 use the accepted Procrustes identity from
[R1's rigidity proof, Section6](../gaussian_contraction_rigidity/PROOF.md).
There is an orthogonal Q with A^T BQ positive semidefinite and

    sum_i |A_i-(BQ)_i|^2 <= 2F/k = H.                       (13)

For completeness, putting U=A+BQ,V=A-BQ gives
`F=(1/2)tr(U^T U V^T V)+(1/2)tr((U^T V)^2)`;
the latter matrix U^T V is symmetric and U^T U>=kI. Estimate (13)
follows. Block scatter spectra, d, losses and congruence are invariant
under the endpoint translations/alignment. Apply Theorem1 in those frames.
Separate translations or a reflection of an endpoint preserve the Gaussian
hinges and ball volumes; they need not be undone by a motion in R3.

## 4. A uniform cover with arbitrarily many exact zero losses

Let epsilon=max Delta_ij and suppose every cross loss is at least
rho epsilon, where 0<rho<=1. Double centering of the loss matrix yields
`4F<=sum_(i,j)Delta_ij^2<=n^2 epsilon^2`. Hence the entire real parameter
domain

    n^2 epsilon^2 <= 2k kappa,
    C n^2 epsilon <= 2rho k                                (14)

satisfies Corollary2. The case epsilon=0 is congruence. At fixed n, positive
scatter bounds and diameter bound, all sufficiently small losses in this
sector are covered, even though the minimum loss over all pairs is zero.
There is no lower bound on atom weights.

This actually removes a partially tight sector from the finite all-variance
search. In an adverse input with a partition of this kind, at least one of
(3)'s guards must fail. It does not sign all partially tight faces:
components with preserved edges but without complete within-component
congruence are not automatically eligible; cross losses can be too small,
and positive block eigenvalues can collapse. Nor does this give a universal
finite atom budget or transfer a cubature certificate to diffuse hinges.
The existing indecomposable reduction and its effective height bounds are
unchanged. In particular, this is not a claim to resolve its remaining
connected tight-framework configurations.

## 5. A nonvacuous full paired-rank family

The control below calibrates the cover; it is not a separately proposed
catalogue of examples. Let

    V = {(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)},
    c_1=(-16,0,0), c_2=(16,0,0), c_3=(0,16,0).

For each b take the four source points c_b+v. The targets are

    y_(b,v) = (1-t)c_b + R_b(t)v,
    R_1=I, R_2=R_z, R_3=R_x,
    cos(angle)=(1-t^2)/(1+t^2), sin(angle)=2t/(1+t^2).

For every `0<t<=1/16384`, all eighteen within-block distances are
preserved and all forty-eight cross distances strictly decrease. The block
scatters are 4I, d^2=1160, C=588, and

    E=3072t^2+64t^2/(1+t^2) <= 3136t^2,
    delta_cross >= 192t,
    588*3136/192 = 9604 < 16384.                            (15)

Here is an interval proof of the loss bound, rather than a numerical grid.
For a cross pair put D=c_b-c_a, w=v-v'. Then |w|<=4,
`512<=|D|^2<=1024`, `|D|<=32`, and the difference between the rotated
offset pair and w has norm at most6t. For `0<t<=1/4`, expansion gives

    Delta >= t[(2-t)|D|^2-20|D|-48-36t]
          >= 199t >= 192t.

Equation(15) proves both guards throughout the stated interval.

The paired affine rank is six for every t>0: the within-block differences
of the first tetrahedron span the graph of I; those of the second and
third span the graphs of R_z and R_x. A linear functional vanishing on all
three would have to be a common fixed vector of both rotations, hence zero.
Moreover, no global target isometry makes straight interpolation contract:
preserved tetrahedron distances force its aligned edge vectors to remain
identical, requiring the same rotation on all three blocks, which they do
not have. Thus the new motion deals with a real limitation of straight
alignment, not only its numerical constant. This does not exclude other
previous positive motion classes or claim that these examples were open.

## 6. Reproducibility and trust boundary

[verify.py](verify.py) implements both guards with exact rational
arithmetic. It checks all losses, partition membership, block scatter
eigenvalue lower bounds on their actual ranges, and the global scatter
bound for the invariant guard. Rank, range projections, and PSD tests use
exact elimination and all principal minors, not floating-point spectra.
It reconstructs F both from Gram products and from double-centered losses.

The finite controls include one-, two-, and three-dimensional blocks;
singletons; equality; independent endpoint reflection and translation;
the twelve-site family with paired rank six; and rejected expansion,
broken-congruence, bad-scatter, excessive-displacement and insufficient-
cross-budget inputs. A univariate exact polynomial calculation checks the
whole family interval. No input from a private ledger or omitted corpus is
required. Runtime is subsecond to a few seconds, not a large search.

The written proof, rotation logarithms, continuous-motion comparison and
Procrustes argument are conventional mathematical trust boundaries. Exact
finite checks do not formalize them or supply independent acceptance.
Historical novelty of this precise certificate remains unverified.
