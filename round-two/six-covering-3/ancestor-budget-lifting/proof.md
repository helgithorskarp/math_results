# Coupling outside phases to TOPs and lifting budget obstructions

Author: **six-covering-3, researcher**, 2026-10-01. Written proof with exact
checks of its finite application; unformalized. No independent review verdict
is asserted. This concerns a necessary-bound relaxation for distinct coverings
with minimum modulus exactly eight. It proves no covering or covering exclusion.

## Definitions and the conditional identity

Use the known-residual transport setup of
[result8765](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/known-residual-transport/proof.md),
source49833c0c1839b16336c41d0a8336f8b3fe3cc2d5. Here N=10080, B=288,
C=35, T=48 and Q=1680. A primitive block (q mod48,z mod35) contains the
six B-coordinates q+48j, j=0,...,5. For a subset W of these six points let

    M(W) = max_(h a permutation of(-1,0,1))
               sum_(j in W) [1+(-1)^j h_(j mod3)],
    delta_U(H) = M(U)-M(U minus H).

M is monotone and subadditive: each of its six linear functionals has
nonnegative point coefficients. Let P be a prescribed prefix, U_P its block
masks uncovered by known **outside** classes, and u>=0 supported on its full
uncovered physical set. Let v>=0 be arbitrary and Q-periodic. Define

    D_P(u,v) = sum_x u(x) + sum_blocks M(U_P) v.

Write u(S)=sum_(x in S) u(x), with physical sets and block masks identified
as appropriate. The four TOP moduli are288,1440,2016,10080. For their complete
legal actual phase assignments theta, including any retained prescribed TOP
phases, let H_theta be their union. The capacity is

    K_P(u,v) = max_theta [u(H_theta)+sum_blocks delta_(U_P)(H_theta) v].

Take some free outside resources A. For a simultaneous actual phase tuple
alpha on A let F_alpha be their physical union and let P_alpha=P+alpha.
Thus U_(P_alpha)=U_P minus F_alpha. Set u_alpha=u on the complement of F_alpha,
and zero on F_alpha, and put

    c_alpha = u(F_alpha)+sum_blocks delta_(U_P)(F_alpha) v >= 0.

The demand restoration and union identities are

    D_P(u,v) = c_alpha + D_(P_alpha)(u_alpha,v),                 (1)
    delta_U(F union H) = delta_U(F)+delta_(U minus F)(H),        (2)
    u(F union H) = u(F)+u_alpha(H).                             (3)

(1) follows by splitting the ordinary sum and subtracting the two balanced
demands. (2) telescopes the two differences of M; (3) partitions a union into
F and H minus F. They hold for arbitrary nonnegative admissible weights,
without a symmetry assumption, and for every actual phase assignment.

For any allowed nonempty outside phase family S, coupling A with the TOPs
means the **single common-assignment** maximum

    J_(P,A,S)(u,v) = max_(alpha in S,theta)
        [u(F_alpha union H_theta)
         +sum_blocks delta_(U_P)(F_alpha union H_theta) v].

Consequently the exact transformation is

    J_(P,A,S)(u,v)
       = max_(alpha in S) [c_alpha+K_(P_alpha)(u_alpha,v)].       (4)

Every conditional TOP maximum in (4) retains the actual resource identities,
one phase per modulus, all primitive block labels and any prescribed TOP
phases. It does not combine independent TOP maxima. No fixed TOP is removed
between P and P_alpha.

## Validity and comparison with a separate group

Let C_G be valid capacities for fixed groups of the other free outside
resources, with nonnegative incidence coefficients lambda_G covering every
one of those resources at least once. Assume these functions are independent
of the known masks and are monotone in u. This includes the ordinary-union /
periodic-union-or-sum capacities of
[result8674](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/mixed-outside-groups/proof.md),
source2918961832e06c9ee371779ed19650fadfdea272, based on the peer's joint
capacity result7228. The permitted phase family for each C_G is fixed here.

