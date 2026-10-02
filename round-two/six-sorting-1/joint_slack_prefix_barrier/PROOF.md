# A changed 22-comparator prefix requires at least45 comparators

Author and executing agent: **six-sorting-1**, role **researcher**,
2026-10-01. Status: proved with two exact representations by this
researcher; unformalized and independently unreviewed.

Let N19 be the literal first19 comparators of the maintained N13L46D9
word, copied in [fixture.json](fixture.json). Define

~~~text
B21 = N19;(4,8);(3,6)
E22 = B21;(3,9)
E23 = E22;(9,11).
~~~

Every comparator(a,b), a<b, puts min on a and max on b. Its position
in the prefix is part of the hypothesis.

**Theorem.** Every standard thirteen-input sorter beginning with E22
has at least45 comparators, at arbitrary suffix order and depth. This
also excludes every literal E22;(a,b) extension at total size<=44.
No45-comparator completion of E22, exclusion of all B21 completions,
reverse-oriented suffix theorem or unrestricted S(13)=45 is claimed.
The primary thirteen-input size interval remains44..45.

## Ordinary marked profiles and anchored passages

Place the two largest distinct values at each original pair of inputs,
with the other eleven inputs free. Let D count prefix comparisons
meeting either mark, once even when both are marked. Stationary touches
count. The marked pair's route is independent of the free values. At a
current pair z retain d(z)=max D over its original witnesses, and put
W=sum_z2^d(z). A comparator has at most two old pair configurations
per new configuration; a double fibre charges both. Therefore
2^(1+max(d1,d2))>=2^d1+2^d2 shows W cannot decrease.

At the end of a total-m sorter, both marks occupy11/12. Pruning them
leaves an eleven-input generalized sorter with at most m-D comparisons.
The established S(11)>=35 and standardization give D<=m-35. Hence
W<=2^(m-35) at every prefix of that sorter. The large primary proof
corpus for S(11) is imported, not replayed here.

For a reachable unary-maximum port p define
M_p=sum_{z containing p}2^d(z). If a comparator touches the unary
maximum route p and sends it to q, the pair map restricted to pairs
containing p is injective and every such pair is charged. Thus
M_q(next)>=2 M_p. If the unary route is untouched, membership of its
port is preserved and the ordinary fibre inequality gives nondecrease.
If that route has r future touches, including stationary ones, then

~~~text
2^r M_p <= 2^(m-35).
~~~

This is the ordinary case of established anchored extreme transport.
Its proof retains original marked placements for counting, and does
not merge conditional free-input images to decide identity deletions.

## Exactly one possible first maximum event

The certificate reconstructs every original two-high placement. At E22
the unary-maximum candidates are precisely9,11,12 and the ordinary
anchored two-high masses are

| Candidate port p | M_p | Maximum remaining touches if m<=44 |
|---|---:|---:|
|9|128|2|
|11|96|2|
|12|224|1|

Every candidate route must coalesce at12. A comparator meeting two
currently distinct routes merges them; one meeting just one route is
a unary event. Three routes require exactly two binary merges. The
route beginning at12 has only one touch available, so it can join only
at the final merge, and has no unary allowance. The routes from9 and11
must first merge with each other and then join12. Each uses its entire
two-touch allowance, leaving no unary event for either one.

Consequently the first comparator meeting any current unary-maximum
candidate must be(9,11). Every earlier comparator avoids9,11,12,
and therefore is disjoint from this first event. Commute(9,11) to the
suffix front, preserving the full sorting function and the total size.
The resulting word begins with literal E23. No limit on the number
of earlier preparations, depth or subsequent comparisons is imposed.

The computational first-event audit examines all78 standard pairs.
The inherited anchored leaf labels at E22 are9:42,11:42,12:43, whose
weights sum to2^44. There are45 pairs avoiding all three candidates,
one permitted live pair(9,11), and32 excluded live pairs. This exact
dyadic audit agrees with the passage-budget argument above.

## The compulsory event already violates the budget

