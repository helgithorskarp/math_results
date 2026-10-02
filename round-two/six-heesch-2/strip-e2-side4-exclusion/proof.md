# No registered identity-offset-four contact survives E2

Actual author **six-heesch-2**, role **researcher**. This is an exact,
author-checked computer-assisted local lemma. Independent review and
formalization remain pending. No record or historical priority is asserted.

## Shape, filters and statement

For each integer k>=6, in axial unit-hex coordinates define the unmarked
polyhex

```text
T_k = {(0,0),(-2k,k-1),(-2k-1,k)}
      union, 0<=r<k,
      {(-2r-1,r+1),(-2r-1,r+2),(-2r-2,r+1),(-2r-2,r+2)}.
```

In coordinates u=x+2y,v=y its columns are

```text
u=-2: k-1; u=-1: k; u=0: 0..k; u=1: 1..k; u=2,3: 2..k+1.
```

Its area is4k+3. The literal model, connectivity, hole absence and unique
D6 frame are established in the
[column/frame source](../parametric-strip-obstruction/proof.md).
A registered pose(M;a,b) sends(u,v) to M(u,v)+(a,b), with M a D6 matrix
and a,b integers; reflections are allowed.

E0 consists of disjoint touching registered root contacts. Recursively,
g belongs to E_(r+1) only if it belongs to E_r and the fixed pair(I,g)
has a packing covering its full original open cell halo, with every
touching pair among fixed and added copies having relative pose in E_r.
Local holes are allowed. Added copies' own halos need not be covered at
this step. These local necessary filters are not complete coronas.
See the [preceding definitions](../parametric-strip-obstruction/proof.md).

**Lemma.** For every integer k>=6 and integer b, (I;4,b) is outside E2.
Swapping centers gives the corresponding identity-offset-minus-four
statement. In addition, (I;4,3) is outside E1.

This does not prove the full E2-subset-A2 hypothesis, a Heesch number,
an unconditional global corona upper, plane tiling or a finite-five example.
The all-motion registration and corona-depth implications remain separate.

## Complete raw contacts

The complete column-pair reduction from
[9404](../strip-contact-domains/proof.md) gives overlap intervals
[2-k,2) and[3-k,3). The six closed-halo intervals have union[2-k,k+3).
After subtracting overlap their union is exactly

```text
3 <= b <= k+2.
```

All affine endpoint orders have only cut6. This is an exact unbounded
integer parameter reduction, not interpolation from sampled contacts.

## A moving copy supplies a fixed occupied block

Let g_b=(I;4,b). For every3<=b<=k+2, g_b contains the five cells

```text
K0 = {(4,k+2),(4,k+3),(5,k+3),(6,k+4),(7,k+4)}.
```

For every5<=b<=k+2, it also contains the thirteen cells

```text
K1 = {(4,k+j): 2<=j<=5}
     union {(5,k+j): 3<=j<=5}
     union {(6,k+j),(7,k+j): 4<=j<=6}.
```

These are occupied-cell constraints, not extra copies or extra halo
obligations. Each membership follows from a displayed prototype column:
the source height is k+j-b. Its two column inequalities hold on the
entire stated wedge. The checker minimizes each Ak+Bb+C exactly at
b equal to its lower bound or k+2, then checks the k>=6 tail slope.

Write the following affine poses, all in UV coordinates:

| Name | Matrix M | Translation(a,b) |
|---|---|---|
| A | [[-1,3],[0,1]] | (2-3k,2) |
| B | [[-1,0],[-1,1]] | (3,k+2) |
| C | [[1,-3],[1,-2]] | (3k+2,3k+2) |
| Z | [[2,-3],[1,-1]] | (3,k+2) |

The demand P0=(3,k+2) is empty in(I,g_b) for3<=b<=k+2 and adjacent
to the root cell(2,k+1). Every registered copy covering P0 and avoiding
both the root and K0 is **one of A,B,C,Z**, for every k>=6.

Here is the complete finite reduction behind this four-supplier claim.
Choose any of12 orientations M, any of six prototype columns c, and
a source height z in that column. The pose covering P0 is uniquely
P0-M(c,z). Root overlap is an exact union of forbidden z intervals from
the preceding published kernel. For a blocked cell Q, put
(du,dv)=M^-1(Q-P0). Its preimage is(c+du,z+dv), so a prototype column
d contributes the forbidden interval[L_d-dv,H_d-dv+1) exactly when
c+du=d. All endpoints and active predicates are retained. Their complete
parameter partition has only cut6, and every surviving interval has
constant bounded width. All72 orientation/source-column cases reduce
to the four displayed affine poses. There is no source-height cutoff
or truncation of a growing interval.

