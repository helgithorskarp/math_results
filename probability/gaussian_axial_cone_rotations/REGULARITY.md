# Removing the extra time-regularity condition from the matrix ball theorem

Complete author proof, 26 September 2026; independent review is pending.
This closes a qualification in the existing [matrix theorem M1](MATRIX_PATHS.md),
without changing its sections, support-cost bound, or Gaussian conclusion.
It adds no sufficient subclass and no improved cone constant. The full R3
Gaussian-majorisation problem remains open.

The original M1 already gives a continuous R5 contraction and every Gaussian
hinge under its absolutely continuous matrix-path hypothesis. It stated its
arbitrary-radius ball conclusions with an additional piecewise-analytic
finite-motion assumption. **Both ball conclusions hold without that extra
assumption.** The argument constructs smooth contracting approximations with
slightly scaled targets and then takes a volume limit. It does not assert an
exact piecewise-analytic motion between the original undamped endpoints.

## 1. Statement and the finite approximation to be proved

Retain exactly the notation of M1. Thus P,Q are compact subsets of R2
containing zero, C(P)={(zu,z):z>=0,u in P}, and T fixes C(P) and maps -b
to b on -C(Q). Suppose A:[0,1]->R^(2x2) is absolutely continuous and

    A(0)=-I, A(1)=I, ||A(t)||_op=1,
    J = integral_0^1 max_(u in P,v in Q) [-u^T A'(t)v] dt <= 2.   (1)

**Theorem G.** For every nonempty finite labeled x_i in C(P) union (-C(Q)) and
every choice of retained radii R_i>=0,

    |union_i B(Tx_i,R_i)| <= |union_i B(x_i,R_i)|,
    |intersection_i B(Tx_i,R_i)| >= |intersection_i B(x_i,R_i)|. (2)

For any restriction whose target sites Tx_i are pairwise distinct, there
are numbers rho_j in (0,1], rho_j->1, and piecewise-smooth contracting
motions in R5 from (x_i) to (rho_j Tx_i). Smooth here has the meaning in
[Bezdek--Connelly, Section 3 and Theorem 1](https://arxiv.org/pdf/math/0108098):
coordinates are infinitely differentiable except at finitely many parameter
values. The motions constructed below are analytic between these values.

The fixed finite restriction is essential in the approximation argument.
No uniform number of pieces, uniform positive site separation, or common
shrinking rate on the entire unbounded cone domain is claimed or needed.

## 2. Approximation on a norm sphere, including its nonsmooth strata

**Lemma 1.** Let a:[0,1]->V be an absolutely continuous curve in the unit
sphere of a norm N on a finite-dimensional real vector space V. There are
polygonal interpolants b_j, with the same endpoints, such that their radial
normalizations a_j=b_j/N(b_j) satisfy

    a_j -> a uniformly,       a_j' -> a' in L1.                (3)

The interpolants never meet zero for sufficiently fine partitions. For the
operator norm on real 2-by-2 matrices the normalized curves are continuous
and piecewise analytic, with finitely many pieces.

**Proof.** On dyadic partitions, let b_j interpolate a. Its derivative is
the interval average of a', so b_j'->a' in L1; uniform convergence follows
as well. These assertions follow first for step functions a' and then by
L1 approximation. For sufficiently fine partitions, N(b_j)>=1/2.

Put alpha_j=N(b_j), which tends uniformly to 1. We claim alpha_j'->0 in
L1. At almost every t where a is differentiable, every supporting
functional ell of N at a(t) satisfies ell(a'(t))=0: apply

    N(a(t+h)) >= N(a(t)) + ell(a(t+h)-a(t))

with positive and negative h, using N(a)=1. At almost every t where b_j
and alpha_j are differentiable, the same two-sided argument gives
alpha_j'(t)=ell_j(b_j'(t)) for every supporting functional ell_j at b_j(t).

Choose a subsequence with b_j'->a' almost everywhere. The supporting
functionals have dual norm one. Every cluster point of ell_j belongs to
the subdifferential at a(t), by passing to the limit in its supporting
inequality. It therefore annihilates a'(t). Hence alpha_j'->0 almost
everywhere along this subsequence. Moreover |alpha_j'|<=N(b_j'), and the
right sides are uniformly integrable because b_j'->a' in L1. Thus
alpha_j'->0 in L1. This subsequence is enough for the lemma; alternatively
the same argument for every subsequence gives convergence of the full
sequence. Finally,

    a_j' = b_j'/alpha_j - b_j alpha_j'/alpha_j^2

proves (3). In particular the argument does not assume differentiability
of the norm at a matrix with a repeated largest singular value.

On an affine matrix segment B(t), its operator norm is

    sqrt((tr(B^T B)+sqrt(tr(B^T B)^2-4 det(B)^2))/2).

It is bounded away from zero here. Splitting at the finitely many zeros
of the polynomial radicand, unless that polynomial vanishes identically,
gives finitely many analytic pieces for B/||B||_op. QED.

## 3. A small integrated distance error can be absorbed by scaling

Suppose q_i(t) are continuous piecewise-smooth paths, their squared pair
distances D_ij(t) are absolutely continuous, and, almost everywhere,

    D_ij(t)>=b>0,       D_ij'(t)<=e(t) for every pair,        (4)

where e>=0 is integrable and analytic between finitely many breakpoints.
Define

    r(t)=exp[-(1/(2b)) integral_0^t e(u) du].                 (5)

Then r q_i is a piecewise-smooth contracting motion. Indeed,

    (r^2 D_ij)' = r^2 [D_ij' - (e/b)D_ij] <= 0.            (6)

