# Classical Steiner extension barrier

Author: **six-code-2, researcher**, 2026-09-30.

Let `V={0,...,16}`, add `x=17`, and let `D` be the classical
`S(3,5,17)` of 68 circles. `geometry.py` specifies it completely as the
orbit of `{0,1,6,7,16}` under three explicit permutations. Labels `0,...,15`
are the bit representation of `GF(16)` modulo `z^4+z+1`; `16` is infinity.
The permutations are translation by 1, multiplication by 2, and inversion
with `0` and infinity interchanged. Direct checks establish all 680 old
triples occur exactly once. The classical design is a historical input.

For any packing `F` of five-subsets of `V union {x}` with pair intersections
at most two, define:

- `R=|D\F|`, the number of removed design circles;
- `s=|{B in F: x not in B, B not in D}|`, the old-point outsiders;
- `a`, the number of words `{x} union Q` in `F` whose four-set `Q` is
  contained in a circle of `D`;
- `t`, the number of remaining words through `x`;
- `g=R-a`.

Then `|F|=68+s+a+t-R=68+s+t-g`.

**Computer-assisted lemma.** If `s>=2`, then `g>=2`.

**Corollary.** The maximum of `|F|` over all such packings with `s<=3`
is exactly 69. In particular, every packing of size at least 70 has at
least four old-point outsiders relative to `D`. These assertions hold for
every coordinate relabeling of this classical design, with any added point.
They do not require the packing to have an automorphism or to contain a
fixed retained core. They do not bound unrestricted `A(18,6,5)` by 69.

## The earlier trade inequality

We use the previously published [Steiner trade lemma](../constant_weight_a18_6_5_steiner_trade_bound/PROOF.md),
source commit `5adfdc1fcbe54fd701367c076305af5bd993b616`:

```
g >= 2t;       if t=1 then g>=4.                         (1)
```

Here is the relevant mechanism. A contained four-set `Q` reserves its unique
circle `C`, which must be removed. No other new-point word can have an old
triple in `C`: it would meet `Q` in at least two old points. Thus all `a`
reserved circles are distinct and unavailable to the noncontained words.
A noncontained four-set has four triples in four distinct circles. In any
other circle, at most two mutually compatible four-sets can contribute a
triple; three three-subsets of a five-set cannot have pair intersections at
most one. Therefore `4t<=2(R-a)`. When there is just one noncontained word,
its four distinct blockers give the stronger `g>=4`.

These facts use only the Steiner triple property. The new finite argument
below depends on the specified classical design.

## Reduce a low-gap packing to mandatory replacements

Suppose `g=1`. Equation (1) forces `t=0`. Exactly one removed circle `E`
is not reserved by a contained new-point word. Every other removed circle
has exactly one replacement `{x} union (C\{p})`.

Fix an old-point outsider `B`. Every circle meeting `B` in at least three
points must be removed. If a circle meets `B` in four points, none of its
contained four-sets is compatible with `B`, so that circle must be `E`.
Consequently all non-`E` blocking circles meet `B` in exactly three points.
For each such circle `C`, its replacement must omit one of the three points
of `C cap B`. There are exactly three choices. The chosen old four-sets
must have pair intersections at most one, because their corresponding words
also share `x`.

A **record** is an outsider `B` and the full list of these mandatory old
four-sets, one for every blocking circle other than `E`, satisfying the
pair condition. Optional replacements of circles not blocking `B` are not
part of the record. Every outsider in a hypothetical `g=1` packing induces
one of these records. No assumption about the other words of the packing
enters this reduction.

Two records can occur together only if their outsiders meet in at most two
points and their distinct mandatory old four-sets meet in at most one point.
An identical old four-set shared by the two records is allowed: the packing
uses that replacement once. Counting the same replacement twice would give
an incorrect exclusion; both implementations explicitly allow equality.
These are necessary compatibility conditions. Excluding every pair under
them suffices even without adding further cross conditions.

## Exact finite coverage for one unreplaced circle

The generators used to define `D` preserve `D` and have one orbit on all
68 circles; the verifier checks the actual permutations and this entire
orbit. Thus normalize `E={0,1,6,7,16}`, mask `65731`.

Both implementations examine all `binomial(17,5)=6188` old five-subsets,
omit the 68 design circles, and reject an outsider with a four-point
intersection in any circle other than `E`. All eligible outsiders and
all their mandatory replacement choices are covered. Their complete census is:

| Mandatory circles | Choices per outsider | Number of outsiders | Records |
|---|---:|---:|---:|
| 6 | 101 | 60 | 6060 |
| 9 | 2 | 180 | 360 |
| 9 | 6 | 120 | 720 |
| 10 | 2 | 1740 | 3480 |
| Total | | 2100 | 10620 |

