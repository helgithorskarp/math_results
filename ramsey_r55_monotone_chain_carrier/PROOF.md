# Monotone-chain compression of the complete Ramsey carrier

## Statement and exact scope

A good graph has no red or blue K5. Fix one ordered maximal-packing task:
vertices 0,...,42 have q four-blocks, the first r red and the rest blue,
followed by a fixed core, where 7 <= q <= 10 and 5 <= r <= q. The task also
forbids red K4 on vertices 4r,...,42 and imposes the published root-column
and same-color whole-block orders. Fix **every core and block-to-block
color**, but leave all four-block/core-vertex stars free. Call this choice
a frame. No symmetry of the graph is assumed.

**Theorem.** Put m=q(43-4q) and

    L(z) = 5 + 3z^2 + 3z^-2 + z + z^-1 + z^3 + z^-3,
    A_m = [z^0]L(z)^m + [z^1]L(z)^m.

The 15^m star vectors in every frame admit an explicit, disjoint partition
into A_m saturated chains under inclusion of red edges. In each chain,
let H be its first graph with no blue K5, if there is one. The original
task has a model in that chain if and only if H has neither a red K5 nor
a residual red K4. Thus every frame needs **at most one candidate per
chain**. Each negative chain obligation has a certificate consisting of
at most two actual parent forbidden vertex sets and a RUP proof of at most
two additions to its restricted chain formula.

The theorem applies separately to **all 2,189,178 original tasks**, and also
to every core assignment, including unlisted assignments, in all four
physical M_r bases (r=5,6,7,8). In particular, all 956 core-guarded q8
cohorts have the same strict factor greater than 20 in the number of
candidate obligations. This is a change of candidate graph within the
**same task and frame**, not an assertion that every old model already
satisfies a new implicate, and not recovery of erased original colors.

The result establishes no original-task retirement, closed physical
cohort, good43, new Ramsey bound, or measured runtime improvement. It is a
complete-carrier reduction with a certificate interface. No target SAT
solver was invoked.

## 1. Local domains and a disjoint partition

For a red four-block the incident star cannot be 1111; for a blue
four-block it cannot be 0000. Otherwise that block and the core vertex
already form a forbidden five-set. These are exactly the 15-element star
domains in the reviewed carrier. No other domain restriction is used.

Here is the deterministic local chain partition, in mask notation. Mask
bit j is the red color at block position j.

    red block:  (0,1,3,7), (8,9,11), (4,5,13), (12), (2,6,14), (10)
    blue block: (1,3,7,15),(8,9,11), (4,5,13), (12), (2,6,14), (10).

Both lists partition their domain and have lengths 4,3,3,1,3,1. Every
successive step adds one red edge. The lists can also be obtained by the
classical symmetric-chain construction on B4 and removing the appropriate
endpoint of its longest chain. The truncated local domains themselves
are not asserted to have symmetric rank sequences.

Choosing one local chain at every star partitions the star product into
rectangular boxes. Each box is a product of finite chains, and hence has
an explicit symmetric chain decomposition. For completeness, the exact
construction and coverage proof follow; no external chain theorem is
needed as a soundness premise.

For [a] x [b], with coordinates 0,...,a-1 and 0,...,b-1, take, for each
0 <= t < min(a,b), the hook

    (0,t),(1,t),...,(a-1-t,t),
    (a-1-t,t+1),...,(a-1-t,b-1).

It has length a+b-1-2t. Every point (i,j) lies in exactly the hook
`t=min(j,a-1-i)`: if j=t it lies in the horizontal part; otherwise
`i=a-1-t` and it lies in the vertical part. This proves both coverage and
disjointness, including rectangles of unequal side lengths. Successive
ranks increase by one, and the first and last ranks sum to a+b-2.

Inductively multiply a previously decomposed product by its next chain.
A previous chain starting at rank s and ending at rank D-s, of length a,
when multiplied by a length-b chain produces hooks whose endpoint rank
sums are `2s+a+b-2=D+b-1`. Thus the chains are symmetric in the rank of
the **whole box**, as required. Boxes may have different centers; they
are never merged by an unjustified common-center assumption.

