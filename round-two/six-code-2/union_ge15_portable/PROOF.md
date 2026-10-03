# Four empty Steiner parents covering at least fifteen points

Actual author **six-code-2**, role **researcher**, 2026-10-03.
This is an author-checked finite theorem with exact computational certificates
and ordinary completeness arguments. All algorithms are by the same author.
The ordinary arguments are unformalized; independent-person review and
historical priority remain pending.

## Precise theorem

Let X={0,...,16}, y=17, and let D be the literal 68-block design in
[PARENT.json](PARENT.json), field `words`. Bits represent points. Its exact
input SHA256 is
`32e66195e3252e2a50a2d6c55ed7d9af9a8693e7f7121276aeca1474f80c3758`.
The blocks partition all 680 triples of X. The whole literal partition is
reconstructed by the physical audits; no uniqueness theorem for S(3,5,17)
is assumed.

Let F be any family of distinct five-subsets of X union {y}, with every pair
intersecting in at most two points. Write R=|D minus F|, s for the number of
old-point words outside D, a for the number of y-words whose four-point
tails are contained in a D-block, and t for the number of other y-words.
A contained tail has a unique parent: two possible parents would share
four points, contradicting the triple partition. Its parent is deleted,
and two different tails on one parent cannot occur together. Hence the a
contained tails represent a distinct deleted parents. Put h=R-a and let H
be the set of unrepresented deleted parents.

**Theorem.** Suppose t=0 and h=4. If the union of the four parents H has
15 or 16 points, then s<=4 and |F|<=68, sharply for every such H. If its
union has 17 points, then s<=3 and |F|<=67, sharply for every such H.
There are respectively 65,280, 6,120 and 765 actual quartets H.

**Corollary.** In this specified D,y,t=0,h=4 model, any packing with at
least 69 words must have |union H|<=14.

The count identity is |F|=68-R+s+a+t=68+s+t-h=64+s here. Caps and optional
contained tails are arbitrary. There is no symmetry requirement on F,
degree profile, prescribed noncontained tail, or retention premise. The
theorem also holds after a common relabeling of D,y,F. It does not bound
an arbitrary code through a different design, other t/h values, or the
unrestricted endpoint A(18,6,5). It does not assert that union<=14 is
sufficient to attain 69.

## Complete carrier and physical compatibility

For an actual old-point cap C outside D, any B in D outside H meeting C
in at least three points must be represented by a tail. Such B cannot
remain in F and cannot be an unrepresented deletion. If |C intersect B|
were at least four, every four-subset of B would meet C in at least
three, impossible. Thus prospective caps are exactly the five-subsets
outside D whose four-or-more intersections are confined to H. Each of
the 13 specified cases has 2,280 such candidates; this cardinality is
checked after enumerating all 6,188 old five-subsets.

For every candidate, a core assigns one contained four-tail on each
required parent B outside H with |C intersect B|=3. The tail must omit
one of those three shared points. Its intersections with C have size
two; distinct assigned tails must meet in at most one old point. All
valid assignments, including zero-core candidate prefixes if present,
are included. An actual F restricts to one such core for each cap.
Extra optional tails can only impose additional restrictions.

[caps.py](caps.py) uses a fixed parent order and exact pair-resource masks,
with a literal positive 65-word packing check at every completed core.
[audit_ordered.py](audit_ordered.py) imports no producer: its credited
pure helper [physical_helpers.py](physical_helpers.py) reconstructs the
entire assignment-key set in an adaptive minimum-domain parent order
using literal point sets. It checks every core key, every candidate
prefix and the full cardinality. The two enumeration algorithms agree.

Graph vertices are cores. Distinct cap words must meet in at most two
points; every cross cap-tail intersection must have at most two old
points; distinct tails must meet in at most one old point. Identical
shared tails are a single y-word and are permitted. Different tails on
the same parent conflict, as do distinct cores on the same cap. These
pairwise conditions exactly express physical compatibility.

[graph.py](graph.py) forms the graph using encoded word comparisons and
an inverse occurrence dictionary. The physical audit independently
reconstructs every row from literal cap triples, tail triples and tail
pairs, and compares every whole supplied row entrywise. It checks vertex
domain, self edges, symmetry and the exact edge count. Its graph source
is thus the complete physical graph, not an unverified producer count.

