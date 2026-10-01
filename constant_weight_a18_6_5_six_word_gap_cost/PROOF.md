# Six noncontained words have sharp forced-gap cost fourteen

Author: **six-code-2, researcher**, 2026-10-01. This is an author
computer-assisted proof with a separate literal-set verification. Independent
peer review and proof-assistant verification are pending.

Let `D` be the classical Steiner `S(3,5,17)` constructed in `common.py`,
on `V={0,...,16}`. Let `Q1,...,Q6` be distinct four-subsets of `V`, none
contained in a circle of `D`, with `|Qi intersect Qj|<=1` for `i!=j`.
Define `T(Q)={C in D:|C intersect Q|>=3}`. Then

**Theorem.** `|T(Q1) union ... union T(Q6)|>=14`. Equality is attained.
The statement also holds after any coordinate relabeling of this explicitly
constructed design. No uniqueness of abstract Steiner designs or symmetry
of an unknown packing is assumed.

For a packing `F` of five-subsets of `V union {x}`, with intersections
at most two, let `R=|D\F|`, let `s` count its words avoiding `x` and
outside `D`, and let `a,t` count its contained and noncontained old
four-parts through `x`, respectively. The theorem gives

```
t=6 => R>=a+14, |F|<=60+s.
```

This is sharp for `s=0`, allowing arbitrary `a`: the supplied sixty-word
fixture has `a=s=0,t=6,R=14`. Consequently a seventy-word construction
with `t=6` needs at least ten old outsider words. These conditional results
do not improve the unrestricted campaign interval `69<=A(18,6,5)<=71`.

The following sharing argument was already established in the author's
[Steiner trade-capacity contribution7560](../constant_weight_a18_6_5_steiner_trade_bound/PROOF.md),
source `5adfdc1fcbe54fd701367c076305af5bd993b616`. It is restated to make
the present finite reduction self-contained; it is not new in this package.

Every noncontained four-part has four triples, with four distinct owners
in `D`. Two triples with the same owner would imply containment of their
union, the four-part. Any circle contains triples from at most two
compatible four-parts: two three-subsets of a five-set with intersection
at most one already cover the five-set, and no third three-subset can
meet both in at most one.

Two compatible four-parts share at most one owner. Disjoint four-parts
cannot both have triples in a five-circle. If their common point is `p`,
a shared circle consists of `p`, two points from each of their disjoint
three-point tails. Two shared circles would intersect in `p` and at
least one point of each tail, contradicting Steiner triple uniqueness.

Thus owner-sharing defines a simple graph on the six four-parts, of
maximum degree four. If it has `e` edges, its owner union has `24-e`
circles, since no owner belongs to three four-parts. A union of at most
thirteen would force `e>=11`. Such a graph has a degree-four vertex:
otherwise its degree sum is at most eighteen, less than `2e>=22`.
Choose such a four-part as the root. It has four sharing neighbors and
one nonneighbor `Z`.

The explicit design-preserving generators in `input.json` have an orbit
of size2040 on `Q0={0,1,2,3}`. Both implementations regenerate the entire
noncontained four-part inventory and check that this orbit is exactly
that inventory. Each generator is checked to preserve the actual circle
list. Therefore an actual design relabeling takes the chosen root to
`Q0`; it relabels the whole unknown family. Neither the order nor the
full automorphism group of the design is needed.

The root has132 compatible sharing partners. Their four shared root
owners partition them into groups of33. A valid family of four root
neighbors uses each owner once, since an owner cannot belong to three
compatible four-parts. The graph induced on those four neighbors has
at least three edges: deleting the root's four edges and `Z`'s at most
four edges from `e>=11` leaves at least three. This gives a small,
complete finite carrier.

`produce.py` constructs all286 sharing edges among the132 partners.
It builds connected families by repeatedly adjoining a vertex adjacent
to some chosen vertex, retaining exact compatibility and distinct root
owners. Every connected graph has an ordering with this property,
obtained from a spanning tree. At each level duplicates are removed
only by the exact sorted vertex key. The connected census at sizes
two, three and four is286,608,808. Every disconnected four-vertex graph
with at least three edges is a triangle plus an isolated vertex; those
are enumerated separately and give172 further families.

`verify.py` instead partitions literal four-subsets by their shared root
owner. It examines every one of the42 labeled graph patterns on four
owner labels having at least three of the six possible edges. For each
pattern it selects one word from each group, in fixed owner order,
requiring literal word compatibility and exactly the prescribed sharing
or nonsharing relation with every earlier choice. Induction on the
chosen owner roles proves completeness: any valid four-neighbor family
has exactly one such pattern and one choice in each role. This recursion
does not use the producer's connected census, triangles, candidates or
negative verdict. Both algorithms give the same980 actual family keys,
compared entry for entry.

