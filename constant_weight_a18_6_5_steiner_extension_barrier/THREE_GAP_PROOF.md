# Three gaps cannot support four old-point outsiders

Author: **six-code-2, researcher**, 2026-09-30.

Let `V={0,...,16}`, `x=17`, and let `D` be the classical 68-circle
Steiner `S(3,5,17)` generated and checked in `geometry.py`. A packing `F`
consists of distinct five-subsets of `V union {x}` whose pair intersections
are at most two. Define:

- `R=|D\F|`;
- `s=|{B in F : x not in B, B not in D}|`, the old-point outsiders;
- `a`, the number of words `{x} union Q` with `Q` contained in a circle of `D`;
- `t`, the number of other words through `x`;
- `g=R-a`.

The exact identity is

```
|F| = 68+s+t-g.                                            (1)
```

**Computer-assisted lemma.** For this classical reference design,
`s>=4` implies `g>=4`, for arbitrary `t`.

**Second computer-assisted lemma.** If `t=1` and `g=4`, then `s<=4`.
This bound is attained by the explicitly checked 69-word packing in
`single_word_witness69.json`, with `s=4,a=16,t=1,R=20,g=4`.

**Corollary.** The maximum of `|F|` over all packings with `s<=5` is
exactly **69**. Thus every packing of size at least70 has at least
**six old-point outsiders** relative to every coordinate copy of this
classical design, for every choice of the added point. There is no
automorphism or retained-core hypothesis on `F`.

These statements restrict proximity to a specified design. They do not
improve the unrestricted numerical interval `69<=A(18,6,5)<=72`.

## Ownership, gaps, and deletion

Every contained four-set `Q` belongs to exactly one circle `C`, since
the old triples have unique circles. The word `{x} union Q` forces `C`
out of `F`. Two contained words cannot use the same circle: different
four-subsets of a five-set meet in three points, while words through `x`
need old-part intersections at most one. Hence `a<=R`. The `g` deleted
circles without a contained replacement are called gaps. Each nongap
circle contributes exactly one word: itself, or its unique contained
replacement.

If `g<=3`, deleting the contributing word of a nongap circle raises `g`
by one. Deleting an original circle increases `R`; deleting a contained
replacement decreases `a`. Neither deletes an old-point outsider.
There are at least65 contributing circles, so a packing with `s>=4`
and `g<3` can be reduced to one with `s>=4,g=3`. Noncontained words can
also be discarded without changing `R,a,s,g`. It suffices to exclude
four outsiders with exactly three gaps.

## Complete mandatory-replacement records

Fix the gap set `G` and an outsider `B`. A circle meeting `B` in at
least three points cannot be retained. A nongap circle meeting `B` in
four points cannot have a compatible contained replacement either:
every four-subset of that circle meets `B` in at least three points.
Such an outsider is therefore rejected.

For each remaining nongap circle `C` meeting `B` in exactly three
points, its mandatory contained replacement has old part `C\{p}`,
where `p` is one of those three points. These are exactly the three
alternatives compatible with `B`. A record consists of `B` and one
alternative for each mandatory circle, with all selected old four-sets
meeting pairwise in at most one point. Optional replacements are omitted.

Join records if their outsiders meet in at most two points and every
pair of **different** old four-sets, one from each record, meets in at
most one point. An identical shared four-set is allowed: it represents
one common word. Records with the same outsider are incompatible.
Every collection of outsiders in an actual packing induces a clique
in this complete graph.

These conditions also allow a clique to be expanded into a packing.
Different alternatives from the same circle meet in three points,
so the graph forces consistent choices on shared mandatory circles.
Remove the gaps and every circle blocked by an outsider. Keep all
other circles; add the outsiders and the union of their mandatory
replacements. Any replacement is compatible with every outsider:
either its circle is not a blocker for that outsider, or clique
consistency supplies that outsider's own permitted alternative.
Other pair conditions follow directly from the design and graph.
For `h` outsiders and `r` gaps, this expansion has `68+h-r` words.

## All three-gap configurations are covered

Use the three global generators in `geometry.py` and its Frobenius
permutation. Each is directly checked to preserve the 68 circles. The
production code acts on unordered circle triples by these generators.
The separate checker instead closes the full group of permutations
on17 points; its order is16320. Applying all of these actual
permutations to the13 representatives below gives disjoint orbits
whose union equals all `binomial(68,3)=50116` gap triples.

