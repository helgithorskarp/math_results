# Arbitrary inflation: nonrepair and exact universally safe blocks

Theo, literature-researcher-4, 2026-10-05. Status: author uniform partial
argument awaiting Lyra's separate independent check. Target410 remains the
full boxed2143 growth decision and is not solved. This is a new versioned
claim, outside the earlier accepted increasing-block packet and its public
commit. No priority or novelty claim is made.

For p in S_m and nonempty permutations tau_1,...,tau_m, the inflation
p[tau_1,...,tau_m] replaces each p_i by a consecutive position block with
relative order tau_i. Each block occupies a consecutive value interval, and
the intervals are ordered as the values of p. Write occ(p) for its number
of boxed2143 occurrences. Every value and every position is distinct.

## 1. Arbitrary inflation cannot remove an existing occurrence

**Lemma A.** For arbitrary nonempty blocks, every boxed2143 occurrence of p
has a canonical boxed lift. Consequently

    occ(p[tau_1,...,tau_m]) >= occ(p).

**Proof.** Let blocks i1<i2<i3<i4 be an original boxed selection, in value
order p_i2<p_i1<p_i4<p_i3. Select the last position of block i1, the maximum
value of block i2, the minimum value of block i3, and the first position of
block i4. The value bands imply the same2143 order. Other entries of the
first and fourth selected blocks are horizontally outside the new box. Other
entries of the second block are below its selected maximum, which is the
new minimum boundary; other entries of the third are above its selected
minimum, which is the new maximum boundary. Each unselected block between
i1 and i4 is vertically outside: its original point was outside the original
box, so its entire value interval is below block i2 or above block i3.
Thus no extra point is inside the lifted rectangle.

The lift is injective on original selections, since its four selected points
identify their original blocks. It makes no assumption on any internal block
pattern. QED.

Thus changing to arbitrary block permutations cannot repair an arbitrary
nonavoiding input. This strengthens the nonrepair direction of the checked
increasing-inflation lemma, without asserting equality for general blocks.
For example, inflating12 by21,21 gives2143, so new occurrences can appear.

## 2. Exact additivity for blocks anchored at their extrema

Call a nonempty block anchored when its first entry is its minimum and its
last entry is its maximum. A singleton is anchored. Internal block patterns
need not avoid anything in the next lemma.

**Lemma B.** For anchored tau_i,

    occ(p[tau_1,...,tau_m]) = occ(p) + sum_i occ(tau_i).

Moreover, the cross-block occurrences are precisely the canonical lifts in
Lemma A; internal occurrences are the unchanged occurrences of each block.

**Proof.** Selected entries of the same block must be consecutive in the
selected order. If two belong to roles2 and3, their minimum and maximum
enclose both remaining selected values. Those values cannot lie in other
disjoint value bands, so all four selected points would have to lie in that
same block. Three selected points in one block likewise force all four there:
in roles1,2,3 the omitted role4 is between the selected block minimum and
maximum; in roles2,3,4 the omitted role1 is between them.

Consider a cross-block occurrence with roles1 and2 in one block. Its selected
first value exceeds its selected minimum. The block's last point, its maximum,
must therefore be after role2: it cannot equal either of those roles. This
unselected point is horizontally inside the box and vertically above the
selected minimum and below the selected maximum in a higher value block.
It blocks the occurrence. Similarly, if roles3 and4 share a block, its first
point is its minimum and must be before role3. That unselected point is
horizontally inside and vertically between the selected minimum in a lower
band and the selected maximum; it blocks the occurrence. These exhaust the
ways a cross-block selection could repeat a block.

Every remaining cross-block occurrence uses four distinct blocks. Its
projection is boxed in p: any original interior point would contribute an
interior point from its whole value band. Its first selected point must be
the first block's last entry, since every later point of that intermediate
band would be inside. Its fourth must be the fourth block's first entry.
Its second point must be its block's maximum, since any larger point of
that block is horizontally inside and vertically between the new boundaries.
Its third must be its block's minimum, by the symmetric argument. Thus it
is exactly the canonical lift of Lemma A, and each original occurrence has
exactly one cross-block lift.

A selection wholly inside one block has unchanged order and interior points;
every other block is horizontally outside. These internal selections are
disjoint from the cross-block ones and from one another. Counting gives the
identity. QED.

## 3. Classification of blocks which preserve avoidance in every context

A nonempty tau is universally safe if, for every boxed2143-avoiding p and
every position i, replacing p_i by tau and every other entry by a singleton
still gives a boxed2143 avoider.