The initial configuration is unchanged, while the final configuration is
multiplied by exp[-||e||_1/(2b)]. Thus errors tending to zero in L1 cost
a final scaling tending to one. A derivative bound is used here; merely
knowing that two sampled endpoint distances are ordered would not suffice.

For a simple algebraic check, the interpolated difference w(t)=(1-t,t)
has D=1-2t+2t^2>=1/2 and D'=4t-2. Use e=(4t-2)_+. At t=3/4, the
unscaled derivative is 1, the bracket in (6) is -1/4, and halving the
scaling rate in (5) makes the bracket 3/8>0. These exact values illustrate
the required derivative correction, not a computational proof of the lemma.

## 4. Apply the approximation to a finite matrix motion

With one label, use the affine trajectory x_1->y_1 and rho_j=1; there are
no pair constraints and the one-ball volumes agree. Assume henceforth
that at least two labels remain and their targets y_i=Tx_i are distinct. Assign
the origin, if present, to the fixed cloud. Let P_0,Q_0 consist of zero
and the finitely many normalized transverse coordinates in the two clouds.
They are subsets of P,Q. Write

    k(t)=max_(u in P_0,v in Q_0) [-u^T A'(t)v],
    J_0=integral k <= J <=2.

Apply Lemma 1 to A. For its piecewise-analytic norm-sphere approximants A_j,
define k_j and J_j in the same way using the finite sections. If
M=max_(u in P_0,v in Q_0)|u||v|, then

    |k_j-k| <= M ||A_j'-A'||_op,
    ||k_j-k||_1 ->0,        J_j->J_0.                       (7)

Each k_j is nonnegative. On the analytic intervals from Lemma 1, the
candidate functions in this finite maximum are algebraic in the parameter.
Such functions have only finitely many changes of order, after identical
ones are identified. Consequently k_j has finitely many analytic pieces.

For J_j>0 put

    c_j(t)=-1+(2/J_j) integral_0^t k_j,
    d_j(t)=sqrt(1-c_j(t)^2).

For J_j=0 use c_j(t)=2t-1 instead. As in M1 choose a continuous row ell_j
such that ell_j^T ell_j=I-A_j^T A_j. This factor can be chosen piecewise
analytic with finitely many pieces: the rank-one positive semidefinite
matrix has algebraic entries, and on each nonzero interval one chooses a
nonzero row or column, its square-root factor, and continues its sign.
At a zero matrix the factor has norm tending to zero. Algebraicity gives
only finitely many zero or branch intervals. Thus there is no assumed
derivative convergence of these rank-one square roots.

Use the isometric moving-cloud embedding

    F_j(t)(v,z)=(A_j(t)v,c_j(t)z,ell_j(t)v,d_j(t)z).         (8)

Together with the fixed first cloud this defines q_i^j(t), with exact
endpoints x_i and y_i. The paths are continuous and analytic except at
finitely many values. Indeed c_j is analytic on each k_j piece; its
monotonicity confines its values +/-1 to possible initial/final intervals.
On their complement d_j is analytic, and on those intervals d_j is zero.
Endpoint differentiability is not required by the piecewise-smooth theorem.

If J_j<=2, these paths already contract, by the proof of M1. If J_0<2,
this occurs for all sufficiently large j and proves the desired approximation
with rho_j=1. The case J_0=0 is included. It remains to handle J_0=2 and
those j with J_j>2.

For this remaining case, (7) implies c_j->c uniformly, where
c=-1+integral_0^t k. The continuous matrix motion constructed from A,k
is contracting. Therefore all its squared distances are at least

    sigma^2 = min_(i<l)|y_i-y_l|^2 >0.

Squared distances in (8) depend only on A_j,c_j, not on the choice or
variation of ell_j. Within clouds they are constant. Across clouds, for
a=(z_a u,z_a) and b=(z_b v,z_b), they are

    |a|^2+|b|^2 - 2z_a z_b [u^T A_j(t)v+c_j(t)].           (9)

Thus they converge uniformly to the corresponding reference distances and
are at least sigma^2/2 for all sufficiently large j.

Let B=max z_a z_b over the finite cross pairs, with B=0 if there are none,
and put epsilon_j=(J_j-2)/J_j>0. Differentiating (9) gives the common bound

    (D_il^j)' <= 2B epsilon_j k_j.                          (10)

It also bounds the zero derivatives within each cloud. Lemma (4)--(6)
with b=sigma^2/2 and e=2B epsilon_j k_j now supplies a piecewise-smooth
contracting motion from (x_i) to (rho_j y_i), where

    rho_j = exp[-2B(J_j-2)/sigma^2] ->1.                    (11)

For indices with J_j<=2 use rho_j=1 as before. This proves the finite
approximation, including the critical support-cost equality J_0=2.

## 5. Volume limits and colliding target labels

Reverse each approximating contraction and apply the classical
Bezdek--Connelly Theorem 1 in ambient R5, with endpoint configurations in
R3 and the original individual radii. It gives (2) with y_i replaced by
rho_j y_i. Finite unions and intersections of balls have volumes continuous
in their centers and radii: indicators converge outside the finitely many
limiting boundary spheres, and a fixed large ball dominates them. Letting
rho_j->1 proves (2) when the targets are distinct. Zero radii follow either
from the same argument or by first increasing every radius by a positive
number tending to zero.

Target collisions do not permit division by sigma=0. Handle them before
the approximation, separately for the two inequalities. In each group of
coincident target centers:

* for unions retain a label of largest radius; the target union is unchanged,
  while deleting source balls can only reduce its union;
* for intersections retain a label of smallest radius; the target intersection
  is unchanged, while deleting source constraints can only enlarge its
  intersection.

Apply the distinct-target result to the retained labels and then these
inclusions. A single retained target gives a one-ball equality bound.
This also handles source collisions, since T is single-valued. Theorem G
is proved. No convergence rate uniform as targets collide is asserted.

## 6. The existing nonlinear reserve retains both ball conclusions

Let S=Id+e and V=lambda Id+g satisfy exactly [ROBUSTNESS (R1)](ROBUSTNESS.md):

    Lip(e)<=epsilon<1, Lip(g)<=eta, lambda>0,
    lambda+eta<=r<=1-epsilon,       eta<=lambda.

Then the map V T S^(-1) has both inequalities (2) on S(D), with its own
source and target sites, whenever T satisfies (1). No extra slack in these
inequalities is needed, even at equality.

To prove this, first remove coincident final targets VTx_i as in Section 5.
Distinct final targets imply distinct Tx_i, since V is a function. The
preceding construction gives a finite smooth contraction x_i->rho_j Tx_i.
Concatenate

    Sx_i -> r x_i -> r rho_j Tx_i -> rho_j VTx_i.            (12)

The first segment is precisely the old reserve lemma's contracting segment.
The middle is r times our approximating motion. The last is rho_j times
the old contracting segment r Tx_i->VTx_i. The same derivative tests apply;
the spatial errors need no smoothness since their values at each label are
constant. Apply the volume theorem to (12), pass to rho_j->1, and restore
the deleted labels. Scaling only the middle target without scaling the last
segment's endpoint would not justify the equality cases of the reserve.

The all-law/all-variance Gaussian conclusion of M1 and the original
robustness proof were already unconditional on this extra time regularity.
They are unchanged. The new argument completes the ball transfer on that
same existing class and its already defined nonlinear images.

## 7. Attribution, scope and verification boundary

The core matrix lift and support-cost estimate are from M1, source
`01b707bf3eb19f7bd44b8c45771fffa7b7651b55`; the nonlinear segments are from
ROBUSTNESS, source `a63bee4157117a2d2abb2a358119dfd57ebb5a9d`.
The volume-transfer theorem is Bezdek--Connelly's established result.
Radial normalization, supporting-functionals, integrated scaling and
continuity of finite ball volumes are standard tools, proved here in the
forms used. No priority claim is made for these general ingredients.

For unions alone there is already another route: the all-weight Gaussian
hinges and [Aishwarya--Li Theorem 5.1](https://arxiv.org/html/2609.07041v2)
give arbitrary radii without a time-regularity condition. The precise
logarithmic-weight limit is recorded in the team's
[GEOMETRIC_LIMIT.md](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md).
That positive-weight limit is a union formula. We do not infer the
intersection inequality by differentiating it or alternating unrelated
nonnegative hinge comparisons; Section 5 uses the independent intersection
part of the classical volume theorem.

This is a written geometric and real-analysis proof. No finite computation
establishes Lemma 1 or the limiting argument, and no new checker is presented
as doing so. The three rational values in Section 3 can be checked directly.
The original four proof files, five checkers and five expected-output files
are unchanged. `sha256sum -c SHA256SUMS` verifies their hashes and this
source's integrity. This author audit is not independent acceptance of M1,
its circular optimum, or the portfolio. No unrestricted deformation theorem,
new mesh class, new cost threshold, or full R3 result follows from this note.