An actual packing with k caps gives a k-clique of the corresponding
restricted cores. Consequently no K5 implies s<=4, and no K4 implies
s<=3. Conversely, glue a compatible selection by inserting its caps
and unique y-tails, deleting H and their represented parents, and
retaining every other D-block. Different tails on one parent would
conflict, so the represented parents are in bijection with the inserted
tails. Retained parents cannot conflict with a cap, since every such
parent was required, nor with tails on different D-parents, since the
D-blocks share at most two points. This gives exactly 64+k words.
For attainment the actual generated packets of every size 64 through
the claimed maximum are additionally checked as literal packings:
domain, distinctness, all pairs, all triples, t=0, R=a+4, and exact H.
The maximum witnesses are included compactly in
[POSITIVE_WITNESSES.json](POSITIVE_WITNESSES.json).

## Ordered finite-graph certificate

For a finite simple ordered graph and any edge i<j set
C(i,j)=N(i) intersect N(j) intersect {v:v>j}. Visit every edge ell<m
in C(i,j), and check the entire third domain
C(i,j) intersect N(ell) intersect N(m) intersect {v:v>m}.
A member r is an actual K5 on i,j,ell,m,r. Conversely every K5, written
in increasing order, appears in exactly this test. Each K4 is one
inner-edge test with its two smallest vertices as the outer edge; each
triangle is counted once in the sum of |C(i,j)|. These are general
ordinary graph arguments, not an inference from finite test graphs.

The physical audit tests all these ordered neighborhoods and obtains
zero K5 in every case, and zero K4 in the two union-17 cases. It matches
all complete triangle/K4/K5/K6 counts against the producer's separate
increasing-clique traversal. The auditor's proof-state sum is MRV nodes
plus physical rows plus actual outer edges plus actual ordered inner
edges, with the original two-million guard.

The ordered kernel is also checked by
[check_ordered_finite.py](check_ordered_finite.py) against a separate
literal subset-edge-mask oracle on all 32,768 labelled six-vertex
graphs. Every triangle/K4/K5 count and all 172 positive five-clique
witnesses agree. Totals are 81,920 triangles, 7,680 K4, 192 K5 and one
K6; the entire two count streams have identical SHA256
`248c43e0fb93fcc4d4fe1230c1436cf7eae6b57aca113e3ea7bebb0d6ba2d6f4`.
Eight actual semantic damages include K5/K6 refutations of absence,
asymmetric/self/out-of-domain edges, suppressed positive counts, a
positive witness containing a nonedge, and omitted labelled coverage.
This finite check validates the algorithm; the ordinary ordered-graph
argument separately supplies the general completeness bridge.

An earlier unordered case-76 audit actually stopped at its unchanged
two-million-state guard: 337,302 K4 require 2,023,812 inner incidences
under that older six-incidence method, before other costs. That stopped
run supplied no absence. Its source and failure receipt remain intact
privately. The new ordered kernel was first validated on the whole
six-vertex domain and on the already certified case 83, before changed
case 76. No time, state, memory or process limits were increased. The
present portable replay uses the ordered certificate for all 13 cases.
No priority is claimed for the generic ordered-graph algorithm.

## Literal representatives and exhaustive physical coverage

The component numbers below are retained coordinate labels, not a
claim of a minimal inequivalent-orbit classification. All K5 and K6
counts are zero; the listed positive maximum is attained.

| Label | Literal parent masks H | Union | Actual targets | Cores | Edges | Triangles | K4 | Ordered audit states | Maximum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | 61,334,1190,92672 | 15 | 8160 | 29100 | 272039 | 489632 | 144807 | 544904 | 68 |
| 59 | 61,334,2721,115728 | 15 | 4080 | 29500 | 284199 | 429602 | 56112 | 469425 | 68 |
| 72 | 61,334,4808,92672 | 15 | 16320 | 29606 | 283136 | 621315 | 233740 | 646344 | 68 |
| 75 | 61,334,10380,53761 | 15 | 4080 | 29272 | 267986 | 529000 | 161404 | 557703 | 68 |
| 76 | 61,334,13072,23680 | 15 | 4080 | 30142 | 298910 | 732136 | 337302 | 767446 | 68 |
| 81 | 61,334,13072,100736 | 15 | 8160 | 30254 | 300539 | 725380 | 367788 | 799852 | 68 |
| 82 | 61,334,23680,42624 | 16 | 2040 | 29388 | 276388 | 502432 | 114028 | 519109 | 68 |
| 83 | 61,334,23680,47168 | 15 | 8160 | 29500 | 278073 | 547668 | 194114 | 601274 | 68 |
| 84 | 61,334,23680,98882 | 16 | 4080 | 29388 | 283098 | 412974 | 50376 | 462308 | 68 |
| 85 | 61,334,23680,100736 | 15 | 4080 | 29500 | 278023 | 547836 | 171528 | 578674 | 68 |
| 89 | 61,334,47168,71200 | 15 | 8160 | 30150 | 297314 | 736092 | 383258 | 811640 | 68 |
| 90 | 61,2258,13072,115728 | 17 | 85 | 30912 | 318960 | 804432 | 0 | 452776 | 67 |
| 91 | 61,2258,38146,92672 | 17 | 680 | 30576 | 313437 | 702150 | 0 | 446032 | 67 |

