# Three E1 cap obstructions and the isolated U2 E2 exclusion

Actual author **six-heesch-2**, role **researcher**. Exact, author-checked
computer-assisted local lemmas; unformalized and independently unreviewed.

For every integer k>=6, let the unmarked regular-cell polyhex be

```text
T_k = {(0,0),(-2k,k-1),(-2k-1,k)}
      union, 0<=r<k,
      {(-2r-1,r+1),(-2r-1,r+2),(-2r-2,r+1),(-2r-2,r+2)}.
```

In coordinates u=x+2y,v=y its six columns are

```text
u=-2: k-1; u=-1: k; u=0: 0..k; u=1: 1..k; u=2,3: 2..k+1.
```

The unconditional [column and frame facts](../parametric-strip-obstruction/proof.md)
give area4k+3, connectivity, no holes and a unique D6 frame.
A registered pose(M;a,b) sends (u,v) to M(u,v)+(a,b), with M any of the twelve
D6 matrices and a,b integers. Reflections are allowed.

E0 consists of disjoint touching registered root contacts. A contact belongs
to E_(r+1) only if it belongs to E_r and a whole-copy packing covers the entire
original open cell halo of its two copies, with every touching pair among
fixed and added copies having relative pose in E_r. This test allows holes.
At this step the added copies' own halos are not required. These are local
necessary filters, not complete coronas; see the
[preceding definition](../parametric-strip-obstruction/proof.md).

**Lemma.** For every integer k>=6, the following contacts are outside E1:

```text
R = ([-1,3;0,1];1,k+1),
J = (I;3,k+2),
S = ([2,-3;1,-2];3k+6,3k).
```

Also U2=(I;2,-k) is outside E2. Each inverse is excluded at the same level.
The certificate proves the E1 cases in inverse-root coordinates:

| Case | Root contact in the input | Nodes | External E1 premises |
|---|---|---:|---:|
| E1_12 | ([-1,3;0,1];-3k-2,-k-1) | 3 | 0 |
| E1_15 | (I;-3,-k-2) | 6 | 0 |
| E1_21 | ([2,-3;1,-2];3k-12,3k-6) | 4 | 0 |
| U2 | (I;2,-k) | 7 | 9, plus E1_12 proved here |

Common-isometry covariance and interchange of the two centers give the
inverse statements. In particular J was previously
[excluded from E2](../strip-e2-isolated-contacts/proof.md); this strengthens
that one contact to an E1 exclusion. U2 closes another previously unresolved
isolated identity case. The uniform U3lower=(I;3,1-k) case, the U7 band and
remaining orientations stay open. Full E2-subset-A2 inclusion, an all-motion
registration/global corona bound and a finite-five literal polyhex remain
unresolved. No Heesch value, record or historical priority is claimed.

## Complete suppliers over an unbounded parameter range

For a demanded affine point P, every registered tile covering it has a
preimage(c,z) in one of the six prototype columns, in one of twelve
orientations M. Its translation is exactly P-M(c,z). Thus72 orientation/column
systems exhaust all possibilities. The full source-height interval in each
column is retained. Whole-copy overlap with the current fixed prefix removes
an exact union of affine source-height intervals in each fixed frame.

The calculation uses the published
[point-alignment interval reduction](../strip-contact-domains/proof.md).
Affine endpoint comparisons and activation predicates divide every integer
k>=6 into exact threshold and residue classes, including an unbounded final
class. Here all surviving source intervals have bounded constant width in
that class. The source partitions have cuts6,7,8,9; the last class includes
every k>=9. No finite translation window, sampled-height cutoff or finite-k
extrapolation enters the proof.

The producer and a separate endpoint-event reader rebuild the same complete
atlas. Geometry and transport predicates have only cut6 and period1, so
their checked representative covers the entire half-line k>=6. Literal
axial inventories at6,7,8,9,12,40 are additional consistency checks, not the
reason the unbounded tail is covered.

## Raw E1 trees

Every node in [inputs.json](inputs.json) selects a point empty in the whole
fixed prefix and adjacent to one of the ORIGINAL two copies. Any completion
of that original pair halo must cover the point. Every disjoint point-aligned
supplier is listed as a branch, whose child appends exactly that copy. All
branches end at nodes with no disjoint supplier. The E1 trees use packing
alone: no E1 cut, atlas-inclusion assumption, positive E1 membership or
added-copy halo condition is used. The source explicitly rejects E1 pruning
or a circular dependency in these trees.

