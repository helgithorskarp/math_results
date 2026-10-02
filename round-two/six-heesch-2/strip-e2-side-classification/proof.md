# The surviving identity-side contact of the polyhex strips

Actual author: **six-heesch-2**, role **researcher**. This is an author-checked
exact computer-assisted lemma with an ordinary coordinate reduction. It is
unformalized and independently unreviewed.

Use axial integer coordinates with neighbours
`(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)`, and set `(u,v)=(x+2y,y)`.
For integer `k>=6`, let

```
T_k = {(0,0),(-2k,k-1),(-2k-1,k)}
      union {(-2r-1,r+1),(-2r-1,r+2),
             (-2r-2,r+1),(-2r-2,r+2): 0<=r<k}.
```

This is the literal `4k+3`-cell strip of the earlier
[column lemma](../parametric-strip-obstruction/STRIP_COLUMN_LEMMA.md).
The prototype is connected and hole-free. A pose `(M;U,V)` acts in UV
coordinates by `p -> M p+(U,V)`, with `M` a conjugated D6 matrix.
The construction permits reflections. All copies below are registered whole
copies in this hexagonal grid.

For a finite set of cells `F`, its open halo is all adjacent cells outside F.
Let `E0` consist of registered disjoint touching pairs. Inductively, a pair
is in `E_(r+1)` if it is in `E_r` and the **entire original pair halo** has a
packing cover by further whole copies such that every touching pair among
the fixed and added copies belongs to `E_r`. Local holes are allowed. This
is the local domain used in the earlier
[parametric obstruction](../parametric-strip-obstruction/proof.md).
The added copies' own halos are not extra demands at this step.

**Lemma.** For every `k>=6`, the pair with fixed poses

```
I = ((1,0,0,1);0,0),   h = ((1,0,0,1);6,3-k)
```

belongs to E2. Consequently, for every integer b,

```
((1,0,0,1);6,b) belongs to E2  if and only if  b=3-k.
```

The reverse implication is the new construction. The classification's
forward implication uses the published
[E1 notch restriction](../strip-contact-domains/README.md) and
[E2 exclusion of b=4-k](../strip-e2-shift-exclusion/proof.md).
No unproved inclusion `E2 subset A2` is used. This lemma gives no Heesch
number, plane-tiling conclusion, unrestricted-motion classification or
globally coherent corona construction.

## The eight-copy halo cover

Add the following eight poses, in this order. Number I and h as copies0 and1,
and these copies2 through9.

| Copy | UV matrix | U | V |
|---|---|---:|---:|
| 2 | `(-1,0,-1,1)` | 7 | 4 |
| 3 | `(-1,0,0,-1)` | 11 | k+6 |
| 4 | `(1,0,1,-1)` | 10 | 5 |
| 5 | `(-1,0,-1,1)` | 1 | -k |
| 6 | `(1,0,1,-1)` | -4 | k-2 |
| 7 | `(-1,0,0,-1)` | 5 | 2 |
| 8 | `(-1,3,0,1)` | -3k+2 | 2 |
| 9 | `(1,-3,0,-1)` | 0 | k+1 |

The ten copies pack, and copies2 through9 cover every cell of the original
I/h halo. The whole-halo verification below proves these statements over
the infinite parameter tail. Every touching pair is one of the following19:

```
01,02,05,06,08,09,12,13,14,15,17,23,28,34,47,56,57,69,89.
```

Here, for example, `69` means the pair of copies6 and9. Given two copy poses
g and f, express their relative pose as `g^-1 f`, and identify it with its
inverse by taking the smaller symbolic tuple. The19 pairs have exactly the
following11 types. Literal E1 covers for the ten constant-count cases are
in [inputs.json](inputs.json); the array case is described next.

