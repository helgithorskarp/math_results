# ACL69 completion bounds for every pair of saturated coordinates

Agent **six-code-3**, role **researcher**. This is an exact computer-assisted
core-completion theorem for a fixed published 69-word code. It supplies 66
conditional exclusions for searches for a code of size at least 70. The global
bounds on `A(18,6,5)` remain 69–72.

## Input and theorem

Identify a binary constant-weight `(18,6,5)` code with a family of 5-subsets of
`{0,...,17}` whose distinct members have intersection at most two. Let `C` be
the 69 rows in [acl69.txt](acl69.txt), obtained from
[Brouwer's public incumbent file](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69).
The leftmost character is coordinate **0**. The seed's SHA-256 is
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
The verifier checks the seed size, weights, distinctness and minimum distance.

Precisely these coordinates have degree 20 in `C`:

```
S = {0,1,2,5,7,8,9,10,12,14,15,16}.
```

**Theorem.** For every unordered pair `{p,q}` in `S`, put

```
K(p,q) = {B in C : p not in B and q not in B}.
```

Then `|K(p,q)|=34`, and the largest `(18,6,5)` code containing `K(p,q)` has
size **exactly 69**. The additional words may be any 5-subsets of the 18
coordinates; they need not belong to `C` or meet `{p,q}`.

The theorem is restricted to these fixed retained cores. It is not an upper
bound of 69 for arbitrary `(18,6,5)` codes. If `x_B` indicates selection of a
block, each pair gives the necessary search constraint

```
sum(x_B for B in K(p,q)) <= 33,   conditional on total code size >= 70.
```

## Mathematical reduction

We use the established theorem `A(17,6,4)=20` of
[A. E. Brouwer, report ZW 62/75, December 1975](https://ir.cwi.nl/pub/6883/6883D.pdf).
For any `(18,6,5)` code `F` and coordinate `q`, delete `q` from each word
containing it. This produces a `(17,6,4)` code, because the common coordinate
contributes nothing to Hamming distances. Thus **every coordinate has degree
at most 20 in `F`**. Saturation refers to the seed `C`, not an additional
hypothesis on `F`.

For each pair, enumerate the full residual universe

```
R = {B : |B|=5, B not in K(p,q), |B intersect D|<=2 for every D in K(p,q)}.
```

There are exactly `binomial(18,5)=8568` possible blocks. Every word of
`F \ K(p,q)` belongs to `R`. Define `L_q = {B in R : q not in B}`.

For **63 pairs**, the certificate proves that `L_q` contains no compatible
16-subset, with `p<q`. Hence any completion has at most 15 residual words
avoiding `q`, and at most 20 words containing `q`. Its size is at most
`34+15+20=69`. This argument allows residual words avoiding both coordinates;
five of these pairs have such words.

For exactly three pairs, the one-side bound has an exception:

```
{0,5}, {7,15}, {12,14}.
```

For each, the exhaustive certificate instead establishes:

1. No residual word avoids both coordinates.
2. `L_q` has exactly one compatible 16-subset, and so does `L_p`.
3. These two unique subsets contain a conflicting pair of words.

If a completion had at least 70 words, it would have at least 36 residual
words. The degree bound at `q` would force at least 16 residual words in
`L_q`; the degree bound at `p` would force at least 16 in `L_p`. They would
contain the two unique 16-subsets and their conflicting words, a
contradiction. Explicit cross-conflicts checked in `expected.json` are:

| Coordinates | Word in `L_q` | Word in `L_p` | Intersection size |
|---|---|---|---|
| `{0,5}` | `{0,3,4,8,9}` | `{3,4,5,8,9}` | 4 |
| `{7,15}` | `{1,3,5,7,10}` | `{1,3,5,10,15}` | 4 |
| `{12,14}` | `{1,2,7,8,12}` | `{1,2,7,8,14}` | 4 |

In every case the original code `C` is a size-69 completion, proving equality.

## Exhaustive certificate and independent check

For a side universe ordered by the increasing integer `sum(2**p for p in B)`,
the certificate tree classifies **all** compatible 16-subsets. At each node,
`Q` is the already selected compatible family and `P` consists of the
remaining candidates compatible with `Q`.

- A node `{"v":v,"i":...,"o":...}` partitions the possibilities according
  to whether vertex `v` is selected. Inclusion adds `v` to `Q` and restricts
  `P` to its compatible neighbors; exclusion removes `v` from `P`.
- A leaf `{"c":[...]}` partitions `P` into fewer than `16-|Q|` conflict
  cliques. Each positive integer encodes one class as a bitset of side
  indices. Distinct words in a class intersect in at least three points,
  so at most one can be selected. No 16-subset can extend `Q` there.
- A leaf `{"w":[...]}` identifies the sorted indices of `Q` when `|Q|=16`.

The branches are exhaustive, every cover includes every active vertex
exactly once, and witness leaves occur only when 16 words are selected.
Induction on the finite tree proves completeness of the classification.
Stopping at a witness leaf loses no 16-subset: any 16-subset containing
16 already selected words equals those words.

`generate.py` proposes trees using triple-owner blocker masks and greedy
conflict-clique partitions. `verify.py` imports no generator. It independently
enumerates all 8568 blocks using Python sets and direct intersections with
each retained core, checks every branch and every cover, and checks the
coupled obstructions. It does not trust search counts, solver statuses,
limits or the generator's residual enumeration. There is no symmetry
quotient and no floating-point proof arithmetic.

The external theorem `A(17,6,4)=20`, the elementary reduction above, Python's
integer/set semantics and the verifier are the trust boundary. Brouwer's
theorem and the reduction have not been formalized in a proof assistant.
The generator has resource limits; a limit aborts generation as **INCOMPLETE**
and supplies no exclusion.

## Reproduction

Python standard library only. Verified with CPython **3.11.2** and
**3.12.14**. Run from the repository root:

```sh
python3 coding_theory/a18_6_5_saturated_pairs/verify.py \
  --expect coding_theory/a18_6_5_saturated_pairs/expected.json
python3 coding_theory/a18_6_5_saturated_pairs/generate.py \
  --check coding_theory/a18_6_5_saturated_pairs/certificates.json
python3 coding_theory/a18_6_5_saturated_pairs/audit.py
```

Expected summary: **66** pairs, all cores size **34**; **63** one-side bounds
and **3** coupled bounds; **3315** tree nodes, **1686** cover leaves and
**6** witness leaves. The verifier checks **21631** residual-word occurrences,
**3720** side-word occurrences and **39794** within-class pairs. Each of
the exceptional pairs has 16 cross-conflicts. `audit.py` requires rejection
of nine incomplete or mathematically invalid certificate mutations.

`certificates.json` is 233933 bytes with SHA-256
`8f3290a40c14ece9ca7cf5454419f105387a99ca4d7935ac9db72a45c4574ba1`.
On this worker, the 3.11 checker took 2.70 seconds and maximum child RSS
24156 KiB. Generation took about 0.17 seconds. Each run uses one process
and one thread; no solver or package installation is needed.

## Literature and relation to earlier work

The size-69 construction is historical:
[Aw, Chee and Ling, *Six New Constant Weight Binary Codes* (2003), Theorem 1
and Appendix A](https://ymchee66.github.io/home/PDF/6cwc.pdf).
[Brouwer's current table](https://aeb.win.tue.nl/codes/Andw.html), checked
2026-09-30, lists 69–72 for this parameter. Reproducing the seed is validation,
not a new construction. The new content here is the exact retained-core
completion theorem and the exhaustive side classifications; no priority
claim is made beyond the sources searched.

The earlier
[35-coordinate-core theorem](../a18_6_5_coordinate_cores/README.md) covers
all singleton supports and all pairs containing coordinate 17. This
package covers a different complete cohort of 66 pairs. It uses neither
the earlier certificate nor another researcher's completion classification
as a mathematical dependency.
