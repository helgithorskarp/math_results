# Fixed-word barriers and the remaining seven-outsider construction

Author: **six-code-2, researcher**, 2026-09-30.

Fix the classical 68-circle Steiner `S(3,5,17)` generated and checked in
`geometry.py`, on `V={0,...,16}`, and add `x=17`. Let `F` be any packing
of distinct five-subsets of `V union {x}` with pair intersections at
most two. Define `R=|D\F|`, let `s` count old-point words outside `D`,
let `a` count words `{x} union Q` whose old four-set is contained in a
circle of `D`, and let `t` count the other words through `x`. Put `g=R-a`.
Then

```
|F| = 68+s+t-g.                                             (1)
```

The following are exact computer-assisted restricted results:

1. If `t=2,g=7`, then `s<=5`. The exact maximum packing size under
   these two conditions is **68**. In particular, `s>=6,t=2` implies
   `g>=8`, using the ordinary lower bound `g>=7`.
2. If `t=1,g=6`, then `s<=6`. The exact maximum packing size under
   these two conditions is **69**. Together with the earlier five-gap
   lemma, `s>=7,t=1` implies `g>=7`.

**Construction consequence.** A packing with `s=7` and size at least70
must have exactly `t=0,g=5`, and its size must be exactly70. Thus every
packing of size at least71 requires at least **eight old-point outsiders**
relative to **every coordinate copy** of this classical design and
**every choice of added point**. Among packings with `s<=7,t>=1`, the
exact maximum size is69. No packing automorphism or retained-core
condition is imposed. The remaining `s=7,t=0,g=5` construction branch
is open here. The unrestricted primary bounds remain69--72.

## Complete fixed-word record model

The ownership, deletion and record bridges are the earlier
[four-gap proof](FOUR_GAP_PROOF.md). A contained old four-set has one
owner circle, and two contained words cannot have the same owner.
The `g` gap circles are the removed circles having no contained
replacement. Every nongap circle contributes itself or one replacement.
Deleting this contribution increases `g` by one while preserving `s,t`.

A noncontained old four-set has four triples in four distinct circles.
Each of these circles must be a gap: every four-subset replacement of
such a circle would intersect the noncontained four-set in at least
two points. Two compatible noncontained four-sets share at most one
forced gap circle, by the ordinary
[Steiner trade proof](../constant_weight_a18_6_5_steiner_trade_bound/PROOF.md).
Their union of forced circles therefore has at least seven members.

For a specified gap set and fixed noncontained four-sets, inspect all
6188 old five-sets `B`. Reject design circles, words with
`|B intersection Q_i|>2`, and words meeting a nongap circle in at
least four points. Each nongap circle meeting `B` in three points
must use one of its three compatible four-subsets. Retain exactly
the choices intersecting every fixed `Q_i` in at most one point.
A record lists `B` and one choice for each mandatory circle, with
all chosen four-sets pairwise intersecting in at most one point.

Two records are adjacent when their outsiders intersect in at most
two points and distinct replacement four-sets from the two records
intersect in at most one. A shared identical replacement represents
one word and is allowed. Equal outsiders are incompatible. All records
induced by an arbitrary packing form a clique. If two outsiders block
the same nongap circle, graph compatibility forces the same replacement;
this also ensures compatibility of every replacement with every outsider.

Expand a clique by deleting the gaps and all circles blocked by an
outsider, keeping the remaining circles, and adding the outsiders,
the union of mandatory replacements through `x`, and the fixed
noncontained words. Every nongap circle contributes once. For `h`
records, `r` gaps and `t` fixed words, the size is `68+h+t-r`.
Every attaining fixture is also checked directly as eighteen-point sets.
Optional contained replacements in an original packing need not appear
in a record; the clique implication and expansion remain valid.

## Two words and seven gaps

All2040 noncontained four-sets form one directly checked permutation
orbit. Normalize the first to mask15, or `{0,1,2,3}`. Its stabilizer
inside the checked generated group has eight elements. If `g=7`, the
second word must be compatible with the first and share one forced
gap circle, so the seven gaps are precisely their forced union.

Exactly132 possible second four-sets meet these conditions. They
have a disjoint cover by18 actual stabilizer orbits. The production
normalization closes the generated17-point group; the separate checker
closes it in the opposite composition convention, checks all16320
elements on the design, and applies the actual eight stabilizer
permutations to every representative. It checks each orbit entry
and verifies that the union equals the independently defined132-set
domain. Neither an intersection signature nor a classification of
packing automorphisms substitutes for this cover.

The complete record graphs have1124--2746 vertices. Their exact
maximum outsider counts, in manifest order, are

```
3,4,5,5,4,4,3,5,4,4,4,5,4,3,4,5,4,5.
```

Thus three cases have exact maximum packing size66, nine have67,
and six have68. Each graph is six-clique-free, which proves the
first lemma without any assumption about the number of outsiders.
The expansion proves attainment in every case and sharpness of68
over the entire `t=2,g=7` class.

## One word and six gaps

