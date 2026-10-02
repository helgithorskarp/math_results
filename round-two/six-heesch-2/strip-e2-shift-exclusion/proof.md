# A shifted contact is absent from E2 for every strip length k >= 6

Actual author: **six-heesch-2**, role **researcher**. Exact computer-assisted
intermediate lemma; author checked, unformalized and independently unreviewed.
This is a registered local contact obstruction. No Heesch-number value or
finite-five construction is asserted.

## Literal object and contact convention

In axial hex-cell coordinates let

\[
T_k=\{(0,0),(-2k,k-1),(-2k-1,k)\}
\cup\bigcup_{r=0}^{k-1}
\{(-2r-1,r+1),(-2r-1,r+2),(-2r-2,r+1),(-2r-2,r+2)\}.
\]

Set `(u,v)=(x+2y,y)`. Its six columns are
`-2:{k-1}`, `-1:{k}`, `0:{0,...,k}`, `1:{1,...,k}` and
`2,3:{2,...,k+1}`. The literal area is `4k+3`. We use integer translations
and all twelve D6 orientations, including reflections. A pose `(M;U,V)`
maps a source UV cell `z` to `Mz+(U,V)`. Matrices below are row-major.

E0 consists of disjoint touching registered pairs. Recursively a pair in
E_r belongs to E_(r+1) only if its **entire fixed-pair halo** can be covered
by whole registered copies packing together with the pair, with **every
touching contact among all these copies in E_r**. Holes are allowed in
these local tests. Two demands alone form a relaxation of the whole halo;
their rejection is an obstruction, and their cover would not prove an
E2 cover. This definition is separate from finite necessary D1/D2 domains
or global corona depth.

## New claim and precise predecessors

For every integer `k>=6`, the disjoint touching contact

`g=(I;6,4-k)`

does **not** belong to E2. Its inverse is absent as well by transporting a
putative pair cover with an isometry and interchanging the two fixed copies.

The following published intermediate results are used with their exact scopes:

* [9404](../strip-contact-domains/proof.md) forces
  `R=(-I;5,3)` in any E2 cover of `(I,g)` and supplies the angle and
  shifted-side E1 exclusions used by `model.py`.
* [9474](../strip-e2-branches/proof.md) gives the complete alternative
  `S=(-1,0,-1,1;7,5)` or `P=(2,-3,1,-2;3k+6,2k+5)` after R.
* [9542](../strip-e2-forced-p/proof.md) eliminates the entire S branch for
  every `k>=6`. Thus any E2 cover of g must contain **P**.

The E1 exclusions in those two latter input tables are reusable pair
exclusions, as proved there. Eliminating the S **branch** is not treated as
an E1 exclusion for the isolated S pair. The conditional 32-pose E2
inclusion in [9321](../parametric-strip-obstruction/proof.md) remains unproved
and is not used. Only its unconditional literal columns, unique frame and
affine geometry code are dependencies. The separate axial audit module
from [9051](../strip-t5/exact.py) is used as code, not for its numerical T5 value.

## Six additional E1 obstructions

All six poses below are disjoint touching contacts for every `k>=6`.
Each is outside E1 by the complete whole-copy supplier computation in
`generate.py` and search-free replay in `check.py`. Literal demands and cap
trees are in `inputs.json`; no finite k sample is used as a parameter proof.

| Case | M | U | V | Complete obstruction |
|---|---|---|---|---|
| B01 | `(-2,3,-1,2)` | `-3k-4` | `-k-3` | `(-1,k-1)` has no supplier |
| B02 | `(1,-3,1,-2)` | `3k+5` | `2k+6` | Three caps at `(4,7)`; all branches empty; four nodes |
| B03 | `I` | `4` | `5` | Three original demands, twelve suppliers, three-node negative DAG |
| B04 | `(1,0,1,-1)` | `6` | `k+7` | `(5,k+2)` has no supplier |
| B05 | `(1,0,1,-1)` | `-5` | `k-3` | `(-1,k-1)` has no supplier |
| B06 | `(-2,3,-1,2)` | `4` | `5` | Three caps at `(5,7)`; all branches empty; four nodes |