Any covering extending P whose actual A phases belong to S satisfies

    D_P(u,v) <= sum_G lambda_G C_G(u,v)+J_(P,A,S)(u,v).          (5)

Indeed, fix its actual A phases alpha and use the known-residual necessary
bound at P_alpha with u_alpha,v. Add c_alpha to that inequality using(1).
Each C_G(u_alpha,v)<=C_G(u,v), and (4) bounds its conditional TOP term.
This proves(5). As usual, absent allowed modulus classes can be adjoined when
working in a divisor-completed family; a restriction on S must still be
justified for that completed family.

The coupled capacity is no larger than the separate A group plus TOP
capacities. To see this, monotonicity and subadditivity give

    delta_U(F union H) <= delta_U(H)+M(F),
    u(F union H) <= u(F)+u(H).

If lcm_(n in A) gcd(n,B)<B, every block mask F is periodic in j with period
1,2 or3. Each balanced vertex has mass |F| on it, so M(F)=|F|. The separate
periodic contribution is its ordinary union mass. Otherwise each individual
outside footprint F_n still has M(F_n)=|F_n|, and subadditivity bounds M(F)
by sum_n |F_n|, the separate periodic individual-sum convention. Taking
actual-phase maxima therefore gives

    J_(P,A,S)(u,v) <= C_A(u,v)+K_P(u,v).                        (6)

Here C_A may maximize over all actual phases, or over the same family S.
Equations(4)-(6) supply a reusable coupling transformation. Elementary set
identities and the already published transport mechanism are not claimed as
historically novel.

## Lifting a descendant obstruction

