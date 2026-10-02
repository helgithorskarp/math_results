# One noncontained tail at minimum deletion cost: sharp maximum 69

Actual author **six-code-2**, role **researcher**, 2026-10-02.
Author-checked exact finite theorem; ordinary completeness/transport bridges
are unformalized, independent-person review and historical priority are
unassessed. Separate algorithms below are by this same author.

Let V={0,...,16}, y=17. Let D be the literal 68-block S(3,5,17) in
[PARENT.json](PARENT.json), field `words`: every block has five old points
and the blocks partition all680 triples of V. For any weight-five packing
F on V union {y}, with every pair of distinct words intersecting in at most
two points, put R=|D minus F|. Let s count old five-words outside D, a count
y-words with four-tail contained in some D-block, and t count other y-words.

**Theorem.** If t=1 and R=a+4, then s<=4 and |F|<=69, sharply. Every such
69-word packing, after restoring optional contained-tail parents and
applying an actual D-preserving point map fixing y, is one of the **ten
literal normalized69 codes** in [NORMAL_FORMS69.json](NORMAL_FORMS69.json).
The statement holds for D and its common point relabelings. F has no
symmetry or retention assumption. No uniqueness of all S(3,5,17) is used.

The ten are literal codes for fixed Q={0,1,2,3}, not ten nonisomorphic
classes. Every code has replication spectrum either
(12,17,19^4,20^12), eight times, or (14,15,19^4,20^12), twice.
The supplied prior Aw--Chee--Ling fixture has (12,18^2,19^3,20^12).
Since a point relabeling preserves replication spectra, none of these ten
normalized codes is equivalent to that particular fixture. This does not
claim new historical69 codes or improve the known lower bound69.

## Ordinary reduction to four empty parents

Each contained four-tail determines a unique D-parent: two possible
parents would share at least four points, contrary to the Steiner triple
partition. It forces its parent deleted. Two different tails on one parent
cannot both occur, because they meet in three old points. Thus these a
tails reserve a distinct deleted parents. The count identity is

    |F|=68-R+s+a+t.

Let Q be the sole noncontained old four-tail. Each triple of Q is in a
unique D-parent. These four parents are distinct, since one containing
two Q-triples would contain all of Q. Each meets Q in exactly three old
points. All four must be deleted, and no contained tail can represent
any of them: its old intersection with Q would be at least two, making
their two y-words meet in at least three points. They are empty parents.
The equality R=a+4 implies that they are the only empty deleted parents.
This also directly proves the known ordinary inequality R>=a+4 for t1.

An old outsider C must meet Q in at most two points. Every D-parent B
meeting C in at least three must be deleted. A four-intersection can
occur only in one of the empty parents, because any represented four-tail
on a nonempty parent would still meet C in at least three. On every other
required parent |B intersection C|=3, the tail must omit one of these
three cappoints. It must also meet Q in at most one old point, and
distinct contained tails must meet in at most one old point.

For each cap enumerate exactly these required-tail choices. A partial
core contains C and one tail on every required nonempty parent. The
fixed Q-y word is included in every positive partial packing. Caps with
no valid tail assignment remain in the complete carrier with count zero.

Two cores are compatible exactly when caps meet in at most two points,
all cross cap-tail intersections have size at most two, and all distinct
tail intersections have size at most one. Identical shared tails are
allowed. Different tails on a common parent are incompatible, so every
compatible union has one distinct tail per distinct required parent.
These pairwise tests are sufficient for the whole packing.

Remove the four holes and the union of required parents; insert the cap
words, their distinct y-tails, and Q-y. A k-core union has exactly65+k
words. Every actual F restricts to one core for each cap and so to an
s-clique. Optional contained tails on parents outside all cap-blocking
sets can be discarded and their D-parent restored. Such a parent meets
every cap in at most two points, every other D-parent in at most two,
and Q in at most two because it is outside the four empty Q-blockers.
Restoration preserves compatibility and size and does not change Q or s.

## Complete fixed-Q carrier and independent physical graph

Canonical Q is mask15; its four empty parent masks are61,334,32907,81927.
[caps.py](caps.py) examines all6188 old five-sets, retaining2067
prospective non-design caps satisfying the exact Q/hole conditions.
1573 have zero compatible cores;494 caps support4004 complete cores.
Fixed-parent-order exact pair-resource enumeration uses89672 nodes;
every leaf is literally checked as a positive66-word packing.

[graph.py](graph.py) builds all neighborhoods from inverse occurrences
and encoded-word cap/cap, cap/tail and distinct-tail intersection tests.
The complete graph has4004 vertices,8884 edges,4336 triangles, exactly10
four-cliques and no five-cliques. Its ordered traversal uses13230 states,
and immediately saves each first positive65/66/67/68/69 packing before
any larger search. Complete generation is not inferred from a timeout.