## Exact packing restrictions at the first demand

B overlaps g_b for the entire raw domain: its source cell(0,b-2)
maps to g_b's terminal cell(3,k+b). Its source height lies in0..k.
C overlaps g_b at(3,k+3) for b=3. For b>=4 it contains(4,k+4),
which is in g_b's column4. A overlaps g_b for b=3 or4 at terminal
(2,k+b-1).

The exact overlap intervals also prove the complete supplier domain:

| Offset b | Suppliers covering P0, disjoint from I and g_b |
|---|---|
| 3 | none |
| 4 | Z only |
| 5..k+2 | A and Z |

Thus (I;4,3) is already outside E1. Published
[9542](../strip-e2-forced-p/proof.md), literal case E02, proves Z outside
E1. Since Z touches the root, no E2 cover can use it. This excludes b=4
and forces A for every remaining5<=b<=k+2. No claim that A belongs
to E1 is needed: that membership would follow from the putative E2 cover.

## The second original demand

Put P1=(3,k+4). For5<=b<=k+2 it is absent from I,g_b,A and adjacent
to g_b's cell(4,k+4), hence remains an **original pair-halo** demand.
It is not introduced by asking to surround A.

Avoiding the fixed copies I,A and the common occupied block K1 gives
exactly four possible suppliers for P1. They are A',B',C',Z', obtained
from A,B,C,Z respectively by adding(0,2) to the translation. The same
complete72-case source-height reduction again has only cut6 and four
constant affine suppliers for every k>=6.

Every one is impossible in an E2 pair cover:

* B' contains g_b's terminal(3,k+b): its source cell is(0,b-4), whose
  height is in0..k for5<=b<=k+2.
* C' overlaps that terminal at(3,k+5) for b=5. For b>=6, C' contains
  (4,k+6), which belongs to g_b's column4.
* The relative pose from A to A' is(I;6,2). Published9404 allows an
  identity-offset-six E1 contact only at vertical offsets3-k or4-k.
  Neither is2 for k>=6, so this touching contact is outside E1.
* The relative pose from A to Z' is([[1,0],[1,-1]];5,k+2). Its inverse
  is([[1,0],[1,-1]];-5,k-3), the E1 exclusion B05 in
  [9578](../strip-e2-shift-exclusion/proof.md). These copies touch.

Consequently P1 has no admissible supplier, proving the E2 exclusion
throughout5<=b<=k+2. Together with the raw-domain and first-demand
reductions this proves the lemma for every integer b.

## Reproduction and trust boundary

See [README.md](README.md) and run [verify.py](verify.py). The producer
[prove.py](prove.py) checks both cap inventories, the full b overlap
intervals, common-block/demand wedge inequalities and the precise cited
E1 contacts. Cap partitions have cut6; the moving-copy collision intervals
have cuts6,7, with the last class covering every k>=7.

The search-free [reader](check.py) imports neither the new producer nor
its point-block kernel. It reconstructs blocked-cell predicates in axial
coordinates, uses a separate endpoint event sweep, and independently
rebuilds the moving-copy b intervals by intersecting source columns.
It checks every source case, parameter class, exact demand/common-block
certificate and intended exclusion. Direct literal axial cell enumeration
at k=6,7,8,9,12,40 checks both cap atlases and every raw b at those
parameters. These material checks validate implementation; complete exact
endpoint partitions and wedge arguments establish the unbounded range.
Three damaged wedge controls and seven damaged reader certificates reject
in normal and optimized Python. Guards and incomplete jobs are inconclusive.

Shared older affine and whole-copy source-height kernels, the ordinary
point-alignment completeness argument and the cited E1 lemmas remain
disclosed trust boundaries. Checks are by the same author, not independent
peer review. [expected.json](expected.json) pins the source and prior inputs.
No finite D1/D2 inventory, conditional full E2 inclusion or private peer
result is used as an E1/E2 premise.

Primary context is [Kaplan's manuscript](https://arxiv.org/abs/2105.09438)
and [author census/conventions](https://cs.uwaterloo.ca/~csk/heesch/),
reopened2026-10-02. The numerical T5 Heesch value is not a premise;
its existing exact module is an imported geometry dependency of the
prior reader. The [U5 exclusion](../strip-e2-side5-exclusion/proof.md)
is complementary, not required here. The full domain inclusion and
finite-five target remain unresolved.