[SPEC.json](SPEC.json) contains the 13 literal representatives and four
actual point permutations. [cover.py](cover.py) regenerates their subgroup
by permutation composition from the identity. It records 16,320 distinct
actual maps, validates every whole D image and y, and produces the
representatives' positive images. It assumes neither that this is the
full automorphism group nor a uniqueness theorem for D.

[audit_cover.py](audit_cover.py) imports no producer and independently
examines all 814,385 quartets of D using literal point-set unions. It
selects exactly 72,165 with union at least 15. It validates all 16,320
actual supplied point bijections against all 68 D-blocks: 1,109,760
D-word images. Every one of 288,660 four-parent images is checked;
each target occurs once, and the whole union of the 13 image packets
equals the entire freshly reconstructed domain. State units are the
unchanged point-audit units: one per examined quartet, actual map and
covered target, totaling 902,870. Five meaningful damages reject
nonbijective maps, whole-D failures, wrong target images, duplicated
targets and omitted valid domain targets.

Any certified point map fixes y and sends D to itself. Its inverse
transports any target packing to the representative and preserves all
intersections and t,h,s,H. Its forward direction transports the literal
maximum witness to the target. Thus every physical target inherits
both its certified upper bound and attainment. Positive map coverage
alone never supplies a packing bound: all 13 cap certificates are also
required. The cases cover 71,400 sharp-68 and 765 sharp-67 quartets.

## Source-only reproduction and trust boundaries

The public bundle needs only Python's standard library. Each cold run
starts from the small literal design, credited known-69 fixture, the
four generators and the 13 representative coordinates. No private
graph, core corpus, full 92-component atlas or point-map packet is an
input. All large generated packets are regenerated in a chosen scratch
directory and omitted from publication.

[replay.py](replay.py) freezes every source and fixture before a run,
launches one ordinary child at a time with native threads one and the
original 60-second/two-million-state mathematical guards plus 60-second
child-process guard, and preserves completed-stage journals. Normal
and optimized modes use separate fresh source copies and independent
generated directories. No assertion is required for a mathematical
check. Every core/graph/witness/cover packet is compared by whole-byte
size and SHA256; all fields of every mathematical record, including
traces, counts, zero prefixes and domains, are retained.

Only measured execution time and RSS are omitted from producer-summary
comparisons. A physical result's raw producer-summary pin is first
verified against that mode's actual whole raw summary, and only then
removed for mode comparison. Every other field is compared. Prior
unordered traces/method/state multiplicities are explicitly distinguished
from the new ordered ones; all invariant physical fields and complete
packets must reproduce. New ordered traces are retained whole and
compared between normal and optimized runs. Published compact expectations
and whole-result hashes are in [EXPECTED.json](EXPECTED.json).

Each mode performs 42 serial successful mathematical children: one
whole finite oracle, one positive point cover, one whole physical domain
audit, and 39 carrier/graph/physical-audit stages. Across the two modes,
all 13 physical cases contribute 130 intended semantic negative trials,
the finite oracle contributes 16 and the point cover contributes 10,
for 156 trials. The known ACL69 fixture is literally checked 26 times;
these reproductions are validation of prior art, not new research.
Timeout, incomplete enumeration, UNKNOWN, memory termination or a
different packet produces no absence conclusion and stops the replay.

The computational completeness argument rests on the literal-core
restriction, physical compatibility/gluing, ordered-neighborhood
equivalence and actual point transport proved above. These bridges
are ordinary arguments, not proof-assistant theorems. Different exact
algorithms and normal/-O agreement are same-author validation, not an
independent person's review. The earlier review of the different
t=1,h=4 result does not transfer here.

The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html)
inspected 2026-10-03 lists 69..72. [Aw, Chee and Ling,
Six New Constant Weight Binary Codes, Theorem 1 and Appendix A](https://ymchee66.github.io/home/PDF/6cwc.pdf)
provides the known 69 construction. D is a supplied classical design,
not a new Steiner construction. The literal fixture and pure helper
provenance are recorded in [DERIVATION.json](DERIVATION.json) and
[DEPENDENCIES.md](DEPENDENCIES.md). This result removes a complete
large-union region of one construction model; its union<=14 cap
completion region and the unrestricted endpoint remain open.
