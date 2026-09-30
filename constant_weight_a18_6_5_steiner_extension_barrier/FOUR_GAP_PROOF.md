# Seven old-point outsiders are necessary to reach 70

Author: **six-code-2, researcher**, 2026-09-30.

Fix the classical 68-circle Steiner `S(3,5,17)` built and directly checked
in `geometry.py`, on `V={0,...,16}`. Add `x=17`. Let `F` be any family
of distinct five-subsets of `V union {x}` with pair intersections at
most two. Define `R=|D\F|`, and let `s` count members of `F` avoiding
`x` and outside `D`. Let `a` count words `{x} union Q` with `Q` contained
in a circle of `D`, and `t` count other words through `x`. Put `g=R-a`.

The exact identity is

```
|F| = 68+s+t-g.                                             (1)
```

**First computer-assisted lemma.** If `s>=5`, then `g>=5`, for
arbitrary `t`.

**Second computer-assisted lemma.** If `t=1` and `g=5`, then `s<=5`.
Consequently `s>=6,t=1` implies `g>=6`.

**Corollary.** Among all such packings with `s<=6`, the exact maximum
size is **69**. Every packing of size at least70 therefore has at
least **seven old-point outsiders**, for every coordinate copy of this
classical design and every choice of added point. No automorphism or
retained-core hypothesis is imposed on `F`. This does not improve the
unrestricted numerical bounds `69<=A(18,6,5)<=72`.

## Complete record reduction

The ownership and record construction are those of the earlier
[three-gap proof](THREE_GAP_PROOF.md). A contained four-set has a
unique circle. Different contained words cannot use the same circle,
since different four-subsets of a five-set meet in three points.
Thus each of the `a` contained words replaces a distinct removed circle.
The remaining `g` removed circles are gaps. Each nongap circle
contributes exactly one word, itself or its contained replacement.

Deleting the contributing word of a nongap circle increases `g` by
one without removing an outsider. Discarding a noncontained word
changes none of `R,a,s,g`. There are at least64 nongap contributions
when `g<=4`. Hence the first lemma reduces to excluding five outsiders
with exactly four gaps and no noncontained words.

For a fixed gap set `G`, consider every old five-set `B` outside `D`.
A nongap circle meeting `B` in four points cannot be retained or
replaced compatibly, so reject `B`. Every nongap circle `C` meeting
`B` in three points requires one of exactly three replacements,
`C\{p}` with `p in B intersection C`. A record is `B` and one such
choice per mandatory circle, with all chosen four-sets intersecting
pairwise in at most one point. Optional replacements are omitted.

Two records are adjacent when their outsiders meet in at most two
points and every pair of distinct replacement four-sets, one from
each record, meets in at most one. An identical shared replacement
is allowed, since it represents one word, not two. Equal outsiders
are incompatible. Records induced by an arbitrary packing form a
clique. Shared mandatory circles have consistent choices: different
four-subsets of one circle meet in three points and are forbidden.
This also ensures each chosen replacement is compatible with every
outsider, including those from other records.

A clique expands to a packing by removing the gaps and every circle
blocked by an outsider, retaining all other circles, and adding the
outsiders and the union of mandatory replacements through `x`.
Every nongap circle still contributes once. With `h` outsider records
and `r` gaps, the expansion has `68+h-r` words. The separate checker
verifies the positive controls directly as18-point sets.

## All four-gap configurations

The production normalization uses actual circle permutations induced
by the three checked global generators and Frobenius in `geometry.py`.
It partitions all `binomial(68,4)=814385` unordered circle quadruples
into **92** disjoint orbits. A packing itself need not be invariant.

The separate checker closes the entire generated17-point permutation
group, in the opposite composition convention. It checks all16320
elements against the design and their faithful actions on68 circles.
For each of the92 representatives, it applies every group element.
The orbit sizes agree, the orbits are disjoint, and their union has
814385 valid quadruples. This equals the full possible universe.
Neither an intersection signature nor a claim about the full abstract
automorphism group substitutes for this checked cover.

For every case both implementations examine all6188 old five-sets.
The four-point obstruction leaves2280 eligible outsiders, including
outsiders with no possible replacement assignment. The complete case
graphs have27864--30912 records, totaling2669983 records over92 cases.
The [compact manifest](four_gap_expected.json) supplies every actual
representative, orbit size, record count and canonical record/graph
digest. It contains no full record or graph corpus.

The mask generator recursively chooses a smallest remaining domain,
rejecting only a four-set sharing at least two points with an already
selected four-set. Its complete recursion generates every valid
assignment. The checker instead considers every four-subset of each
mandatory circle as a set, filters directly against `B`, and visits
the circles in fixed order with disjoint old-pair ownership.
Validation compares the two entire sorted record lists entry by entry.

The production graph explicitly intersects replacement four-sets.
The checker reconstructs conflicts by old triples and replacement
pairs, removing identical-replacement owners from a conflict row.
A valid record owning `Q` cannot own another four-set conflicting
with `Q`, so this removal allows exactly the shared identical word.
The full canonical adjacency-row digests agree.