The local-chain choices and successive hook choices are unique addresses.
`chains.py` ranks and unranks these addresses by exact suffix counts,
and decodes any within-chain position to all physical star masks. A
chain has length at most 3m+1. The empty product has one singleton chain.

## 2. Exact number of chains

In a box with side lengths b_i, let D=sum(b_i-1). Every symmetric chain
meets rank floor(D/2) exactly once. The number of its chains is the middle
coefficient of the product of `(1+x+...+x^(b_i-1))`.

Center the rank of each factor and double its exponent. A length-one
chain contributes 1; a length-three chain contributes `z^-2+1+z^2`; a
length-four chain contributes `z^-3+z^-1+z+z^3`. Summing over the six
local choices gives L(z). If D is even, the middle coefficient is at
exponent zero; if D is odd, either exponent -1 or 1 gives it. All
exponents in a given box have the parity of D. Consequently summing
`[z^0]+[z^1]` over all boxes counts exactly one middle coefficient per
box, proving the stated expression for A_m.

An independent integer recurrence records the lengths of the constructed
chains. Start `d_0(1)=1`. For each old length a, each new local length b
with multiplicities `mult(1)=2, mult(3)=3, mult(4)=1`, and each
`0 <= t < min(a,b)`, add

    d_(m+1)(a+b-1-2t) += mult(b) * d_m(a).

Then `A_m=sum_a d_m(a)` and `sum_a a*d_m(a)=15^m`. The latter also checks
that chain lengths sum to the full carrier volume. This recurrence, the
Laurent coefficient calculation, and the suffix rank/unrank count agree
exactly at every campaign value of m. Exhaustive small-product checks
are controls for the implementations, not the proof of all-m coverage.

## 3. A single boundary graph decides the chain

Write the graphs of a chain as H_0,...,H_(ell-1), adding one red edge at
each step. Deleting blue edges cannot create a blue K5. Therefore the
states without a blue K5 form an upper interval, possibly empty. Adding
red edges cannot remove a red K5 or a red K4 in the prescribed residual.
The states with neither red obstruction form a lower interval.

If the upper interval is empty, the top graph has a blue K5 whose edges
are blue throughout the chain. Otherwise let k be its first index. If
any H_j in the chain is a model of the task, j >= k and H_k is a red
subgraph of H_j. It has no red obstruction, no blue K5 by definition,
and all fixed-frame conditions still hold. Conversely a passing H_k
is itself a task model. This proves the equivalence **within each chain**.

For k>0 the preceding graph has a blue K5. If H_k has a red obstruction,
these two witnesses cover all states below and above the cut. For k=0
only the red witness is needed. If the top fails in blue, only that blue
witness is needed. No claims about frozen-edge rigidity, automorphism
orders, or local packing thresholds enter the argument.

The implementation locates k by binary search, using at most
`1+ceil(log2(ell))` blue-clique tests (plus a witness extraction at k-1
when needed), then tests red obstructions at one graph. Binary search is
not trusted for negative certificates: their two literal witnesses
already cover the entire chain. Positive packets are checked directly
against every physical five-set and every residual red four-set.

## 4. RUP chain certificates and the receiving boundary

Let e_1,...,e_(ell-1) be the successive physical edges turned red, and
write y_j for the red color of e_j. All other physical colors are fixed.
The chain states are exactly the assignments satisfying

    (not y_(j+1) or y_j),   1 <= j < ell-1.

These assignments are the prefixes of ones followed by zeros. These
clauses are **chain restrictions**, not consequences of an unrestricted
parent. Actual physical variables are renamed y_j only after restriction.