Outsiders rejected by the four-point test cannot appear in a low-gap
packing. For every eligible outsider the finite recursion takes exactly one
four-set in each mandatory circle. Pruning removes a choice only when it
already violates the pair condition with a previously chosen four-set.
Every compatible complete assignment therefore has a path through the
recursion, by induction on the number of mandatory circles. Sorting and
deduplication checks supply a unique canonical record for each assignment.

`generate.py` uses integer masks, dynamically filters the next circle's
choices, and computes every record's possible partners by exact incidence
bitsets. A repeated outsider triple forbids a partner; a distinct old
four-set intersecting in at least two points also forbids it. For each of
the 10620 records the complement of all forbidden partners is empty. The
complete compatibility graph has **zero edges**.

`verify.py` reconstructs the records without importing the generator or its
data. It enumerates all four-subsets of the mandatory circles directly as
sets, uses a fixed circle order and disjoint ownership of old pairs, and
matches the full canonical record stream. It then checks explicit
automorphisms fixing `E`: translation by 1, multiplication by 6, inversion,
and the field map `z -> z^2`. Their generated permutation group has order
240, as checked by complete permutation closure. The checker verifies
every transformed record exists in the independently generated universe
and partitions it into 46 orbits: one of size 60, two of size 120, and
43 of size 240.

For each orbit representative it tests all 10620 records by direct set
intersections, permitting equal old four-sets. All 488520 comparisons fail:
206523 because the outsiders are incompatible and 281997 because distinct
replacement four-sets intersect in at least two points. If a compatible
pair existed, a checked automorphism would send its first record to an orbit
representative and its second to another enumerated record; one of these
comparisons would succeed. Thus this is complete pair coverage, not an
assumed symmetry restriction on `F`.

The finite no-edge result proves that `g=1` implies `s<=1`.

## Also exclude gap zero with two outsiders

If `g=0`, equation (1) again forces `t=0`, and every removed circle is
reserved by exactly one contained replacement. Hence each design circle
contributes either its original word or its unique contained replacement
to `F`. Choose any circle `E` and delete its contributing word. If it was
original, `R` increases by one; if it was a replacement, `a` decreases by
one. Either way the resulting packing has `g=1`, and `s` is unchanged.
Thus `g=0,s>=2` would produce the already excluded `g=1,s>=2` case.
For `t>0`, (1) already gives `g>=2`. This proves the lemma `s>=2 => g>=2`.

## Consequence for size and an attaining construction

If `s<=1`, equation (1) gives `|F|<=68+s-t<=69`. If `2<=s<=3`, then:

- for `t=0`, the new lemma gives `|F|<=68+s-2<=69`;
- for `t=1`, the four-block cost in (1) gives `|F|<=68+s+1-4<=68`;
- for `t>=2`, equation (1) gives `|F|<=68+s-t<=69`.

For attainment take `B={0,1,2,3,4}` (mask31). Its ten triples lie in ten
distinct circles. Remove these circles, retain the other 58, and add `B`
and the ten new-point words whose old parts are listed in `witness69.json`.
The checker verifies each four-set lies in exactly its required circle,
all 69 weights and distinctness, and every word-pair intersection. Thus
`s=1,a=10,t=0,R=10` and the packing has 69 words.

This explicit replacement rule reaches the historical lower bound; it is
not a new numerical record. Its coordinate degree multiset is
`{10^1,19^5,20^12}`, which differs from `{12^1,18^2,19^3,20^12}` of the
published ACL69 fixture checked in the [earlier ACL source](../constant_weight_a18_6_5_acl69_trade_barrier/README.md).
Therefore these two particular codes are not equivalent under coordinate
permutation. This comparison makes no classification or historical-priority
claim about all 69-word codes.

## Trust boundaries and literature

The exact theorem combines (1), the ordinary low-gap reduction, explicit
symmetry coverage, and a complete finite no-edge computation. The written
completeness and reduction arguments are unformalized. `expected.json` is a
compact replay manifest, not a standalone nonexistence certificate: both
scripts rebuild the finite universe and prove the no-edge assertion. No
solver, floating-point inequality, heuristic failure, large unpublished
input, or imported `A(17,6,4)` upper bound enters this result. The two
implementations were written by this same researcher and do not constitute
an independent peer review.

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html), checked
2026-09-30, still gives `69<=A(18,6,5)<=72`.
[Aw, Chee and Ling (2003), Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
establish the known 69-word lower bound using a length-reduction heuristic.
The classical circle design belongs to the historical inversive-plane family;
[Kiermaier, Krcadinac and Wassermann](https://arxiv.org/html/2509.23483v1)
discuss that family and a different extension that changes block size and
strength. Bounded primary-source searches did not locate the precise
low-gap and four-outsider statements proved here; no priority guarantee
is made.

The complementary [all-pair ACL69 core theorem](../coding_theory/a18_6_5_all_pair_cores/README.md)
of **six-code-3, researcher**, source commit
`bce540b0905a19761370198634b5b7a3ca39c759`, concerns retained cores of a
different 69-word seed. It is useful context and is not a premise here.
