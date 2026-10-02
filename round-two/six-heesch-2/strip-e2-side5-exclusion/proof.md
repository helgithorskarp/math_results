# No identity-U5 contact survives the registered E2 filter

Actual author: **six-heesch-2**, role **researcher**. An author-checked exact
computer-assisted local lemma, unformalized and independently unreviewed.
No historical priority or Heesch record is asserted.

## Literal family and conventions

For every integer k>=6, in axial unit-hex coordinates let

```text
T_k = {(0,0),(-2k,k-1),(-2k-1,k)}
      union, 0<=r<k,
      {(-2r-1,r+1),(-2r-1,r+2),(-2r-2,r+1),(-2r-2,r+2)}.
```

In coordinates u=x+2y,v=y its six columns are

```text
u=-2: v=k-1; u=-1: v=k;
u=0: 0..k; u=1: 1..k; u=2,3: 2..k+1.
```

The area is4k+3. Connectivity, absence of holes and unique D6 frame are
proved in the [column/frame source](../parametric-strip-obstruction/proof.md).
A registered pose(M;a,b) acts by M(u,v)+(a,b), where M is one of the twelve
D6 matrices and a,b are integers; reflections are allowed.

E0 consists of disjoint root contacts. Recursively, g belongs to E_(r+1)
when g belongs to E_r and the fixed pair(I,g) has a whole-copy packing
covering its entire original open cell halo, with every touching pair among
fixed and added copies having its relative pose in E_r. Local holes are
allowed. Covering additional copies' own halos is not required at this
step. These are necessary local tests, not complete admissible coronas.
See the [preceding definitions](../parametric-strip-obstruction/proof.md).
The all-motion registration and corona-depth bridges remain separate.

**Lemma.** For every integer k>=6 and every integer b,
the relative pose(I;5,b) is outside E2. The corresponding identity-U=-5
statement follows by swapping the centers and applying a common isometry.

Two supporting statements are also established: for3<=b<=k+1,
(I;5,b) is outside E1; and Q=([[2,-3],[1,-1]];-1,0) is outside E1.
No complete E2-subset-A2 assertion, global Heesch bound, plane-tiling
statement or finite-five construction follows here.

## The complete raw domain

Apply the exact column-pair translation reduction from the
[complete-contact source](../strip-contact-domains/proof.md).
For the identity matrix and U=5, the root-overlap interval is
[3-k,3), using half-open integer endpoints. The closed-halo intersection
regions are the four intervals

```text
[2-k,2), [3-k,3), [3-k,k+3), [4-k,4).
```

They come from all six source columns and all42 unmerged shifted halo
columns. Their union for every k>=6 is[2-k,k+3). Subtracting root overlap
gives exactly

```text
b=2-k, or 3<=b<=k+2.
```

The producer checks every affine endpoint comparison, with only the
critical cut6. Thus this is a complete integer translation domain for the
whole unbounded parameter range, not a fit to finite pose counts.

## An isolated cell eliminates the middle interval

Fix g=(I;5,b) with3<=b<=k+1. The unit cell P=(4,b) is absent from both
fixed copies. All six UV neighbors of P are already occupied:

| Copy | Occupied neighboring cells |
|---|---|
| I | (3,b), (2,b-1), (3,b-1) |
| g | (5,b), (6,b+1), (5,b+1) |

Membership follows directly from the displayed six columns and the
inequalities k>=6 and3<=b<=k+1. P is an original halo demand. A connected
registered polyhex of area greater than one has an internal cell neighbor
at every prototype cell. Therefore a copy covering P must also occupy at
least one of its six neighbors, contradicting disjointness.

This proves the E1 exclusion even though local holes are allowed: the
original pair halo must still be covered. The code independently checks
the exact minima of the membership inequalities on the full integer wedge,
by reducing each Ak+Bb+C>=0 to its minimum edge b=3 or b=k+1 and the
unbounded k tail. This is an ordinary combinatorial argument with exact
integer arithmetic, not a finite parameter extrapolation.

Only g_-=(I;5,2-k) and g_+=(I;5,k+2) remain possible in E2.

## A two-branch E1 obstruction for Q

For the fixed pair(I,Q), the original halo demand(-2,1) has exactly two
registered suppliers disjoint from the fixed copies:

```text
A = ([[2,-3],[1,-1]];-2,1),
B = (-I;-3,k+1).
```

After selecting A, the original demand(-3k-1,1-k) has no disjoint supplier.
After selecting B, the original demand(-2,2) has no disjoint supplier.
All three demands belong to the original(I,Q) halo for every k>=6.
The complete source-height calculations include every orientation, source
column and source cell height; none is discarded through an empirical
translation cutoff. The two branches exhaust every cover. Hence Q is
outside E1. The existing separate cap-tree reader reconstructs these
inventories with another interval event sweep and checks original-demand
membership and material axial geometry.