The masks in the table denote subsets of `V` in the ordinary bit basis.
Equal intersection signatures are not treated as equivalent: cases0
and2, for example, both have pair intersections0,2,2 and empty common
intersection but are different actual orbits.

| Case | Gap-circle masks | Orbit | Records | Edges | Triangles | Four-cliques |
|---:|:---|---:|---:|---:|---:|---:|
| 0 | 362,661,1178 | 4080 | 22848 | 139013 | 108148 | 0 |
| 1 | 362,661,3457 | 8160 | 23386 | 144929 | 157518 | 0 |
| 2 | 362,661,16553 | 4080 | 22848 | 139373 | 139152 | 0 |
| 3 | 362,661,19476 | 4080 | 23274 | 143266 | 135340 | 0 |
| 4 | 362,661,50241 | 2040 | 23924 | 157639 | 226260 | 0 |
| 5 | 362,661,80896 | 136 | 23700 | 153885 | 23370 | 0 |
| 6 | 362,1178,1828 | 4080 | 22976 | 142932 | 113184 | 0 |
| 7 | 362,1178,2840 | 8160 | 22560 | 132780 | 113708 | 0 |
| 8 | 362,1178,6155 | 1360 | 22620 | 127860 | 123492 | 0 |
| 9 | 362,1178,9223 | 8160 | 22954 | 137703 | 140690 | 0 |
| 10 | 362,1178,9440 | 1360 | 22374 | 139914 | 61264 | 0 |
| 11 | 362,1178,12564 | 4080 | 23490 | 148188 | 173352 | 0 |
| 12 | 362,3457,12564 | 340 | 24036 | 159480 | 201108 | 0 |

Both implementations inspect all6188 old five-subsets in every case.
After excluding68 design circles, exactly2220 outsiders pass the
four-point obstruction. Indeed each circle has60 noncircle five-sets
meeting it in four points; a noncircle five-set cannot meet two circles
in four points. Of the6120 outsiders,4080 have one such circle and2040
have none. Allowing three gaps gives `2040+3*60=2220` eligible outsiders.
Each case uses325 distinct contained old four-sets, namely340 minus the
five four-subsets of each of the three gap circles.

The mask generator recursively chooses an alternative from a smallest
remaining domain. Its only pruning rule rejects an alternative sharing
at least two points with a selected four-set. Induction on the remaining
mandatory circles shows that every compatible complete assignment is
generated. The separate checker enumerates every four-subset of every
mandatory circle as a set, filters directly against `B`, and recurses
in a fixed circle order with disjoint old-pair ownership. All records
are sorted and checked for duplication. The full assignment censuses
and canonical record hashes are in `three_gap_expected.json`.

The production graph explicitly intersects distinct replacement
four-sets. The checker instead indexes records by outsider triples,
replacement pairs, and identical replacements. For a four-set `Q`, the
union of its six pair rows lists records containing a four-set that
meets `Q` in at least two points. Remove records owning `Q` itself:
a valid record owning `Q` cannot contain a different conflicting
four-set. This yields exactly its forbidden partner records, while
allowing identical shared replacements. Canonical graph rows agree
between the implementations.

The production exclusion uses complete increasing clique recursion,
pruned by greedy **proper** colorings of each remaining candidate
graph. Each color is an independent set; fewer colors than the
remaining clique size is an exact upper bound. All other candidates
are visited recursively.

The checker uses a different exclusion: for every increasing edge
`i<j`, list all `k>j` adjacent to both. For every resulting triangle,
check that no `l>k` is adjacent to all three. Every four-clique has
exactly such an increasing ordering. It verifies symmetry, absence
of self-loops, and twice the enumerated edge count equals the sum
of all row degrees. The checks complete for every case, with no
four-clique. The clique reduction and deletion prove the first lemma.

## One noncontained word with four gaps

Suppose `t=1`. Its old four-set `Q0` is not contained in a circle.
Its four triples lie in four distinct circles. A circle containing
one of these triples can neither be retained nor have a contained
replacement compatible with `{x} union Q0`: every four-subset of
that circle contains at least two points of `Q0`. Thus those four
circles are gaps. If `g=4`, they are the complete gap set.

The checked generators have one orbit on all2040 noncontained old
four-sets, so normalize `Q0` to mask15, or `{0,1,2,3}`. Its four
blocking circles are masks6155,9223,16910,33037. There is no symmetry
assumption on `F` in this normalization.

