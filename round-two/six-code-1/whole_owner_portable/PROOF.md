# A finite whole-owner obstruction and complete Hub-label transport

six-code-1, researcher, 2026-10-03. This is an ordinary combinatorial proof
supported by exact finite enumeration. The enumeration/alignment, normalization,
classification and application bridges are unformalized; independent person
review is pending. The public cold reconstruction validates reproducibility of
the previously private result and is not an additional mathematical discovery.

**Claim.** In the explicitly defined selected inventory below, none of the
48 original named x-owner rows belonging to the following 18 colored types can
be completed with the whole Q4 t-star, in either prescribed root view, and a
right owner whose interface belongs to the regenerated 697-type D2 inventory:

```
1426,1427,1439,1440,1452,1453,
1599,1619,1646,1666,1725,1745,1772,1792,1819,1839,1866,1886.
```

The prohibited configuration is the corresponding 49-word union of three
20-word stars with pairwise overlaps 3,5,3 and no three-center word. The stronger
computational statement used in the proof excludes the necessary right
mate/free partition already at the 37-word two-star union. A surviving
partition would not by itself establish existence of a right 20-star.

## Explicit finite inventory and hypotheses

The ground is `{0,...,17}`; individually named Hubs are `{0,...,4}` and centers
are `t=15,x=16,y=17`. `inventory/fixtures.json` contains all 23 literal source
20-quadruple stars on `{0,...,16}`, copied without changes from the published
[P36 source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/five_hub_pair_total36/fixtures.json).
Its SHA256 is
`c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7`.
Each fixture has simple pairs. The checker verifies its deficit mass 5,
16-edge leave, leave degree `1+3d(p)`, and no LOW–LOW leave edge, with
`d(p)=5-r(p)`, LOW={d=0} and HIGH={d>0}.

For every fixture consider every five-subset H, subject to the *explicit*
finite predicate: all deficits are at most 2; for every HIGH point p,

```
d(p) + |L(p) intersect (LOW minus H)| <= 5;
```

no source quadruple is contained in H; exactly one quadruple meets H in three
points. Let A be that triple and m its fourth point. This gives 42,763 physical
T1 owners. The selected subset additionally requires `d(h)=0` for all h in H
and `d(m)=0`; it contains 4,691 physical owners. The condition includes the
displayed propagation predicate, rather than an unrestricted zero-deficit
owner census. The other 38,072 physical owners are outside this result.

The five actual triples through m partition 15 source points. Their unique
unused point f is outside H and has deficit 1 or 2. The actual triples through
f are disjoint, avoid m, and number 4 or 3. Assign the 3! orders of A to Hub
slots 0,1,2 and the 2! orders of H minus A to slots 3,4. For each of these 12
roles, recover all actual mate triples M, free triples F, the distinguished
hole set, every incidence cell and the original 17-point map. The normalization
sends f to 15, m to 17, and the remaining non-Hub points to 5 through 14 by
canonical cell order. Adjoining center 16 gives the entire x-star.

The complete key consists of deficit, the Hub membership of every free/hole
column, and the Hub membership and non-Hub cardinality of every M-row/column
cell. Minimize over all free-column orders and unordered M rows, keeping the
hole column last. Lexicographically sorted distinct keys define the type IDs;
every original row index and full point map are retained, not just a class
representative. There are 56,292 named rows and 2,117 keys: 1,420 D1 and 697 D2.
For D2, the latter set is the right-interface inventory in the claim.

Two independent physical readers scan, respectively, all C(17,5) H sets and
all 20*4*C(13,2) owned-block/mate/extra-Hub routes. Their entire retained
physical records and auxiliary coordinate multisets agree. Separate bit/set
readers recover all mate/free triples and all colored cells. A third literal
checker verifies every original point map, actual triple image, cell, and key.
Thus this packet generates the stated finite inventory from the compact
fixture; no prior list of owners, keys, maps or expected outcomes is an input.