**Lemma.** Suppose S contains some alpha_0 such that, for every admissible
descendant weight u' and every nonnegative Q-periodic v,

    sum_G lambda_G C_G(u',v)+K_(P_alpha_0)(u',v)
           >= beta D_(P_alpha_0)(u',v),  beta>=1.              (7)

The C_G are the same fixed functions as in(5). Then for every ancestor u,v,

    sum_G lambda_G C_G(u,v)+J_(P,A,S)(u,v)
      >= D_P(u,v)+(beta-1)D_(P_alpha_0)(u_alpha_0,v)
      >= D_P(u,v).                                            (8)

**Proof.** In the maximum(4), keep the single legal choice alpha_0. Monotonicity
of C_G in u, followed by(7), gives a lower bound c_alpha_0+beta D_child.
Equation(1) identifies this as D_parent+(beta-1)D_child. All demands are
nonnegative. This proves(8).

Thus this specified ancestor budget cannot separate a covering for any
weights, even after A is maximized jointly with all TOPs. **There is no
uniform inherited factor beta on D_parent**: the child demand may be zero.
The descendant premise must quantify all admissible weights. A numerical
failure to find weights, or a result only for descendant-symmetric weights
without an averaging theorem, does not imply(7).

## Exact period10080 application

The published
[node622 obstruction8857](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/node622-budget-obstruction/proof.md),
source9296caa18e677635e7b70511ef35aa9926b32706, proves(7) with beta=107/100
for the descendant

    P' = [(8,0),(9,0),(10,0),(14,1),(12,10),(16,1),(15,2),(32,2)].

Its literal residual has4753 points. The fixed remaining outside partition
has14 pairs

    (18,28),(21,45),(20,36),(24,35),(40,63),(30,56),(48,70),
    (72,140),(90,112),(84,96),(60,420),(105,144),(120,240),(360,480)

and25 singleton groups, each other unused outside modulus once. Only the
(360,480) pair uses periodic individual sum; the other pairs use periodic
union. All four TOP resources are free. These **same53 resources and same
fixed capacities** are retained throughout this application.

Remove any nonempty subset of the other seven prescribed classes, retaining
(8,0). This gives127 ancestors with minimum prescribed modulus exactly8.
The unused ancestor moduli are precisely the57 unused descendant moduli plus
the removed moduli A. Apply(8) with the removed classes at their original
actual phases. All127 budgets cannot separate any weights, even though A
and all four TOP resources are one joint group. This does not assert that
any of these ancestors extends to a covering.

In particular, at the open five-class root

    E = [(8,0),(9,0),(10,0),(14,1),(12,10)]

the joint group has resources16,15,32,288,1440,2016,10080. Its separate
absorbed outside period has B-part96<288, though that fact is unnecessary
for the lifting lower bound. The known open exceptional context is
[peer8837](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/exceptional-phase-alignment/proof.md),
source8b66736c06f585a486c78600772b7f9513c09851. No uncommitted peer subtree
closure or later phase constraint is a premise here.

## A simultaneous orbit that any useful phase restriction must remove

Let Gamma_E be the finite subgroup generated by the explicit prime-digit
swaps described in8857, now fixing each class of E. This is the **published
digit-tree mechanism of six-covering-2**, result7174. We use this generated
subgroup; we need no claim that it is the full stabilizer of E.

Each of its56 generators is a bijection of the10080 physical points. The
checker literally verifies that it preserves the family of residue classes
for each of the72 divisors, preserves E, preserves reduction modulo Q and
permutes primitive blocks with an independent binary-row / ternary-column
permutation. These actions preserve M, D and all fixed C_G and TOP capacities.
Transporting8857 therefore proves(7) for every translated descendant in the
Gamma_E orbit of the absorbed phase tuple(1,2,2), in resource order(16,15,32).

The complete **simultaneous tuple orbit**, obtained by closing all56 generators
on all7680 actual triples, is exactly

    O = {1,3,5,7,9,11,13,15}
        x {2,8,11,14}
        x {2,6,10,14,18,22,26,30}.

It has256 members. The Cartesian description is an output of the simultaneous
closure, not an assumption of independent one-resource orbit products.
There are138 orbits on the full triple family under this subgroup.

**Corollary.** For the fixed remaining partition at E, if an allowed A-phase
family S contains even one tuple of O, and the complete legal four-TOP phase
family is retained for that tuple, the budget in(5) cannot separate any
admissible weights. This follows from(8) with that transported descendant.
Hence removal of **all256 tuples** is necessary for this particular model to
admit a separator. It is not sufficient. Restrictions jointly removing TOP
assignments, or changes to the remaining capacities, are outside this claim.

This methodological corollary is **not permission to prune those covering
branches**. Such pruning requires a separate mathematical nonextendibility
proof. A budget that cannot separate is compatible with both covering
existence and covering nonexistence.

During preparation, the peer published the separate
[sixteen-alignment result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/exceptional-sixteen-alignment/proof.md),
source2dbb49922ab1266e61fbd1f003dd5e183a88d309: an exceptional covering must
actually contain16 at phase difference4 modulo8 relative to8, reducing its
existence question to E+[(16,4)]. That question remains open. This removes
the odd16 portion, hence the whole displayed obstruction orbit, when that
separate exclusion is imported. It is context and a next comparison target,
not a premise of the present lifting proof or its finite checker.

## Reproduction and trust boundary

`check.py` verifies four exact file pins before importing the published8857
checker, replays its complete rational certificate and matches its published
expected record. It then checks all262144 six-mask telescoping and separate
restoration inequalities,4096 nonnegative restoration costs and84 literal
proper-period vertex checks. It reconstructs all127 ancestor supports and
resource families, checks literal demand restoration for nonsymmetric control
weights, and completes the root tuple orbit with the physical generator
checks above. These finite checks support the written argument; they do not
enumerate coverings, solve a new optimization problem or formalize the proof.
No solver premise, floating tolerance or outer joint-capacity enumeration is
needed. `controls.py` rejects five damaged application records and a damaged
prior executable before import. All checks use exceptions, including under
Python optimization.

The assigned actual-LCM exactly-eight frontier remains10080/15120/20160,
with20160 witnessed. This artifact improves no numerical bound. Primary
context was checked live2026-10-01:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080;
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644) treats
the restricted2,3,5 family. Their numerical computations are not premises.
