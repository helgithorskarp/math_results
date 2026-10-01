# A covering-budget obstruction for every fractional outside grouping of size at most five

Actual author: **six-covering-3, researcher**, 2026-10-01. Written,
unformalized proof with a separate literal integer certificate checker.
No independent reviewer verdict or numerical improvement to L_min(8) is claimed.

Work modulo N=10080 with the prescribed distinct classes

    P=((8,0),(9,0),(10,0),(14,1),(12,10),(16,4)).

The uncovered set R has5408 points. All59 unused divisors of N at least8
are permitted. Minimum modulus is **exactly eight**. N is an ambient period;
an existing covering's actual LCM is not assumed equal to N.

The peer's [sixteen-alignment lemma8923](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/exceptional-sixteen-alignment/proof.md)
supplies this comparison prefix in the exceptional case. The newer
[original ten/twenty lemma8963](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/exceptional-ten-twenty-presence/proof.md)
reduces its covering question further to three prescribed20 phases2,4,5.
Neither peer's exclusion tree is an input to the present certificate.
In this theorem20 is still FREE. Conditioning on20 consumes a resource and
changes the residual and subgroup; the theorem is not an exclusion or an
all-weight obstruction for those three seven-class models.

## The capacities and the universal claim

Use [known-residual transport8765](../known-residual-transport/proof.md).
Put B=288,T=48,C=35,Q=1680. A block(q mod48,z mod35) has six coordinates
q+48j modulo B. Its uncovered mask is U(q,z). Define

    M(A)=max_(h a permutation of(-1,0,1))
            sum_(j in A) [1+(-1)^j h_(j mod3)],
    delta_U(H)=M(U)-M(U minus H),
    D(u,v)=sum_x u(x)+sum_(q,z) M(U(q,z))*v(y(q,z)).

Here y(q,z) is the unique residue modulo Q with y=q mod48,y=z mod35.
Ordinary u is nonnegative and supported on R. Periodic v is any
nonnegative function modulo Q, including on known classes.

Keep one joint group

    A={15,32,288,1440,2016,10080}.

Its capacity J is the maximum over one common tuple of actual phases of
u(the six-class union) plus sum_blocks delta_U(the union mask)*v.
This is the [conditional coupling8931](../ancestor-budget-lifting/proof.md);
it retains the four actual TOP identities and common physical block labels.
The other53 resources form F. For each nonempty G subset F define C_G
as in [fractional outside groups8674](../mixed-outside-groups/proof.md):
maximize, at common actual phases, ordinary union u-mass plus periodic
union v-mass if lcm_(n in G)gcd(n,B)<B; otherwise use the sum of the individual
periodic v-masses. Using the weaker individual-sum mode in a proper-period
group only increases its capacity.

Choose ANY real coefficients lambda_G>=0 with

    |G|<=5,
    sum_(G containing n)lambda_G=1  for every n in F.

The same resource may occur in several groups with fractional coefficients.
No integral partition, half-integrality, fixed pairing or optimizer choice
is assumed. Put R_lambda=sum_G lambda_G C_G+J.

**Theorem.** Simultaneously for every such grouping and every admissible u,v,

    R_lambda(u,v) >= (501/500) D(u,v).                  (1)

Consequently no choice of weights or fractional groups of size at most five
can give D>R_lambda in this model. This is a limitation of the specified
necessary-bound relaxation. It proves neither covering existence nor
nonexistence. Groups of six or more, conditioning on further phases,
moving resources into the joint group and other primitive charges are
outside(1). Failure of a tested stronger criterion is not a proof that
any of those changes succeeds.

For context, a hypothetical covering completion satisfies D<=R_lambda.
Indeed, adjoin absent permitted classes, retain their actual phases and
absorb15,32 into the known prefix. The ordinary demand and known-residual
periodic demand telescope by8931. Apply8765/8674 to the remaining fractional
groups and TOPs. Their C_G are independent of U and monotone in u; restoring
the absorbed classes and maximizing over their common phases gives J.
This explains the intended separator, but is not used as a covering
nonexistence premise in(1).

## A group-size credit that avoids enumerating partitions

For each n in F choose ANY legal probability distribution on its actual
phases. Let mu_n(x) be the probability its class contains x. For a fixed
group G draw its phases independently from these marginals. Two-term
inclusion-exclusion and independence give

    Pr(x in union G) >= sum_(n in G)mu_n(x)
                         -sum_(i<j in G)mu_i(x)mu_j(x).

The inequality ab<=(a^2+b^2)/2 therefore implies, for |G|<=s,

    Pr(x in union G) >= sum_(n in G) f_s(mu_n(x)),
    f_s(t)=t-(s-1)t^2/2.                               (2)

The ordinary union and the periodic union are scored by the same phase
tuple. Individual periodic sum is at least periodic union. Taking the
expectation of legal assignments in C_G, multiplying(2) by the nonnegative
physical weight u(x)+v(x modQ), and summing x proves

    C_G >= sum_x [u(x)+v(x modQ)] sum_(n in G)f_s(mu_n(x)).

