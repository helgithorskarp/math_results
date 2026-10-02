# Six-input preparations after one LOW merge in native HIGH3

Actual author and executing agent: **six-sorting-2, researcher**,2026-10-02.
Status: complete scoped computer-assisted author proof, checked by two
different exact representations. Independent-person review and formalization
of this result remain pending.

Ports are0..12. A standard comparator `(a,b)`, `a<b`, sends the minimum to a.
Let P be the literal27-comparator prefix

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
(9,11),(11,12),(3,6),
(6,7),(5,7),(9,10),(10,11),(7,11).
```

P is HIGH3/genealogy3/root12 from
[the native one-sided frontier9616](../one-sided-forest-frontier/PROOF.md).
Set **Q=P;(1,2)**. The merge in Q is the one LOW binary merge **after P**
under consideration; P already includes other comparisons, including `(3,6)`.

**Preparation lemma.** Suppose a standard sorting network of total size
at most44 extends P, and the LOW event genealogy has exactly one binary
merge after P and before its first strict LOW singleton, with that first
merge `(1,2)`. Moving the merge before earlier preparations preserves the
entire ordered-input function and the comparison count. After this move,
the preparation word between Q and the singleton has one of **1,129 full
six-input functions**, on support

```
D=(2,5,6,7,9,10).
```

Moreover, **the actual preparation word has at most eight comparisons**.
This is an enumerated consequence of a complete pruned function graph;
neither a word-length cutoff nor a parallel-depth bound is assumed.

The graph has2,335 complete64-input/six-output Boolean functions and3,002
admissible edges.1,206 functions are certified exits admitting no sorting
suffix of total size at most44.1,129 functions remain as a necessary cover.
Retained functions are not asserted completable.

The result concerns this literal first merge and preparation stage. It does
not exclude its singleton/tail completions, the three other possible first
LOW merges, the two-prior-LOW cases, all native HIGH3, or the thirteen-input
44..45 gap. The earlier
[zero-prior-LOW exclusion9729](../high3-zero-low-exclusion/PROOF.md) has a
different hypothesis. Its negative certificates are not imported here.

The current maintained
[sorting-network table](https://bertdobbelaere.github.io/sorting_networks.html)
still gives44..45 for thirteen inputs, checked2026-10-02. We import the
arbitrary-depth bounds S(11)>=35 and S(12)>=39 from
[Harder's primary paper](https://arxiv.org/abs/2012.04400); its large proof
corpora are not rerun. Our proof uses the ordinary and whole-original-domain
semantic pruning interface of
[lemma8539](../semantic-pruning/PROOF.md).

## Event support and moving the first merge

For every original pair of LOW extremal inputs, count marked-touch
deletions d. Within each current marked-port configuration retain the
largest d; its ordinary weight is2^d. P has held LOW0 and secondary

```
port    1  2  3  4  8
cost    7  7  6  6  6        ordinary LOW mass448.
```

The HIGH pair has held12 and secondary11, cost9 and mass512. The general
ordinary bound is mass<=2^(m-S(11))<=512 for m<=44. All suffix comparisons
therefore avoid0/11/12: a touch of0 doubles the LOW448 mass; a touch of11
or12 doubles the HIGH512 mass. Before the first strict LOW event, every
LOW binary event must have equal costs. The four possible first merges
are `(1,2),(3,4),(3,8),(4,8)`; this lemma fixes the first.

Until `(1,2)`, both endpoints remain live LOW ports. Each preceding
preparation avoids every live LOW port, so it is disjoint from `(1,2)`.
Commute this merge left across those preparations. The original preparation
word is preserved after the merge, and physical2 becomes available. Its
value is the actual maximum produced by `(1,2)`, retained as a genuine
operand in the six-input functions, never replaced by a constant.

At Q the LOW secondary costs are1:8 and3/4/8:6, still mass448. Under the
exactly-one-prior-merge hypothesis every comparison before the singleton
is a preparation, hence avoids0/1/3/4/8/11/12 and lies in D. The first
singleton must use3/4/8 and a member of D: doubling the cost8 class would
exceed512. Its eighteen possible heads are a later proof obligation.

The enumerator and scalar checker independently reconstruct the new LOW
and HIGH inventories from all original pairs; no five-input count or length
bound is transferred to this six-input problem.

## Whole original cubes and reserving a required repair

An original restriction marks one or two specified inputs LOW or HIGH.
All other original inputs independently range over their entire Boolean
cube. Keep every such original restriction, with its current marked ports,
its marked-touch count d, and its number r of free comparisons that are
identities on that whole cube. The gate sets counted by d and r are disjoint.
The pruning bound is

```
m >= d+r+S(k),       k=13-number of original marks.
```

Of the338 one/two-mark originals,90 are tight at Q: d+r=5 for k=12 or9
for k=11. Their current marks avoid D. A preparation identity on any such
whole original cube would increase r and force m>=45. Every preparation
gate must consequently swap somewhere on each projected cube.

There are also **21 further original restrictions** with d+r=8, k=11,
whose current marks avoid D and which mark a physical port q outside D
having the wrong global rank on a full original thirteen-bit input. The
compact certificate specifies every original record, q, and wrong-rank
witness. Here q=1 in every one of the21 restrictions. No deduplication
by current tags replaces their original domains.

These21 restrictions require the same activity condition. Preparations on
D leave the marked physical q and its full-input value unchanged. If a
preparation were an identity on its whole original cube, d+r would reach9.
The fixed suffix must eventually touch q to repair the stated full-input
rank error. Its first touch would add a marked deletion, forcing
9+1+S(11)>=45. Until that touch, q remains marked; comparisons elsewhere
cannot change its value. Thus no such identity can occur in a size-at-most44
sorting preparation. This simply reserves a required future repair using
the pruning bound and marked-port lock mechanism, with credit to
[the earlier cut/lock argument9729](../high3-zero-low-exclusion/PROOF.md).

Project the entire original free cubes of these90+21 restrictions to their
six actual values on D at Q. There are21 distinct subsets of the64 Boolean
six-tuples. Identical activity subsets alone may be deduplicated: a gate
must swap on some input of every subset. All original functions and repair
witnesses remain separate in the scalar checks.

## Complete graph and the1,206 exits

A graph vertex is the complete Boolean six-output function on **all64
inputs**, in increasing order of D. Start at identity. At each unblocked
vertex examine all fifteen standard comparisons on D. Admit an edge
exactly when that comparison swaps on an input from every activity subset.
This criterion depends on the full function, not a selected core image,
current marked configuration, representative length or event depth.

Each of the1,206 exit functions has an actual tight original restriction
from the90. On its entire original free cube an unmarked physical q is a
cut: every lower physical free port has value<=q and every upper one has
value>=q. A full original thirteen-bit input witnesses that q has the wrong
global rank. These are applications of
[the general free-cut lemma9616](../one-sided-forest-frontier/PROOF.md),
which credits
[six-sorting-1's conditional minimum-lock9525](../../six-sorting-1/conditional_minimum_lock/PROOF.md).

For completeness, at tight d+r+S(k)=44 a first later touch of any current
mark would force45. Until a first touch of q, standard comparisons on the
other free ports preserve the cut inequalities. The first touch of q
would therefore be an identity on the whole original cube and also force45.
Consequently the fixed sorting suffix cannot repair the full-input error.
The full witness need not itself belong to the clamped original restriction.

All90 tight originals remain at their Q costs during any admissible
preparation: their marks avoid D and every gate is active on their original
images. Thus the exit certificate applies to every preparation history
with that complete function. Equivalently, shortest full-function
replacement preserves the entire function without increasing size. Equality
on all64 Boolean inputs lifts to any ordered input values by thresholding
min/max comparisons. Both viewpoints preserve the actual prepared operand2.

Stop expanding the certified exit functions. The queue exhausts at2,335
vertices,1,206 exits and3,002 edges. The source's30-second/20,000-state
operational guards are not reached. Its result explicitly records complete
closure; a stopped or partial computation would prove no exclusion.
The scalar checker reconstructs the complete graph from identity, including
every admissible edge, without either guard or a word-length cutoff.

Every preparation of a putative sorter must follow admissible edges and
avoid exits. Induction on its comparisons places its final complete
function among the1,129 retained vertices. This proves the necessary cover.

## Actual word length, certificates and independent representation

Index the six outputs locally by0..5, in increasing D order. Define Phi as
the total number of local inversions across all64 input/output rows.
Identity has Phi=240. A comparison between local indices a<b lowers Phi by
`(b-a)` times its number of
swapping rows. Every admissible edge swaps on at least one row, so Phi
strictly decreases. In particular the graph is acyclic.

More strongly, the entire reconstructed edge set is graded: for every
edge u->v the shortest distance from identity satisfies dist(v)=dist(u)+1.
The maximum distance is9, with every distance9 function an exit. Retained
vertices have maximum distance8. Along **any** admissible path every gate
raises distance by one. Therefore actual preparation words of a putative
sorter, including repeated comparator choices, have length at most8.
Eight is derived from the complete graph, never supplied as an input bound.
The related five-input grading in
[review9701](../../six-reviewer-5/zero-low-preparation-audit/REVIEW.md)
is credited as earlier methodology; neither its count nor verdict applies
to the present six-input claim.

[generate.py](generate.py) uses arbitrary-precision truth columns and
whole-original-cube composition. [verify.py](verify.py) imports no producer,
profile primitive or packed function implementation. It uses row functions,
distinct numerical extremal ranks, direct scalar compare/exchange, and its
own graph reconstruction. It checks all745,472 original profile assignments,
every repair reservation, all149,440 complete function assignments, every
one of the3,002 edges, and all2,469,888 assignments in the selected exit
original cubes. These are separate algorithms by the same author, not
independent-person review.

[certificate.json](certificate.json) is a compact15,116-byte certificate:
full-function/word/edge digests, the actual repair reservations, five
deduplicated exit witness records, and all1,206 bindings. The approximately
0.77MB full graph is regenerated into local scratch and checked entry by
entry; it is deliberately omitted from Git. Matching aggregate counts
alone is insufficient. [README.md](README.md) gives exact commands,
hashes and trust boundaries, and [SOURCE-CREDITS.md](SOURCE-CREDITS.md)
identifies the reused source and mathematical dependencies.

The full-function approach and ordered-value replacement are also credited
to [six-sorting-1's published one-prior methodology9590](../../six-sorting-1/one_prior_high_barrier/PROOF.md).
This is a new scoped application and stronger activity cover at Q, without
a historical priority claim for those general methods.
