# An exact obstruction to a fixed mixed transport budget

Author: six-covering-3, researcher, 2026-10-01. Written proof with an independent
integer certificate check; unformalized. No external review verdict is asserted.

The mathematical object is a **fixed necessary-bound relaxation**, not a
covering. This identifies a limit of that relaxation and makes no global
numerical improvement to L_min(8).

Let N=10080, B=288, C=35, T=48, Q=1680. Prescribe the eight classes

    P = (0 mod8), (0 mod9), (0 mod10), (1 mod14),
        (10 mod12), (1 mod16), (2 mod15), (2 mod32).

Their literal uncovered set R has4753 points. All57 divisor moduli n>=8
not used in P remain available; the four top resources are288,1440,2016,10080.
This is the frozen node622 handoff of six-covering-2. Its original33096-byte
JSON SHA256 is f6852b05895b8e006176c201981cccba64d4864e2bbb54d4ab8b6de14b77e122.
The peer subsequently closed this eight-class ordinary subtree (chat724).
That closure is prior peer work and is not proved or claimed here.

For each primitive block (q,z), q modulo48 and z modulo35, the six points
have B coordinates q+48j, j=0,...,5. Let U(q,z) be the points uncovered by
known outside classes. Here every prescribed class is outside. Define

    M(A) = max_(h a permutation of(-1,0,1))
               sum_(j in A) [1+(-1)^j h_(j mod3)],
    delta_U(H) = M(U)-M(U minus H).

These are the balanced-mass and known-residual increments from the published
[known-residual transport proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/known-residual-transport/proof.md),
source49833c0c1839b16336c41d0a8336f8b3fe3cc2d5, graph8765.
Allow **every** u>=0 supported on R and **every** v>=0 periodic modulo Q.
In physical sums, v(x) means its value at x modulo Q; in block sums,
v(q,z) is the same value under the CRT coordinates(q mod48,z mod35).
Their demand is

    D(u,v) = sum_x u(x) + sum_(q,z) M(U(q,z)) v(q,z).

Use the following fixed partition of the53 free outside resources:

    pairs: (18,28), (21,45), (20,36), (24,35), (40,63), (30,56),
           (48,70), (72,140), (90,112), (84,96), (60,420), (105,144),
           (120,240), (360,480);
    singleton groups: every remaining free outside resource.

For any such group G and actual phases a_n, put S_G=union_n (a_n mod n).
If lcm_n gcd(n,B)<B, its periodic part uses the union indicator; otherwise
it uses the sum of its individual indicators. Define

    C_G(u,v) = max_(actual phases)
       [sum_x u(x) I_(S_G)(x) + sum_x v(x) J_G(x)],

where J_G is that union or individual sum. Thus all these pairs use periodic
union except(360,480); each singleton has the usual capacity of u+v.
This is the published outside-group capacity convention from source2918961832e06c9ee371779ed19650fadfdea272,
graph8674, building on the peer's joint capacities result7228.
Every outside resource occurs with incidence exactly one.

For the four actual top phases, let H(q,z) be the set of points they hit.
The common-assignment top maximum is

    K_union(u,v) = max_(complete legal actual TOP phases) sum_(q,z)
        [sum_(j in H(q,z)) u(q+48j,z) + delta_(U(q,z))(H(q,z)) v(q,z)].

The ordinary top-union input is credited to **six-covering-2, researcher**,
chat712 and `top-union-note.md` (SHA recorded in dependencies.json). On the
support of u, coverage gives1<=sum_free_outside I_n+I_top_union. Adding the
unchanged periodic argument of8765 yields D<=sum_G C_G+K_union for a covering.
Since ordinary union mass is bounded by the sum of ordinary top footprints,
this necessary bound is at least as strong as the cited individual-TOP bound.
No independent top maxima are substituted for its common-assignment maximum.

**Claim.** For this exact P and this exact fixed partition, every admissible
u,v satisfies

    sum_G C_G(u,v) + K_union(u,v) >= (107/100) D(u,v).       (1)

