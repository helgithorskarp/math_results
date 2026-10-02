# Uniform pair exclusions leave two E2 cover branches

Actual author: **six-heesch-2**, role **researcher**. Status: ordinary
computer-assisted author proof, unformalized and independently unreviewed.
All statements below quantify over **every integer k >= 6**.

## Literal shape, coordinates, and domains

In axial hexagon coordinates `(x,y)`, let

```
T_k = {(0,0), (-2k,k-1), (-2k-1,k)}
      union over r=0,...,k-1 of
      {(-2r-1,r+1), (-2r-1,r+2), (-2r-2,r+1), (-2r-2,r+2)}.
```

Use `u=x+2y, v=y`. The occupied columns, with inclusive height intervals, are

| u | v |
|---|---|
| -2 | k-1 |
| -1 | k |
| 0 | 0,...,k |
| 1 | 1,...,k |
| 2 | 2,...,k+1 |
| 3 | 2,...,k+1 |

A pose `(M;a,b)` means `(u,v) -> M(u,v)+(a,b)`. All matrices used here belong
to the twelve rigid symmetries of the hexagon grid in these coordinates.
An affine integer `[A,B]` in the source means `Ak+B`, not a sampled value.

The halo of a union of cells consists of unoccupied edge-neighbor cells.
`E0` consists of disjoint registered copies touching the root copy. Recursively,
`E_(r+1)` consists of members of `E_r` whose fixed-pair halo admits a complete
packing by whole registered copies, with every contact among the fixed and
added copies having its relative pose in `E_r`. Local covers may leave holes.
These are the registered necessary domains of the
[previous contact-domain lemma](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-heesch-2/strip-contact-domains/proof.md),
source commit `f4e3acc9c69137eb3d05bed98374dbfa0116eac0`, graph9404.

The shape is connected, hole-free, of area `4k+3`, with a unique D6 frame.
Only those unconditional geometric facts and the implementation are imported
from [the earlier conditional lemma](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-heesch-2/parametric-strip-obstruction/proof.md),
source `41bf6af8891df8c07f5a71db1c81a40b52c7b4ca`, graph9321.
Its proposed uniform E2 inclusion is **not** a premise.

## Six uniform E1 exclusions

Each following pose is a disjoint registered contact and is outside `E1(T_k)`:

| Source name | Matrix M | Translation (a,b) | Certificate |
|---|---|---|---|
| side4 | `(1,0,0,1)` | `(4,4)` | 2 cells,5 suppliers,2-node DAG |
| angle1_long | `(1,-3,1,-2)` | `(3k+5,2k+5)` | 3 cap branches,4-node tree |
| angle2_const | `(-2,3,-1,2)` | `(4,4)` | 3 cap branches,4-node tree |
| angle1_const | `(-1,3,-1,2)` | `(4,4)` | 2 cap branches,3-node tree |
| angle2_short_at_shift | `(-2,3,-1,1)` | `(-2,k+1)` | 3 cells,14 suppliers,3-node DAG |
| reflection_at_shift | `(-1,3,0,1)` | `(-2,k)` | 3 cells,12 suppliers,3-node DAG |

This excludes the literal poses in the table. In particular, the last two
rows do not by themselves exclude their different root-relative translations
`(4,5)` and `(4,4)`.

For `side4`, demand the pair-halo cells `(1,k+1)` and `(3,k+2)`.
Exactly five affine suppliers are disjoint from the fixed pair:

```
(-2,3,-1,2; -3k, 1-k)
(-1,0,-1,1; 1, k+1)
(-1,0,0,-1; 0, 2k+1)
(2,-3,1,-1; 1, k+1)
(2,-3,1,-1; 3, k+2).
```

The first four can fill the first cell. The last alone fills the second cell,
and overlaps all four other suppliers. Therefore no packing covers both.
For each of the last two table rows, demand `(5,k+2)`, `(4,k+1)`, and
`(5,k+1)`. Complete point alignment gives14 and12 suppliers, respectively.
The saved three-node packing rejection exhausts all suppliers at its chosen
uncovered cells. All three finite matrices are constant on `k>=6`; their
critical partition is `[6,infinity)`, with period1.

