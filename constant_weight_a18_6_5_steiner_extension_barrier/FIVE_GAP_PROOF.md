# Five-gap outsider obstruction and the linear extension envelope

Author: **six-code-2**, role **researcher**, 2026-10-01.

**Status:** complete exact computer-assisted restricted result. The primary
computation and separate final-source replay cover all 789 cases, comparing
every record and projected graph row. Both implementations are by this
researcher; independent peer review is pending and ordinary proof bridges
are unformalized.

## Statement and scope

Let `F` be any family of distinct five-subsets of an eighteen-point set,
with distinct members intersecting in at most two points. Choose any added
point `x` and any coordinate copy `D` of the explicit classical 68-circle
`S(3,5,17)` supplied by [geometry.py](geometry.py) on the other points.
Define:

- `s`: old-point words outside `D`;
- `a`: words `x ∪ Q` with `Q` contained in a circle of `D`;
- `t`: words `x ∪ Q` whose old four-set is not contained in a circle;
- `R`: absent original circles of `D`;
- `g = R-a`: circles contributing neither an original word nor a contained
  replacement.

The new finite claim is **`g=5` implies `s<=5`, for arbitrary `t`**. Five
outsiders are attained by a directly checked 68-word packing with `t=0`.
Together with the preceding published lemmas this gives

    |F| <= max(69, s+62).

Consequently every packing of size `M>=70` has

    s >= M-62,     g >= t+6,

relative to **every** chosen added point and **every** coordinate copy of
this classical design. Sizes 70, 71 and 72 therefore require at least
8, 9 and 10 old-point outsiders respectively. The restricted maximum
for `s<=7`, and separately for `g<=5`, is exactly 69.

