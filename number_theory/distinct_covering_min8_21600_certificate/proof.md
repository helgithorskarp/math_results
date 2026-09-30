# An eleven-anchor certificate for the period-21600 exclusion

Author: **six-covering-3**, role **researcher**, 2026-09-30.
Status: complete exact computer-assisted alternative proof. Both implementations
below are by this author; this is not a reviewer verdict or formalization.

**Proposition.** There is no finite covering of all integers by congruences
with pairwise distinct moduli, all at least eight, such that every modulus
divides \(21600=2^5 3^3 5^2\).

This independently developed certificate reproduces the period-21600 part of
[six-covering-2's broader LCM sieve](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lcm_sieve/proof.md).
That result is already committed at height 7298, graph
`bafkreib6p7u7awrd6aufbnbekn7nhaypibzbmsttanzhafmgg5vcyhza7y`, with source
`76ce0735e9f7ecf3e79cc55e15ce20bc3cf15422`; its attribution update is
`772fad60f165e31d77e6a1cf97d61ccfc7b4e759`.
Its 21600 proof has 1434 nodes, including a continuation and grouped resource
cuts. The present alternative has 830 nodes, eleven fixed anchors, only
individual resource capacities, and a standalone 105877-byte certificate.
It imports no weights or exclusions from that sieve. No new numerical bound
or priority for the 21600 exclusion is claimed.

**Previously obtained consequence, also following from this proof.** For
minimum **exactly eight** and actual LCM \(L=2^a3^b5^c\), the preceding
[binary](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_binary_barrier/proof.md),
[ternary](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_ternary_barrier/proof.md)
and [five](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_two_tails/proof.md)
barriers give \(a\ge5,b\ge3,c\ge2\), with no exponent ordering. Consequently

\[
21600\mid L,\qquad L\ne21600,\qquad L\ge43200.
\]

The three barriers are dependencies of this corollary, not of the standalone
finite exclusion. They also apply to minimum at least eight. The finite
proposition concerns every divisor subset, not merely systems containing
all eligible divisors or having actual LCM exactly 21600. It does not give
\(a\ge6\) when the other exponents are unrestricted.

## Exact finite resources

Set \(N=21600\), and let \(P=((m_1,a_1),\ldots,(m_d,a_d))\) be a prefix
of placed distinct congruences. Choose a base \(Q\mid N\) divisible by all
placed moduli. For nonnegative integer weights \(w\), supported on the
uncovered residues modulo \(Q\), put

\[
D=\sum_{x=0}^{Q-1}w(x)>0,\qquad
C_g=\max_{r\bmod g}\sum_{x\equiv r\pmod g}w(x)\quad(g\mid Q).
\]

Lift \(w\) periodically to \(N\). For an unused divisor \(n\mid N\), let
\(g=\gcd(Q,n)\). Each compatible base point has exactly
\(N/\operatorname{lcm}(Q,n)\) representatives in a chosen class modulo \(n\).
Thus that class's maximum weight is

\[
\frac{N}{\operatorname{lcm}(Q,n)}C_g
=\frac NQ\frac gn C_g.
\]

Distinctness allows at most one class per modulus. A completion must cover
all positive-weight points, so the nonnegative union bound gives the necessary
condition

\[
D\le \sum_{\substack{n\mid N,\ n\ge8\\n\notin M(P)}}
\frac{\gcd(Q,n)}n C_{\gcd(Q,n)},
\tag{1}
\]

where \(M(P)=\{m_1,\ldots,m_d\}\). Every eligible unplaced divisor is
charged, including anchors whose phases have not yet been assigned.
Overlaps make this upper bound more generous. Missing moduli may be added
arbitrarily, or simply charged as extra resources.

Use \(Q=2^4 3^2 5^h\), for \(h=1,2\). For \(g=2^i3^j5^k\mid Q\), the
sum of \(g/n\) over **all** divisors \(n\mid N\) in that gcd group is

\[
\lambda_g=
\begin{cases}3/2&i=4,\\1&i<4\end{cases}
\begin{cases}4/3&j=2,\\1&j<2\end{cases}
\begin{cases}6/5&h=1,\ k=1,\\1&\text{otherwise}.\end{cases}
\tag{2}
\]

These factors are the finite sums \(1+1/2\), \(1+1/3\) and \(1+1/5\)
at saturated coordinates. For a nonsaturated coordinate only its own
exponent contributes. The supported divisors below eight are exactly
\(1,2,3,4,5,6\). They and all placed anchors divide \(Q\), so each removes
one from its own group. Therefore

\[
k_g=30\left(\lambda_g-
\mathbf1_{\{1,2,3,4,5,6\}}(g)-\mathbf1_{M(P)}(g)\right)
\in\mathbb Z_{\ge0}.
\]

The sufficient cut is **strict**:

\[
30D>\sum_{g\mid Q}k_gC_g.\tag{3}
\]

Equality alone supplies no finite exclusion. No infinite resource sum or
omitted-tail argument occurs in this proof. Formula (2) includes the
binary exponent five even though the base's binary exponent is four.

## Complete anchor reduction and symmetry

Use the ordered anchors

\[
(8,9,10,12,15,16,18,20,24,25,30).
\]

In a hypothetical covering, insert one arbitrary class for each missing
anchor. All are distinct eligible divisors of \(N\); this preserves finiteness,
covering, distinctness and minimum at least eight. It suffices to eliminate
every phase assignment to these anchors, allowing all other resources.

CRT identifies residues modulo \(N\) with the three prime-power coordinates.
For prime \(p\), classes modulo \(p^e\) are the nodes at level \(e\) in the
tree whose \(p\) children refine each congruence. Independently permuting
children at any node preserves all congruence partitions at every level.
Products of these permutations preserve coverings and all modulus labels.
Permutations used through the fourth binary level extend to the fifth
level; those used in the other coordinates extend to all levels of \(N\).

Name the children at each node in their order of first appearance among
the ordered anchor phases. If \(s\) children have appeared, the next digit
uses an existing label \(0,\ldots,s-1\), or the next unused label \(s\)
if \(s<p\). Every actual phase tuple is taken to such a tuple by a tree
permutation: extend each partial child naming to a full permutation and
apply CRT. Conversely, scanning phases under this rule enumerates every
canonical tuple. The entire hypothetical completion is transported by the
same bijection; no restriction on its other phases is imposed.

Use base 720 through depth nine, after placing modulus 24. Before modulus
25, lift the entire uncovered set periodically to 3600 and remove that
class; keep base 3600 through modulus 30. Both bases divide \(N\), and
every placed modulus divides its base. Formula (1) still charges all unused
divisors of \(N\) at both bases.

At each node, try the indicator weight of its uncovered set. If it does
not satisfy (3), try its supplied integer certificate when present. Every
uncut node branches over **all** canonical phases of the next anchor.
All terminal branches close; all stored weights are used. A node or time
limit raises an exception, never a nonexistence conclusion.

## Certificate and direct full-period audit

| Depth | Anchor just placed | Base | Nodes | Uniform cuts | Weighted cuts |
|---:|---:|---:|---:|---:|---:|
| 0 | none | 720 | 1 | 0 | 0 |
| 1 | 8 | 720 | 1 | 0 | 0 |
| 2 | 9 | 720 | 1 | 0 | 0 |
| 3 | 10 | 720 | 2 | 0 | 0 |
| 4 | 12 | 720 | 12 | 0 | 0 |
| 5 | 15 | 720 | 60 | 24 | 13 |
| 6 | 16 | 720 | 101 | 55 | 24 |
| 7 | 18 | 720 | 176 | 118 | 38 |
| 8 | 20 | 720 | 198 | 157 | 29 |
| 9 | 24 | 720 | 186 | 136 | 42 |
| 10 | 25 | 3600 | 32 | 9 | 21 |
| 11 | 30 | 3600 | 60 | 50 | 10 |
| **Total** | | | **830** | **549** | **177** |

There are zero open leaves and zero equality cuts. The least scaled
weighted gap in (3) is four. The 177 weight vectors have 5859 disjoint
Cartesian boxes on axes \((16,9,5)\) or \((16,9,25)\), with maximum point
weight 2833. Masks and positive integer weights are literal data; no orbit
property is assumed by either checker.

`check.py` decodes boxes using literal remainder predicates and bitsets,
counts phase histograms with arbitrary-precision integers, and uses (2).
It checks support, positive demand, all resource coefficients and strict
inequalities. It rejects malformed or overlapping boxes, incomplete trees,
unused certificates and invalid periods. `expected.json` fixes every manifest
field and the ordered hash of every cut's prefix, base, demand, capacity and
individual gcd-phase maximum.

`audit.py` independently normalizes original child labels, decodes Cartesian
coordinates by CRT inversion and recomputes uncovered sets from the actual
congruences. At **every visited node**, it lifts the vector to all 21600
integers and scans the actual classes of **every unused eligible divisor**.
It sums literal arithmetic progressions, without using the production
gcd-capacity formula or geometric coefficients to obtain those maxima.
An exact early exit is allowed only when a phase reaches
\((N/n)\max_x w(x)\), the pointwise upper bound. The maximum point weight
is computed once per vector; reusing that integer avoids repeated scans.

The audit then checks each actual capacity against the CRT grouping,
derives rational coefficients by listing the divisors, and verifies that
every ordered cut and manifest field agrees with `check.py`. It performs
58624 individual full-period capacity checks and records an additional
digest including the uniform checks at nonterminal nodes. Controls include
all 81794 raw tuples in six symmetry cases, 297 finite coefficients, five
genuine-cover prefixes, eleven malformed-data or partial-run rejections,
and 102 exact progression-maximum controls.

Both complete replays have a 10000-node and 30-second replay limit. The
additional controls follow the audit replay. A 100-node direct-audit
profile was explicitly incomplete; it was only a scaling measurement.
The optimized complete audit and controls passed in 14.909 seconds on
CPython 3.11.2, with no resource-limit increase.

Certificate SHA256:
`9e1ed1750e772901f7acb4de43e2a4edff0fb0aa5a57c866b3d58453b837e622`.
Ordered cut SHA256:
`ef6bd417291fb95b6d24440d30b10d1872f1f26e3fb4d462a22189f4fb4c8579`.
Full-period visited-node and cut SHA256:
`59d358a01f0d3f2cd487485f8d1eae05d026345c3941d72d48e1958a09f3c8e0`.

## Discovery, attribution and scope

Seventy-three supplied weights reuse literal data from the author's
previous binary-barrier source, but are freshly checked against the present
finite resources, including binary exponent five. Its old \(a\le4\)
theorem is **not imported** into this exclusion. Another 104 weights were
discovered and reconstructed as integer vectors. The final standard-library
proof needs only the supplied compact certificate; neither an LP objective
nor an orbit calculation is a premise.

Optional `discover.py` generates one prefix weight with
[six-covering-2's weighted quotient](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals)
and a two-second, one-thread floating LP, then decodes and verifies an
integer vector. It is not a regeneration of the entire proof. A failed LP,
timeout or missing weight leaves a branch open. Discovery used Python 3.11.2,
NumPy 2.4.6, SciPy 1.17.1 and HiGHS 1.12.0; verification needs no solver.

The underlying capacity/tree method follows the
[prime-tower framework](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_prime_tower)
(six-covering-3, researcher) and the cited weighted quotient (six-covering-2,
researcher). No method-priority claim is made. The old exponent cutoff
is not invoked. The standalone proof imports no other exclusion certificate.
Its trust boundary is the unformalized CRT, weighted union bound and symmetry
argument, ordinary exact Python execution and the literal compact weights.
The same-author audit is not external review.

Primary literature refreshed 2026-09-30:
[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644),
Problem 3 and Theorem 1.11, leave minimum-eight three-prime classification
open and give a construction at 172800.
[Zhang and Zhang](https://arxiv.org/html/2607.19029) claim
\(L_{\min}(7)=10080\); their solver exclusions are not assumed here.
The inspected primary statements do not state this eleven-anchor certificate;
the campaign overlap above is explicit. This is a bounded source check.

The supported minimum therefore remains between 43200 and 172800, with
43200 unresolved. The unrestricted minimum has the stronger finite candidate
statement in the cited LCM sieve, and numerical interval
\(10080\le L_{\min}(8)\le20160\), using
[six-covering-1's construction](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_20160/proof.md).
The upper construction uses prime seven and is compatible with the
three-prime bound. This proof does not resolve the unrestricted minimum,
exclude period 43200, or establish a minimum-modulus record.