| Induced neighbor degrees | Number of families | Five-word forced union |
|---|---:|---:|
|`0,2,2,2`|172|13|
|`1,1,1,3`|160|13|
|`1,1,2,2`|600|13|
|`1,2,2,3`|44|12|
|`2,2,2,2`|4|12|

There are1461 compatible root nonneighbors with disjoint forced-owner
sets. For each of the980 five-word frames, the verifier tests every
one of those1461 literal four-parts, checking compatibility with all
four neighbors and the actual owner union size. All1,431,780 tests
reject an owner union of at most thirteen. This is a complete finite
enumeration, not a solver or heuristic verdict.

The producer uses a different last step. If a five-word frame has `h`
owners, a proposed sixth word needs at least `h+4-13` shared owners.
Because an owner belongs to at most two compatible words and a pair
shares at most one owner, these are shares with distinct neighbors.
The producer intersects the sharing-neighbor carriers for every subset
of the needed size, then checks the remaining literal requirements.
Every necessary intersection is empty in all980 cases. Its complete
inventory agrees with the verifier's complete empty inventory.

The exact negative proves the theorem's lower bound. For equality use
the following old-point masks, where bit `p` labels point `p`:

```
15, 240, 6161, 9249, 16914, 98561.
```

Both implementations check that these are six distinct, compatible,
noncontained four-parts and that their forced-owner union has size14.
Remove those fourteen circles and append `Q union {17}` for the six
four-parts. The sixty resulting five-words are checked literally for
distinctness, weight, and every pairwise intersection. Their sorted
word-list digest is
`81ba8d36bfd8f43c4c2b8ac1220670ba14cb3317515a5cd4add00b458a89ee83`.

To transfer the bound to `F`, a contained four-part has a unique owner
circle, which must be removed. Different contained words reserve
different circles. A noncontained word compatible with that contained
word cannot have a triple in its reserved circle: the contained
four-part omits only one circle point, so it would intersect the other
old four-part in at least two. Hence the `a` reserved circles and the
noncontained forced-owner union are disjoint. This proves `R>=a+14`.
Counting the words gives `|F|=68-R+s+a+6<=60+s`.

The public package has exact standard-library source, the literal
68-circle input and four actual transport maps, a small manifest and
the sixty-word fixture. It contains no private search trees or full
980-family dump. `reproduce.py` regenerates and compares the actual
arrays before comparing compact hashes. The manifest alone is not a
standalone negative-proof certificate. Its mathematical digest is
`3c74ddc5e7af6d2410720f06b748605e4ca5b4ad7c16be2e61c416086647ca93`.

CPython3.11.2 exact integer/set semantics and the written completeness
arguments are the trust boundary. The implementations have the same
author. Forty-two graph-pattern cases and980 final frames are separate
finite cases, each limited to40000 states and45 seconds; no limits or
host settings were raised. The largest pattern has21784 states; each
last-stage frame has1461 tests. The full dual replay takes about four
seconds and19MiB peak RSS in this environment. Nine corruption controls
and two genuine INCOMPLETE controls also pass under `python3 -O`.
Timeout, guard failure, interruption, memory kill or UNKNOWN supplies
no mathematical exclusion. Earlier scratch attempts that hit a total
state guard were incomplete; the complete owner-role decomposition
reported here supplies the proof.

The classical inversive-plane construction is existing mathematics;
[Kiermaier--Krcadinac--Wassermann](https://arxiv.org/abs/2509.23483)
discuss Steiner3-design extensions, which change design strength and
block size. [Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1 and AppendixA, supplies the known69-word lower bound, whose
[public fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69) was
exactly reproduced earlier in this campaign. That reproduction is
validation. [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html)
was checked live2026-10-01 and still lists69--72; the campaign upper71
comes from [six-code-1's separately proved bound](../constant_weight_18_6_5_equality_structure/UPPER71.md)
and [its independent review](../constant_weight_upper71_review1/REVIEW.md).
The new conditional gap cost is not a global bound improvement.
The [earlier extension envelope8112](../constant_weight_a18_6_5_steiner_extension_barrier/PROOF.md)
gives `|F|<=max(69,s+62)`; the present `t=6` consequence strengthens that
conditional envelope to `60+s`. The independently scoped
[special-circle barrier8338](../constant_weight_a18_6_5_special_circle_gap_barrier/PROOF.md)
is a parallel restricted construction result, not a premise here.
Bounded primary-source searches did not locate this exact six-word
cost statement. Historical priority has not been established.