The three middle rows have growing supplier families at some halo cells.
Those families are not cut off. Instead first fill a cap cell having a
complete finite supplier list, and reject **every** choice using a different
original halo demand whose supplier list becomes empty:

| Fixed pose | Cap cell | Chosen cap supplier | Unfillable cell |
|---|---|---|---|
| angle1_long | `(4,6)` | `(-2,3,-1,2;4,6)` | `(6,7)` |
| angle1_long | `(4,6)` | `(1,-3,1,-2;3k+5,2k+7)` | `(3k-2,2k+2)` |
| angle1_long | `(4,6)` | `(I;4,6)` | `(6,7)` |
| angle2_const | `(5,6)` | `(-2,3,-1,2;5,6)` | `(3k+4,2k+5)` |
| angle2_const | `(5,6)` | `(I;5,6)` | `(4,k+1)` |
| angle2_const | `(5,6)` | `(1,0,1,-1;6,k+7)` | `(5,k+2)` |
| angle1_const | `(5,5)` | `(I;5,5)` | `(4,k+1)` |
| angle1_const | `(5,5)` | `(1,0,1,-1;6,k+6)` | `(5,k+2)` |

For each fixed pose, the cap suppliers listed in its rows are **all** possible
cap suppliers, across all parameters. Every unfillable cell belongs to the
original fixed-pair halo and is outside the chosen cap copy. No registered
copy containing that cell is disjoint from the root, fixed neighbor, and cap
copy. Thus every cap choice contradicts a complete pair-halo packing. This
proves the exclusion without an assumption that the unrestricted original
supplier family is finite.

The exact height-event cut sets, including leaves, end at8 for angle1_long,
14 for angle2_const, and9 for angle1_const; the respective unbounded tails
are checked explicitly. Equality endpoints are retained. These cuts are
derived from affine inequalities, not fitted from k6/k7 data.

## Why the supplier and packing reductions are exhaustive

For a demanded point `p`, a copy containing it has some matrix M, source
column c, and integer source height t from that column's interval. Its
translation is necessarily `p-M(c,t)`. This exhausts the twelve orientations
and all source cells, including copies not touching the original root.

To test overlap with a fixed copy f, transform p and M by `f^-1` and compare
each source column to each target column. Column equality either fixes a
height difference or makes two height intervals overlap. The result is a
union of forbidden integer intervals in t, with affine endpoints and affine
activation conditions. Sweep all endpoints and subtract the forbidden
intervals from the legal source-height interval. This is an exact integer
description, with no floating-point decisions.

Partition k at every change in endpoint order and every change in activation,
including singleton equality classes and residues where needed. The full
first interval and final unbounded interval are included. A finite atlas is
returned only if every surviving source-height interval has bounded width;
an unbounded family is reported as incomplete, never rejected mathematically.
For the cap roots and selected leaves above, complete finite atlases do
exist, and every leaf atlas is empty on every parameter class.

For a finite collar, the producer encodes coverage, packing conflicts, and
availability of every supplier. Its universal relaxation ORs coverage and
availability across parameter classes and ANDs conflicts. This only admits
more covers. A rejected relaxation therefore rules out all original classes.
The separate reader reconstructs the height intervals by difference events,
reconstructs the critical partition, and checks every supplier branch of
each negative DAG. The supplier-tree reader instead checks the entire cap
atlas and reconstructs the empty atlas at every leaf. It introduces no new
halo demand after selecting a cap.

Separate materialized axial geometry enumerates all point-aligned copies at
every supplier-class representative and checks the complete inventories.
It also checks the finite matrices at their representatives. These material
checks are audits of the symbolic reduction, not the argument for the
unbounded tails. The reusable unit-edge code comes from the
[T5 publication](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-heesch-2/strip-t5/exact.py),
source `a5052d63996131ca4eaceb22c1293a6fd4f9a056`, graph9051; its T5-specific
Heesch values are not premises here.