At E23 the ordinary anchored two-high mass at11 is320. A unary
maximum still reaches11, so a full sorter needs at least one further
touch on that route to reach12. The anchored inequality would require

~~~text
2*320 <= 2^(44-35) =512,
~~~

which is false. Thus E23 has no total-size-at-most44 completion, and
the commutation proves the same for E22.

As an independently reconstructed auxiliary check, semantic anchors
from the full unary-high, two-high and mixed families give at E22
the leaves9:42,11:42,12:43, and at E23 the leaves11:44,12:43. The
normalized high mass increases from512 to768 at base35. This gives
the same size45 lower bound. The ordinary proof above needs only
S(11)>=35; S(12)>=39 enters this auxiliary family check.

At B21 the ordinary two-low mass is448, with leaves1/2/4 of cost7
and leaf3 of cost6; its unary-high anchored leaf weights also sum to
448 at base35. Gate(3,9) raises both masses to512, explaining this
construction experiment's two budget ceilings. Saturating both does
not give a valid44-completion: the first required high merge fails.

**Conditional B21 consequence.** If the first suffix comparator
meeting the original live support{0,1,2,3,4,9,11,12} is(3,9), all
preceding gates avoid3 and9, so it commutes to the suffix front and
creates E22. That first-event branch is therefore excluded. This
does not classify other B21 event branches or arbitrary preparations
using a future event's free endpoint.

## Exact evidence and provenance

[generate.py](generate.py) uses the credited hash-pinned packed-column
profile and anchor production modules. [verify.py](verify.py) imports
no producer, profiler, sibling checker, solver or nonstandard package.
It instead executes scalar distinct low/high ranks on every original
conditional free Boolean assignment, recovering D, whole-domain free
identities R, their masks, current ports and envelopes entry by entry.
The ordinary proof uses D alone; additional semantic data are checked
rather than assumed. Both original marks and their entire domains are
retained separately before class maxima are formed.

The three literal stages B21/E22/E23 comprise975 original domains and
2,076,672 free assignments. All78 first-event pairs are audited. Two
known sorters of45/46 comparators pass all16,384 original Boolean
controls; these controls do not supply completions of E22. Nine damaged
cost/mask/domain/anchor/event/prefix certificates reject. Normal and
optimized runs agree on every finite mathematical field and production
certificate bytes. The compact certificate has34,529 bytes, SHA256
813faa0b8a86cf2698479daa29def96a506ae835ccdfee69b64b8c64f997d764.
Scalar runs took17.387/17.378s with17,912/20,168KiB peak RSS, each
under the unchanged55-second guard, one CPU job and threads1.

Primary literature: [Harder, Section3.2](https://arxiv.org/html/2012.04400v3#S3.SS2)
for pruning/standardization and S11/S12, and the
[maintained primary table](https://bertdobbelaere.github.io/sorting_networks.html)
checked2026-10-01 for the continuing44..45 global interval. The general
pruning/route/Huffman/anchored techniques are established methods.
Campaign premises are the credited
[semantic pruning proof](../../six-sorting-2/semantic-pruning/PROOF.md),
graph8539 bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4,
and [anchor transport](../../six-sorting-2/semantic-pruning/ANCHORS.md),
graph8604 bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle.
The native fixture and known controls come from
[the earlier three-touch source](../three_touch_prefix_barrier/fixture.json),
commitdf4e3aa03d6bf96c21e7bdab1330b98db7e0fad2, graph8999.

The already committed [native P22 theorem](../../six-sorting-2/native24-kernel-cover/P22.md),
sourcebc3d409028c7cfdc4e773717a1b73eadc6d19386, graph9082
bafkreifanz5f6siwpdk5zpws6i2xgrxl2d4deqp5tggfwu3iqz64p3tjru,
is different literal prior art. Its method informs this first-event
proof; its complete cover is not transferred. E22 changes gates20/21
and appends a different gate22. The new result is this exact changed
prefix and conditional first joint-event branch, not a new general
transport theorem, complete B21 cover or global size45 lower bound.
