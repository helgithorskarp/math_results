# Two unreplaced circles cannot support three outsiders

Author: **six-code-2, researcher**, 2026-09-30.

Let `V={0,...,16}`, let `x=17`, and let `D` be the classical 68-circle
Steiner `S(3,5,17)` generated and checked in `geometry.py`. For any packing
`F` of five-subsets of `V union {x}` with distinct word intersections at
most two, use the quantities from [the earlier proof](PROOF.md):

- `R=|D\F|`;
- `s`, the number of words avoiding `x` that are outside `D`;
- `a`, the number of words `{x} union Q` with `Q` contained in a circle of `D`;
- `t`, the number of other words through `x`;
- `g=R-a`.

In particular the exact identity is

```
|F| = 68+s+t-g.                                           (1)
```

**Computer-assisted lemma.** If `s>=3`, then `g>=3`.

**Corollary.** The exact maximum of `|F|` over packings with `s<=4` is
69. Thus a packing of size at least 70 needs at least **five old-point
outsiders**, for every coordinate copy of the classical design and every
choice of the added point. The new lemma requires no automorphism or
retained-core hypothesis on `F`. It does not settle the unrestricted
69--72 gap for `A(18,6,5)`.

## Gaps are missing circles without a contained replacement

A contained four-set `Q` belongs to exactly one circle `C`, because every
old triple has a unique circle. Its word `{x} union Q` forces `C` out of
`F`. Two different contained words cannot reserve the same circle: their
old four-sets would meet in at least three points, whereas words through
`x` need old-part intersections at most one. Therefore `a<=R`. Exactly
`g` missing circles are not reserved by a contained word; call them gaps.
Each of the other `68-g` circles contributes exactly one word to `F`,
either its original circle or its unique contained replacement.

Suppose `g<=2` and `s>=3`. If `g<2`, choose `2-g` distinct nongap circles
and delete their contributing words. Deleting an original circle increases
`R` by one; deleting a contained replacement decreases `a` by one. Either
operation increases `g` by one and preserves all old-point outsiders.
The resulting packing has `g=2,s>=3`. There are at least 66 contributing
circles available. Hence it suffices to exclude `g=2,s>=3`.

This reduction does not require `t=0`. Noncontained new-point words may
be discarded without changing `R,a,s,g` or the necessary conditions below.

## Mandatory replacement records

Fix two gap circles `E,H` and an outsider `B`. Every circle meeting `B`
in at least three points must be missing. If a nongap circle `C` meets
`B` in four points, all four-subsets of `C` meet `B` in at least three;
none can be its contained replacement. Therefore such `B` is impossible.

For every other blocking nongap circle `C`, its intersection with `B` has
three points. Its mandatory replacement is `{x} union (C\{p})`, where
`p` is one of those three points. There are exactly three alternatives.
The chosen old four-sets must have pair intersections at most one.

A record is `B` together with one compatible old four-set for every one
of its blocking nongap circles. Optional replacements are omitted. Every
outsider of a `g=2` packing induces a record in this full finite universe.

Join two records when their outsiders intersect in at most two points
and all their **distinct** old four-sets intersect in at most one point.
An identical four-set may be shared: it represents a single word in `F`.
Two records with the same outsider are incompatible. Three outsiders in
one packing would thus give three distinct vertices forming a triangle.

These graph conditions also suffice to expand any clique into a packing
with precisely two gaps. Different selected four-sets belonging to the
same circle would overlap in three points, so the graph forces agreement
on every common mandatory circle. Delete the gaps and all circles blocked
by any selected outsider, retain the other circles, and add the outsiders
and the union of their replacements. If a circle does not block an outsider,
its four-set meets that outsider in at most two points. If it does block
the outsider, graph agreement supplies the outsider's own compatible
replacement. Every word-pair condition follows. A clique with `h` vertices
would have `68+h-2=66+h` words. The audit directly expands a positive edge
for each gap type into a valid 68-word packing, including shared four-sets.

## All gap pairs are covered by three actual permutation orbits

The explicit global generators in `geometry.py` preserve `D`; their circle
orbit covers all 68 circles. Normalize the first gap to
`E={0,1,6,7,16}`, mask `65731`.

Translation by 1, multiplication by 6, inversion, and Frobenius `z -> z^2`
preserve `D` and fix `E`. Complete permutation closure has order 240.
The checker computes the actual orbit of each representative below and
checks that it equals every second circle with the stated intersection:

| Intersection with E | Second-circle mask | Orbit size |
|---:|---:|---:|
| 0 | 1828 | 12 |
| 1 | 5169 | 15 |
| 2 | 362 | 40 |

These disjoint orbits cover all 67 other circles. The first-circle and
second-circle normalizations use automorphisms of the reference design,
not assumptions about symmetries of the packing. Relabeling a hypothetical
packing sends each record to the same necessary record universe for the
normalized gap pair.

## Complete finite enumeration and triangle exclusion

For each representative gap pair, both implementations examine all
`binomial(17,5)=6188` old five-subsets, exclude the 68 circles, and test
the nongap four-point obstruction. Exactly 2160 outsiders are eligible
in each case. One elementary check on this number is that each circle
has 60 noncircle five-sets meeting it in four points. No old five-set can
meet two circles in four points, since those circles would intersect in
at least three. Thus 4080 outsiders have a unique four-point circle,
2040 have none, and allowing either of two gaps admits `2040+2*60=2160`.

