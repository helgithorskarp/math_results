# Nested semantic class weights close the native prefix

Author and executing agent: **six-sorting-2, researcher**, 2026-10-01.

Let P be the literal first 24 comparators of `N13L46D9` in
[fixture.json](fixture.json). **P has no standard sorting extension with
at most 44 comparators in total, regardless of suffix order or depth.**
Here a standard comparator `(a,b)`, `a<b`, sends the minimum to `a`.
This closes the fourteen cases remaining after [NORMALIZE.md](NORMALIZE.md).
The proof below supplies a uniform certificate for all 45 canonical
32-comparator roots in the original complete cover. It does not assume
that P covers all thirteen-input networks. The global interval remains
`44 <= S(13) <= 45`.

## A reusable compositional potential

Fix `n,l,h`, put `k=n-l-h`, and choose a nonempty **fixed** finite set F
of original clampings. Each clamping fixes `l` input positions to distinct
ranks below 0 and `h` others to distinct ranks above 1. The remaining
positions retain their entire Boolean cube. F may be a selected subset
of placements; it need not be a complete clamping-family census.

For each original clamping f after an oriented comparator prefix P:

* D_f counts gates touching a marked value, once even if both endpoints
  are marked.
* R_f counts unmarked gates acting identically on that original
  clamping's complete current free-input image.
* C_f=D_f+R_f. Delete these gates and follow free carriers through marked
  exchanges. Normalize the retained oriented word Q_f by the increasing
  physical order of its current free output wires. Its input coordinates
  may be permuted; their domain is still the full `k`-input Boolean cube.

Let B_k(Q) be an integer function satisfying all three conditions:

1. B_k(Q) is a lower bound on the total number of comparators in any
   sorting extension beginning with the oriented prefix Q.
2. B_k is invariant under global wire permutation.
3. B_k(Q;g) >= B_k(Q) for every appended oriented comparator g.

For each current **pair** of low/high marker masks z, define

    lambda_f(P) = C_f(P) + B_k(Q_f(P)),
    lambda_z(P) = max_(f in F at z) lambda_f(P),
    M_F(P) = sum_(realized z) 2^lambda_z(P).

**Nested class theorem.** Every oriented sorting extension N of P with
m total comparators satisfies `M_F(P) <= 2^m`. The extension has no
restriction on gate order, depth, repeated gates or interleaving.

### Proof of transport

Consider one next comparator. If it is marked, C_f increases by one and
Q_f changes only by a global relabelling of its free carriers. If it is
an unmarked identity on f's full current image, C_f increases by one
and the retained word is unchanged. Thus lambda_f increases by one in
either deleted case. Otherwise the gate is appended to Q_f, so lambda_f
cannot decrease by condition 3. Existing charges are determined at their
original times on the same original full cube; later gates do not
retroactively change them.

The transition of the low/free/high tags depends only on z and the
comparator. Outside its endpoints z is unchanged. Sorting two endpoint
tags has at most two preimages; a double fibre consists of the two
orders of different tags. Both preimages meet a mark, because two free
tags have only one order. Both therefore receive a unit charge.

For each old class choose an original clamping attaining its maximum
lambda. Follow those original histories separately. A singleton fibre
preserves at least its old weight. In a double fibre, the new class has
label at least `1+max(lambda_1,lambda_2)`, and hence weight at least
`2^lambda_1+2^lambda_2`. Summing disjoint fibres proves that M_F never
decreases. This argument does not identify the conditional Boolean
images of histories sharing marker positions.

At the output of N, all histories in F have the same marker masks:
the low marks occupy the first l outputs and the high marks the last h.
The completely pruned word Q_f(N) sorts the full k-input Boolean cube
with `m-C_f(N)` gates. Its initial input permutation preserves that cube.
Condition 1 gives `B_k(Q_f(N)) <= m-C_f(N)`, so every terminal label is
at most m. There is one terminal class and `M_F(N) <= 2^m`.
Monotonicity proves the result. Numeric marked-input sorting follows
from the usual zero-one principle applied to the full sorter.

### Implemented inner bound

