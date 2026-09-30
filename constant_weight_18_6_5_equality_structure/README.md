# Equality structure for A(18,6,5)

Researcher: **six-code-1**, 2026-09-30.

A binary length-18, weight-5 code of minimum distance at least six is
equivalently a family of five-element subsets with intersections of size
at most two. The maintained table still gives **69–72**.

[SUPPORT15.md](SUPPORT15.md) proves a necessary restriction on the equality case:
in any 72-word code, at least **fifteen** points have three or more neighbors
in the support of the deficits `t[x,y] = 5 - d[x,y]`, where `d[x,y]` counts
blocks on a pair. If a pair occurs in no block, its endpoints form the
only support-degree-one pair and the other sixteen points have support
degree at least three. Entire support components of degree two are
impossible. [SUPPORT12.md](SUPPORT12.md) establishes an intermediate
twelve-point restriction and its local carrier; [SUPPORT14.md](SUPPORT14.md)
excludes twelve and thirteen. The final strengthening excludes fourteen,
using actual forced blocks and the established nonexistence of a resolvable
triple group divisible design of type `2^6`. The global upper bound remains 72.
[PROOF.md](PROOF.md) supplies the incidence facts, the earlier nine-point
restriction, and the local catalog.

The same incidence analysis reduces each saturated point's abstract
triple-leave graph to one of **48** types. The new design obstruction filters
this to a **47-type necessary carrier** for actual saturated points. The
remaining types still require quadruple decomposability and global compatibility.
The compact catalog records
the positive deficit partition and high-degree core. This carrier uses
only necessary degree conditions; quadruple decomposability and global
compatibility remain additional obligations.

[AFFINE_SPLIT.md](AFFINE_SPLIT.md) proves that a degree-two point's twenty
shortened quadruples are obtained by splitting a point of an affine plane
of order four. This applies at any replication-twenty point, including in
codes smaller than 72. No uniqueness classification of affine planes is used.

## Reproduce

Python 3.11.2, standard library only; exact integer arithmetic, one
process, no solver or numerical-library dependency:

```sh
python3 constant_weight_18_6_5_equality_structure/reproduce.py
python3 constant_weight_18_6_5_equality_structure/check_support12.py
python3 constant_weight_18_6_5_equality_structure/check_support14.py
python3 constant_weight_18_6_5_equality_structure/check_support15.py
```

Run from the repository root. The script regenerates the catalog in
memory, compares it entry by entry with `local_types.json`, checks its
orbit counts by Burnside averaging, exactly verifies the published
69-word certificate in `baseline69.txt`, and checks the local leaves at
its twelve points of replication twenty. It also rejects malformed and
invalid code fixtures. It exits unsuccessfully on any disagreement with
`expected.json`. Expected principal outputs are:

* 69 distinct valid words; minimum distance 6; 690 covered triples;
  126 leave triples.
* Saturated baseline points: 12.
* Abstract local types: 48, with counts `1,1,1,3,3,13,26` over the seven
  descending partitions of five; 901 admissible labeled core masks.

The second script independently checks path leave-indicator constraints
for lengths 3–18, the omission arithmetic, and the finite six-root carrier
by exact matching. It compares its compact output with
`support12_expected.json`. The third script checks the additional odd
matching, isolated-point capacity and two-root pair restrictions against
`support14_expected.json`. The fourth script checks the complete four-point
weighted carrier and 91 forced-block conflicts, identifies the one excluded
catalog entry, and checks all thirty nonempty proper point splits of an explicit
order-four affine plane. Its report is `support15_expected.json`. It reproduces
the known twenty-word lower certificate for `A(17,6,4)` but does not re-prove the
external resolvable-design nonexistence theorem. These scripts produce validation reports;
none enumerates 72-word codes. The structural lemmas are proved in
prose independently of these computations.

## Baseline provenance and scope

`baseline69.txt` was downloaded from the maintained code certificate:
<https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69>.
Its SHA-256 is
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
This reproduces the 2003 Aw–Chee–Ling lower bound, not a new construction.
The proof explicitly depends on Brouwer's established
`A(17,6,4) = 20`. The fifteen-point strengthening additionally imports
Rees–Stinson (1987), Lemma 3.5, excluding a resolvable triple design of type `2^6`;
see [SUPPORT15.md](SUPPORT15.md) for the primary citation and complete parameter
bridge. See [PROOF.md](PROOF.md) for primary sources and trust
boundaries. No external solver output, unpublished enumeration or large
certificate is needed.
