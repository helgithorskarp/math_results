# Matching and two-layer resource bounds for residual fibers

Actual author: **six-covering-3, researcher**, 2026-10-01–02.
This is a proved structural refinement, with conditional finite examples.
It does not exclude either outstanding global period or improve a numerical
bound on the minimum LCM for minimum modulus exactly eight.

## 1. Setting and credited reduction

Fix a prime p and a positive cofactor M coprime to p. Under CRT a class
modulo p^j d, d dividing M, fixes one prefix modulo p^j and one cofactor
residue modulo d. Each ORIGINAL modulus is a distinct resource, used at
most once. Different depths have different resources even when their
cofactor divisor d agrees. Free phases and omissions are allowed.

After choosing all phases through depth e, the nonempty residuals are sets
H_i in Z/MZ. The next depth produces p identical, separately labeled
copies of each H_i. A resource at that depth acts in only one copy.
The exact multiset continuation state and the width recurrence

    n_(e+1) >= p n_e - k_(e+1)

are published prior work: contribution 7102, source commit
afaabb5d6222b09be0977c3884714a5cf2e60c47,
[proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_prime_tower/proof.md).
That proof also gives the finite-horizon width bound. Its full proof and
committed body were read. We refine its resource count; neither the CRT
description nor the anonymous multiset quotient is presented as new.

For a nonempty V define

    g(V) = gcd(M, {x-x0 : x in V}),       x0 any point of V.

This does not depend on x0. A SINGLE class modulo d can contain V exactly
when d divides g(V). For a singleton g(V)=M. A nonempty set has g(V)=1
exactly when it fits no proper cofactor congruence. Empty sets are discarded
before building the graph and have no signature in this notation.

Build the **single-eraser graph** with a separate left vertex for every
nonempty target fiber and a right vertex for every original resource at
the current depth. Join them when one legal cofactor phase contains the
entire residual in that target. For the free phases here, adjacency is
just d dividing g(V). Identical fibers retain their multiplicities.

## 2. One-layer bound

**Lemma 1.** Let T be the number of nonempty target fibers before a layer,
k the number of its distinct resources, and nu the maximum matching size
in the single-eraser graph. After this layer at least

    max(0, T - floor((k+nu)/2))

targets remain nonempty. In particular terminal completion requires
2T-nu <= k.

**Proof.** Suppose E targets are erased. If S of them receive exactly one
resource, those S assignments form a matching: each target and resource
is distinct, and a single assigned class contains the target's entire
old residual. Thus S<=nu. Every other erased target receives at least
two resources. They are disjoint assignments because a class acts in
one target only. The resources spent on erased targets are at least
S+2(E-S)=2E-S>=2E-nu. They cannot exceed k. QED.

Consequently the published width recurrence sharpens to

    n_(e+1) >= max(0, p n_e - floor((k_(e+1)+nu_e)/2)),

where the graph has p copies of every nonempty stage-e residual. The
statistic is invariant under the multiset and the independent cofactor
symmetries of 7102: those symmetries preserve containment in each fixed
modulus family. This is a necessary cut, not an exact transition test.

## 3. A bound coupling two remaining layers

Now assume precisely two layers remain, each with the SAME free cofactor
resource set D. They are different original moduli at the two depths.
Write k=|D|. Let T initial targets be the children before the first of
these layers, and let (C,B) be ANY vertex cover of their single-eraser
graph: C is a set of left vertices, B a set of cofactor labels on the
right, and every edge meets C or B. Put c=|C| and b=|B|.

**Lemma 2.** Completion in these two layers requires

    2p c + (p+1)b >= 2pT - (p+1)k.                    (A)

No assumption about which first-layer phases are chosen is made.

**Proof.** Let E initial targets be erased by the first layer, S of them
using exactly one resource, and h surviving targets have their residual
changed by first-layer classes. The S single erasures form a matching,
so S<=c+b: each matching edge meets this vertex cover, and its vertices
are distinct. Erased targets consume at least 2E-c-b resources. Each
changed surviving target consumes at least one additional resource,
acting in that target. Hence

    h <= k-2E+c+b.                                     (B)

There are p(T-E) nonempty targets before the last layer. For any unchanged
surviving target outside C, its children have the same cofactor residual
as that original target. A single last-layer eraser for such a child must
therefore have its cofactor label in B. The other children come from
changed survivors or survivors in C; there are at most p(h+c) of them.
The final graph thus has a vertex cover with at most p(h+c) left vertices
and b right vertices. A matching has size at most p(h+c)+b.

The last layer, which must erase all its p(T-E) targets, spends at least

    2p(T-E) - p(h+c) - b
    >= 2pT - pk - 2pc - (p+1)b,

