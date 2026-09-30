# A(18,6,5): an exact ACL69 completion and trade barrier

Agent **six-code-2**, role **researcher**, 2026-09-30.

A code here is a family of 5-subsets of `{1,...,18}` with every pair
intersecting in at most two points. Equivalently, it has binary length 18,
weight 5 and minimum distance at least 6.

Let `C` be the 69-word Aw--Chee--Ling code in `acl69.txt`, in the row order
of [Brouwer's plain certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69).
The certificate equals the columns of Appendix A in
[Aw, Chee and Ling, Six New Constant Weight Binary Codes (2003)](https://ymchee66.github.io/home/PDF/6cwc.pdf),
after transposition. Let `K` be the 57-word subcode obtained by deleting
the **one-based** source rows

```
6, 9, 14, 17, 22, 27, 30, 32, 37, 54, 55, 58.
```

## Claims and scope

1. Every admissible code containing this fixed labeled `K` has at most
   69 words. Exactly **84** such codes have 69 words.
2. These 84 codes form the entire component of `C` under a move replacing
   one word while preserving size and admissibility. The component has
   **192** undirected edges. Its common intersection is exactly `K`.
3. No improving exchange from `C` deletes at most **five** words.
   Consequently any 70-word code differs from this labeled `C` in at
   least six deleted words. This also holds after any common permutation
   of the 18 coordinates.
4. More strongly, every admissible code retaining **at least 56 of the
   57 words in `K`** has at most 69 words. Thus any 70-word construction
   must omit at least two words of `K`.
5. The bound extends to retaining **at least 55 of the 57 words in `K`**.
   All `binomial(57,2)=1596` two-core-deletion cases have directly
   checked 14-clique covers, proving `55+14=69`. Hence a 70-word code
   must omit at least **three** words of `K`.

These are restricted completion and local exchange results. They do not
improve the global bounds `69 <= A(18,6,5) <= 72` recorded in
[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html)
when checked on 2026-09-30. The known 69-word construction is attributed
to Aw--Chee--Ling; reproducing it is validation, not a new lower bound.
The new scoped calculation identifies a completely classified family
that a construction search must leave to obtain 70 words. No priority
claim is made beyond the primary sources and graph context searched.

## Proof mechanism

All `binomial(18,5)=8568` blocks are enumerated. Exactly 26 blocks outside
`K` can coexist with it. They are listed as five **one-based** point labels
in `certificate.json`. That file partitions their conflict graph into
12 cliques, using **one-based** candidate indices. Each code can use at
most one block from each clique, giving the upper bound `57+12=69`.
The original `C` supplies equality.

The fourth claim is certified for all 57 choices of a deleted core word.
For 49 choices no further outsider becomes compatible; the residual
candidate count is 27 including the deleted word. For eight choices
exactly two new outsiders appear, giving 29 candidates. Each new outsider
fits into a listed existing conflict clique; the deleted word is put in
a thirteenth singleton clique. The resulting 13-clique cover proves
`56+13=69` in every case. The eight exceptional lists and clique placements
are in `one_core_deletion_extensions` in `certificate.json`.

For two core deletions, every residual candidate is either one of the 26
original candidates, a deleted core word, or an outsider whose nonempty
core-blocker set is contained in the deleted pair. Exhausting all 8568
blocks finds 16 outsiders with one core blocker and 166 with two. There
are between 28 and 36 residual candidates per deletion pair. A small
backtracking generator extends the 12 base cliques with the two deleted
words as singleton cliques, inserting each new outsider into a conflict
clique. A separate direct check verifies each returned cover's exhaustive
vertex coverage and every within-clique intersection. The generator's
success is verified for all 1596 pairs. Its search optimality and search
completeness are unnecessary for the resulting upper certificate.
The original `C` still contains every 55-word anchor, proving equality.

The cliques have sizes ten times 2 and twice 3. Enumerating their
`2^10 * 3^2 = 9216` choices and rejecting intersecting pairs gives exactly
84 size-12 completions. For each resulting code the verifier tests every
five-subset against its covered triples, finds all single-word exchanges,
and checks that their destinations belong to the same 84-code list.
The resulting graph is connected from `C`, so closure and connectivity
prove the component statement.

For the five-word barrier, associate to each outsider `B` its set `S(B)`
of conflicting words in `C`. A compatible outsider family `T` requires
deleting at least `union_{B in T} S(B)`. If its size exceeds that union's
size it gives an improving exchange. Any improvement deleting at most
five words contains such a subfamily with at most six additions.
The verifier exhausts all increasing compatible outsider tuples whose
blocker union has size at most five, and finds none satisfying this strict
inequality. There are 1487 eligible outsiders and the visited tuple counts
by number of additions 1 through 5 are

```
1487, 10142, 15756, 7802, 15.
```

There are no eligible tuples of length six. Increasing candidate indices
eliminate repetition without a symmetry assumption. Every outsider in an
eligible tuple has at most five blockers, justifying the candidate filter.
Words removed and then re-added can be canceled before this reduction.

## Reproduction and evidence

Requires Python 3.11 or later with its standard library; no solver or
floating-point computation is used. Run from the repository root:

```
python3 constant_weight_a18_6_5_acl69_trade_barrier/verify.py --radius5
```

The command verifies all five claims. Omitting `--radius5` verifies the
completion classification, the entire single-word component, and the
one- and two-core-deletion extension bounds.
On Python 3.11.2 the full check takes a few seconds on one CPU and uses
well under 100 MiB. Timing/RSS fields are measurements, not proof data.
`expected.json` records the compact deterministic result fields.

The raw seed SHA-256 is
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
The component hash, from sorted codes of sorted integer masks serialized
as compact JSON with no newline, is
`4e0bc333779c5bab37f00d7af4e84a2fded1e21f4dd902a54c4052f95340b8c5`.
Point 1 is bit 0 in this serialization.

The candidate list is checked both by direct pairwise intersections with
`K` and by the disjointness of covered triple sets. The clique upper
certificate can be checked without trusting the maximum-set enumerator.
The 84-family classification and local exchange barrier rely on the
documented exhaustive enumeration and the ordinary Python/runtime trust
boundary; no proof-assistant formalization is claimed. No large corpus,
opaque imported solver proof, or private input is required.

## Prior work and next construction frontier

The 2003 paper obtained `C` by a length-reduction heuristic.
[Rosin (2026)](https://arxiv.org/abs/2603.00174) and
[Echols (2026)](https://arxiv.org/abs/2608.13906) describe modern bit-swap
and seeded tabu methods; their located improvements do not change this
parameter's maintained bound. A bounded exploratory tabu run here found
no larger code and is not evidence of nonexistence.

The complementary work by **six-code-3**, role **researcher**, proves
[coordinate-core completion obstructions](https://github.com/helgithorskarp/math_results/tree/main/coding_theory/a18_6_5_coordinate_cores)
for all singleton supports and all two-coordinate supports containing the
last coordinate. The present dispersed 57-word core contains none of
those 35 retained coordinate cores, so that cohort does not already imply
the present fixed-core upper bound. Both methods use conflict-clique
certificates, with different retained families. The single-word component
and five-word trade classification here are additional distinct results.

The precise next constructive frontier is to alter at least three of the
57 core blocks and at least six seed blocks, then reconstruct compatible
blocks from the resulting triple leave. The present result explains why
single-word neutral movement and all five-deletion improving trades from
this incumbent cannot reach 70. It places no bound on other components,
larger trades, or arbitrary 18-point packings.
