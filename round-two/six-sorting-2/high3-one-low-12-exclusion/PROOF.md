# HIGH3: one prior LOW merge (1,2) before the strict singleton

Actual author and executing agent: **six-sorting-2, researcher**,2026-10-02.
Status: complete scoped computer-assisted author proof. Cold source
reconstruction and separate same-author exact algorithms agree on the whole
mathematical record in normal and optimized Python. New independent-person
review and formalization remain pending.

Ports are0..12. A standard comparator(a,b),a<b, writes min at a. Let P be
this literal27-comparator prefix:

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
(9,11),(11,12),(3,6),
(6,7),(5,7),(9,10),(10,11),(7,11).
```

This is HIGH genealogy3/root12 in [9616](../one-sided-forest-frontier/PROOF.md).
All event counts start AFTER this entire P27, so the included LOW gate(3,6)
is not a later prior event.

**Conditional exclusion.** No standard sorting completion
of P of total size<=44 has its first strict ordinary two-LOW mass increase
a singleton, with exactly ONE earlier binary LOW merge after P, namely(1,2).
Arbitrary preparation words, repeated comparisons, interleaving and suffix
depth are allowed. There is no claim that P is a normal form for every
sorter, nor that the other three possible first LOW pairs are covered.

The new finite step tests all20322 normalized head/tail alternatives from
[the one-prior preparation lemma9780](../high3-one-low-preparation-cover/PROOF.md),
sourcea5e06f2fb29441691c2b941d631fd480f62ce10c. Its preparation theorem is
imported and reconstructed. Its source did not exclude these heads/tails.
The zero-prior theorem9729 and its earlier five-input preparation review9701
supply no new negative record or verdict here. This scope leaves first
pairs(3,4),(3,8),(4,8), two-priorLOW, other HIGH roots and the global44/45
gap open. The [current table](https://bertdobbelaere.github.io/sorting_networks.html)
still reports44..45.

## Arbitrary-depth normalization and complete tail structure

Import ordinary original-domain pruning and dyadic tag masses from
[8539](../semantic-pruning/PROOF.md). For l distinct original LOW ranks and
h distinct original HIGH ranks, keep the WHOLE Boolean cube of k=13-l-h
free inputs. D counts comparisons touching marked values; R counts
unmarked comparisons that are identities on every original assignment.
These are disjoint gate sets and C=D+R gives m>=C+S(k) for any sorter.
The pruning interface permits arbitrary l,h; it does not substitute another
original domain merely because its current marker pattern is equal.

Use published arbitrary-depth S11>=35/S12>=39 from
[Harder](https://arxiv.org/abs/2012.04400), and S9>=25 from
[Codish, Cruz-Filipe, Frank and Schneider-Kamp](https://arxiv.org/abs/1405.5754).
Their large lower-bound proof corpora are not re-proved here. A fixed-depth
UNSAT certificate is not a premise.

At P the LOW secondary costs are7,7,6,6,6 at1,2,3,4,8; mass448, held0.
HIGH has held12 and only secondary11 with cost9/mass512. In size<=44
all suffix comparisons avoid0/11/12. The published9780 preparation proof
commutes the stipulated first equal merge(1,2) before its preceding
preparations, since both endpoints remain continuously live until it.
Its Q=P;(1,2) inventory has LOW costs8,6,6,6 at1,3,4,8, mass448. Freed
physical2 is the TRUE max(old1,old2), never a substitute constant.

Before the first singleton all preparations act on D=(2,5,6,7,9,10).
Lemma9780 enumerates the full64-row/six-output functions with complete
closure:2335 functions/3002 admissible edges/1206 whole-original exits,
1129 retained functions. Its90 tight plus21 required-repair originals are
not replaced by their21 activity images in any negative certificate.
Every actual retained preparation word has length<=8, and its shortest
full-function representative F has the same ordered-input function by
threshold lifting. Replacing it never increases size, and every new
original record is recomputed on that representative.

Only a cost6 root can singleton without exceeding mass512. Thus H pairs
one of3/4/8 with one of the SIX D ports:18 labelled heads for each of1129 F,
20322 total. Let r=min(H), and u<v be the unselected two cost6 roots.
After H the live costs are8 at1,7 at r,6 at u and v, and mass512. Every
later LOW event must be an equal-cost binary merge; a singleton or unequal
merge would exceed the ceiling. To collect every original two-LOW class
at the correct secondary port1 requires exactly three such merges.

There is precisely one labelled word: compare(u,v), then compare(r,u),
then compare(1,min(r,u)). Sorting each pair's endpoints gives the standard
literal comparators. Complete recursion on labelled live costs admits
only that word, of length3. The separate checker reconstructs all18
head types and evaluates the resulting whole4-input/four-output function
on all16 Boolean rows; root1 is their minimum. No depth or tail-order
cutoff is present.

After H the live pool only shrinks. Every future merge endpoint is live
continuously until its merge, so intervening preparations avoid both of
its endpoints. Move each later merge left across those disjoint preparations,
keeping all LOW events in their original mutual order. A newly freed port
may be used by preparation gates but cannot be an endpoint of a later
merge. This covers arbitrary repetitions and interleavings; no comparison
is deleted or added. Every supposed sorter has a front Q;F;H, or the
normalized front Q;F;H;T followed by an arbitrary suffix. The latter front
has32+len(F) comparisons and remaining budget12-len(F),4..12.

The checker directly verifies every8192 full input at Q:0/11/12 are correct,
and the minimum at1/3/4/8 equals global rank1. Since0 holds the minimum,
every other value is at least global rank1. D-preparations preserve that
fact. H and T collect this second minimum at1. Threshold lifting extends
the statement to every totally ordered input. Thus no wrong held output
is discarded by a residual-image convention.

## Every actual front receives an original-domain obstruction

The compact [certificate](certificate.json) contains the ENTIRE1129-by18
head interface. An integer is a negative head reference; a one-entry list
supplies the unique negative tail if the head survives its earlier test.
There are11063 negative heads and9259 tail alternatives,20322 negative units.

| Stage/type | Number |
|---|---:|
| Negative heads, direct original cost |8805|
| Negative heads, tight marked-port lock |2258|
| Tail direct original costs |631|
| Tail tight original free cuts |1244|
| Tail tight marked-port locks |7384|
| All actual negative bindings |20322|

The1129 previously proposed tails use one/two-mark free cuts; the other
8130 require four marks. All11440 four-original-mark restrictions, each
with512 free Boolean assignments, were searched as sufficient selectors.
Those new proposals are631 direct,115 free cuts and7384 marked locks.
Failure of a sufficient selector would not have implied feasibility.
The final source only needs the actual selected originals, not the whole
search log. Its357 distinct witness records use34 original domains:
1 single-mark,12 two-mark and21 four-mark, with all four-mark l/h families
represented. Identical catalogue bytes share storage; each actual front
binding is separately replayed on its own full original cube.

DIRECT_COST has C+S(k)>44 and immediately excludes any sorting suffix.
For TIGHT_MARKED_PORT_LOCK, C+S(k)=44, port q is marked on the whole original
cube, and a supplied full13-input Boolean witness shows it at the wrong
global rank. A sorter must eventually touch q; avoiding q leaves that full
wrong output unchanged. Before the first such touch q remains marked on
all original assignments, so the touch adds a deletion, forcing>=45.
This is the credited pruning/marked-port lock from8539/9729.

For TIGHT_FREE_CUT, C+S(k)=44 and q is unmarked. On every original assignment,
every unmarked port left of q is<=q and every unmarked port right of q is>=q.
Any future marked touch already adds D and forces>=45. Until such a
touch, the marked physical ports remain fixed. Unmarked comparisons avoiding
q preserve the cut: within a side by min/max, and across q because the
endpoints are already ordered. A sorting suffix eventually touches the
globally wrong q, or has already contradicted tightness by touching a mark. If that first touch involves a mark it adds D;
otherwise the whole original cut makes it a free identity adding R. Either
case forces>=45. This is [9616's general cut mechanism](../one-sided-forest-frontier/PROOF.md),
with the minimum-lock precursor credited to [9525](../../six-sorting-1/conditional_minimum_lock/PROOF.md).

Combining any completed actual negative certificate with the exhaustive
normalization excludes every sorter satisfying the stipulated hypothesis.
All20322 certificates and24 intended controls have completed their separate
replay in both modes, completing the stated conditional exclusion.

## Source and trust boundary

The packed [producer](generate.py) rebuilds every selected original record
from [recipes](recipes.json) and the public9780 source. It checks repeated
recipe aliases agree on complete records. The scalar [checker](verify.py)
imports neither producer nor packed profile; it assigns distinct numerical
marked ranks and follows every free assignment. It checks all retained
full64-row functions, complete head/tail coverage, every selected D/R/tag/
identity mask, whole-cube cut and full wrong-rank witness. [Controls](controls.py)
include the genuine45-comparator network on all8192 Boolean inputs and all
selected numeric original domains, plus intended semantic damages.

[reproduce.py](reproduce.py) regenerates the parent graph locally, runs its
separate exact verifier, reconstructs the entire new catalogue, then checks
complete40-function slices in a serial native1 pipeline,55s per child. Large
generated arrays stay local in ignored generated/ or a selected scratch path.
Source manifest binds whole bytes and exact upstream provenance. Guard failure,
partial coverage or UNKNOWN is never a mathematical nonexistence statement.
Different same-author algorithms are not independent-person review. The
ordinary pruning/threshold/commutation bridges remain unformalized.

The complete mathematical record SHA256 is
`dfd9468069854c015d7aebc228bb3b5a6e6ce6748d83568d9c1086beb6c238da`; the147038-byte certificate SHA256 is
`9343691b400dc94b560cf4b6ad94c9b6796f70004b1bb5f3c0349af5cc08fee6`. All original34 selected numeric domains are
also sorted by the genuine45-gate positive control:39424 assignments,
plus8192 complete Boolean inputs and64 six-input positive rows. Every
new mathematical child completed under55s. No operations limit was raised.

Both full source runs used the documented author--record-only bootstrap:
all mathematical children, parent reconstruction and controls completed.
The final frozen-record comparison is checked against both entire saved
mathematical outputs. The default entrypoint was not rerun after the
checks.json metadata freeze; the mathematical source code and input bytes
are unchanged. This is stated explicitly rather than implying a later
uninterrupted default-entrypoint run.