The certificate uses `k=7` and

    B_7(Q) = max(16, B_low_anchor(Q), B_high_anchor(Q)).

The two semantic anchor bounds are defined and proved in
[ANCHORS.md](../semantic-pruning/ANCHORS.md), committed lemma 8604,
`bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle`,
source `b49096c7b4af0920e93e78c489d69bd7105363cb`.
They use the five original families `(1,0),(0,1),(2,0),(0,2),(1,1)`.
For a reachable unary minimum port p, a family contributes
`S_lower(7-l-h)+ceil(log2 M_family,p)`. Take the largest contribution
at p and aggregate all ports with the `1+max` Huffman rule. Maxima are
dual. The anchor theorem proves validity and monotonicity under each
oriented comparator. A global permutation bijects original clampings,
current masks and unary ports, preserving both anchor bounds. The
constant 16 is the established lower bound `S(7)>=16`. Smaller imported
bounds needed inside these anchors are `S(5)>=9` and `S(6)>=12`.

Taking B_k to be the constant `S_lower(k)` recovers precisely
`2^S_lower(k)` times the selected semantic class mass of
[PROOF.md](../semantic-pruning/PROOF.md), committed lemma 8539,
`bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4`,
source `97bd126fa1aa3756008e6dc7c1e04a4f9542bffe`.
The free-carrier pruning bridge is also used in [TOUCH.md](TOUCH.md),
committed lemma 8909,
`bafkreibfvq5abfuzrwlq7byncp32ro3r7i2eptegh75of6dxaowubiffwe`,
source `e260dd848eb8616697a952840c0027965e5851c3`.
The present addition composes those proved ingredients and supplies
strict concrete exclusions. No priority is claimed for pruning,
Huffman, Kraft bounds, or compositional use of lower bounds.

## Exact native application and coverage

The original [complete kernel cover](PROOF.md), committed lemma 8690,
`bafkreigxneqt4bxabyiwkznuhldfniqc43ee2ddxrkpvvsdvlwv5nkioyy`,
source `68f3f94cca06df709c264d7d72147aa347bef5aa`, proves that every
standard size-at-most-44 completion of P can be rearranged by commuting
disjoint gates into

    P ; (11,12) ; (1,2) ; T_i ; E,

where `i=0..44` and T_i is one of the 45 literal six-gate kernels.
Its complete equal-merge cover and analytic commutation argument are
imported here. The original scalar checker enumerated all 900 event
orders and checked their 45 representatives. The present checker
reconstructs the 45 canonical matching kernels and checks their literal
agreement with the pinned original certificate; it does not rerun that
900-order calculation or the imported smaller-network proof corpora.
The original cover's soundness, including `S(11)>=35`, is a dependency.

For each `P_i=P;(11,12);(1,2);T_i`, [nested-fixture.json](nested-fixture.json)
selects four to seven original clampings, all with `(l,h)=(3,3)`. Their
current configurations are distinct. [nested-certificate.json](nested-certificate.json)
records every exact pruning and inner bound. Each selected mass exceeds
`2^44=16*2^40`. The following table displays `M_F(P_i)/2^40`:

| Kernel IDs | Selected mass in units of 2^40 |
|---|---:|
| 19 | 17 |
| 0, 4, 5, 9, 13, 27, 29, 43 | 20 |
| All other IDs among 0..44 | 18 |

Thus every P_i requires at least 45 total comparators. The cover then
excludes every standard size-at-most-44 completion of P. The root
inequalities themselves cover **arbitrary oriented** continuations;
standard comparators enter only through the imported cover from P.
There is no fixed-depth encoding or assumed enumeration of suffixes.

The selected packet contains 236 domain occurrences, 32 distinct original
mask pairs and 203 distinct retained seven-wire prefixes. Inner bounds
are 16 (one occurrence), 17 (150), 18 (80) or 19 (five). Every individual
label is at most 43: the exclusion comes from class aggregation, rather
than from one clamping already forcing 45. The fourteen newly closed
preceding targets are
`2,8,15,20,24,31,32,33,34,36,38,39,41,42`.
The other 31 were excluded in earlier contributions; their rechecks here
make the uniform packet independent of that later exclusion chain.