**Theorem C.** A block is universally safe if and only if it avoids boxed2143,
starts with its minimum and ends with its maximum. In particular the number
of universally safe blocks of size r>=2 equals a_(r-2); size1 has one.

**Proof of sufficiency.** All singleton blocks are anchored and avoid. If
tau also has those two properties, Lemma B says the inflated occurrence
count is zero. This even allows simultaneous inflation by any collection
of universally safe blocks.

**Proof of necessity.** If tau itself has an occurrence, inflate the unique
entry of p=1; the output is tau and is not avoiding. Now let tau have size r
and fail to start at its minimum. Set c=tau_1>1 and let d be the first later
entry smaller than c. All entries strictly between c and d in position exceed
c. Inflate the maximum entry of the avoiding parent213 by tau. The result
is(2,1,tau+2). Its selected2,1,c+2,d+2 have2143 order. The intervening block
entries exceed c+2, so its rectangle is empty. Thus tau is unsafe.

If tau fails to end at its maximum, set b=tau_r<r and choose a as the last
earlier entry exceeding b. All entries between a and b in position are below
b. Inflate the minimum entry of the avoiding parent132 by tau. The result
is(tau,r+2,r+1). Its selected a,b,r+2,r+1 have2143 order and no interior
point: the intervening tau entries are below b, and b is the last block point.
Thus tau is unsafe. Both parent permutations have size3 and therefore avoid
the length4 pattern. The cases cover every failure of the stated conditions.

For r>=2 an anchored block is(1,q+1,r), with q in S_(r-2). Its two boundary
points cannot be selected in any boxed2143: the first is the global minimum
and has no predecessor for role2, while the last is the global maximum and
has no successor for role3. Every occurrence lies in q and its rectangle
is unchanged. Hence such a block avoids exactly when q does, giving a_(r-2).
The r=2 case uses the empty q and a_0=1. QED.

Both boundary requirements matter. A block132 starts at its minimum but is
unsafe: inflating the minimum of132 gives13254, with occurrence3254. A
block213 ends at its maximum but is unsafe: inflating the maximum of213
gives21435. A block1324 has both boundaries and avoids, so increasing order
is not necessary.

## 4. Full occurrence composition formula for arbitrary blocks

For a block tau, let R(tau) count its right-to-left maxima which have a
greater earlier entry. Let L(tau) count its left-to-right minima which have
a smaller later entry. In particular R(tau)=0 exactly when tau ends at its
maximum, and L(tau)=0 exactly when it starts at its minimum. Necessity follows
by taking the last or first point if the corresponding boundary fails;
sufficiency follows because that boundary dominates every other record.

Write Box_k(p) for the position selections which form a boxed occurrence of
the indicated pattern k, with the same strict bounding-rectangle convention.
For k=12, this is a pair; for132/213 it is a triple. Empty extra selections
do not affect the following formula.

**Theorem D.** For arbitrary nonempty blocks, with P=p[tau_1,...,tau_m],

    occ(P) = occ(p) + sum_i occ(tau_i)
           + sum_((i,j,k) in Box_132(p)) R(tau_i)
           + sum_((i,j,k) in Box_213(p)) L(tau_k)
           + sum_((i,j) in Box_12(p)) R(tau_i)L(tau_j).

**Proof.** Partition each selection according to its selected blocks. Four
distinct blocks have exactly the canonical lift of Lemma A: the first and
last points are forced to their block position boundaries, and the minimum
and maximum roles are forced to the appropriate block value extrema.
Projection is boxed because every original interior point supplies a whole
interior band. This gives occ(p), with no assumption on block anchors.
Selections in one block contribute its unchanged internal occurrences.

Three entries in one block force all four there, by the value-band argument
in Lemma B. A repeated block in roles2/3 likewise forces all four there.
The remaining cases are therefore roles1/2 in one block, roles3/4 in one
block, or both pairs in two separate blocks.

For roles1/2 in block i, write a>b for their two values. Every other point
of this block after a is horizontally inside the selected box and below
the selected maximum in a higher band. It must therefore be below b.
Equivalently, b is a right-to-left maximum with a greater earlier entry,
and a is its nearest earlier greater entry. That a is unique; all entries
after a other than b are below b. There are exactly R(tau_i) such pairs.
With the last two roles in distinct blocks j,k, their relative block order
is132. The selected maximum is the minimum of block j; the selected final
point is the first point of block k. Projection is boxed exactly when the
three block points are boxed132 in p. Every such boxed triple and every
one of the R(tau_i) pairs supply one occurrence, giving the first extra sum.

