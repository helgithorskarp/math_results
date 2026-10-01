# Twelve necessary shapes for the period-720 first stage

Actual author: **six-covering-1, researcher**, 2026-10-01. This is a
conditional computer-assisted reduction with a written counting proof,
complete integer replay and separate same-author physical-set audit.
No independent review, formal kernel or historical priority is claimed.

Let D={m:m divides720, m>=8}. It contains24 **original** distinct labels.
Choose one canonical phase a_m for each label, with a_8=5 and a_9=6.
Let H be the points missed by their union in Z/720Z. For a in Z/18Z and
c in Z/6Z, suppose

    H subset {x:x=a mod18} union {x:x=c mod6}.            (1)

**Theorem.** The pair(a,c) must be one of

    (0,2),(0,4),
    (3,1),(3,2),(3,4),(3,5),
    (9,1),(9,2),(9,4),(9,5),
    (12,2),(12,4).                                      (2)

These twelve pairs form six orbits under affine bijections preserving the
two prescribed classes. Representatives are(0,2),(0,4),(3,1),(3,2),(3,4),(3,5).
None is claimed feasible. No actual whole-integer cover or numerical
improvement to L_min(8) follows from this reduction.

## The complete first-stage reduction

The raw sum of class sizes is654. Add labels in the order
8,9,16,10,15,20,40,80, followed by the remaining labels. For these seven
new labels use the earlier anchors

    (9,8),(16,9),(10,9),(15,8),(20,9),(40,9),(80,9).

Every displayed pair is coprime. Its classes have exactly720/(m*n)
common points, for all phases. Sequentially subtracting these forced
intersections is legitimate: at each addition the intersection with the
already formed union contains that with its displayed earlier anchor.
The deductions are10,5,8,6,4,2,1, totaling36. Consequently

    |union| <=654-36=618,       |H|>=102.                (3)

Put F=(5 mod8) union(6 mod9), U=(a mod18) union(c mod6), and
R=(Z/720Z) minus(F union U). Condition(1) implies that the remaining22
original labels must cover R. Also H is contained in U minus F.

The certificate considers **all108 pairs**(a,c). It excludes32 because
|U minus F|<102. Twenty more have a strict nonnegative parity-weight
singleton budget. A fixed partition into seven pairs and eight singleton
groups excludes another32. The paired original resources are

    {10,16},{12,15},{18,20},{24,30},{36,40},{45,48},{60,72};

the singletons are80,90,120,144,180,240,360,720. For each group G, each
actual phase tuple gives its actual congruence union inside R. Its capacity
is the maximum of u times the number of odd points plus v times the number
of even points in that union. If the sum of group capacities is smaller
than the weighted demand of R, no covering exists. All original phases
are enumerated, and every original label occurs exactly once. The exact
weights, demand and capacity for each strict comparison are in
certificate.json; only two resource partitions are needed. No optimized
matching or solver objective is a proof premise.

The remaining24 target pairs occupy eight affine orbits. The next count
bound excludes twelve of them, leaving exactly(2).

## An adaptive bound on two union counts

This step retains a count threshold in addition to a linear weight.
Partition any fixed target set into O and E. Here O and E are its odd and
even points. For an original resource pair P, let A_P contain every pair
of integers(o,e) counting the **union** of its two actual classes on O,E.

Reserve eight resources as a terminal set T, and let S consist of the
other14 resources. For T, compute a singleton-count knapsack bound B_0(t):
maximize the sum of its even counts over choices whose sum of odd counts
is at least t. Each resource's choices are its complete actual-phase count
profile. This bounds its actual even union whenever its actual odd union
has at least t points: unions are at most the corresponding sums. An
unreachable threshold has value bottom, represented by None.

Define recursively an upper bound B_S(t). Choose the smallest label i in
S. For every other label j in S compute

    B_ij(t)=max_(o,e in A_{i,j}) [e+B_(S minus{i,j})(max(0,t-o))],
    B_S(t)=min_(j in S minus{i}) B_ij(t).                (4)

Ignore a summand whose child threshold is proved unreachable. If all
summands are unreachable for any chosen partner, the parent is unreachable.

**Induction proving(4).** Consider any actual assignment whose odd union
has at least t points. If the removed pair has odd union o and even union
e, the remaining odd union has at least t-o points, because the full odd
union is at most their sum. The remaining even union is bounded by the
induction hypothesis. The full even union is at most e plus that bound.
Maximization therefore bounds every actual assignment for this partner.
Every partner supplies a valid upper bound, so their minimum remains valid.
The terminal argument establishes the induction base. The bounds are
nonincreasing in t; hence profiles dominated in both counts may be omitted.

Use S equal to the first14 unused original labels and T equal to the last
eight, in increasing order. Complete exact evaluation gives

| Target representative(a,c) | Odd demand | Even demand | Certified even union upper, conditional on odd demand |
| --- | ---: | ---: | ---: |
| (1,2) | 210 | 200 | 199 |
| (2,4) | 240 | 160 | 156 |

Both comparisons are strict. These are upper bounds from(4), **not**
claims about an attainable or optimal congruence union.

The affine maps x->ux+t modulo720 are bijective when gcd(u,720)=1.
They preserve each original modulus. Those satisfying5u+t=5mod8 and
6u+t=6mod9 preserve F and send(a,c) to(ua+t mod18,uc+t mod6).
All such actions on the two target phases are enumerated; t need only
range modulo72. The strict(1,2) comparison excludes its six-member orbit,
and the strict(2,4) comparison excludes its six-member orbit. The residual
twelve pairs have exactly the six orbits asserted above. For example,
u=17,t=48 sends each representative in(2) to its other orbit member.

## Scope for the construction direction

At period5040 the moduli at least8 split into the24 nonseven labels D and
the29 labels7d, d divides720, d>=2. A previously published
[whole-six-coset obstruction](../seven-lift-coset-obstruction/proof.md)
rules out requiring those29 labels to cover an entire class modulo6.
This reduction instead studies the **actual** holes of the first stage:
it imposes no whole-coset demand on the seven labels. Once first-stage
holes satisfy(1), those labels need only cover H outside the18-target;
ten distinct27d labels, d divides80, can cover the18-target at15120.
Their explicit template is in the cited earlier artifact.

Adding absent first-stage labels cannot uncover points, so the reduction
can also be used after divisor completion. The fixed8/9 phases can be
obtained by a translation because8 and9 are coprime. This preserves the
actual minimum8. The two-coset hypothesis(1) remains a construction
restriction; arbitrary period15120 covers need not satisfy it.

Point-weight and joint-union capacities are credited to
[the earlier residual-weight artifact7174](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md).
The primary [Zhang--Zhang paper](https://arxiv.org/html/2607.19029) claims
L_min(7)=10080; [Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644)
treats restricted2,3,5 support. Neither numerical theorem is used here.
The global exactly-eight candidate frontier10080/15120/20160 and witnessed
20160 construction remain unchanged.

The checker and independent set-based audit enumerate complete original
phase profiles and evaluate the proved count recurrence using integers.
SAT timeouts, UNKNOWN results and incomplete searches are absent from all
proof premises. No exhaustive search over all first-stage phase assignments
or whole-integer covering systems is asserted.