Records must now also satisfy `|B intersection Q0|<=2` and
`|Q intersection Q0|<=1` for every mandatory replacement `Q`.
The production recursion imposes these conditions before and during
enumeration. The separate checker first constructs all28213 records
for these four gaps, then filters the complete records by these
conditions. Both yield exactly4004 records. The checker rebuilds
the graph by pair incidences. It has8884 edges and4336 triangles.

`single_word_colors.json` is a proper four-coloring of this entire
graph, with color sizes2537,970,359,138. The checker verifies every
record index occurs exactly once, all indices are in range, and no
edge has both ends in a color. A clique has at most one vertex in
each color, so five outsiders are impossible. This proves the
second lemma. The certificate is19115 bytes, SHA-256
`af3c0d76f5aa513268e3081df9a69bb16378d8ee8503d623e4e5fed543668604`.
Its record and graph digests are checked against independently
rebuilt universes; the hash alone is not the proof.

The four compatible records103,625,1391,2484 give outsiders with
masks6163,9238,16922,33052. Their union has16 contained replacements.
The second lemma is tight: keeping48 circles and adding these four
outsiders,16 contained words, and the one noncontained word gives69
words. The checker verifies all2346 distinct word pairs directly
using18-point sets, and checks the exact parameters and degree
multiset `12^1,17^1,19^4,20^12`. This attains the historical numerical
lower bound; no new numerical record or historical priority for
the example is claimed.

## The six-outsider corollary

The previous [two-gap proof](TWO_GAP_PROOF.md), source commit
`82e1f2b9369c778cea3ded680b611fc3fa3cd808`, proves `|F|<=69` for
`s<=4`. For `s=5`, use the ordinary
[Steiner trade bounds](../constant_weight_a18_6_5_steiner_trade_bound/PROOF.md),
source commit `5adfdc1fcbe54fd701367c076305af5bd993b616`:

```
g>=2t;
t=1 implies g>=4;
t=2 implies g>=7;
t=3 implies g>=9.                                         (2)
```

The three small costs follow from four distinct blocking circles per
noncontained four-set, with two compatible four-sets sharing at most
one blocking circle; in general `g>=4t-binomial(t,2)` as well as
`g>=2t`. These are ordinary combinatorial bounds, using only the
Steiner property.

For `s=5,t=0`, the first new lemma gives `g>=4`, so (1) gives
`|F|<=69`. For `s=5,t=1`, (2) gives `g>=4`, and the second new lemma
rules out `g=4`; hence `g>=5` and again `|F|<=69`. For `t=2`, (1)--(2)
give `|F|<=68`; for `t=3`, they give `|F|<=67`. For `t>=4`, they give
`|F|<=73-t<=69`. These cases cover every nonnegative integer `t`.

The checked 69-word example has `s=4<=5`. The conditional maximum
is therefore exactly69, and every larger packing needs `s>=6`.
Relabeling transports this result to every copy of the classical
design and every choice of `x`.

## Reproduction and trust boundary

Use CPython3.11+, standard library only, one process at a time:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B generate_three_gap.py --check three_gap_expected.json
python3 -B verify_three_gap.py
python3 -B audit_three_gap.py
```

The replay manifest contains small exact censuses and SHA-256 digests,
not full record or graph dumps. Both programs reconstruct the entire
finite universe; the coloring is separately verified after reconstruction.
During source validation the mask and set record streams were also
matched entry for entry for all13 cases and the fixed-word branch.
The audit checks the clique kernels against every graph on five vertices,
compares actual record adjacency with direct set conditions, and rejects
corrupted color certificates and words. Assertions are not used for
proof obligations: normal and optimized checker runs agree.

Every phase has an explicit elapsed-time guard; graph and production
record counts have memory guards. A failed guard raises `INCOMPLETE`
and does not yield a negative mathematical conclusion. The ordinary
ownership, deletion, recursion-completeness, normalization, and
cardinality bridges are written here and have not been formalized.
Both implementations are by this same researcher; no independent
peer review is claimed for these new lemmas.

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
rechecked2026-09-30, still lists69--72.
[Aw, Chee and Ling (2003), Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
give the historical69 construction. The classical inversive-plane
design is a historical input, generated and checked directly here.
Bounded primary-source searches did not locate the exact three-gap
and six-outsider statements; this is not a priority guarantee.

For a size70 target with exactly `s=6`, (1) requires `g=t+4`.
The trade costs exclude `t=2,3,4` and `t>=5`; remaining branches are
`t=0,g=4` and `t=1,g=5`. These are concrete construction frontiers,
not excluded by the present claim.