The production search initially targeted six-cliques and uses complete increasing recursion
with proper-color pruning. Independent color classes give an exact
clique upper bound. The separate checker enumerates increasing edges,
triangles, four-cliques and five-cliques, and checks every five-clique
for a larger vertex adjacent to all five. Every six-clique has this
ordering. It also checks symmetry, absence of self-loops and the
complete edge census. No five-clique occurs, which also excludes
six-cliques and strengthens the original production target. The exact
maximum outsider count is three in cases61 and91, and four in the
other90 cases: their triangle/four-clique censuses establish attainment
via the expansion above. For `t=0,g=4`, the exact maximum packing sizes
are67 in those two cases and68 in the others. The deletion reduction
proves the first lemma.

## One noncontained word with five gaps

The old four-set `Q0` of a noncontained word has four triples in four
distinct circles. Each of these circles must be a gap: it cannot be
retained, and every contained replacement in it intersects `Q0` in
at least two points. If `g=5`, there is exactly one further gap.

All2040 noncontained four-sets form one checked orbit. Normalize
`Q0` to mask15, or `{0,1,2,3}`. Its forced gap-circle masks are6155,
9223,16910,33037. Its stabilizer in the checked group has eight elements, directly
checked to preserve `Q0` and the design. Acting on the64 circles
outside the forced gaps gives13 disjoint extra-gap orbits. The
separate checker rebuilds the entire group and every orbit, including
an entrywise comparison of the64-circle partition.

Records must also have `|B intersection Q0|<=2` and every replacement
old part must intersect `Q0` in at most one point. The production
recursion imposes these constraints during generation. The separate
checker enumerates all records for the five gaps before filtering
them by direct set conditions. Both generate the same5068--7096
records per case, entry by entry, and the same graph rows.

Every graph is six-clique-free. Their exact maximum clique sizes,
in manifest order, are

```
4,5,5,4,4,4,4,4,4,4,4,5,4.
```

The separate clique census excludes five-cliques in each claimed
maximum-four case, and verifies an attaining packing for every case.
Thus the second lemma is tight. Cases1,2,11 have directly checked
69-word packings with `s=5,t=1,g=5`. These attain the historical
numerical lower bound; no numerical record or historical priority
for these examples is claimed.

If `t=1,g<5,s>=6`, delete nongap contributions until `g=5`, preserving
the fixed noncontained word and every outsider. The second lemma
excludes the resulting packing. This proves `g>=6` when `s>=6,t=1`.

## The seven-outsider corollary

The earlier [three-gap proof](THREE_GAP_PROOF.md), source commit
`e68a38858372ec635c5489e4b2194a1cdb29290a`, proves `|F|<=69` for
`s<=5`. For `s=6`, use the new lemmas and the ordinary
[Steiner trade costs](../constant_weight_a18_6_5_steiner_trade_bound/PROOF.md),
source commit `5adfdc1fcbe54fd701367c076305af5bd993b616`:

```
g>=2t;
t=2 implies g>=7;
t=3 implies g>=9;
t=4 implies g>=10.
```

Together with (1), these give size at most69 for `t=0,1,2`, at most68
for `t=3,4`, and at most `74-t<=69` for `t>=5`. This covers every
nonnegative integer `t`. The checked69-word positive controls have
`s=5<=6`, so the conditional maximum is exactly69. Relabeling gives
the same necessity for every coordinate copy and every added point.

## Reproduction and trust boundary

Use CPython3.11+, standard library only, one process at a time:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B generate_four_gap.py
python3 -B generate_five_gap_single.py
python3 -B verify_four_gap.py --compare
python3 -B audit_four_gap.py
```

`--case N` selects a single case, and the verifier's `--single`
selects a one-word case when `--case` is supplied. Partial checks
identify their selected coverage; they are not a complete proof.
The verifier can save compact per-case replay summaries using
`--checkpoint-dir /path/under/workspace/scratch`. Full generated
corpora and graphs remain omitted.

Every important phase has a45-second elapsed-time guard. Production
record counts and both graph builders have40000-record memory guards. A guard failure raises
`INCOMPLETE`; it is not evidence of nonexistence. The exact arithmetic
uses arbitrary-precision integers and sets, without a solver or
floating-point assumptions. The normalization, ownership, deletion,
enumeration-completeness, adjacency and cardinality bridges are
written above and have not been formalized. Both implementations
are by this same researcher; no independent peer review is claimed.

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
rechecked2026-09-30, still gives69--72. The historic69 construction
is in [Aw--Chee--Ling2003, Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
Its public plain certificate was fetched afresh and checked directly,
and equals the earlier baseline byte for byte. The classical design
is a historical input. Bounded primary-source searches did not
locate these exact gap/outsider statements; this is no priority
guarantee and no claim about all Steiner designs on17 points.
