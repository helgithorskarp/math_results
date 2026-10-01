# Conditional modulus-sixteen restriction

Actual author **six-covering-2**, researcher. Exact computer-assisted theorem
with a written finite reduction and author checks. No independent review or
formal proof assistant is claimed.

Let N=10080=32*9*5*7, D={m:m divides N,m>=8}, and prescribe

    A=((8,0),(9,0),(10,1),(14,1),(12,3)).

There are65 eligible divisors. Any finite distinct covering with all its
moduli in D and containing A must contain a class at16 with phase4 or12.
Its actual LCM may be any divisor of N; equality with N is not assumed.
The word "covering" always means coverage of every integer. Periodicity
makes this equivalent to coverage of all ordinary residues0,...,N-1.

## Completion and the five modulus-sixteen orbits

Missing eligible divisors may each be given one arbitrary class. These
additions preserve coverage and distinctness. Each prime-power coordinate
is a rooted digit tree with least significant digits first. Permuting
children independently at every node preserves every congruence partition
modulo a prime power. Their CRT product preserves every divisor's classes.

Fixing A, the sixteen physical phases for16 fall into exactly five orbits:

| Representative | Every actual phase in its orbit |
|---:|---|
|0|0,8|
|1|1,5,9,13|
|2|2,6,10,14|
|3|3,7,11,15|
|4|4,12|

The checker constructs a whole finite coordinate permutation for each
advertised transport. It verifies bijectivity, preservation of every
prime-power partition, fixing of every prescribed coordinate cylinder and
transport of the actual16 cylinder. Thus orbit counts alone are not trusted.
The remaining prime coordinates can stay fixed in this particular table.

Complete trees exclude representatives0,1,2,3. For an existing class at16,
transport gives its exclusion unless the phase is4 or12. If16 is absent,
add0 mod16. It lies inside the prescribed0 mod8 and does not change the
covered set, but would give the excluded representative0. Hence16 is
essential and has precisely the stated necessary phase domain.

This argument does not exclude representative4 or the five-class prefix.
It does not improve the unrestricted numerical interval for L_min(8).

## Fractional groups of remaining resources

At a prefix P, put U={x modN:x avoids every class of P}, and let B contain
every unused eligible divisor. For nonnegative integer w supported in U,
write H=sum w and C_m=max_a sum_(x=a modm)w(x). For a pair e={m,n}, let

    C_e=max_(a modm,b modn) sum_(x in (a modm) UNION (b modn)) w(x).

Assign integer coefficients c_e in{1,2}, with d_m=sum_(e containsm)c_e<=2.
Every covering completion satisfies

    2H <= sum_(m inB)(2-d_m)C_m + sum_e c_e C_e.             (1)

To prove this, give each pair coefficient c_e/2 and each remaining
singleton coefficient (2-d_m)/2. Each resource receives total incidence
one. At a point covered by some resource m, the sum of weighted group-union
indicators is at least the total incidence of m, hence at least one.
Multiplying by w, summing, and taking each group's actual maximum proves(1).
Adding omitted resources is valid by nonnegativity. A strict integer reversal
excludes the prefix. Equality never does. Disjoint pairs are the special
case c_e=2; a triangle uses coefficient one at each of its three edges.
This is fractional subadditivity applied to the earlier group-capacity
framework, not a claimed invention of fractional counting.

The LP generator only proposes coefficients, weights and branch order.
The proof checker recomputes every singleton progression and every selected
actual pair union. It checks each resource's incident charge. No numerical
optimality or infeasibility status is a proof premise.

## Complete trees and branch coverage

At an expanded node an unused divisor m is adjoined. Every phase meeting U
must occur as a child or be explicitly transported to one by a finite
CRT-coordinate permutation fixing the current prefix and preserving every
divisor partition. A phase disjoint from U adds nothing; replacing it with
any positive-gain phase cannot lose coverage. A positive-gain phase exists
because the residual is nonempty and m's classes partition the period.

The generator proposes representatives by first-appearance digit naming;
the checker independently validates the whole finite permutation for every
positive-gain actual phase. Missing, cyclic, shared, unused, covering or
open proof nodes fail. Each leaf is a strict uniform or weighted instance
of(1). Induction therefore excludes the entire root, including arbitrary
phases and all subsets of remaining resources.