For an interior cut 0<k<ell, the blue witness at k-1 gives a positive
parent five-clause whose remaining variables have indices at least k.
Negating y_k propagates all those variables false through the chain
clauses. Thus adding the unit y_k is RUP. The red witness at k gives a
negative parent five-clause, or a negative residual four-clause, all of
whose remaining variables have indices at most k. The new unit propagates
them true, giving a conflict. Adding the empty clause is RUP. If an
endpoint witness is used, its restricted forbidden-set clause is empty
already. This proves the two-addition bound without a SAT-solver premise.

`check.py` imports no producer module. It reconstructs the full physical
chain from the local-chain/hook path, checks its integer index and every
single-edge step, checks the actual witness vertices and fixed colors,
then emits the restricted parent clauses and chain clauses. It checks
each RUP addition by unit propagation. For a positive packet it checks
all five-sets and all residual four-sets literally. It is a separately
structured author implementation, **not independent peer review**.

A receiver must keep the complete obligation identity: original task or
physical base/guard, fixed frame, and chain index. A chain closure is
**not** an original-task refutation or a cohort cover certificate. To
close a parent by this route, every frame/chain obligation in its exact
range must be certified, and the disjoint-cover theorem must be used.
A list or interval manifest with a missing chain is incomplete. The
current R2 unit-assumption importer cannot import these chain refutations
as unguarded parent RUP lemmas. No such import is claimed or performed.
The written exhaustive chain join is an additional trust boundary; no
single monolithic DRAT proof of the complete carrier is supplied.

## 5. Exact consequence for the reviewed complete carrier

Put a=r-1, b=q-r, n=43-4q. The fixed-frame factor in an ordered task is

    K(q,r) = binom(1998+a-1,a) * binom(1931+b-1,b)
             * 37823^(binom(a,2)+binom(b,2)) * 35714^(a*b).

The root multisets retain ties. Pair domains, core, and root orders are
unchanged. All stars are independent carrier coordinates. Hence the
exact old count is `K(q,r)*15^(qn)`, and the exact number of new chain
obligations is `K(q,r)*A_(qn)`. These counts include failing candidates;
they are not numbers of solutions or isomorphism classes.

| q | core order | m | old star states / new chain obligations |
|---|---:|---:|---:|
| 7 | 15 | 105 | 22.0392182377... |
| 8 | 11 | 88 | 20.1840778698... |
| 9 | 7 | 63 | 17.0940295922... |
| 10 | 3 | 30 | 11.8387084895... |

The exact integers and strict bounds >22, >20, >17, >11 are in
`COUNTS.json`. Summing with core multiplicities 640, 546356, 362, 4
reproduces the complete h3887 old integer P **exactly**. Its ratio to
the new total is 16.9037761721... . No separate reduction factor has
been multiplied into a count taken from a different representation.

`bridge.py` exposes an exact indexed original-task adapter. Because the
stars are the last mixed-radix coordinates in the pinned carrier, the
old frame index is `old_code // 15^m`. Replace the final radix by A_m.
The adapter maps each old graph to its unique new chain code and position,
and reconstructs all 903 physical edge colors exactly. This works for
every core index by the identical frame/star factorization. The 18
macro-class round-trip controls exercise beginning, middle, and endpoint
old codes; they are not a census of the 2,189,178 formulas.

## 6. Complete physical q8 and compatibility limits

M_r has eight four-blocks and an **arbitrary** eleven-vertex core. Each
239-leaf guard partition restricts seven or eight of the 55 core edges.
For a guard of length g, the number of full core assignments is 2^(55-g),
regardless of how many catalog representatives its cylinder contains.
For every one of the four bases and every guard, the exact counts are

    old: K(8,r) * 2^(55-g) * 15^88,
    new: K(8,r) * 2^(55-g) * A_88.

The factor 20.184... therefore applies to **all 956 cohorts**; no listed
core, guard, r value, or sampled carrier is selected for the theorem.
The 17 guards of length seven and 222 of length eight partition all
2^55 assignments. Their complete physical volume identity is checked.
Cores failing a pure-core obstruction can be rejected immediately, but
remain included in these raw complete coordinate counts.