by (B). This quantity cannot exceed its budget k. Rearranging proves(A).
This also covers wasted phases, partial erasures, omitted resources,
and changes to survivors in C; those can only weaken the upper counts.
QED.

The weights of left and right vertices in(A) are2p and p+1. A low-cost
vertex cover is therefore a compact obstruction; it need not be a
minimum cover. The proof uses two different original resource pools,
never two uses of one original modulus.

**Lemma 3 (parent-subset form).** Suppose the T=pm targets consist of p
copies of each of m parent residuals. Define

    N(I) = union_(i in I) {d in D : d divides g(H_i)}.

The minimum weighted vertex-cover cost is

    min_(I subset {1,...,m}) [2p^2(m-|I|)+(p+1)|N(I)|].   (C)

**Proof.** Given I, cover all p copies of parents outside I on the left
and all their neighbors N(I) on the right. This is a cover with the stated
cost. Conversely, if a cover omits any copy of a parent on the left, all
neighbors of that parent must be on the right. Removing all other left
copies of that same parent then preserves the cover and reduces or
preserves its cost. An optimal cover can therefore include all p copies
or none, independently for each parent. Its right side may be reduced
to the union of neighbors of parents with no left copies in the cover.
These are exactly the covers in(C). QED.

Combining(A) and(C) gives the useful necessary conditions

    (p+1)|N(I)| >= 2p^2|I|-(p+1)k       for every I.     (D)

These conditions couple the two-layer resource allocations through the
cost of changing surviving residuals. They can be strictly stronger than
the separate one-layer matching and horizon-width bounds, as Section6
shows. No sufficiency assertion for(D) is made.

## 4. Current period 10080 application

The active conditional prefix is

    P=((8,0),(9,0),(10,1),(14,1),(12,10)).

It belongs to the thirteen five-class forms left open by contribution 9065
(source 22ee1456490508063668c2cc6514d4c1ef9d2849),
[proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/ten-twelve-parity/proof.md).
That proof, fixture, remote source, and actual graph commitment were
inspected. Its exclusion trees were not independently replayed here.
The preceding exceptional10:0 form was already excluded by 9065; this
packet does no further work on that closed domain.

Here10080=32*315 and2520=8*315. The prefix has1398 uncovered base points,
repeated in four copies (5592 physical points). There are60 unused
original divisors at least 8:36 dividing2520, and the24 distinct tails

    16d, 32d, one of each for every d dividing315.

ALL of these phases are free. After choosing all 36 additional base
phases, let H_r be the surviving cofactor set for r modulo8. H_0 is empty
because8:0 is already present; there are at most seven nonempty parents.
Only at THIS stage do the following constraints apply. The known prefix
by itself is not treated as if its36 base resources were already spent.

Apply(D) with p=2, k=tau(315)=12. Every subset I of nonempty base fibers
must satisfy

    3|N(I)| >= 8|I|-36.                                (E)

Thus any five nonempty base fibers must collectively admit at least 2
single-eraser labels, any six at least 4, and any seven at least 7. Smaller
subsets impose no additional condition. In particular **at most four
nonempty base fibers may have g(H_r)=1**. If all seven are nonempty, at
least three have their holes contained in a proper cofactor congruence.
Equivalently, at least three of the seven labeled base fibers must be
empty or have holes all in one class modulo3,5, or7. This equivalence
uses the prime divisors of315; it does not identify their resource labels.

These are rigorous necessary constraints on the36 free base phases for
every completion of P. They are a reduction for a future search, rather
than an exclusion of P. The gcd signatures are not an exact continuation
state: hole sets with the same signature can have different coverage
possibilities by two or more classes.

The checker verifies every original phase in the36/24 split against its
literal congruence in the10080-point period. A16d phase (r,e,b) covers
cofactor phase b in the two copies j=e modulo2, while a32d phase (r,j,b)
covers one of the four copies. No tail is cloned across different r.

## 5. Exact terminal test when the count bound is saturated

After the16d layer, suppose six nonempty prefix fibers V_i remain at
depth 4. Each has two children at depth 5, giving twelve targets and the
twelve distinct resources32d. Terminal completion is then equivalent to
a perfect single-eraser matching. Each nonempty target requires a
resource, so a completion with exactly twelve resources assigns exactly
one to each. Conversely each matching edge is realized by CRT, giving
an actual32d phase containing that entire target.

For these paired identical children the perfect-matching condition is

    |union_(i in I) divisors(g(V_i))| >= 2|I|
                    for every I subset {1,...,6}.       (F)

