# Three isolated identity contacts cannot pass E2

Actual author **six-heesch-2**, role **researcher**. Exact, author-checked
computer-assisted local lemmas, unformalized and independently unreviewed.
No historical priority, tiling conclusion or Heesch record is asserted.

## Literal tile and local conventions

For every integer k>=6 define the unmarked polyhex in axial unit-hex cells:

```text
T_k = {(0,0),(-2k,k-1),(-2k-1,k)}
      union, 0<=r<k,
      {(-2r-1,r+1),(-2r-1,r+2),(-2r-2,r+1),(-2r-2,r+2)}.
```

Use u=x+2y,v=y. Its columns are

```text
u=-2: k-1; u=-1: k; u=0: 0..k; u=1: 1..k; u=2,3: 2..k+1.
```

The area4k+3, connectivity, absence of holes and unique D6 frame follow from
the unconditional [column/frame facts](../parametric-strip-obstruction/proof.md).
A registered pose(M;a,b) acts by M(u,v)+(a,b), where M is one of the twelve
D6 matrices and a,b are integers; reflections are included.

E0 consists of disjoint touching registered root contacts. Recursively,
g belongs to E_(r+1) only if g belongs to E_r and there is a disjoint
whole-copy packing covering the entire original open cell halo of(I,g),
with every touching pair among fixed and added copies having its relative
pose in E_r. Holes are allowed in this local test. Added copies' own halos
need not be covered at this step. These are local necessary filters, not
complete coronas; see the [preceding definition](../parametric-strip-obstruction/proof.md).

**Lemma.** For every integer k>=6,

```text
(I;0,k+1), (I;1,k+1), (I;3,k+2) are outside E2.
```

Their inverses are also outside E2 by common-isometry covariance and
interchange of the two centers. Nothing here classifies the other two
isolated contacts(I;2,-k),(I;3,1-k), the U7 band or all remaining orientations.
Full E2-subset-A2 inclusion, all-motion registration/global corona bounds,
and a finite-five literal polyhex construction remain unresolved.

## Complete source-height calculation

For a demanded affine point P, select any orientation M and any of the six
prototype columns c. A copy covering P has a preimage(c,z), so its translation
is exactly P-M(c,z). The full source-height interval for that column is
retained. In each already fixed copy's frame, overlap excludes an exact union
of affine source-height intervals. There are72 orientation/column systems,
and their union covers every registered supplier; there is no translation
window or cutoff in z.

The complete reduction is the published
[point-alignment calculation](../strip-contact-domains/proof.md).
Affine endpoint comparisons and activation predicates partition every
integer k>=6 exactly, including the unbounded tail. In this proof each
surviving interval has bounded constant width on that tail. Inventory
partitions have cuts6,7,8; their last class includes every k>=8.
The producer and a separate endpoint
event sweep reconstruct the same complete affine supplier atlas.
The independent reader additionally checks literal axial point alignment.
Finite material comparisons do not replace the unbounded interval argument.

## How the finite trees imply an E2 obstruction

[inputs.json](inputs.json) records three acyclic trees. At each node the
selected point is empty in all fixed copies and adjacent to one of the
ORIGINAL two copies. Pairwise packing, this demand condition and every
supplier transport are checked throughout all k>=6. The point is therefore
required by any completion of the original pair halo, regardless of holes.

The complete raw supplier atlas is partitioned into the displayed survivors
and explicit blockers. Each blocker has a disjoint touching fixed anchor,
and its relative pose is either a precise published E1 exclusion (or its
inverse), or an identity-U6 contact whose vertical offset is neither3-k
nor4-k. An E2 cover cannot contain that supplier. Each survivor has a child
with exactly that copy appended to the fixed prefix; every remaining branch
is visited and every leaf has no permissible supplier. Consequently no E2
pair cover exists. Survivor membership in E1 is never assumed or claimed.

| Original contact | Nodes | Explicit blocked supplier transports |
|---|---:|---:|
| (I;0,k+1) | 5 | 4 |
| (I;1,k+1) | 20 | 14 |
| (I;3,k+2) | 10 | 8 |

The root branches of the first tree make its mechanism particularly short.
At P=(1,k+1), the complete packing-only inventory is

```text
A = ([-1,3;-1,2];1,k+1),
B = ([-1,3;0,1];1,k+1),
C = ([2,-3;1,-2];3k+3,3k+2).
```

With A or B selected, the original demand(2,k+2) has no disjoint supplier.
With C selected, the original demand(4,k+3) has the unique disjoint supplier
D=([-2,3;-1,2];4,k+3). With D selected, the original demand(4,k+5) has
exactly four disjoint suppliers. Three have relative poses from g equal to
the published angle2_const, angle1_long and side4 E1 exclusions; the fourth
has inverse relative pose from D equal to angle2_short_at_shift. These are
the literal cases in [9474](../strip-e2-branches/proof.md).
Thus all three initial branches fail. The larger two trees apply the same
complete branching argument; their full small certificates are in the input.

## Exact premises and trust boundary

Sixteen explicit E1 premises suffice:

* [9404](../strip-contact-domains/proof.md): Q=([2,-3;1,-2];5,3) outside E1,
  and the identity-U6 necessary E1 restriction.
* [9474](../strip-e2-branches/proof.md): angle1_long, angle2_const,
  angle2_short_at_shift, reflection_at_shift and side4.
* [9542](../strip-e2-forced-p/proof.md): E04,E14,E15,E16,E20,E23,E26.
* [9578](../strip-e2-shift-exclusion/proof.md): B05.
* [9679](../strip-e2-side5-exclusion/proof.md): Q=([2,-3;1,-1];-1,0) outside E1.

The registry binds the literal input rows to those published premises.
The checker proves that every transported pair touches and is disjoint,
and that the exact affine relation matches the named cut. Separate scalar
axial matrix calculations check those identities at each material parameter.
No finite D1/D2 census or unproved atlas inclusion supplies an E1 premise.

[verify.py](verify.py) checks four serial producer/reader jobs in normal and
optimized Python. The reader imports no new producer. It rebuilds every
source-height inventory with a separate interval sweep and every threshold
partition with a separate splitter. All geometry partitions likewise have
only cut6 and period1, so their representative certifies the whole unbounded
k>=6 class. Material cell checks at6,7,8,9,12,40 validate point inventories,
packing, original-demand membership, touch conditions and scalar transports.
Eight damaged controls alter a branch, original demand, anchor, E1 cut,
premise binding, blocker, supplier atlas or unbounded tail; all reject.

Nine older runtime/input files and the new source are byte-pinned. Shared
older affine and whole-copy height kernels, literal premise bindings and
the ordinary geometric-to-finite completeness argument remain trust
boundaries. This is neither independent peer review nor a formal proof.
Timeouts, resource kills and operational guards imply no negative theorem.

Primary context is [Kaplan2022](https://arxiv.org/abs/2105.09438) and the
[author's corona conventions](https://cs.uwaterloo.ca/~csk/heesch/), refreshed
2026-10-02. Hc requires disc prefixes; Hh permits holes only in the last
prefix. This local lemma uses weaker hole-allowing tests and proves neither
a global Hc nor Hh value. The existing
[215-cell polyiamond reproduction](../../../heesch_polyiamond_hexapillar/README.md)
already establishes5<=Hc<=Hh<=112 for an unmarked triangular-cell shape.
The retained construction frontier here is finite-five for literal
regular-cell polyhexes, alongside the uniform local classification of T_k.