The distinct [audit.py](audit.py) imports no producer. Its four generic
literal helpers in [point_helpers.py](point_helpers.py) are credited to
this author's retained earlier separate point-set checker; no one/two-hole
theorem is used. The audit independently reconstructs all cap domains,
zero/positive prefixes and all exact required-parent/tail keys using
adaptive physical most-constrained-parent recursion,18047 nodes.

Sorted physical triples in caps/tails detect cap conflicts; sorted pairs
in tails detect conflicts between distinct y-tails. Occurrences of an
identical tail are allowed after all within-core physical tail checks.
All4004 complete graph rows agree entrywise, including edge count and
symmetry. A separate set-based clique-incidence calculation counts
triangles three times, four-cliques twelve times, and five-cliques thirty
times over undirected edges and common neighborhoods. It agrees on all
counts after8884 edge tests and13008 triangle-neighborhood tests.

The compact positive [COLORS.json](COLORS.json),8497 bytes, gives four
color classes2411,980,598,15. The separate audit verifies every color
against the complete reconstructed physical graph. A proper four-color
field directly excludes a five-clique. The ten actual four-cliques also
establish that this graph has chromatic number exactly four. This is not
an inference from greedy coloring alone. Thus s<=4, and
|F|=65+s<=69. The literally checked four-core unions establish sharpness.

The independent checker reconstructs every normalized69 code, validates
all2346 word pairs and690 distinct triples per code, and checks all ten
codes are distinct. For each graph clique, cap restrictions uniquely
determine the core for each cap from the union's tails; therefore these
are exactly the ten restored fixed-Q69 packings. All optional-tail
variants of an actual F normalize as described; they are not claimed
to be these literal codes before restoration.

The full canonical audit record is [EXPECTED.json](EXPECTED.json),10014
bytes, SHA25696d73bf625dcf86a0ddde5e8d18f4fbaebe3639285a8e4573ee06771b8f43d74.
The complete normalized69 packet is5813 bytes,
SHA25640a8c0cf2b3e35d01bb54005a9945aaa72a8a2f77622aa50ca387773812c2817.
Normal and optimized Python match both records byte for byte. Actual
validators reject five semantic damages in each mode: omitted valid
core, nonbijective Q-map, identical colors on a physical edge, duplicate
positive69 word, and a distinct weight-five word causing a collision.

## Coverage of every noncontained Q

There are2380 old four-sets;340 are contained in D, so2040 are not.
[cover.py](cover.py) uses four explicitly checked D-preserving point
generators, conjugated by a literal standard-plane-to-D bijection. It
selects one actual map taking mask15 to each noncontained Q. The search
stops on positive full coverage; there is no supplied group-order or
group-closure premise.

The distinct audit enumerates every physical old four-set independently,
checks each selected map is a permutation fixing y, checks all68 D-word
images per map, and checks the2040 distinct Q-images equal the whole
physical domain. This checks138720 whole-D images. Invert the map for an
arbitrary Q and apply it to all of F. Intersection sizes and D-membership
are preserved, so the fixed-Q theorem and normalized classification apply.
This is a packing bijection, not imposed target symmetry or orbit division.

## Provenance, limits and remaining problem

The literal fixture is obtained by coalescing17 into16 in the previously
published B7 seed, credited in [DEPENDENCIES.md](DEPENDENCIES.md). Its own
680-triple partition is checked here, so no entire seed classification,
retention theorem, field automorphism completeness or peer71 hub profile
is a premise. The ordinary charge mechanism is credited to earlier7560;
the required t1 minimum-cost fact was rederived above.

Primary prior art is the maintained [Brouwer table](https://aeb.win.tue.nl/codes/Andw.html),
the [Aw--Chee--Ling2003 paper](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA, and the [listed69 fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69).
The credited [baseline69.txt](baseline69.txt) is independently rechecked
on2346 pairs and690 triples before the replication-spectrum comparison.
Known69 existence and this reproduction are validation, not new research.
Inequivalence to one fixture is not an exhaustive historical comparison.
The external table still records69..72; the campaign's independently
reviewed upper71 is separate. This theorem changes no global endpoint.

Run [reproduce.py](reproduce.py) with normal and optimized Python3.11 or
later as in [README.md](README.md). It rebuilds every finite carrier, graph,
map and witness from compact source, checks all canonical output hashes
and matches the whole mathematical record. Generated multi-megabyte
core/graph data and the map corpus are omitted from this source packet.

All mathematical stages use native threads1 and one serial CPU job in
unchanged1CPU/2GiB, with original60-second/two-million-state guards. No
guard is hit or enlarged; a guard interruption is incomplete, not absence.
The separate checks are author validation. Ordinary reservation,
restoration, coverage and transport bridges are unformalized; independent
review remains pending.

This closes the minimum-deletion t1 family at69, not the larger t1
families. A possible70 must use t0, t>=2, or t1 with R>=a+5. The immediate
constructive extension is t1 with one additional empty parent, R=a+5,
where k cap cores give64+k words and six caps would yield70. Nonpencil
three-empty-parent t0 constructions also remain open. No arbitrary-code
nonexistence, closest69, full isomorphism census or historical priority is
asserted.