The unrestricted [maintained interval is still 69--72](https://aeb.win.tue.nl/codes/Andw.html).
No 70-word packing, unrestricted upper improvement, uniqueness of all
Steiner designs, historical-priority guarantee, formalization, or
independent peer review is asserted.

## Ownership, word count and deletion

Every old triple belongs to exactly one circle in `D`. A contained
four-set therefore has a unique owner circle. Two contained four-sets in
one circle intersect in at least three points, so their words through `x`
cannot coexist. Nor can an original circle coexist with one of its
contained replacements. Unique ownership gives `0<=g<=68`.
Each non-gap circle contributes exactly one of
these words. All other words are counted by `s` and `t`; hence

    |F| = 68+s+t-g.                                      (1)

Deleting the contributing word of a non-gap circle increases `g` by one
without changing `s,t`. For an original circle, `R` increases; for a
contained replacement, `a` decreases. There are `68-g` such contributing
words, so whenever `g<=5` we can reach exactly five gaps by `5-g`
deletions. All pair intersections remain valid. A five-gap exclusion
therefore implies the corresponding exclusion for every smaller gap
count, with `s,t` preserved.

## Complete records at fixed gaps

Fix a five-circle gap set `G`. For each old outsider `B`, examine every
non-gap circle `C`. If `|B∩C|>=4`, neither `C` nor any of its four-subset
replacements is compatible with `B`, so this outsider is impossible.
If `|B∩C|=3`, the original circle is impossible, and its replacement must
be one of the three sets `C\{p}`, with `p∈B∩C`. These are all the
four-subsets of `C` meeting `B` in at most two points.

A record is `(B, sorted mandatory replacement four-sets)`. It chooses one
of those three alternatives for each circle meeting `B` in three points,
and requires any two chosen four-sets to intersect in at most one point.
All 6,188 old five-sets are considered, including and then rejecting the
68 design circles. Records are sorted lexicographically, without
deduplicating distinct choices over the same outsider. Both enumerators
check absence of duplicate canonical records.

Every actual outsider induces a record from its actual contained
replacements. Optional contained replacements need not be stored; omitting
them only relaxes the test. Noncontained words through `x` can likewise be
omitted. Thus the reduction applies to arbitrary `t`, without asserting
that an arbitrary record choice is extendible to those omitted words.

Two records `(B,Q)` and `(E,T)` are compatible exactly when `B!=E`,
`|B∩E|<=2`, and every distinct `q∈Q,r∈T` has `|q∩r|<=1`. Identical
replacement sets shared by two records are allowed. The unique-owner
argument ensures all cross old-word/replacement intersections: if the
owner circle of `r` meets `B` in at least three points, `B` mandates a
replacement in the same circle. A different choice in that circle would
intersect `r` in at least three points, so record compatibility forces the
identical choice. When the owner meets `B` in at most two points, `r`
already meets `B` in at most two points.

An actual packing with `s` outsiders consequently induces a clique of
`s` records. This direction suffices for every exclusion here.

## Necessary outsider projection

Partition the records into groups `I_B` by their outsider. The projected
graph `P(G)` has one vertex per nonempty group. It joins `B,E` precisely
when **some** compatible record pair in `I_B × I_E` exists. A record
clique injects into a clique of the same size in `P(G)`, since equal
outsiders are never adjacent. A projected clique need not lift to a record
clique: its edge witnesses can choose mutually inconsistent records.
No converse is used in an exclusion or a construction assertion.

The two implementations compute this exact necessary graph differently.
Write `U` for the complete record universe, `O_B` for records whose old
word meets `B` in at least three points, and `D_q` for records containing
some replacement `r!=q` with `|q∩r|>1`. The forbidden row of a record
`(B,Q)` is `O_B ∪ ⋃(q∈Q) D_q`. The union of its allowed rows over `I_B` is

    U \ [ O_B ∪ ⋂((B,Q)∈I_B) ⋃(q∈Q) D_q ].              (2)

Production builds old-word conflicts by triple incidence, constructs each
`D_q` by literal four-set intersections, and evaluates the intersection of
forbidden replacement rows in (2). It then tests which outsider groups
have a record in that allowed union.

The separate checker instead uses literal-set, fixed-circle-order
enumeration. It constructs replacement conflicts by incidence of old
pairs, with the identical-`q` records removed. This removal is sound
because internally valid records cannot also contain a distinct
replacement sharing a pair with `q`. It then explicitly takes the **union
of allowed rows for every record**, and projects their owner groups.
With `--compare`, the entire canonical record list, outsider list and every
projected adjacency row are compared entry by entry with production.

Production's exact search uses proper-color bounds and exhaustive
increasing-vertex branching. The separate checker uses no production
search: it enumerates every increasing clique through size five and
rejects every possible sixth member. Each clique appears once, according
to its unique increasing vertex sequence. It also checks self-loops,
symmetry and the complete edge census. Guards return incomplete status;
elapsed time is not mathematical evidence.

## Normalization covers every five-gap choice

The explicitly generated point group has 16,320 permutations. Every one
is checked to preserve all 68 circles; its circle action is faithful and
transitive. This checked generated group suffices. No completeness claim
about an abstract automorphism group or a symmetry of `F` is needed.

Production augments each of the 92 preceding four-gap representatives by
each of its 64 absent circles. Every five-gap choice contains a four-gap
choice, so these 5,888 augmentations cover the new domain up to the actual
group action. A selected circle is transported to circle zero, then the
240-element stabilizer is applied to find a canonical image. Choosing
each of the five selected circles in turn gives 789 representatives.

The separate normalization replay does not rely on that augmentation
argument or its canonicalizer. It applies **every** checked circle
permutation to each representative, retaining images containing circle
zero. Removing that circle gives a set of four-tuples in `1,...,67`.
These 789 pointed orbit sets are nonempty, disjoint, and their union is
checked literally against all `C(67,4)=766,480` tuples.

Transitivity implies that a full orbit of size `L` has `5L/68` members
containing any specified circle. The checker derives `L` from this
identity, and independently checks `L=16,320/stabilizer_order` against the
literal representative stabilizer. Its full orbit sizes sum to
`C(68,5)=10,424,128`. Thus every five-circle gap set is represented, and
the exclusions transport back by actual coordinate permutations.

## Primary exact output and attained fixtures

The primary complete computation enumerated 27,400,427 records over all
789 representatives. Per case there are 32,850--37,002 records, 2,340
projected outsider vertices, and 3,826--7,416 projected edges. Every
projected graph is six-clique-free. The primary total case time was
1,389.49 seconds, with measured peak RSS 53,976 KiB. These timings are
reproducibility information only.

The complete final-source replay regenerated all 789 cases and all
27,400,427 records, comparing every canonical record and projected graph
row with production. Its complete increasing-clique census has zero
six-cliques. Summed case time was 3385.801083 seconds,
slowest case 7.216059 seconds, with measured peak
RSS 135,824 KiB. It ran in resumable bounded batches under
one unchanged Python/source/input fingerprint. Selected private replays
and direct controls remain implementation validation, separate from this
whole-domain verification. The complete census by clique sizes 1--6 is
`{"1":1846260,"2":3809482,"3":4734554,"4":2093395,"5":374097,"6":0}`.

The compact [expected manifest](five_gap_expected.json) contains each
representative, its full orbit size, exact record count/digest, projected
edge count/digest, and the small case-zero attaining fixture. The latter
has five distinct outsiders, sixteen contained replacements, twenty-one
absent original circles, no noncontained words, `g=5`, and 68 total words.
The checker reconstructs and tests every eighteen-point word pair. This
shows that the outsider upper five at exactly five gaps is sharp.

The separate [audit](audit_five_gap_projection.py) compares both projectors
with literal compatible-record-pair projection on all 255 nonempty
subsets of an eight-record pool, including alternative records over the
same outsiders, and on 256 seeded controls of at most twenty records.
Ten fixture pairs share identical replacements. These are algorithm
controls, not additional gap-orbit coverage.

The already published [69-word fixture](witness69.json) has `s=1,t=0,g=0`.
The audit rebuilds all its words and checks weights, distinctness, unique
owner circles and all pair intersections. This is validation of a known
construction; it makes the two restricted upper bounds below sharp.

## Ordinary consequences and imported inputs

The new finite result plus deletion gives

    s>=6 ==> g>=6, for arbitrary t.                       (3)

For `s>=7`, combine (3) with the
[previous fixed-word lemmas](FIXED_WORD_GAP_PROOF.md) and
[ordinary/classical trade costs](../constant_weight_a18_6_5_steiner_trade_bound/PROOF.md):

| Noncontained count `t` | Required gap lower bound | Therefore `g-t` |
| --- | --- | --- |
| 0 | 6, by (3) | at least 6 |
| 1 | 7, by the preceding `s>=7` fixed-word lemma | at least 6 |
| 2 | 8, by the preceding `s>=6` fixed-word lemma | at least 6 |
| 3 | 9, by the ordinary trade bound | at least 6 |
| 4 | 10, by the ordinary trade bound | at least 6 |
| 5 | 12, by the exact classical five-word theorem | at least 7 |
| at least 6 | `2t`, by the ordinary trade bound | at least `t>=6` |

Hence `s>=7` implies `g>=t+6`. Equation (1) then gives `|F|<=s+62`.
For `s<=6`, the [preceding four-gap proof](FOUR_GAP_PROOF.md) already
establishes `|F|<=69`. This proves the displayed envelope in the statement.
For `M>=70`, the latter case is impossible, so `s>=M-62` follows.
In particular `s<=7` gives `|F|<=69`. Also `g<=5` implies `s<=5` by
deletion and the finite result, so the same previous bound gives 69.
The known 69-word fixture attains both restrictions. No attainment at 70
is claimed.

An equivalent useful form is obtained by writing `r_x=a+t` and
`I=|F∩D|=68-R`. Since `|F|=s+I+r_x`, every `M>=70` packing satisfies
`I+r_x<=62`: at most 62 of its words lie either in the reference design
or through the added point. In particular a point of replication twenty
allows at most 42 original reference circles. This is a rephrasing of
the same envelope and requires no additional finite computation.

The fixed-word source was verified at commit
`7ea6b95df212f5fb0a43cce175caad4faa9ad0ea`, graph
`bafkreifdhyio3qerrawomi2u6xb2rflfteshpbsi6jjlt5t6245ixj5vvi` (height 7902).
The four-gap and `s<=6` source is
`aa775990f13c916b2fb10da55c4ccfd1c1b6797d`, graph
`bafkreiakztl76jwczy5htefbf7ravrc6xpyswhblqamb5iosu7etuhq6re` (7849).
The trade source is `5adfdc1fcbe54fd701367c076305af5bd993b616`, graph
`bafkreia46uplm4yyhg6lrjq7yanu2hmfyuhrcdsimbctp3oymu247d3uum`.
The exact `t=5` classical input remains part of the computational trust
boundary; the earlier computations are imported, not rerun here.

## Reproduction and trust boundary

Use CPython 3.11+ and its standard library. From this directory, run one
command at a time:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B generate_five_gap_projection.py --normalize
python3 -B verify_five_gap_projection.py --compare --checkpoint-dir /tmp/a18-five-gap-check --resume
python3 -B audit_five_gap_projection.py
```

The first command reproduces production; the second suffices for a full
separate replay with production entry comparisons. `--case`, `--from-case`
and exclusive `--to-case` give explicit partial coverage. Normalization
is independently replayed even on a partial checker run. Resume accepts
only complete per-case summaries with matching source/input fingerprint,
case, gaps, record digest, projected graph digest and requested comparison
status. Checkpoints and logs belong in scratch storage, outside the
publication repository. A whole-domain checker summary must report
`complete_cases=789`, `coverage=all789cases`, `all_entrywise=true`,
`total_records=27400427`, and zero six-cliques.

All mathematical arithmetic is exact Python integers or finite sets. The
record cap is 40,000; phase guards remain 45 seconds. No incomplete phase,
timeout, solver status, or memory kill proves an exclusion. Full record
lists, adjacency corpora, verbose logs and checkpoints are omitted from
publication. The manifest is compact replay evidence, not a standalone
nonexistence certificate. Ordinary ownership, deletion, normalization,
record-compatibility, clique-injection and consequence arguments remain
unformalized. Both implementations are by the same researcher and share
the explicitly checked geometry and group generators.

Primary context is Aw--Chee--Ling (2003), *Six New Constant Weight Binary
Codes*, Theorem 1 and Appendix A,
[author PDF](https://ymchee66.github.io/home/PDF/6cwc.pdf), and Brouwer's
[maintained table](https://aeb.win.tue.nl/codes/Andw.html). The known
[69-word certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
is a baseline, not this result's construction claim.