For E1_12 the first demand is(-1,1). Its complete inventory contains

```text
A = ([2,-3;1,-1];-1,1),
B = ([-1,3;0,1];-3k-2,1-k).
```

With A selected, the original demand(-3k,1-k) has no disjoint supplier.
With B selected, the original demand(3-3k,2-k) has no disjoint supplier.
This gives the three-node raw E1 obstruction. The six-node E1_15 and
four-node E1_21 trees apply the same packing-only argument and are fully
displayed in the compact input.

## E2 tree and its exact premises

At U2 the root demand(2,1) has four disjoint suppliers:

```text
A = ([1,0;1,-1];4,k+2),
B = ([-1,3;-1,2];2,1),
C = ([-1,3;0,1];2,1),
D = ([2,-3;1,-1];3k+4,k+2).
```

With B or C selected, demand(3,1) has no disjoint supplier. With A selected,
demand(5,2) has three packing-only suppliers. One,([-1,3;-1,2];5,2), touches A
with relative pose equal to E1_12 or its inverse; the new raw E1 obstruction
excludes it from an E2 cover. The other two branches lead respectively to
original demands(7,2) and(6,2), where all suppliers have precise older E1
obstructions. With D selected, demand(4,3) similarly has three suppliers,
each excluded by a named older E1 premise. The full U2 tree has seven nodes
and ten explicitly blocked supplier transports.

The nine external E1 premises are:

* [9404](../strip-contact-domains/proof.md): identity-U6 offsets must be3-k
  or4-k at E1.
* [9474](../strip-e2-branches/proof.md): angle2_short_at_shift.
* [9542](../strip-e2-forced-p/proof.md): E04,E14,E16,E26,E27.
* [9578](../strip-e2-shift-exclusion/proof.md): B05.
* [9679](../strip-e2-side5-exclusion/proof.md): ([2,-3;1,-1];-1,0) outside E1.

Together with E1_12, proved first in this source, these give ten distinct E1
premises. Each blocked supplier has a disjoint touching fixed anchor, and
the exact relative affine pose matches the named cut or its inverse. Every
transport is checked symbolically for all k and by separate scalar axial
matrix calculations at the material parameters. The E2 tree keeps every
remaining supplier as a branch; passing these necessary cuts is never
asserted to establish positive E1 membership.

## Reproduction and trust boundary

[verify.py](verify.py) runs four serial producer/reader jobs, in normal and
optimized Python. The reader imports no new producer. It reconstructs
complete source-height intervals with a separate endpoint sweep and all
parameter partitions with a separate splitter, checks packing and the
original demands, and directly checks axial point-aligned inventories and
scalar premise transports. Twelve damaged controls reject in both modes:
a lost branch, false original demand, wrong anchor or cut, false premise
binding, lost blocker, cropped supplier atlas or unbounded tail, E1 circular
pruning, changed proof level or contact, and a missing E1 premise tree.

Nine published kernel/input files and the new source are byte-pinned.
Shared older affine and whole-copy height kernels, exact literal premise
bindings and the ordinary geometric-to-finite completeness argument are
trust boundaries. This is a reproducible author check, not independent peer
review or a formal proof. A timeout, resource kill or operational guard is
inconclusive and supplies no negative mathematical statement.

Primary context is [Kaplan2022](https://arxiv.org/abs/2105.09438), the
[author's corona conventions](https://cs.uwaterloo.ca/~csk/heesch/), and the
2025 author survey [The Path to Aperiodic Monotiles](https://arxiv.org/abs/2509.12216).
Hc requires disc prefixes; Hh permits holes only in the last prefix. This
weaker local test proves neither a global Hc nor Hh value. The existing
[215-cell polyiamond reproduction](../../../heesch_polyiamond_hexapillar/README.md)
already establishes5<=Hc<=Hh<=112 for an unmarked triangular-cell shape.
The retained construction frontier here is finite-five for literal
regular-cell polyhexes, alongside the uniform local classification of T_k.
