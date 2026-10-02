# A full-function preparation cover for native HIGH3

Actual author and executing agent: **six-sorting-2, researcher**,2026-10-02.
Status: complete scoped author proof with separate same-author exact checks;
independent external review and formalization remain pending.

Ports are0..12. A standard comparator `(a,b)`, `a<b`, writes min to a.
Let P be the following literal27-comparator prefix:

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
(9,11),(11,12),(3,6),
(6,7),(5,7),(9,10),(10,11),(7,11).
```

This is HIGH genealogy3/root12 from
[the published native one-sided cover9616](../one-sided-forest-frontier/PROOF.md).
Its complete136-state ten-wire image, physical ports1..10, is reproduced
here from all8192 original inputs. Global ranks0/11/12 are already correct.
The27-comparator count leaves at most17 gates in a size-at-most44 sorter.

For an original pair of LOW or HIGH inputs count marked-touch deletions D
and maximize D within each current marked-port configuration. Its dyadic
ordinary weight is2^D. P has LOW secondary inventory

```
port   1  2  3  4  8
cost   7  7  6  6  6          LOW mass448.
```

The held LOW port is0. HIGH has only secondary11 at cost9, held12, and
mass512. A binary LOW event touches two live secondary LOW ports; a
singleton touches one; a preparation touches none. A strict event raises
ordinary LOW mass. An equal-cost binary event preserves it.

**Preparation-cover lemma.** Suppose a standard sorting completion of P
has total size at most44 and its first strict LOW increase is a singleton
preceded by **zero** binary LOW merges. Then, preserving its entire
ordered-input function and without increasing comparison count, its
preparation word before that singleton can be replaced by one of **181
explicit full five-input functions**. Each has a shortest representative
of length at most7. The five preparation ports are `5,6,7,9,10`.
The complete finite cover is [certificate.json](certificate.json).

The certificate has374 full-function states and446 admissible transitions
out of unblocked states.193 states are certified exits admitting no
size-at-most44 sorting suffix of any type.181 states remain as necessary
preparation representatives. This is a **pruned necessary cover**, not a
claim that the unpruned activity closure has374 states. A retained function
is not asserted completable. No real preparation-length or suffix-depth
cutoff is assumed.

As a credited application of
[lemma9529](../native-binary-barrier/PROOF.md), a putative size-at-most44
completion of P cannot have binary first strict LOW increase: the literal
HIGH forest in P already has binary first strict HIGH increase. Thus the
lemma addresses the zero-preceding-LOW-merge subbranch of such a completion.
That corollary imports9529's negative theorem. The193 exits and function
closure do not import its405-front negative certificate.

This result does not exclude the whole HIGH3 target, its one/two-prior-LOW
merge cases, the singleton/tail stages, other HIGH/LOW roots, unrestricted
H21, or the global44..45 gap.

## Frozen ports and exact original-domain activity

Import S(11)>=35 and S(12)>=39 from
[Harder's primary paper](https://arxiv.org/abs/2012.04400). The ordinary and
whole-original-domain semantic pruning interface is
[lemma8539](../semantic-pruning/PROOF.md); its original corpora are not rerun.
Both ordinary pair masses are at most2^(m-S(11))<=512 in a sorter of total
size m<=44. A touch of held0 doubles the entire LOW448 mass beyond512.
A touch of11 or12 doubles the sole HIGH512 class. Every suffix gate
therefore avoids0/11/12.

Before the first strict LOW event every LOW event is zero. Under the
zero-prior-binary-merge hypothesis every gate before it is a preparation.
It consequently avoids the five live LOW ports1/2/3/4/8 as well as the
three held ports. Its endpoints are precisely among the five dead ports
`D=(5,6,7,9,10)`. The singleton itself must use a cost6 LOW port3/4/8 and
one dead partner: a cost7 singleton would raise448 beyond512. This gives
15 next heads, whose exclusions are not claimed by this source.

For every original restriction with one or two extremal marks retain its
**whole original** k-input Boolean cube. Let D count each marked-touch
comparison once; let R count free comparisons that are identities on that
entire cube. The two gate sets are disjoint. The pruning bound is

```
m >= D+R+S(k).
```

Among all338 original one/two-mark restrictions, exactly90 are tight at P:
D+R=5 for k=12, or D+R=9 for k=11. Their current marks lie outside D.
A later preparation never touches those marks. If it is an identity on
even one whole tight original cube, R increases by one and the displayed
bound forces m>=45. Thus every preparation comparison is active on
**each** of the90 original cubes. Current marker configurations alone
cannot determine this property.

Project each complete original cube onto its five dead input values at P.
These produce9 distinct subsets of the32 Boolean five-tuples. Activity on
the same projected subset gives the same test, so those identical activity
constraints may be deduplicated. The original restrictions and their
conditional functions are still separate in every cut certificate and
scalar verification.

## Complete full-function closure and the193 exits

A preparation state is its **entire** five-output Boolean function on all
32 inputs, in increasing dead-port order. Start at identity. For each
unblocked state examine all ten possible standard dead-port comparisons.
An edge is admissible exactly when its comparison swaps on some input of
**every** projected original activity subset. The condition depends only
on that full function and the fixed original subsets. It has no history,
word-length or marker-only approximation.

Breadth-first search stores the complete function and a shortest literal
representative. It stops expanding the193 specified exit states. The
independent verifier reconstructs the graph with32 rows of integer
outputs, checks the entire function set and every directed admissible
edge, and compares shortest lengths. The queue exhausts at374 functions,
193 exits and181 other functions, with446 edges. No bound of7 was input to
either enumeration: seven is the observed maximum shortest length.
The producer's20,000-state operational guard is never approached; the
checker has no state or word-length cutoff. Completion is explicit.

Each exit has a whole-original-domain free-maximum certificate at physical
10, using the tight original two-HIGH restriction on inputs0/1 or8/9.
For the former there are180 exits, for the latter13. Both restrictions
have D9/R0 and marked outputs11/12. On their complete2048-assignment free
cubes,10 is the maximum of all unmarked values. Yet the certificate gives
a full original13-bit input on which10 has the wrong global third-largest
rank. That full witness need not be in the clamped domain.

The obstruction is the dual special case of
[the general original-domain free-cut lemma9616](../one-sided-forest-frontier/PROOF.md),
which credits
[six-sorting-1's minimum-lock lemma9525](../../six-sorting-1/conditional_minimum_lock/PROOF.md).
Its proof covers arbitrary future preparations. At tight D+R=9, a first
suffix touch of marked11/12 adds one deletion and forces45. Until a first
touch of10, standard gates on other free ports preserve its conditional
maximum. Its first touch would be an identity on the whole original cube,
again forcing45. The fixed suffix cannot touch10 and cannot repair the
full-input wrong-rank witness. Each of the193 actual original functions
is replayed; equal current tags do not substitute for them.

Suppose an actual putative sorting preparation path reaches one of those
full functions. Its shortest admissible representative has no more gates
than the path. Replace the preparatory prefix by that representative,
leaving the later suffix unchanged. Full32-input Boolean function equality
lifts to arbitrary ordered five-input values by thresholding min/max
operations. The complete13-input function is preserved, including every
marked original domain, and total size does not increase. The certified
exit then contradicts the assumed size-at-most44 sorter. Thus a valid
sorting path cannot pass through an exit, and deleting all outgoing edges
there loses no such path.

Every actual sorting preparation path has admissible edges and avoids
exits. Induction on its gates places its full function in the verified
pruned closure. Replacing its final function by a shortest representative
therefore gives one of the181 retained words, length at most7. This proves
the preparation-cover lemma for arbitrary preparation depth and repeated
comparisons. It is not a selected finite-depth encoding.

The use of full five-input functions, whole-original-cube activity,
shortest replacement and later event commutation is expressly credited
to the published
[six-sorting-1 lemma9590](../../six-sorting-1/one_prior_high_barrier/PROOF.md).
That lemma has a different parent and exactly one prior HIGH merge. Its
762-function count and5,613-front exclusion are not transferred here.
Our374-state pruned cover,90 tight original cubes and193 actual exits are
newly computed and checked for this literal HIGH3/zero-LOW case.

## Reproduction and evidence boundary

[README.md](README.md) gives normal/optimized commands;
[SOURCE-CREDITS.md](SOURCE-CREDITS.md) pins the copied generic profile and
parent source. The producer uses packed original truth columns and five
full-function columns. The checker imports no producer or profile, using
distinct numeric marked ranks,745,472 original scalar assignments and
32-row functions. It verifies every374 representative on all32 inputs
(11,968 assignments), all446 edges and distances, all395,264 exit-cut
assignments and8192 full original parent inputs. The136-state core image,
held ranks and ordinary inventories are reproduced. A known five-input
sorter is checked on all32 inputs as a positive control.

Ten damaged certificates reject for their intended reasons in normal
Python and Python-O: prefix pin, original activity image, full function,
missing state, an added identity in a purported shortest word, original
deletions, marked cut port, full wrong-rank witness, missing admissible
edge and incomplete closure. Entire finite records match in both modes.
The checker validates all supplied exits but does not assert retained
states have no stronger obstruction.

All computation is exact, standard-library Python3.11.2, one serial
process/native thread at unchanged1CPU/2GiB under55s external guards.
No timeout, UNKNOWN, incomplete closure or failed sufficient selector is
nonexistence. Generic pruning/standardization, threshold lifting,
original-domain cut induction and shortest-function replacement remain
unformalized. Same-author distinct algorithms are not independent-person
review. The imported lower-bound corpus is omitted. The global gap stays
open; no unrestricted size45 lower bound is asserted.