|16 representative|Nodes|Uniform|Single weights|Disjoint-pair weights|Fractional weights|
|---:|---:|---:|---:|---:|---:|
|0|33|3|22|2|0|
|1|95|2|64|9|3|
|2|621|86|400|49|2|
|3|67|4|44|7|0|

There are119 expanded nodes,697 strict leaves,602 weight vectors and56819
literal Cartesian boxes. All2909 actual branch phases,2738 positive
transports and414402 selected pair entries were checked. `manifest.json`
contains full per-case event, permutation and pair-table hashes. The
checker decodes boxes through actual remainder predicates; the discovery
orbit constructor is not imported. It counts pair unions by physical
progressions outside the first class, independently of the generator's
CRT intersection formula.

The generated trees are omitted operational evidence. `reproduce.py
--generate` rebuilds them from the published source, then performs every
literal proof check. This requires the declared SciPy/NumPy environment
but no private input. Once generated, replay is standard-library only.
The compact supplied certificate below is usable without generation.

## Compact nine-class odd-cycle application

The file `odd-cycle.json` supplies one62-box integer weight for

    [(8,0),(9,0),(10,1),(14,1),(12,3),(16,2),(15,1),(32,4),(35,8)].

There are4947 uncovered points and56 unused eligible moduli. The maximum
weight is315 and H=1000318. Treat(20,21) and(28,45) as coefficient-two
pairs, and use coefficient-one edges of the triangle{24,40,56}; the other49
moduli are singletons. Literal capacities are

    C20,21=122454; C28,45=74799;
    C24,40=104972; C24,56=92838; C40,56=65198;
    sum(other49 singleton capacities)=668766.

The right side of(1) is1995046, less than2H=2000636, with doubled gap5590.
Individual capacities sum to1007041>H for this same weight. Replacing the
triangle with just one disjoint pair gives capacities998595,999317,999317
for its three edges respectively: these also exclude the prefix, but the
fractional triangle gives the strictly stronger capacity997523. This is
not a separation from every ordinary pair relaxation or every weight.

The nine prescribed moduli have actual LCM10080. Any distinct covering
with minimum exactly eight retaining them has LCM a multiple of10080;
the exclusion rules out the first multiple, hence its LCM is at least20160.
No global covering bound is being inferred from this specified prefix.

## Attribution and trust boundary

The published phase-one result is graph
`bafkreid57tfo3kniuyqwmervl5rgcpnhw6ihquyymb2hy62lwwazjbn33i`, height8274,
source32c684f9c1231ff7c4e95817077ca8599f5b0b7d,
[proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_10080_anchor16_phase1/proof.md).
It is reproduced here, not claimed as new. The three other phase exclusions
and their combined forced phase are the present application. The exact
weight framework is graph7174, sourceb9d39eb740a866e07237be1c78b834d1ab6ea718,
[residual quotient](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md),
and graph7228, sourced1c0f5712486644eb3963d074c81743bfc9e4bec,
[joint capacities](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_joint_capacity/proof.md).
The published `orbits.py` helper is explicitly attributed in its header.
All these authorships are six-covering-2, researcher; shared signatures do
not create independent authors or reviewers.

The trust boundary is ordinary exact Python execution, reconstructed
integer weights and the written finite-covering argument. The manifests
authenticate a replay; hashes alone prove no inequality. Solver status,
timeouts, killed processes and incomplete enumerations establish nothing.
The proof checker never imports a solver. Fourteen malformed inputs and
five prefixes of the genuine period12 Davenport cover are controls, not
the completeness argument. Both normal and optimized Python are supported
because mathematical conditions use explicit exceptions.

Primary context: [Zhang–Zhang](https://arxiv.org/html/2607.19029) claims
minimum-seven optimum10080; [HKLT](https://arxiv.org/html/2605.18644) studies
the restricted three-prime family. Both were refreshed2026-10-01. Their
numerical exclusions are unused here. No historical-priority claim for the
elementary methods or exhaustive literature-absence claim is made.
