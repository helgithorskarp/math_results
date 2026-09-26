# Uniform localization by the size of a Gaussian majorisation defect

Complete author proof, 26 September 2026; independent review is pending.
This supplies a sign-preserving reduction of the unrestricted question to
compact, explicitly bounded finite configurations. It does not establish
the sign of that finite problem or provide a counterexample.

The earlier [minimax proof](PROOF.md) allows uniquely diffuse optimizers.
Its support-net approximation depends on the diameter of the given support.
Here a shifted spatial partition first removes that dependence: the support
radius and atom count depend only on the permitted loss in a violation.
Conditioning changes the input law, but keeps the original contraction on
the selected support. No optimizer is asserted to be exactly atomic.

## 1. Statement of the finite frontier

Let gamma_s be the Gaussian density with covariance s I_3. For a bounded
probability law mu and a 1-Lipschitz map T on its support, write

    f = mu * gamma_s,       g = (T#mu) * gamma_s,
    H_f(a) = integral (f-a)_+,
    Delta_s(mu,T) = sup_{a>=0} [H_f(a)-H_g(a)]_+.

Let D be the supremum of Delta_s over all these laws, contractions and s>0.
Common spatial scaling shows that one may fix s=1: under z=sqrt(s) w,
the transformed threshold is a s^(3/2), and the hinge integral is unchanged.
In particular 0<=D<=1. The full question is precisely D=0.

For an integer k>=1 put N=k^6 and R=2k. Define D_k to be the maximum of

    H_(sum_i w_i gamma_1(. - x_i))(a)
       - H_(sum_i w_i gamma_1(. - y_i))(a)                       (1)

over the following finite-dimensional parameter set:

    w_i>=0, sum_i w_i=1,             1<=i<=N,
    x_1=y_1=0,                      |x_i|,|y_i|<=R,
    |y_i-y_j|<=|x_i-x_j|             for all i,j,
    0<=a<=(2 pi)^(-3/2).

Zero weights and repeated sites are allowed. The distance constraints force
equal output sites whenever input sites coincide, so they define a genuine
map on the input support. If a globally defined map is desired, Kirszbraun's
extension theorem supplies it. The threshold zero makes D_k nonnegative.

**Theorem 1 (uniform compact finite frontier).** Each maximum D_k is
attained, the sequence is nondecreasing, and

    0 <= D-D_k <= ((3+sqrt(3)) sqrt(2/pi))/k < 4/k.              (2)

Consequently, for any particular violation of size delta>0, every integer
k>=8/delta admits a variance-one violating law with at most k^6 atoms,
both supports in B(0,2k), and hinge gap at least delta/2. A matched site
may be placed at the origin. The resulting threshold is allowed to change.

Thus the radius is O(delta^(-1)) and the number of atoms is O(delta^(-6)),
independently of the original support extent, atom count, or variance.
These are deliberately coarse bounds; they are not a practical enumeration
claim. No value D_k>0 or D_k=0 is established here beyond trivial cases.
Verifying a finite number of D_k=0 would only bound D, not prove D=0.

## 2. The partition inequality: only source overlap costs an error

We first work at a fixed variance and with a finite measurable partition
{Q_i} of the source support. Put

    p_i=mu(Q_i),       mu_i=mu|Q_i / p_i                         (p_i>0),
    f_i=p_i (mu_i*gamma_s),
    g_i=p_i ((T#mu_i)*gamma_s).

Then f=sum_i f_i and g=sum_i g_i. Both f_i and g_i have mass p_i.
Also choose a measurable partition {E_i} of observation space with the
same labels. Extra labels with zero component are permitted. Define

    Lambda = sum_i integral_(R3 \ E_i) f_i.                     (3)

**Lemma 2.** For every a>=0,

    H_f(a)-H_g(a)
      <= sum_(i:p_i>0) p_i [H_(f_i/p_i)(a/p_i)
                                  - H_(g_i/p_i)(a/p_i)] + Lambda. (4)

In particular,

    Delta_s(mu,T) <= sum_i p_i Delta_s(mu_i,T) + Lambda.          (5)

The lemma does not require the contraction assumption. It needs no
separation of the target components and no target partition.

**Proof.** For finitely many nonnegative numbers u_i and a>=0, set

    I_a(u)=(sum_i u_i-a)_+ - sum_i (u_i-a)_+.

If at least one term exceeds a, subtracting a only once is at least as
large as subtracting it from every active term. If no term exceeds a,
the sum on the right is zero. Hence I_a(u)>=0. For any selected label j,
the 1-Lipschitz property of t -> (t-a)_+ gives

    0 <= I_a(u) <= (u_j+sum_(i!=j)u_i-a)_+ - (u_j-a)_+
                 <= sum_(i!=j) u_i.                            (6)

Apply the upper bound to the source with j=i on E_i and integrate. Its
interaction I_f is at most Lambda. Apply only nonnegativity to the target:
I_g>=0, even when target components overlap completely. Therefore

    H_f(a)-H_g(a) = sum_i[H_(f_i)(a)-H_(g_i)(a)] + I_f-I_g
                 <= sum_i[H_(f_i)(a)-H_(g_i)(a)] + Lambda.

Finally H_(p h)(a)=p H_h(a/p), proving (4) and then (5). QED.

This is not an assertion that majorisation survives arbitrary conditioning.
The source interaction is retained as an explicit error. In (4), forgetting
the rescaled threshold a/p_i is also incorrect. The two-component hinge
interaction used in the team's [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
is the elementary special case of (6).

## 3. A support-independent source interaction bound

Let ell>0. For u uniform in [0,ell)^3, partition R3 into half-open cubes

    Q_j(u)=u+ell j+[0,ell)^3,          j in Z3.

Use these cubes both for the source components and for their observation
labels E_j. Only finitely many source components have positive mass because
the original support is bounded. Observation cubes with zero source mass
still receive their labels; they cause no difficulty in (6).

For independent X~mu and Z~gamma_s, the error in (3) is exactly

    Lambda(u)=Pr{X+Z and X have different cube labels}.           (7)

For fixed real x,z in one coordinate, the fraction of shifts in [0,ell)
that place x and x+z in different intervals is

    min(1, |z|/ell).                                             (8)

For |z|<ell, the shifts crossing the intervening interval boundary have
total length |z|; for |z|>=ell, the labels always differ. Boundary choices
affect a null set of shifts. Using the union bound for the three coordinate
events and then E|Z_j|=sqrt(2s/pi), Tonelli gives

    E_u Lambda(u) <= (1/ell) sum_(j=1)^3 E|Z_j|
                  = 3 sqrt(2s/pi)/ell.                          (9)

No density or regularity of mu is needed. In particular there is a shift u
with Lambda(u) at most the right side. The same chosen shift controls all
hinge thresholds, since Lambda is independent of a.

Combining (5) and (9), at least one occupied cube satisfies

    Delta_s(mu_i,T) >= Delta_s(mu,T)-3 sqrt(2s/pi)/ell.           (10)

More strongly, for any specified positive hinge gap delta at threshold a,
(4) selects a cube with normalized gap at least
delta-3 sqrt(2s/pi)/ell at threshold a/p_i. This follows because the
right side of (4), after subtracting the error, is a mass-weighted average
with sum_i p_i=1. The selected cube can depend on the threshold.

The locality comes entirely from the source noise: points and their noisy
observations usually share a large cell after averaging the grid shift.
The target can merge distant source cells; its additional hinge interaction
only improves inequality (4).

## 4. Quantizing the selected cube preserves the contraction

Suppose mu is now supported in one cube of side ell. Divide each axis into
m equal half-open intervals. For every occupied small cube select one
point x_j of the original support in it, move that cube's probability mass
to x_j, and give it the output y_j=T(x_j). Call the resulting law mu'.
There are at most m^3 selected sites. Every moved point travels at most

    r=sqrt(3) ell/m.                                            (11)

The original and selected output points are also at distance at most r,
because T is 1-Lipschitz. In particular, all selected pairs obey the exact
original distance inequalities. There is no separate rounding of targets.

For Gaussian translates, with total variation equal to half the L1 norm,

    TV(gamma_s(. - x), gamma_s(. - x'))
                                <= |x-x'|/sqrt(2 pi s).          (12)

Indeed integrate the directional derivative of the Gaussian along the
segment; its L1 norm in a unit direction is sqrt(2/(pi s)). Convexity of
the L1 norm under averaging transfers (12) to the coupling just described.
For equal-mass densities p,q, at every a>=0,

    |H_p(a)-H_q(a)|<=TV(p,q).                                   (13)

For one direction, the pointwise hinge difference is bounded above by
(p-q)_+; integrate and then interchange p,q. Thus the source and target
hinge differences each change by at most r/sqrt(2 pi s), uniformly in a.
It follows that

    |Delta_s(mu,T)-Delta_s(mu',T)|
                   <= sqrt(6/pi) ell/(m sqrt(s)).                (14)

The same error bounds the change of any specified signed hinge difference.
This is the earlier support-net estimate, now applied to a support whose
size is bounded uniformly by the allowed localization error.

## 5. Proof of the theorem and compactness of the frontier

Given k>=1, apply Section 3 with ell=k sqrt(s). Subdivide the selected
cube using m=k^2 intervals per axis. Equations (10) and (14) produce at
most k^6 sites and lose at most

    3 sqrt(2/pi)/k + sqrt(6/pi)/k
                      = (3+sqrt(3)) sqrt(2/pi)/k.                (15)

Choose a selected site x_1 and translate the input by -x_1 and the output
by -T(x_1). Separate endpoint translations preserve all pair distances and
hinge integrals. All input sites are within sqrt(3) ell of x_1; the same
bound holds for their images by contraction. Scale both endpoints by
1/sqrt(s), changing variance to one. Their radii are at most sqrt(3) k<2k,
and their first pair is at zero. Padding with zero-weight copies at zero
gives a feasible point of (1). The transformed threshold is
s^(3/2) a/p_i when following a specified original witness.

The loss is strictly less than 4/k: using sqrt(3)<7/4 and pi>3, its squared
coefficient is less than (19/4)^2(2/3)=361/24<16. This proves the upper
bound in (2) for every original law and hence for their supremum D. The
lower bound follows because every feasible finite configuration is an
admissible bounded-law comparison.

For attainment, the weights form a closed simplex, both lists of sites
lie in closed radius-2k balls, and the anchor and pair-distance constraints
are closed. Thus the parameter set is compact. All mixture densities are
at most C=(2 pi)^(-3/2), so thresholds greater than C have zero hinge.
On the compact range 0<=a<=C, the integrands in (1) are continuous in all
parameters and dominated by an integrable Gaussian envelope, for example

    C exp(-((|z|-2k)_+)^2/2).

Dominated convergence proves joint continuity, including at zero threshold,
zero weights and colliding sites. Hence the maximum is attained.
Increasing k permits padding with further zero-weight sites and increases
the radius bound. Therefore D_k is nondecreasing, and (2) gives D_k -> D.
The fixed-gap consequence follows from (15) and k>=8/delta. QED.

## 6. What this reduction supplies and what remains

The full bounded-law question is equivalent to D_k=0 for every integer k.
Unlike qualitative finite approximation, (2) gives a uniform error bound
independent of the initial law's support extent. It makes any violation of
a specified size detectable in one explicit compact finite-dimensional
parameter region. It does not restrict the optimizer of the original
minimax problem to that many atoms or preserve that optimizer's value.

The selected sites are actual support representatives; they are not asserted
to lie on a fixed rational grid. Independently rounding both endpoints can
break a contraction, even for an isometry. The earlier [strict rational
witness reduction](../gaussian_majorisation_rank_abel/PROOF.md) still applies
qualitatively, but a fixed coordinate denominator is not supplied here.
No finite parameter search or Gaussian integral optimization was performed.

The [fixed-atom equivalence](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
retains its arbitrary rare packet and exact mass condition. Our conditioning
can select a cell away from that atom, so it does not preserve that condition.
It is a complementary reduction, not a new positive adjunction theorem.
The unique diffuse spherical optimizers in [PROOF.md](PROOF.md) remain
compatible with these approximate, sign-preserving finite witnesses.

The complementary [rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md)
can take such a finite witness as its input. Its extension preserves the
source convex hull when the source spans R3, but can add an unbounded number
of mesh vertices. Thus the k^6 bound belongs to the present finite witness;
it must not be transferred to the mesh after that further reduction.
The compact frontier (1) makes no extremality or rigidity assumption.

The new error bound does not have the threshold-dependent small-variance
scale required for a new Kneser--Poulsen conclusion. No positive class from
the axial, ordered-weight or stability lanes is enlarged. In particular,
the unrestricted Gaussian conjecture, and the sign of (1) in general,
remain open. The useful next obligation is a sign argument on this compact
finite frontier or a rigorously negative instance, not a larger catalogue
of positive samples.

The proof uses elementary hinge superadditivity, a shifted-grid averaging
argument, Gaussian translation bounds and compactness. No priority is
claimed for these ingredients. [SOURCES.md](SOURCES.md) records the primary
problem, related team reductions and validation boundaries. The small exact
audit checks finite partition controls, grid crossing and rounding pitfalls;
the universal theorem rests on the written argument, not finite tests.