Generic coverage of all possible pair-simple twenty-stars is a separate
import credited to the [8933 classification audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md).
The [8323 upper71 audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md)
provides the no LOW–LOW condition in its 71-word application. Those reviews do
not review this new interface argument. The finite claim treats the 23 literal
fixtures and the displayed selection predicate as its domain; any application
to an arbitrary code must separately justify this normalization and selection.

## Complete literal37 calculation for the two bases

The t-star source Q is the entire fixture 4. Both ordered root views
`(u,v)=(13,14),(14,13)` are considered. A point map phi sends u to x and v to y,
and maps the other 15 original points bijectively onto `{0,...,14}`. Its whole
t-star is `{ {15} union phi(q) : q in Q }`. Require exactly the three prescribed
x/t overlaps and all pairs of the 37-word union to intersect in at most 2.
This is exactly weight-five minimum-distance-six compatibility.

Base1426 has **all original rows 1792,1794,2776,2778**. Whole-word comparison
gives exactly two literal owners: 1792=2776 and 1794=2778. Base1599 has **all
original rows 5861,6208**, which give one literal owner. This equality of all
20 words is the sole quotient in the direct map enumeration. The common M is

```
{ {0,1,2},{3,11,12},{4,13,14},{5,6,7},{8,9,10} }.
```

The complete actual F_x partitions are, respectively,

```
1426: { {8,11,13},{5,9,14},{0,6,10} },
1599: { {5,8,11},{0,6,9},{1,3,13} }.
```

These inputs are freshly derived from **every** original row of the regenerated
catalogue. Nothing about previously selected 25-word witnesses restricts phi.
There is no preselected Hub image, right type, mate partition or saved37 map.

For each root view the three disjoint source triples through u must map onto
the three actual F_x triples. There are `3!*(3!)^3=1296` free bindings; both
independent rank functions agree on the entire lists. The six remaining source
points map onto the six target holes in all `6!=720` ways. Hence the two bases
have 5,184 and 2,592 representative whole six-hole cases, or 3,732,480 and
1,866,240 representative full maps. Counting all original named rows gives
7,464,960 and 3,732,480 maps. Identical owner words have identical whole domains.

`literal/producer.py` uses fixed-order DFS, pruning only when a completely
mapped source pair/triple is forbidden by a whole owner word.
`literal/oracle.py` uses factoradic free bindings and independent MRV on
partial actual word intersections. If a partial intersection already exceeds
the allowed bound, extending it cannot repair it. Each DFS maintains
injectivity and tries every unused hole image; these monotone rejection rules
discard no admissible full map. The complete solution lists agree in every
case. Each positive receives direct checking of all 666 actual word pairs.

The complete outcomes are:

| Base | Whole cases | Positive maps | Distinct37 unions | Literal right F_y | All697 comparisons |
| --- | ---: | ---: | ---: | ---: | ---: |
|1426|5,184|36|6|6|4,182|
|1599|2,592|48|8|7|4,879|

The 36 and 48 positive cases each have one full point map; all remaining
5,148 and 2,544 cases are completed negatives. Right F_y is recovered both
from the source words through v and from the actual37 words through t,y;
M is recovered from the five words through x,y. The two SAT-only M rows meet
the right free-point union with patterns (1,1),(1,2) for1426, and
(1,1),(1,2),(2,2) for1599.

For partitions M,F, the complete colored cell key is an exact invariant for
point-partition isomorphism fixing each named Hub. A bijection preserves all
cell data. Conversely, a matching row/column order maps every Hub identically
and matches all non-Hub points inside corresponding cells, producing an
actual bijection. The hole column stays distinguished. This is an ordinary
completeness proof, not a formal proof-assistant theorem.

Every regenerated D2 key is reconstructed as an actual 15-point prototype
and checked back against its entire key. Each of the 13 literal right
interfaces is compared with all 697 keys, using both whole-key equality and
an independent complete MRV enumeration of actual point bijections fixing
all five Hubs. **All 9,061 comparisons have no map.** Each literal interface
has actual positive maps to its own synthetic prototype. Therefore every
possible37 union for either base fails a necessary right-owner condition.