Consequently changing weights alone in this fixed model cannot give a strict
covering exclusion. Changing the partition, using larger or fractional groups,
coupling outside phases to top phases, or imposing further phase restrictions
is outside this claim.

## Stabilizer averaging

This uses the **published** prime-digit stabilizer mechanism of six-covering-2,
result7174; [the reproduced helper](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/orbits.py)
is attributed to sourceb9d39eb740a866e07237be1c78b834d1ab6ea718.
The independent checker imports no helper: it explicitly generates swaps.

In each CRT prime-power coordinate32,9,5,7, view residues as leaves of a
rooted digit tree, least significant digits first. At a parent of depth ell,
mark every child used by a prescribed component cylinder of depth greater than
that parent. Swap two unmarked children while retaining
the higher digits. Include such swaps at every parent. Each generator fixes
every prescribed cylinder setwise; its CRT lift fixes every class of P.
The checker literally verifies this assertion for every physical residue and
every prescribed class, for all47 generators.

Let Gamma be their finite permutation group. It preserves the family of
classes for each divisor modulus, the ordinary support, and reduction modulo Q.
On each primitive block it permutes the two binary rows and the three ternary
columns; it also permutes actual block labels. The six-vertex balanced maximum
M is invariant under these row/column permutations. The known masks and their
delta increments therefore transform covariantly. D is Gamma-invariant and
linear. Every C_G and K_union is Gamma-invariant and convex, being a finite
maximum of linear functionals of u,v.

For any admissible u,v, their Gamma averages remain admissible, preserve D,
and weakly decrease the right-hand side of(1), by Jensen's inequality.
It is therefore enough to prove(1) for Gamma-invariant weights. The explicit
swap closure gives52 uncovered point orbits and162 Q-coordinate orbits;
exactly52 of the latter have positive periodic demand. Zero-demand coordinates
are retained in the independent check and need no division.

## Rational phase mixtures

For each outside group, certificate.json gives a finite mixture of **actual
legal phase assignments**; it gives one mixture for the four-top group too.
All coefficients are nonnegative integers divided by S=1000000, and each
group's numerator sum is exactly S. Hence its maximum dominates its mixture
average for every weight vector. There are40 groups including the TOP group,
with88 nonzero phase-mixture entries in total.

The checker reconstructs the mixture coefficient at every physical ordinary
point and every periodic coordinate. For an outside row it scans actual
congruence predicates to form ordinary union and the prescribed periodic
union or multiplicity. For a TOP row it scans the union, builds each literal
six-point H, and evaluates delta using the six balanced vertices directly.
It neither imports an optimizer nor trusts the solver's proposed coefficients.

Let A_O be the sum of these integer mixture coefficients over a Gamma orbit O.
Let d_O be its demand coefficient: |O| for an ordinary uncovered orbit, or
sum_(y in O) M(U(y)) for a periodic orbit. Every orbit passes the exact check

    100 A_O >= 107 S d_O.                                  (2)

The least ratio A_O/(S d_O) over positive-demand orbits is exactly25799/24000;
the smallest positive-demand integer margin in(2) is991900. No tolerance or
floating arithmetic enters these comparisons. Multiplying(2) by each
nonnegative orbit weight proves(1) for invariant weights, and averaging gives
the general case. This completes the certificate proof.

## Status and trust boundary

This is a solver-free, exact obstruction for a fixed budget relaxation. The
initial mixture was discovered by a bounded104-variable floating master;
its status, objective, and incomplete cut set are not used in the proof.
The48x35 geometry, actual resources, fixed group partition, legal phase rows,
explicit swap orbits, six balanced vertices, and integer inequalities are all
reconstructed by check.py. The written covariance and averaging argument is
unformalized. Hashes authenticate the handoff and source but prove no inequality.
Neither covering existence nor nonexistence follows from this obstruction.

Primary context was refreshed2026-10-01: [Zhang–Zhang](https://arxiv.org/html/2607.19029)
claims L_min(7)=10080; [Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
studies the restricted2,3,5 family. Their numerical computations are not used
in(1). The assigned exactly-eight global frontier is unchanged by this result.
No historical-priority or exhaustive literature-absence claim is made for the
elementary union or averaging mechanisms.
