# Native HIGH3: excluding the zero-prior-LOW singleton branch

Actual author and executing agent: **six-sorting-2, researcher**,2026-10-02.
Status: complete scoped computer-assisted author proof. The new exclusion
has separate same-author exact algorithms; independent-person review and
formalization of this new result remain pending.

A standard comparator `(a,b)`, `a<b`, writes min to a and max to b.
Ports are0..12. Let P be the literal27-comparator prefix

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
(9,11),(11,12),(3,6),
(6,7),(5,7),(9,10),(10,11),(7,11).
```

This is HIGH genealogy3/root12 from the
[native one-sided cover9616](../one-sided-forest-frontier/PROOF.md).
All event counts below begin **after this entire P27**. Its already
included LOW gate `(3,6)` is not a prior event in that count.

**Conditional exclusion.** There is no standard sorting completion of P
of total size at most44 whose first strict increase of ordinary two-LOW
pruning mass is a singleton and has **zero prior binary LOW merges after
P**. The suffix has arbitrary comparator order and depth; repeated gates
and arbitrary interleavings with preparations are allowed.

The new step closes the singleton and equal-tail compatibility of all181
necessary functions from
[the preparation-cover lemma9661](../high3-zero-low-preparation-cover/PROOF.md).
That earlier source did not exclude any of its retained functions. Its
independent
[review9701](../../six-reviewer-5/zero-low-preparation-audit/REVIEW.md)
confirms the preparation cover and additionally bounds actual preparation
words by six gates. The new proof needs only9661's shortest full-function
replacement; the six-gate representatives are checked here, and the
review's stronger actual-word grading is credited, not claimed anew.
The review gives no verdict on this new singleton/tail exclusion.

Together with the credited both-first-binary obstruction
[9529](../native-binary-barrier/PROOF.md), the result removes the case with
zero LOW binary merges before the first strict LOW increase after P:
P's HIGH forest already has a binary first strict HIGH increase, so9529
rules out a binary first strict LOW increase. This corollary imports
9529's theorem; its405-front negative corpus is not replayed here.

The theorem does not remove one/two-prior-LOW cases of this HIGH3 root,
the other roots, the whole one-sided cover, or unrestricted13-input
size44. The maintained table still reports44..45. No claim is made that
this literal prefix is a normal form for every sorter.

## Pruning interface and the fixed event structure

For an original restriction f, fix l original inputs to distinct ranks
below all free values and h to distinct ranks above them. Retain the
**whole original** Boolean cube on k=13-l-h free inputs. D counts each
comparison touching any marked value once. R counts unmarked comparisons
that never swap on that entire original cube; these are disjoint gate
sets. C=D+R. Ordinary comparator pruning, threshold lifting and
standardization give

```
m >= C+S(k).
```

For fixed(l,h), group actual original restrictions by their current LOW
and HIGH port masks and take the maximum C in each group. The semantic
mass V, the sum of2^C over these groups, satisfies

```
V(prefix) <= 2^(m-S(k)).
```

Both statements are imported from
[semantic pruning8539](../semantic-pruning/PROOF.md).
The grouped mass is monotone: the tag map of a comparator has at most
two preimages per output configuration; a double fibre charges one
deletion to both histories and satisfies
`2^(1+max(u,v)) >= 2^u+2^v`. Original conditional functions remain separate
throughout the computation. A selected subset of histories with distinct
current masks gives a valid lower bound on V; it need not exhaust the
original restrictions. The proof of8539 covers general l,h, including
the four-mark cases used here, rather than just its original example.

We import the arbitrary-depth lower bounds S(11)>=35 and S(12)>=39
from [Harder](https://arxiv.org/abs/2012.04400), and S(9)>=25 from
[Codish, Cruz-Filipe, Frank and Schneider-Kamp](https://arxiv.org/abs/1405.5754).
These are published results, not new theorems or internally replayed
large lower-bound corpora. A chosen-depth UNSAT statement is not used.

At P, ordinary two-LOW secondary ports have costs

```
port   1  2  3  4  8
cost   7  7  6  6  6       LOW mass448.
```

LOW's held port is0. The sole ordinary two-HIGH secondary is11 at cost9,
with held12 and mass512. These original inventories and P's complete
136-state ten-core image are supplied by9661; its whole-byte certificate
and fixture are copied in [upstream/](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-sorting-2/high3-zero-low-exclusion/upstream) without modification.
The new scalar checker also replays all8192 parent Boolean inputs.
Ports0/11/12 already have their correct global ranks. Every future gate
avoids them: a touch of0 doubles LOW448 beyond512, and a touch of11 or12
doubles the sole HIGH512 class. The ceiling uses m<=44 and S(11)>=35.

Before the specified singleton there are no LOW merges, so all preceding
gates are preparations on DEAD=(5,6,7,9,10). Lemma9661 proves the complete
necessary cover of their full32-input/five-output functions, without
imposing a real word-length cutoff. A path cannot pass through any of
its193 certified exits. Replace the remaining actual preparation by
its retained shortest full-function representative F. This preserves
the entire ordered-input function, hence every original marked domain,
and does not increase size. Every retained representative has length0..6.

The singleton must involve one of the cost6 ports3/4/8 and one of the
five dead ports. A cost7 singleton would already raise LOW mass past512.
This gives15 heads H for each of181 F, or2715 complete head cases.
The selected class doubles from64 to128 and moves to the smaller physical
endpoint of H. After H the five LOW classes have costs6,6,7,7,7 and
mass512. A preparation does not change this inventory. A singleton or
unequal binary merge would strictly increase mass, and is prohibited.
Every later LOW event is an equal-cost binary merge. Each such event
retains its smaller physical endpoint and removes the larger.

To finish sorting, all two-LOW originals must have the same secondary
port1. The pool therefore falls from five classes to one by exactly
four equal-cost binary merges. The two6-classes must merge to one7-class.
The four7-classes then pair into two8-classes, which merge to one9-class.
This argument determines all event shapes and is independent of suffix
length. There are no later strict LOW events that could recreate a class.

## Moving all four LOW merges to the front

This is the ordinary arbitrary-depth bridge used by the finite tail
cover. After H, the set of live LOW secondary ports only shrinks.
An endpoint of a future binary merge is consequently live continuously
from immediately after H until that merge. Every intervening preparation
avoids all currently live LOW ports and therefore avoids both endpoints
of that future merge. The merge commutes with each such preparation,
since their physical endpoints are disjoint.

Move the first later LOW merge left across the preparations before it,
placing it immediately after H. Those crossed gates still avoid the
remaining live set. Inductively, move the second, third and fourth merge
left across intervening preparations to follow the already moved merges.
Do not cross an earlier LOW event. A port freed by an earlier merge may
occur in preparations, but cannot be an endpoint of a later LOW merge;
that later endpoint must still be live. Thus the induction covers
preparations using newly dead ports and arbitrary repeated comparisons.

All four merge events now form a contiguous word T after H. The moves
preserve the complete13-input function and the exact comparator count;
no preparation is deleted or replaced by an image on a partial domain.
After F's shortest replacement and these moves, an assumed size-at-most44
sorter therefore begins with P;F;H;T, or already contradicts a head
obstruction at P;F;H.

For each H, exhaustive recursion on the five labelled live ports allows
every pair of equal-cost classes, adds one to the surviving smaller
port's cost, and removes the larger port. It ends only at one class.
It gives exactly9 four-gate event orders and exactly3 full five-input
functions, with3 orders per function. [verify.py](verify.py) reconstructs
all of these orders independently, evaluates every word on all32 inputs
and all five outputs, and compares the full function set with the three
representatives in the producer. This finite recursion has no depth
parameter, heuristic selection or unexamined order.

Concretely let u<v be the two unselected ports in3/4/8 and r=min(H).
First compare(u,v). The remaining seven-cost ports are the sorted set
`{1,2,r,u}`. Its three perfect matchings, followed by the comparison of
their smaller endpoints, give the three representative words. An
independent pair merge may precede(u,v); the complete enumeration above
retains those orders and verifies their full-function equality. All
equalities threshold-lift to arbitrary totally ordered values.

The surviving root is physical1, the minimum of the five live candidates.
On every8192 original Boolean input at P, the minimum of ports1/2/3/4/8
already equals global rank1. This is checked directly, in addition to
held0/11/12 and the full parent image. Preparations affect only dead
ports; all their values remain at least global rank1. The singleton and
the equal-tail min gates preserve that minimum and collect it at1.
Threshold lifting gives the same statement on arbitrary ordered inputs.
Thus the complete tails correctly hold0/1/11/12. No wrong held rank is
discarded without a proof; the later exclusions do not depend on a
chosen residual nine-core image or on a selected residual depth.

## Every normalized front has a whole-original obstruction

[certificate.json](certificate.json) contains the full181-by15 head
interface and, whenever the head is not already negative, all three
tail references. Its5295 negative units are

| Stage/type | Number |
|---|---:|
| Negative heads, direct cost |1425|
| Tail direct costs |584|
| Tail tight original free cuts |1674|
| Tail tight original marked-port locks |1571|
| Tail semantic weighted masses |41|
| All negative units |5295|

The1290 head survivors have3870 tail units. Among those tails, one/two
marks suffice for2218, and four marks give the remaining1652. The new
four-mark partition is31 direct,9 free-cut,1571 marked-lock and41 semantic
mass certificates. Failure of the earlier sufficient selectors was not
treated as feasibility; their missing cases were closed by actual new
certificates. Three-mark exploratory failure has no role in the proof.

The215 distinct stored witness records use49 selected original domains:
one single-mark,14 two-mark and34 four-mark. Catalogue deduplication is
only byte deduplication of identical proposed records. Each of the5295
actual front/witness bindings is independently replayed on its own full
original cube; current tag equality never substitutes another domain.
The four obstruction kinds are as follows.

1. **DIRECT_COST.** The supplied actual original has C+S(k)>=45. The
   pruning bound rules out every size-at-most44 sorting suffix.
2. **TIGHT_MARKED_PORT_LOCK.** The supplied original has C+S(k)=44, and
   physical p currently holds a marked value. Any first later touch of
   any current mark adds a deletion, forcing45. Hence p is untouched.
   The supplied full original13-bit Boolean input has the wrong global
   sorted bit at p. The fixed suffix cannot repair it.
3. **TIGHT_FREE_CUT.** Again C+S(k)=44. Port p is unmarked, and on EVERY
   original free assignment all unmarked values below physical p are
   at most its value, while all unmarked values above p are at least it.
   No future mark may be touched, by the same first-touch argument.
   Until a first touch of p, every standard comparator avoids marks and
   p. A comparison within either side of p preserves the inequalities;
   one crossing from below to above also preserves them by min/max.
   A first touch of p is therefore identity on this entire original
   cube and adds an R charge, forcing45. Thus p is untouched and the
   supplied full wrong-rank input cannot be repaired. This is the general
   original-domain cut induction of9616, crediting
   [the minimum-lock mechanism9525](../../six-sorting-1/conditional_minimum_lock/PROOF.md).
4. **SEMANTIC_WEIGHTED_MASS.** All supplied original restrictions have
   the same(l,h), with distinct actual current mask pairs. Their
   `sum 2^C` strictly exceeds `2^(44-S(k))`. They give a lower bound on
   V, so8539 excludes every size-at-most44 suffix. Each selected history
   retains its complete original free function; the certificate does
   not claim to enumerate all11440 four-mark restrictions.

For a concrete marked-lock example, F is identity, H=(3,5), and
T=(4,8);(1,2);(3,4);(1,3). Original LOW inputs0/2/11 and HIGH input4
have current masks LOW{0,1,3}, HIGH{12}, D16/R3 and nine free inputs.
With S(9)>=25 this is tight at44. Physical3 is marked, and full Boolean
input1022 has bit1 at3 but the sorted bit is0. Any sorting suffix must
repair that bit, requiring a forbidden first touch. This example is
part of the checked complete certificate, not a surrogate for the other
5294 bindings. A full Boolean witness need not lie in the clamped domain:
the domain forbids schedule touches, and the same fixed schedule must
sort the supplied unclamped witness too.

The four kinds are established pruning/cut mechanisms. The new result
is their complete application to this literal P27/zero-prior-LOW branch,
combined with its complete equal-tail normalization. The full-function
replacement and event-commutation method also credits
[six-sorting-1's one-prior-HIGH lemma9590](../../six-sorting-1/one_prior_high_barrier/PROOF.md).
Its distinct parent and negative corpus are not transferred. The later
[two-prior heavy HIGH lemma9699](../../six-sorting-1/two_prior_heavy_barrier/PROOF.md)
is family context only, with no dependency or verdict transfer.

Every assumed sorter in the theorem has a retained preparation and one
of the15 heads. A negative head is already impossible. Otherwise all
three complete tail functions are negative, and front-loading and full
function equality place the assumed sorter at one of them. This is a
contradiction in every case and proves the conditional exclusion.

## Exact reproduction and trust boundaries

[README.md](README.md) gives portable commands. The packed producer
reconstructs all5295 original records using [recipes.json](recipes.json)
and copied ancestral [profile.py](profile.py); inputs and copied profiler
are byte-pinned before that import. The scalar checker imports neither
producer nor profile. It uses distinct numeric extremal ranks, explicitly
evaluates every Boolean assignment of every selected original cube,
checks all D/R/current masks/identity bitsets, and verifies all wrong-rank
witnesses, free-cut inequalities, marked locks and distinct semantic
classes. Both modes must agree at the complete record/binding level.

Independent here means a different same-author algorithm, not a second
person. The preparation cover has separate independent review9701; this
new tail reduction and5295 negatives are not covered by that verdict.
Ordinary pruning/standardization, threshold lifting, tail commutation
and free-cut induction remain unformalized. Published lower-bound proof
corpora and predecessor negative corpora are named imports, not silently
replayed inputs. Copied complete parent data establish source correspondence
and retained membership; their graph closure/exits are imported from9661.

The known45-comparator13-input sorter is checked on all8192 Boolean
inputs and all50176 numeric assignments across the49 selected original
domains. All marked outputs and selected semantic masses obey the size45
bound. A known9-gate five-input sorter sorts all32 inputs. Nineteen
semantic damages reject for their intended reasons in both modes,
including parent/prefix/function/interface alterations, wrong imported
bounds, D/R/identity changes, marked/free port swaps, wrong full-input
witnesses, mixed semantic families, duplicate configurations and mass.
These controls do not prove the ordinary unformalized bridges.

The complete scalar replay is divided into fixed40-function batches
(last21), whose union and exact binding hashes are checked. This is an
execution partition of the entire181-function domain, not a mathematical
depth cutoff. Each child is serial, native threads1, standard-library
CPython3.11.2, under a55-second operational guard and unchanged1CPU/2GiB.
The recorded check uses no floating-point decisions, solver UNSAT result,
timeout, memory failure or incomplete enumeration as nonexistence.
Compact certificates and recipes are supplied; raw four-mark scans,
private graph data, credentials and large lower-bound corpora are omitted.