`bridge.PhysicalCohort(r, guard)` ranks the full obligation range by
block-frame index, arbitrary core-cylinder index, and chain index. It
reads the pinned block-domain source and requires no catalog data.
Its checked wrapper binds the base, guard, frame, and chain identity.
The physical guard checker rebuilds the published mapping: variable 1
is true, the 855 non-internal physical variables are 2,...,856, and the
core occupies 802,...,856. A core guard is preserved because the full
core is fixed within each chain. Root comparators use block-to-block
edges only, so their physical inputs and unique auxiliary extensions
are also preserved. The previously forced r=8 edge 119 is the pair
(3,4), a block-to-block edge; its positive branch is preserved as well.
The exact >20 ratio also holds after fixing that edge, since the star
factor cancels. Its exact active frame interval is available in
`PhysicalCohort(8, guard, require_edge119=True)`. There are 213 allowed
red root matrices below 4096; the sorted root multiset is below this
threshold exactly when all seven entries are among these 213. Thus the
excluded fixed-frame prefix has size `binom(219,7)*37823^21`. Subtract
this from K(8,8). In the published colex multiset numbering these entries
form an initial interval, so adding this offset is an exact complete
index for the positive branch. This implements the inherited edge-119
restriction, rather than proving a new stratum exclusion.

The mixed-q7 redirect can be composed by simply omitting q7,r5/r6 from
this complete task sum; the optional count is recorded separately. With
the reviewed R2 cross-stratum join, the same theorem covers all 956 M_r
branches and all 1,010 remaining parents. It does not itself prove or
replace that join.

The pass33 core-exchange normal form can change under star recoloring.
Its reduction factor is **not multiplied** by this one. Additional
q10 regularity/orientation restrictions, arbitrary cross-edge cubes,
and other receiver-specific cuts are not asserted preserved. A cut
using only fixed-frame colors is preserved; a universally proved
consequence of being good43 holds for a passing output graph, but it
cannot be used to claim that arbitrary chain states remain in a chosen
restricted carrier.

## 7. Literature, novelty, and trust

Symmetric chain decompositions are classical: de Bruijn, van Ebbenhorst
Tengbergen and Kruyswijk, *On the set of divisors of a number* (1951),
[primary bibliographic record](https://research.tue.nl/en/publications/on-the-set-of-divisors-of-a-number/).
For a modern author's treatment of explicit product constructions see
[David--Spink--Tiba, *Symmetric Chain Decompositions of Products of Posets with Long Chains*](https://math.stanford.edu/~hspink/LongChain.pdf).
RUP is an established proof system; see the
[author's DRAT-trim documentation](https://www.cs.utexas.edu/~marijn/drat-trim/).
No priority is claimed for these tools or the elementary intersection of
upper and lower intervals. The contribution is the explicit taskwise
Ramsey reduction, its complete physical all-q/all-guard counts, and the
physical two-witness receiver. A targeted literature and graph search
found no identical application, which does not establish priority.

The current published bound remains 43 <= R(5,5) <= 46;
[Angeltveit--McKay, JGT 2026](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.70029)
is the primary source checked during this pass. The historical defective
order-five automorphism exclusion is not a dependency.

The chain theorem, exact recurrence, and negative witness soundness need
no Ramsey catalog and no external Ramsey number. Interpreting the
original registry as a cover of every good43 imports the reviewed
maximal-packing proof, its R(4,5)<=25 and R(4,4)<=18 inputs, catalog
completeness, and its labeling bridges. The physical theorem is stated
for the exact M_r bases independently of catalog completeness. Using the
956+1,010 global join imports that separate result and its source review.
Source hashes and current review state are recorded separately.

The proofs are ordinary unformalized mathematics. Python exact integers,
file semantics, the transcriptions and mapping code, SHA-256, hardware,
and the written complete-cover join remain trust boundaries. The three
external DRAT replays check small protocol certificates, not the whole
carrier. The exhaustive small physical class and positive good42 fixture
validate semantics; neither is evidence of a new finite Ramsey endpoint.