| Case | UV matrix | U | V | Added copies in E1 cover |
|---|---|---:|---:|---:|
| 01 | `(-2,3,-1,1)` | -3k+1 | 2 | 8 |
| 02 | `(-2,3,-1,1)` | 5 | 3 | n+7 if k=2n; n+9 if k=2n+1 |
| 03 | `(-1,0,-1,1)` | -5 | -3 | 8 |
| 04 | `(-1,0,-1,1)` | 1 | -k | 7 |
| 05 | `(-1,0,-1,1)` | 7 | 3 | 7 |
| 06 | `(-1,0,0,-1)` | -1 | k-1 | 6 |
| 07 | `(-1,0,0,-1)` | 5 | 2k+3 | 7 |
| 08 | `(-1,3,0,1)` | -3k-4 | -2 | 7 |
| 09 | `(1,-3,0,-1)` | 0 | k+1 | 7 |
| 10 | `(1,0,0,1)` | -6 | k-3 | 8 |
| 11 | `(1,0,1,-1)` | -4 | k-2 | 6 |

Each cover packs around its two fixed centers and covers their **complete**
halo. This proves E1 directly because every touching contact in a registered
packing is in E0. There is no need to extend those added copies or restrict
their contacts further. In particular, case10 uses the eight-copy pattern
transported by `h^-1` as an E0 halo cover. This proves the fixed I/h pair is
already in E1 without assuming the E2 conclusion; there is no circularity.
Cases and their inverse poses have the same membership by congruence and
interchanging the fixed centers.

## The growing E1 cover for the angled contact

In case02 fix I and `((-2,3,-1,1);5,3)`. Write `k=2n+r`, with `n>=3` and
`r in {0,1}`. Add the array of half-turn copies

```
((-1,0,0,-1);12+6j, k+6+2j),   0<=j<=n-2+r.
```

Add these six common cap poses:

| UV matrix | U | V |
|---|---:|---:|
| `(-2,3,-1,1)` | -3k+4 | 3 |
| `(-1,0,-1,1)` | 7 | 4 |
| `(-1,3,-1,2)` | -3k | -2k-1 |
| `(1,-3,0,-1)` | -3 | k-1 |
| `(1,-3,0,-1)` | 3k+3 | k+1 |
| `(1,0,1,-1)` | -4 | k-2 |

For even k, add two more caps:

| UV matrix | U | V |
|---|---:|---:|
| `(-1,0,-1,1)` | 3k+8 | 4 |
| `(2,-3,1,-1)` | 6k+5 | 2k+4 |

For odd k, add these three instead:

| UV matrix | U | V |
|---|---:|---:|
| `(-1,0,-1,1)` | 3k+7 | k+5 |
| `(1,0,1,-1)` | 3k+8 | 2k+4 |
| `(2,-3,1,-2)` | 6k+6 | 3k+2 |

Array copies are mutually disjoint: their complete u-extents are
`12+6j+[-3,2]`, which are disjoint for distinct j. The interval verification
checks packing of all caps and fixed centers, every array/cap and array/fixed
interaction, and complete coverage of the original fixed-pair halo. There
are finitely many copies for each k: `n+7` or `n+9` added copies. Their mutual
contacts only need E0 at this E1 step.

## Whole-halo verification, including the infinite tail

The literal prototype has the following six vertical UV segments:

```
u=-2, v=k-1; u=-1, v=k;
u=0,  0<=v<=k;   u=1, 1<=v<=k;
u=2,  2<=v<=k+1; u=3, 2<=v<=k+1.
```

Their decomposition follows directly by grouping the literal strip cells.
To cover the open halo of a union of fixed copies, it suffices to cover all
six segments of every fixed copy after each of the six unit-neighbour
translations, including the zero translation. The fixed copies themselves
are included in the covering union. Because the added copies avoid the fixed
ones, any cell in the open halo is covered by an added copy. This checks all
84 integer line segments for a fixed pair; it does not replace the halo by
a few selected cells or impose new auxiliary-halo obligations.

In the frame of a target line `u=c`, a supplier's source column z obeys

```
c = alpha*z + beta*s + U,
t = gamma*z + delta*s + V,   lo_z<=s<=hi_z.
```

For `beta=0`, it supplies an affine vertical interval whenever its column
alignment holds. For `beta=+/-3`, it supplies at most one height; divisibility
and the source-height bounds are required. Represent integer heights by
half-open intervals and scale endpoints by3. The union covers each entire
target segment exactly when these intervals have no gap. Packing uses the
same exact column-intersection formulas, separately from the coverage test.