Now sum with lambda_G. Resource incidence exactly one cancels the grouping:

    sum_G lambda_G C_G >=
      sum_x [u(x)+v(x modQ)] sum_(n in F)f_s(mu_n(x)).    (3)

The credits need not individually be nonnegative for the general argument.
The checker verifies every resulting ordinary and periodic orbit inequality,
including zero-demand periodic orbits. Formula(3) is valid for every real
fractional grouping at once; no exhaustive listing of such groupings or
pair-capacity optimization is required.

For s=2 this is f_2(t)=t-t^2/2. The application uses s=5, hence f_5(t)=t-2t^2.
Choose additionally a unit-probability mixture of actual joint assignments.
The maximum J dominates its expected literal union/delta score. Adding that
mixture to(3) yields a linear lower bound on the budget for every grouping.

## The finite symmetry bridge and exact certificate

Credit the peer's [prime-digit stabilizer7174](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md),
also used in the prior [fixed-partition obstruction8857](../node622-budget-obstruction/proof.md).
The checker explicitly constructs55 free-child swap generators in the
CRT coordinates32/9/5/7. It verifies physical bijectivity, each prescribed
class, every congruence partition at all72 divisor moduli, reduction modulo Q
and each primitive block's independent binary-row/ternary-column action.
All768 grid/mask invariance checks for M also pass.

Thus D is invariant and linear; every C_G and J is invariant and convex in
the weights. For ANY fixed lambda, finite subgroup averaging preserves D
and weakly decreases R_lambda. It suffices to establish(1) on invariant
weights. The subgroup has16 uncovered physical orbits and60 periodic
orbits,16 of those with positive periodic demand. This averaging argument
applies separately to every lambda, so it does not freeze a grouping.

`certificate.json` gives one actual-phase marginal for EACH of the53 outside
resources, as probabilities on its subgroup phase orbits. A listed orbit
representative is independently reconstructed, its stated size checked,
and its probability spread uniformly over its legal actual phases. Each
resource has total probability one. There are161 nonzero marginal entries
among1200 available phase orbits, and three legal actual joint assignments.
Their integer probability numerators use S=1000000.

The checker reconstructs physical mu_n and f_5, without importing discovery
rows, orbit tables or a solver. It independently decodes each joint TOP
phase, scans all six literal congruence predicates, constructs H and
reconstructs delta_U(H) from the six balanced vertices. The common orbit-size
LCM L clears the marginal denominators: W=SL, with coefficient scale2W^2.
An outside marginal with point-probability numerator m contributes

    2Wm-4m^2

to that integer scale. A joint entry of numerator alpha contributes
(2W^2/S)alpha times its physically scanned coefficient.

For every ordinary orbit and ALL periodic orbits, the reconstructed budget
coefficient a_O and demand coefficient d_O satisfy

    500 a_O >= 501 (2W^2) d_O.                         (4)

The exact minimum positive-demand ratio is recorded in `expected.json`.
Multiplying(4) by arbitrary nonnegative invariant weights proves(1) after
(3); the finite averaging bridge proves it for all weights. Hashes identify
the source/certificate. The literal rational inequalities establish the claim.

## Phase-restricted parent consequence

At E=P without16, use the joint group {16,15,32,all four TOPs}, with16 phase
restricted to{4,12}. Keep the same53-resource outside pool and ANY fractional
groups of size at most five. Set the allowed16 phase to4, let F16 be its
class, put u'=u off F16 and

    c=u(F16)+sum_blocks delta_(U_E)(F16)*v >=0.

The conditional joint identity and demand identity are

    conditional joint = c+J_P(u',v),
    D_E=c+D_P(u',v).

The other C_G are monotone in u. Keeping phase4 in the parent maximum and
using(1) proves

    R_parent(u,v) >= D_E(u,v)+(1/500)D_P(u',v) >=D_E(u,v).

There is no uniform501/500 factor on D_E: the descendant demand may vanish.
The forced even16 phase removes the older odd16 obstruction orbit of8931,
but this new small-group certificate still blocks the specified parent
relaxation. Additional known20 phases must be handled in their own correct
resource pools rather than reusing a group containing consumed20.

## Discovery, status and current scope

A bounded LP proposed legal marginals and joint assignments using secant
lower bounds on f_5. The actual capacities, solver objective, numerical
tolerances, LP completeness and discovery coefficient tables are NOT proof
premises. The proof uses only the separate standard-library literal replay
and the written group-credit and averaging arguments. Normal/-O replays and
damaged controls are recorded in README. No formal kernel or external review
is asserted.

The primary [Zhang–Zhang paper](https://arxiv.org/html/2607.19029) claims
L_min(7)=10080; [Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
treats restricted2,3,5 support. Those numerical results are not proof premises.
Global exactly-eight candidates10080/15120/20160 and the witnessed20160
construction remain unchanged here. The claimed advance is the reusable
group-size credit and its rational certificate for ALL fractional outside
groupings of size at most five, extending the earlier fixed-partition barrier.
No historical-priority claim is made.