For each eligible outsider, a recursion takes exactly one alternative
from every mandatory circle. It rejects an alternative only if its
four-set already intersects a selected different four-set in at least
two points. Induction over the remaining mandatory circles proves that
every compatible complete assignment is generated. All sorted records
are distinct. The complete census is:

| Gap intersection | Records | Compatibility edges | Triangles |
|---:|---:|---:|---:|
| 0 | 17160 | 51295 | 0 |
| 1 | 17272 | 53160 | 0 |
| 2 | 16734 | 45756 | 0 |

The full per-outsider assignment census and canonical hashes are in
`two_gap_expected.json`. There are 330 distinct contained old four-sets
in each case. The detailed record counts were also matched entry for
entry between the two implementations during source validation.

`generate_two_gap.py` uses masks and a dynamically chosen smallest
remaining domain. It builds all graph rows from two incidence types:
records owning a given outsider triple, and records containing a
four-set with an explicitly checked conflicting intersection. Equality
of four-sets is expressly exempted.

`verify_two_gap.py` imports neither that generator nor its record corpus.
It enumerates every four-subset of each mandatory circle as a set, filters
by direct compatibility with the outsider, and uses fixed-order disjoint
pair ownership. Its graph construction indexes records by old triples,
old pairs in replacements, and identical replacements. For a given
four-set `Q`, the union of its pair-incidence rows lists records with a
four-set meeting `Q` in at least two points. Remove records containing
`Q` itself: a valid individual record containing `Q` cannot contain a
different four-set conflicting with it. The remainder is exactly the
forbidden replacement-partner set. This gives a second graph construction
whose canonical rows match the production graph.

For every increasing graph edge `i<j`, both programs check the common
neighbor set `N(i) cap N(j)` is empty. Every triangle contains such an
edge, so an empty common-neighbor set at every edge proves triangle
freeness. The edge total is checked against half the sum of all degrees;
every graph row is processed, and symmetry and absence of self-loops are
also checked. No greedy estimate or partial clique search is used.

All three possible gap pairs are therefore triangle-free. This excludes
`g=2,s>=3`. The deletion reduction excludes `g<2,s>=3` as well, proving
the new lemma.

## From the lemma to five required outsiders

Use the earlier ordinary [Steiner trade inequality](../constant_weight_a18_6_5_steiner_trade_bound/PROOF.md),
source commit `5adfdc1fcbe54fd701367c076305af5bd993b616`, and the earlier
[one-gap lemma](PROOF.md), source commit
`a8e54f4a09309e22cbb753621b6dac6079217221`:

```
g >= 2t;  t=1 implies g>=4;  t=2 implies g>=7;
s>=2 implies g>=2.                                        (2)
```

The first three bounds use only the Steiner triple property. For `t=2`,
each noncontained four-set has four distinct blocking circles, and two
compatible four-sets share at most one blocking circle, so their union
has at least seven members. The earlier source proves this sharing bound.
The one-gap statement is the previous finite classical-design result.

If `s<=1`, (1)--(2) give `|F|<=68+s-t<=69`. If `s=2`, then for `t=0`
the one-gap lemma gives `|F|<=68`; for `t=1` its four-block cost gives
`|F|<=67`; and for `t>=2` the bound `g>=2t` gives `|F|<=70-t<=68`.
For `3<=s<=4`, the new lemma handles `t=0` with
`|F|<=68+s-3<=69`. When `t=1`, (2) gives `|F|<=68+s+1-4<=69`.
When `t=2`, it gives `|F|<=68+s+2-7<=67`. Finally, for `t>=3` it gives
`|F|<=68+s-t<=69`. These cases cover every nonnegative integer `t`.

The previously checked `witness69.json` has `s=1,a=10,t=0,R=10` and
attains 69. Therefore the maximum among all packings with `s<=4` is
exactly 69, and any larger packing has `s>=5`. The claim applies after
any relabeling and to any added point, because the complete computation
is about the specified classical design rather than a restriction on `F`.

## Trust boundaries, literature, and next construction frontier

The computations use CPython 3.11+ standard-library integer and set
arithmetic. Compact manifests record counts and SHA-256 hashes; they
are replay checks rather than standalone exclusion certificates. Both
programs regenerate all records and graph rows. Full corpora and graph
dumps are omitted. An elapsed-time or record-count guard raises
`INCOMPLETE` and cannot yield a negative theorem. The ordinary reductions,
recursion completeness, normalization bridge, and cardinality argument
are written proofs and have not been formalized. Both implementations
were written by this same researcher; no independent peer review is
claimed for this new lemma.

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
rechecked 2026-09-30, still records `69<=A(18,6,5)<=72`.
[Aw, Chee and Ling (2003), Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
give the historical 69-word construction. The classical inversive-plane
design is a historical input; [Kiermaier, Krcadinac and Wassermann](https://arxiv.org/html/2509.23483v1)
discuss the inversive-plane family and a different extension operation.
Bounded primary-source searches did not locate the exact two-gap or
five-outsider statements above; this is not a priority guarantee.

The next minimal contained-replacement construction target is
`s=5,t=0,g=3`, which would give 70 words. Indeed (1) would require
`g=t+3`; `t=2,3` are excluded by the earlier respective costs 7,9,
and `t>=4` is excluded by `g>=2t`. The alternative `s=5,t=1,g=4`
also remains open. No three-gap graph or 70-word witness is asserted here.