The symmetric roles3/4 case uses a left-to-right minimum c with a smaller
later entry d, taking d as its nearest later smaller entry. All points before
d other than c exceed c. The first two roles in distinct earlier blocks
give a boxed213 in p, with the first block's last point and the second
block's maximum. This gives the second extra sum.

If both descending pairs repeat their blocks, the two selected block points
form a boxed12 in p. The choices are exactly the R(tau_i) left pairs and
L(tau_j) right pairs just described, independently. Their value bands supply
the required2143 order; unselected blocks are outside if and only if the
parent pair is boxed. This gives the product sum. These cases are disjoint
and exhaustive, proving the formula. QED.

Anchored additivity is the R=L=0 special case. The formula also states the
precise conditional safety criterion for any inflation of an avoiding p:
all internal block counts and the three nonnegative extra sums must vanish.
It is an exact counting identity, not a bound on the unresolved a_n.

## 5. The full growth decision reduces to simple avoiders

An interval of a permutation is a consecutive position segment whose values
are consecutive integers. A permutation is simple when its only intervals
are singletons and the whole permutation. Let s_k count simple boxed2143
avoiders of size k; include both12 and21 as simple size2 permutations.

**Theorem E.** Bounded-exponential growth of a_n is equivalent to
bounded-exponential growth of s_n. If s_k<=D^k for every k>=2, with D>=1,
then the explicit bound a_n<=(16D^2)^n holds for every n>=1.

**Proof.** The forward direction is inclusion, s_n<=a_n. For the converse,
every avoiding permutation has a substitution tree whose internal labels
are simple avoiders and whose leaves are individual points. To construct one,
if a current permutation is simple, make it an internal label with singleton
children (or one leaf for size1). Otherwise choose a nontrivial proper interval
of minimal size. Its standardized permutation is simple: a smaller nontrivial
interval inside it would be a smaller interval of the current permutation.
Its internal boxed occurrences agree with their occurrences in the whole
permutation, so this label avoids. Contract that interval to one point.
The resulting quotient avoids by Lemma A's contrapositive, since inflation
cannot remove any quotient occurrence. Recursing on the smaller quotient
and grafting the contracted simple label at the corresponding leaf gives
the desired tree. A deterministic tie rule makes this an encoding if desired;
evaluating any such tree recovers the original permutation, so two distinct
permutations cannot have the same encoded tree.

For a tree with n leaves and no internal vertex of degree1, the number I of
internal vertices is at most n-1; hence V=n+I<=2n-1 and the sum of internal
degrees is V-1<=2n-2. The number of ordered rooted tree shapes with v vertices
is at most4^(v-1), by its balanced traversal word or the standard Catalan
bound. Summing over1<=v<=2n-1 gives fewer than16^n shapes. Each internal
vertex of degree k has at most s_k<=D^k label choices. Thus at most D^(2n)
labels occur per shape and at most(16D^2)^n encodings altogether. Size1 is
the single-leaf case. The constructed encodings form a subset of these
trees, so extra trees need not evaluate to avoiders for this upper bound.
This proves the equivalence. QED.

The useful new bottleneck is therefore a uniform bound on all simple avoiding
labels or an unbounded-rate family of them. Simplicity alone is not sufficient
for avoidance:531642 is simple and has the contiguous boxed2143 at positions
2,3,4,5 (one based), values3,1,6,4. No claim that all simple permutations
avoid, or that their present finite counts control growth, is made.

## Scope, controls and the remaining full-target obligation

This gives exact substitution boundaries and a reduction of the entropy
obligation, not a solution of that obligation. The safe-block count is
expressed in the same unresolved sequence a_n.
No injection of arbitrary S_m into avoiders, uniform exponential bound or
unbounded root growth is obtained. The usual inflation operation cannot repair
any pre-existing boxed occurrence, while flexible interleaving remains outside
these lemmas.

The source-known increasing size-two preservation is Kitaev–Qiu–Xu,
Proposition7.6, https://arxiv.org/html/2609.13764v1 . The previous increasing
all-positive-size proof is in the separately checked and published structural
packet. The arguments here are derived directly; a future novelty claim would
require a specific literature refresh. No source or graph publication of this
new scope should inherit the older acceptance.

`arbitrary_inflation_controls_v1.py` supplies finite controls for the
canonical lift, anchored additivity, full occurrence formula, explicit
universal-safety counterexample contexts and simple-label contractions/tree
reconstruction. Such controls can falsify these proofs but cannot justify
their infinite quantifiers. A separate different-researcher check is still
required.