Normalize its old four-set to mask15. Four circles are forced gaps;
the other two gaps can be any unordered pair of the remaining64
circles. All2016 pairs are covered by295 disjoint actual orbits of
the eight-element pointed stabilizer. The separate checker rebuilds
the entire permutation group, reconstructs the full2016-pair universe,
and compares every orbit entry.

The complete graphs have6138--10188 vertices. They are all
seven-clique-free. Their exact outsider maxima are four in23 cases,
five in255 cases, and six in17 cases. The maximum-six cases are

```
73,83,92,93,94,95,102,108,112,127,135,140,141,150,154,158,290.
```

Those17 cases have directly verified69-word expansions with
`s=6,t=1,g=6`. The other cases have exact maximum packing sizes67
or68. These examples attain the historical numerical lower bound;
no numerical improvement or priority for the examples is claimed.

If `s>=7,t=1,g<=5`, the earlier
[five-gap lemma](FOUR_GAP_PROOF.md) gives a contradiction, after
deleting nongap contributions to reach five gaps if needed. If
`g=6`, the new lemma gives a contradiction. Hence `g>=7`.

## Construction consequence

The earlier four-gap proof gives size at most69 when `s<=6`, and
gives `g>=5` when `s>=5`, for arbitrary `t`. Consider `s=7`.

For `t=0`, equation(1) and `g>=5` give size at most70. Size at
least70 forces `g=5` and size exactly70. For `t=1`, the new bound
`g>=7` gives size at most69. For `t=2`, the ordinary `g>=7` together
with the first new lemma gives `g>=8`, again size at most69.
The prior ordinary small trade costs `g>=9,10` at `t=3,4` give
size at most69. The prior exact classical cost `g>=12` at `t=5`
gives size at most68. For `t>=6`, the ordinary `g>=2t` gives
size at most `75-t<=69`. These cases cover every nonnegative `t`.

The six-outsider69-word fixtures establish attainment of the
conditional maximum69 when `s<=7,t>=1`. Any packing of size at
least71 must have `s>=8`; relabeling the reference design and added
point gives the stated every-copy/every-point quantifiers.

Dependencies are the earlier seven-outsider barrier, source commit
`aa775990f13c916b2fb10da55c4ccfd1c1b6797d`, and the ordinary/classical
trade costs, source commit `5adfdc1fcbe54fd701367c076305af5bd993b616`.
These do not require the other researchers' point-degree results.

## Reproduction and trust boundary

Use CPython3.11+, standard library only, one CPU process at a time:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B generate_fixed_word_gap.py
python3 -B verify_fixed_word_gap.py --compare
python3 -B audit_fixed_word_gap.py
```

The default generator and checker cover all313 cases. `--branch pair`
or `--branch single`, and `--case N`, identify partial coverage.
`--checkpoint-dir /path/under/workspace/scratch` saves compact per-case
operational summaries. A phase guard is45 seconds; record counts and
graph builders have40000-vertex guards. Failed guards, incomplete
coverage and memory failures are INCOMPLETE, never nonexistence.

The [manifest](fixed_word_gap_expected.json) supplies orbit representatives,
counts, full record/graph digests, complete clique counts, and small
attaining fixtures. It omits all full record and graph corpora. It is
replay evidence, not a standalone exclusion certificate. Both programs
regenerate every finite universe. With `--compare`, their complete
sorted record streams agree entry by entry in all313 cases.

Production uses mask arithmetic, minimum-domain recursion, explicit
replacement intersections and proper-color clique pruning. The
separate checker uses fixed-order set enumeration with pair ownership,
pair-incidence graph reconstruction, and a complete increasing clique
census without color pruning. Each claimed forbidden clique is
excluded by checking every smaller clique's possible increasing
extension. Graph symmetry and the full edge census are checked.
Each exact maximum has a positive clique count and an expanded
fixture whose distinctness, weight, all word intersections and
`s,t,a,R,g` are checked directly.

The complete final public-source replay with entrywise comparison took
426.41 seconds and49760 KiB peak RSS; its slowest complete case took
2.63 seconds. It rebuilt2222715 records across313 cases. The audit
checks1296 small graphs against direct clique definitions, including
all1024 graphs on five vertices and272 eight-vertex controls. It also
checks4161 actual record pairs, including68 compatible pairs sharing
an identical replacement, and rejects ten corrupted witnesses. A
selected optimized-Python replay agrees with the normal result; this
is not a full second optimized replay. Arithmetic is exact
Python integers and sets; timing measurements do not enter the proof.
The ordinary normalization, ownership, deletion, enumeration-completeness,
adjacency, expansion and consequence bridges are unformalized. Both
implementations are by this same researcher, and no independent peer
review or formalization is claimed.

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
rechecked2026-09-30, gives69--72. The historical69 construction is
[Aw--Chee--Ling2003, Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
Its public fixture was reproduced before these claims. Bounded primary
and committed-graph checks did not locate these exact statements;
this is not a guarantee of historical priority. The theorem concerns
the specified classical design and its coordinate copies, without
an imported uniqueness theorem for all Steiner systems on17 points.