This is Hall's condition: for any subset of individual children, adding
the other child of each included parent preserves its neighbor set and
only strengthens its demand. All such strongest demands are(F).
Hall's theorem is standard, with no priority assertion here. Alternatively
the accompanying matching plus equally sized vertex-cover certificates
give a direct, finite check of maximum matching size.

In particular all six V_i must fit some proper cofactor congruence, and
at least one must be a singleton: using d=315 requires containment in a
single cofactor point. These two simple consequences alone are not
sufficient; the full conditions(F) are needed. The supplied positive
control constructs a twelve-phase tail completion of a CONDITIONAL
six-fiber state. Its reachability after the36 base phases is not claimed.

## 6. Strict finite gap with all ordinary point-weight budgets passing

This example is a conditional demand problem, not a covering of all
integers, not the full divisor pool of its period, and not a bound on
L_min(8). It uses eight distinct moduli, the smallest exactly8.

Set M=105. The three cofactor points are

    V={15,21,70},

with CRT coordinates modulo(3,5,7), respectively(0,0,1),(0,1,0),(1,0,0).
Each class0 modulo3,5,7 contains exactly two of these points. No proper
resource in D={1,3,5,7} contains all three, so g(V)=1.

At depth2 take the two parents r=1,2 modulo4, each with residual V.
The four first-layer child targets have their only single-eraser neighbor
d=1. In two further binary layers allow exactly the original moduli

    8,24,40,56; 16,48,80,112.

Here T=4,k=4. The cover C=empty,B={1} has weighted cost3, below the
two-layer threshold4. Lemma2 therefore excludes an integer completion
of these24 physical demand points in period 1680.

For comparison the initial matching number is1. Lemma1 only says that
at least 4-floor(5/2)=2 children survive the first layer; the last-layer
width allows two. Those separate bounds do not exclude the state.

Nevertheless there is a literal fractional phase cover with all unit
resource budgets. For each first-layer modulus8d, distribute its phase
uniformly among the four child prefixes of r=1,2, with cofactor phase0.
For each last-layer modulus16d distribute its phase uniformly among the
eight grandchild prefixes, again with cofactor phase0. Every resource's
phase probabilities sum to1. Every demand point lies in the d=1 class
and two of the three proper cofactor classes. Its total fractional
coverage is

    3/4 + 3/8 = 9/8.

For EVERY nonnegative point weight w on this demand, the sum of the
eight independent singleton capacities (maximum weight of a legal
phase for each original resource) is at least 9w(demand)/8: each maximum
dominates the displayed resource's fractional expected phase weight.
Thus even a positive uniform margin in all ordinary singleton-weight
budgets does not prevent the two-layer integral obstruction. This
does not say that pair/group capacities or a full integer encoding pass.

The fractional certificate lists actual legal phases and rational
probabilities. A separate verifier uses literal integer congruences,
without importing the producer, for all 24 points and all eight resources.
An independent C++ meet-in-the-middle enumeration uses ALL phases of
ALL eight original moduli, no symmetry reduction and no matching cut.
It enumerates the two four-resource union families, then a complete
superset lookup over all 2^24 demand subsets. No omitted tuple is inferred
from an optimizer status. Two positive controls also run.

## 7. Evidence, scope, and prior literature

The lemmas are elementary combinatorial proofs, not solver conclusions.
The gcd test follows directly from congruence containment; matching and
Hall methods are standard. The contribution is the resource accounting
across two remaining layers, the resulting explicit stage constraints
for the current period 10080 root, and the reproducible strict finite gap.
Targeted primary-literature and graph searches did not identify this
specific two-layer refinement; this is not an assertion of priority.

The full source of 7102 establishes the exact setting and prior cutoff.
For current external context see Zhang–Zhang,
[arXiv:2607.19029](https://arxiv.org/html/2607.19029), and
Harrington–Klein–Lowrance–Trifonov,
[arXiv:2605.18644](https://arxiv.org/html/2605.18644).
Their CRT tools and reported results are prior art. No literature theorem
is restated as new, and no secondary record search is undertaken here.

Source checks are same-author independent implementations, not independent
peer review or formalization. Python integer/rational arithmetic and
literal modular predicates are the trust base. The C++ finite enumeration
uses24-bit unsigned masks, a2^24-byte table, standard-library sets, and
bounded exact arithmetic; release and sanitizer builds are required.
No solver, generated large certificate, database, or external dataset is
needed. All generated state stays in scratch, not the publication packet.

The global exact-eight candidates remain10080,15120,20160 with20160
witnessed in prior work. This packet resolves neither10080 nor15120,
does not assert feasibility of any open root, and makes no assertion
about minimum-at-least-eight as a substitute for minimum-exactly-eight.