For the repeated array, a target point `(u(t),v(t))` belongs to source
column z of exactly the following possible index and source height:

```
j = (u(t)+z-12)/6,
s = k+6+2j-v(t).
```

Require integral j, `0<=j<=n-2+r` and the literal source-height bounds.
On a cap or halo line the t coefficients are0 or+/-3 in u. Splitting t into
its two parity classes makes every index and source-height condition either
an affine interval bound or an affine condition on n. The code checks every
division used is exact in its n coefficient. All lower and upper bounds are
retained, so intersections are computed by their maximum and minimum. The
same reduction on each physical cap/fixed segment proves it contains no
array point. Thus the array is checked without enumerating its unbounded
index range or assuming that finite samples extrapolate.

For each line, partition the parameter axis at every change of an activation
predicate and every ordering change of any endpoint. Linear inequalities
have one integer cut; equalities have an isolated integer point; congruences
have their stated residue classes. All predicates, empty intervals and
endpoint orders are constant in each such class, including its infinite
tail. A representative therefore determines the exact interval-union result
throughout that class. Both engines find only the class `k>=6` for all ten
constant-count covers and the outer contact inventory, and only `n>=3` in
each of the two array classes. Coverage in those classes, together with
packing, proves all11 E1 statements. The19-contact inventory then proves
the eight-copy cover is an E1-contact cover, hence `h in E2`.

## A separate axial replay

[axial_reader.py](axial_reader.py) does not import the producer's geometric
functions. It writes each prototype piece as `(c,0)+t*(-2,1)` in axial
coordinates and computes intersections using determinants. Parallel rays
give a translated integer interval; nonparallel D6 rays have determinant
`+/-3`, giving a single candidate with independently checked integrality and
source bounds. It uses a clipped endpoint-event sweep rather than the
producer's interval merge.

For the repeated array, its source-column points are

```
(-4n-2r-z, 2n+r+6) + j*(2,2) + s*(2,-1).
```

The two direction vectors have determinant-6. The reader independently
solves this2x2 system for j and s on a target axial line, checks divisibility
after its two height-residue substitutions, and obtains the integer index
and source-height bounds. It separately checks array/cap packing, all
168 parity halo traces, and both array parity classes.

The UV and axial engines derive matching19-contact/11-type inventories.
Normal and optimized Python reproduce identical evidence per engine. Seven
damaged-witness controls per engine reject a missing outer copy, a duplicate
copy, a missing E1 contact type, a missing even or odd array cap, a changed
declared array bound and a changed fixed-target binding. A separate unit-edge
material audit checks the full11 E1 covers and outer packing at
`k=6,7,8,9,12,40`; this is an implementation check, not the all-k proof.

## The shifted-side classification and limits

For U=6, the second tile's u-extents start at4 while the root ends at3, so
the pair never overlaps. Only its two heel cells at u=4 and5 can touch the
root's columns2 and3. Their possible neighbour heights give exactly
`3-k<=b<=3` as the raw touching range. The prior nine-supplier notch
restriction leaves only `b=3-k` and `b=4-k` in E1 and therefore in E2.
The prior shifted-contact exclusion removes `b=4-k` from E2 for every k>=6.
The new cover proves the remaining endpoint is actually in E2, yielding the
stated classification and, by inversion, its U=-6 counterpart.

Only this shifted-side family is classified. The earlier conditional bound
still needs a complete proof of `E2 subset A2`; this result does not provide
that inclusion. Local E1/E2 witnesses need not glue into global coronas.
The finite-five unmarked-polyform target remains open in this work.

The primary context is
[Kaplan's paper](https://arxiv.org/abs/2105.09438) and
[author census](https://cs.uwaterloo.ca/~csk/heesch/), which distinguish Hc
from Hh. No record or historical-priority claim is made here. The numerical
T5 result is not a premise; its [exact unit-edge module](../strip-t5/exact.py)
is reused only in bounded material audits. Shared literal inputs and the
six-segment model, ordinary unformalized reductions, Python integer arithmetic
and byte-pinned dependencies remain the trust boundary. Separate author
replays are not independent peer review.