## The upper endpoint

For(I,g_+), P_+=(4,k+2) is an original unfilled halo cell. Its complete
supplier inventory has the unique pose

```text
Z = ([[2,-3],[1,-1]];4,k+2).
```

The relative pose of Z from g_+ is Q, and these copies touch. An E2 cover
would require that contact to lie in E1, contrary to the preceding
obstruction. Thus g_+ is outside E2. Separate producer and event-sweep
source inventories agree over the entire k>=6 range.

## The lower endpoint: two forced copies

Fix(I,g_-). The original demand(2,1) has exactly two raw suppliers:

```text
R = (-I;2,1),
S = ([[2,-3],[1,-2]];2,1).
```

With R selected, the original demand(3,2-k) has no disjoint supplier.
Consequently every pair-halo cover uses S. With S selected, the original
demand(4,1) has the unique disjoint supplier

```text
D = (-I;4,1).
```

These three inventories have exactly2,0,1 raw suppliers and only critical
cut6. The force arguments use packing and original-demand coverage, not
an obligation to surround the new copies. Any putative E2 cover must
therefore contain the four-copy prefix(I,g_-,S,D).

## A complete ten-cell collar rejects that prefix at E2

Require these ten original pair-halo cells:

```text
(-1,0), (-2,-1), (-2,0), (-2,1), (-1,1),
(4,3), (4,4), (5,3), (6,3), (7,3-k).
```

Each is unoccupied by the forced prefix and adjacent to I or g_-. For
each cell, enumerate all12 orientations and all six source columns. A
copy containing that cell is determined by its source height. Overlap
with each fixed copy is an exact union of forbidden source-height
intervals. Active conditions, endpoints and their critical parameter
cuts are all retained, including unbounded tails. Every surviving
interval has bounded constant width on its unbounded parameter classes;
bounded exceptional classes are conservatively expanded through their
maximum width. A width guard raises an error, never truncates a family.
The union contains99 affine supplier poses and includes every possible
collar supplier for every integer k>=6.

In an E2 cover, every contact among fixed and added copies must be in E1.
Use the published unconditional E1 cuts from
[9404](../strip-contact-domains/proof.md),
[9474](../strip-e2-branches/proof.md),
[9542](../strip-e2-forced-p/proof.md), and
[9578](../strip-e2-shift-exclusion/proof.md), together with the new
isolated-cell and Q exclusions above. Their literal input rows are
byte-pinned. The computation uses no finite D1/D2 census as an E1 premise.
In particular no part of the unproved32-pose E2 inclusion is assumed.

For each supplier, build exact affine predicates for eligibility and
coverage; for each supplier pair, build packing or forbidden-E1-contact
clashes. Their complete threshold partition is6,7,8,9,10,11, with period1.
The last class represents every k>=11. Demand membership is checked
on every class. The separate reader rebuilds source inventories and
thresholds, then reconstructs each Boolean matrix; its axial footprint
and unit-edge calculations agree on every representative and the
supplementary parameter40. Those material tests validate implementation;
the exact threshold partition proves coverage of the unbounded range.

Take coverage and availability unions over the classes and clash
intersections. Every actual E2 collar cover induces a cover of this
conservative universal matrix. It has78 available poses. A rejection
DAG with20 distinct states excludes it (the search visited27 states).
At each state, a demanded cell is chosen and every available supplier
covering it has a certified child after removing covered demands and
clashing poses. Leaves have no supplier. The search-free reader checks
all branches, including the root; no SAT solver result is trusted.
Hence g_- is outside E2. Combined with the raw and middle-interval
reductions, this proves the lemma for every integer b.

## Reproduction, provenance and limits

Run the [README command](README.md); [verify.py](verify.py) runs six
serial proof/producer/reader jobs in normal and optimized Python.
[expected.json](expected.json) records source/dependency hashes and the
three stable mathematical hashes. The core rejects five damaged
certificates/inequalities; the collar reader rejects six damaged matrices
or DAGs. Guards and incomplete jobs are operational failures, not
mathematical negatives. Generated local evidence is ignored.

The trust boundary includes shared exact affine/source-height kernels,
ordinary unformalized completeness and connectivity arguments, and the
cited earlier E1 lemmas. The reader uses separate endpoint sweeps and
direct axial cell footprints, but all checks here are same-author.
Independent review remains pending.

Primary context is [Kaplan's manuscript](https://arxiv.org/abs/2105.09438)
and the [author census and conventions](https://cs.uwaterloo.ca/~csk/heesch/),
reopened2026-10-02. The [T5 module](../strip-t5/exact.py) supplies exact
unit-edge geometry; its numerical Heesch value is not a premise.
The [earlier U6 classification](../strip-e2-side-classification/proof.md)
is complementary, not required for this U5 exclusion. The broader
finite-five target and full domain inclusion remain unresolved.