## Whole-star Hub transport: the structural mechanism

Let G=S3 x S2 permute `{0,1,2}` and `{3,4}` separately while fixing t,x,y.
For every one of its 12 elements and all 697 keys, independently transform
the whole colored descriptor and an actual point-partition prototype.
The resulting keys agree in all 8,364 cases. Each action is a bijection of
the entire right inventory.

Suppose an 18-point bijection rho fixes t,x,y, induces a Hub permutation in G,
and maps a whole base x-star to a whole target x-star. Composition
`phi -> rho composed with phi` bijects their entire Q-map domains in both
root views. It preserves every intersection, overlap and actual right
partition. If a target right interface matched an inventory key by a
Hub-fixing point bijection, compose with rho and then relabel the output
by the inverse Hub action. Inventory closure would give a Hub-fixing match
for the base interface, contradicting its completed obstruction.

Key equality alone does not establish the required whole-star map. For
every original row of every target type, the checker compares its physical
fixture, H, free root and mate root to an original base row. It composes the
**two entire original17-point maps**, fixes center16, and verifies the resulting
18-point bijection, all three fixed centers, Hub action, full 20-word image,
all actual M/F images and the full colored key. All 190 pairs inside each
target star are also checked. This gives all 24 original rows of the six-type
1426 orbit and all 24 rows of the twelve-type1599 orbit displayed in the claim.
No representative row replaces the other rows. The composition argument
therefore establishes the claim for all 48 original owners.

## Reproduction, trust boundaries and limits

Run the command in README.md. Only CPython3.12 and its standard library are
needed. The declared domain and all mathematical source bytes were frozen
before the complete portable run. Every source is rechecked before each
child. All work is serial with native threads1; original per-case guards
are100,000 states/10 seconds, with60-second focused children and65-second
operational timeouts. Completed case streams and active prefixes are flushed.
A guard hit, timeout, kill, error or incomplete domain never establishes a
negative case. Normal and optimized Python must agree on entire mathematical
records, decisions, point maps, original rows and transport certificates.
The checker remains active under `python -O` and uses no assertions.

EXPECTED.json records compact completed-domain hashes and counts, checked
only after generation. No expected result, old private corpus, graph response,
checkpoint, environment-specific pathname or database supplies a mathematical
input. The large generated records are intentionally omitted from publication;
the source regenerates them in the requested work directory. Source manifests,
literal fixtures, compact expected hashes and proof are published together.

Earlier private inventories, all7,776 decisions,84 literal37 certificates,
9,061 right comparisons and all48 transport receipts are post-completion
comparison targets for the author's validation; they are not public inputs.
The reconstruction itself is validation. The mathematical progress being
made public is the complete whole-owner obstruction and full original-row
transport argument, rather than a failure on saved25-word embeddings.

In the earlier conditional candidate graph this rules out360 oriented
keys/156 undirected edges incident with these18 types. Those graph totals
are context from a separate necessary25-word gate, not an additional
source-only census claimed by this packet. All3,000 earlier positive25-word
certificates remain valid necessary witnesses; the other2,640 candidate
keys/1,248 potential edges have no full-owner verdict here. No clique,
population or global upper-bound consequence is asserted. Type1590 and
its other original owners remain unrun at this full-owner gate.

The [Brouwer table](https://aeb.win.tue.nl/codes/Andw.html), rechecked live on
2026-10-03, lists69–72; the known69 construction is due to
[Aw, Chee and Ling](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Ars Combinatoria67 (2003),313–318. The69 construction was exactly reproduced
earlier (all2,346 word pairs and690 triples); reproduction is not new research.
The campaign's separate upper71 audit is not a claim that this result solves
A(18,6,5). No historical priority is claimed. Code2's fixed-parent cap result
and Code3's distinct three-C result have different hypotheses and are not
premises. No prior review verdict transfers to this new claim.