B02 and B06 are complete supplier **trees**, not truncated height atlases.
After selecting each cap, its prescribed leaf demand stays in the original
two-copy halo and cannot be supplied. The reader checks all packings,
demands and branches. The largest cap-tree cut is 16, and its final
interval includes every integer `k>=16`. Three other cases have literally
empty complete atlases. The four finite collar certificates have six total
DAG nodes; the two cap trees have eight total nodes.

## The two original halo cells close the P branch

Fix the four copies `(I,g,R,P)`. Both `(4,6)` and `(5,6)` are unoccupied
cells in the **original (I,g) halo** for every `k>=6`. Complete packing-only
point alignments yield twelve and thirteen suppliers respectively, with
nineteen distinct poses in their union. No supplier is obtained by
interpolating a finite placement list.

Discard a supplier only if it overlaps a fixed copy or makes a touching
contact with a fixed copy that is outside E1 by one of the six new or
published exclusions. These are necessary conditions for an E2 cover.
The exact all-parameter eligibility leaves the following sets:

| Eligible supplier of `(4,6)` | M | U | V |
|---|---|---|---|
| L1 | `(-2,3,-1,2)` | `4` | `6` |
| L2 | `(-1,0,-1,1)` | `7` | `7` |
| L3 | `(-1,3,-1,2)` | `4` | `6` |
| L4 | `(1,-3,1,-2)` | `3k+5` | `2k+7` |
| L5 | `I` | `4` | `6` |
| L6 | `(2,-3,1,-2)` | `3k+6` | `2k+7` |

| Eligible supplier of `(5,6)` | M | U | V |
|---|---|---|---|
| W1 | `(-2,3,-1,2)` | `5` | `6` |
| W2 | `(-1,0,-1,1)` | `8` | `7` |
| W3 | `(1,-3,1,-2)` | `3k+6` | `2k+7` |
| W4 | `I` | `5` | `6` |

No eligible supplier covers both cells. **Every one of the 6 times 4
cross-pairs physically overlaps**, for all `k>=6`. Hence no packing can
cover both cells. No E1 cuts between the added suppliers are needed in
this last contradiction. The exact matrix has one parameter interval
`[6,infinity)`, with cut list `[6]`; a two-node exhaustive DAG replays the
same contradiction. L4 is retained as eligible; it is rejected only when coupled to an
eligible supplier of `(5,6)`. No isolated E1 exclusion for L4 is asserted.

A putative E2 cover of g must contain R and P by the predecessors. It must
also cover the two original halo cells. The contradiction therefore proves
`g not in E2` for every `k>=6`.

## Completeness, certificates and trust boundary

For a demand cell p, each registered supplier aligns p with a source cell
in one of six columns under one of twelve D6 frames: seventy-two exact
one-height systems. Exact source-height interval reductions and their
endpoint/residue partitions cover all activation cases, including the
unbounded tail. Every surviving bounded system is enumerated. A growing
family or any operational guard aborts without a negative claim.

For finite collars, union coverage/availability and intersection conflicts
across all parameter classes form a conservative relaxation. A negative
exhaustive supplier DAG for that matrix rules out every class. The main
two-cell matrix already has a single class. For the trees, all complete
root caps and all original-halo leaf demands are replayed explicitly.

The reader reconstructs source-height atlases with its separate endpoint
sweep, checks parameter partitions with its separate splitter, and
materializes actual axial cell sets at every representative. For the
main collar, actual axial pose inverse/composition, literal contact cuts,
point membership and physical overlap are checked entry by entry. It
replays the DAG without search and checks all 24 physical cross-clashes.
Seventeen altered-certificate controls must fail in each reader mode.

These are same-author checks with shared affine/height kernels and shared
literal definitions. They are not independent peer review or a formal
proof. Pins, exact inputs, deterministic mathematical hashes and ordinary
proof dependencies are explicit. No SAT-library soundness or floating-point
assumption is required. No global upper bound, non-tiling theorem for the
whole family, or finite Heesch number at least five follows from this lemma.

Primary problem context: [Kaplan's 2022 paper](https://arxiv.org/abs/2105.09438)
and [author census with Hc/Hh conventions](https://cs.uwaterloo.ca/~csk/heesch/),
refreshed 2026-10-02. No historical priority claim is made.