### Corollary for the previously screened projected family

The [867-prefix screen](../../six-sorting-1/projected_prefix_barrier/PROOF.md),
committed lemma 8666,
`bafkreie6zhd7cdcyvreier4yy4vtt322fugavuxsvdsuzw35czga76jewi`,
source `93d450737aec8538ef62ee0b4de54771f0fe4b42`, covers 867 of the
869 distinct literal 24-gate prefixes obtained from its eight pinned
table parents. Its two filter exceptions are index 396 (the present
native prefix) and index 591 (the 45-gate incumbent). The latter
contains the already excluded 20-gate prefix of the
[prior incumbent theorem](../../../sorting_networks/thirteen_twenty_prefix_exclusion/PROOF.md),
committed lemma 7813,
`bafkreifrmmc5ztlhitir24jn2lqdy6iekdndejcf2auf7limrwind5ydby`,
source `c40dcc78d772c2ab1fd1991d8f89e4c270491673`.
The current 45-gate positive fixture literally begins with that same
20-gate word in its pinned [fixture](../../../sorting_networks/thirteen_twenty_prefix_exclusion/fixture.json);
the standalone checker verifies this literal identity. This prior theorem
is imported, not established anew.
Consequently all 869 specified prefixes are excluded for **standard**
size-at-most-44 completions. Their generation and prior exclusion certificates are
not rerun by this packet. Earlier cuts, changed early gates, different
parents and different word orders remain outside this corollary.

## Reproduction and evidence limits

From the repository root, with Python 3.11.2 and its standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-sorting-2/native24-kernel-cover/nested_generate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-sorting-2/native24-kernel-cover/nested_verify.py
```

The producer uses pinned Boolean columns, semantic pruning and dyadic
anchor aggregation. The standalone checker imports no producer, sibling
checker, profiler or solver. It uses distinct numeric marker ranks,
separately replays every original full cube, tracks carriers, verifies
all pruning functions and recomputes all five inner families. Heap merges
check each dyadic anchor calculation independently. Each certificate
field is compared against scalar reconstruction; record hashes do not
replace replay.

The checker also checks 2,304 original one-gate transport steps on four
wires, all 12 oriented first gates, 862 marker fibres including 324
double fibres, 60 terminal families and 24 global relabellings. It checks
all 8,192 Boolean inputs of each known 45- and 46-comparator sorter,
all 128 inputs of a known 16-comparator seven-input sorter, and the 32
selected original domains at cuts 0,24 and terminal of both full sorters.
Eight damaged-certificate/fixture controls are rejected.
These controls test the implementation and bridges; the universal
transport proof above establishes the quantifiers, rather than finite
controls standing in for a theorem.

Expected status: `ALL_NATIVE24_NESTED_CHECKS_PASSED`, 45 roots, 236
selected domains, fourteen newly closed preceding targets and zero
remaining native-prefix targets. The certificate is 214,328 bytes, SHA256
`0f3511b75f66f526febe2475b5a019f94999b325c488ccdf0bc700c69fb6add1`. The final normal-mode
scalar run took approximately 12 seconds and less than 24 MiB peak RSS
on one CPU/thread. Normal and optimized Python modes matched every
finite output field, with explicit guards active in both modes.
Both implementations and the ordinary proof were authored and executed
by this researcher. Algorithmic
independence is not an external reviewer verdict or proof-assistant
formalization. The trust boundary includes the unformalized transport
proof, the imported complete cover and published smaller-network bounds.
No solver verdict, timeout, incomplete search or resource failure is a
mathematical premise.

The classical pruning/Huffman mechanisms and published smaller sizes
are from [Harder's primary paper](https://arxiv.org/html/2012.04400v3),
especially Section 3.2, Theorem 26 and the certificate soundness rules.
The [maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
reports the global thirteen-input interval 44..45. This result excludes
one specified prefix and supplies a reusable certificate operator; it
leaves the unrestricted thirteen-input problem open.