## Necessary two-branch condition for the original E2 cover

Let `g=(I;6,4-k)` and `R=(-I;5,3)`. The published9404 lemma proves that every
E2 halo cover of the fixed pair `(I,g)` must contain R. In that cover the
unfilled halo cell `p=(4,4)` must still receive a copy disjoint from I,g,R.
Exact source-point alignment yields **exactly eight** affine suppliers:

| Supplier pose | Source column,height mapping to p | Disposition |
|---|---|---|
| `(-2,3,-1,1;4,5)` | `(3,2)` | g-relative angle2_short_at_shift |
| `(-2,3,-1,2;4,4)` | `(0,0)` | root-relative angle2_const |
| `(-1,0,-1,1;7,5)` | `(3,2)` | survivor S |
| `(-1,3,-1,2;4,4)` | `(0,0)` | root-relative angle1_const |
| `(-1,3,0,1;4,4)` | `(0,0)` | g-relative reflection_at_shift |
| `(1,-3,1,-2;3k+5,2k+5)` | `(-1,k)` | root-relative angle1_long |
| `(I;4,4)` | `(0,0)` | root-relative side4 |
| `(2,-3,1,-2;3k+6,2k+5)` | `(-1,k)` | survivor P |

The complete height partition has one class `[6,infinity)`, period1. The
reader checks the eight-pose set, not just its cardinality.

The root contains `(3,4)` and g contains `(5,4)` for every k>=6. Hence every
supplier containing p touches both the root and g. In an E2 cover these
contacts must lie in E1. The four root-relative exclusions in the table
apply directly. Applying `g^-1` to the first and fifth suppliers gives,
respectively, translations `(-2,k+1)` and `(-2,k)` with the unchanged matrices;
these are exactly the other two proved E1 exclusions. Both translations and
the required contacts are checked symbolically.

Consequently **every E2 halo cover of `(I,g)` contains S or P**. This is a
necessary disjunction; it does not assert either cover exists or either
survivor lies in E2. Both remaining branches still admit the small relaxed
collar covers tried privately. No uniform exclusion of g, full E2-domain
inclusion, or global Heesch upper bound follows here.

## Reproduction, dependencies, and current frontier

Run `python3 round-two/six-heesch-2/strip-e2-branches/verify.py`. The expected
summary has6 uniform exclusions,8-to2 supplier reduction,18 rejected damaged
controls per reader mode, and matching normal/optimized mathematical hashes.
`expected.json` records the exact hashes. Seven adjacent published code files
are hash pinned; all input points and poses are in the compact `inputs.json`.
Generated records and logs are ignored. Runtime guards remain43s work,45s
signal,47s subprocess,100000 search nodes, with one serial job and all numeric
thread settings1. A timeout, pause, nonnegative collar, or growing-family
refusal is inconclusive.

The shared affine/height kernels remain a trust boundary. Separate readers
and optimized-mode agreement do not constitute independent peer review or
proof-assistant formalization. The elementary geometric and local-domain
bridges above are part of the ordinary author proof.

Primary context, refreshed2026-10-02: Kaplan's
[Heesch Numbers of Unmarked Polyforms](https://arxiv.org/abs/2105.09438), the
[primary census and Hc/Hh conventions](https://cs.uwaterloo.ca/~csk/heesch/),
and [The Path to Aperiodic Monotiles](https://arxiv.org/abs/2509.12216).
Hc forbids holes at every corona prefix; Hh permits holes only in the final
corona. The local registered domains here allow holes and are not themselves
corona constructions or a registration theorem for arbitrary-motion patches.
The distinct [registration boundary](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-heesch-2/proof.md),
source `cf3b672f2bf53a076c057b44a6f1a087ef028fcd`, graph8585, remains separate.
No historical priority is claimed. A rigorously finite unmarked polyhex with
five coronas under all motions, and the general finite-seven planar target,
remain open in this campaign. The next mathematical task is to resolve the
two surviving branches, retaining complete growing-family descriptions.
