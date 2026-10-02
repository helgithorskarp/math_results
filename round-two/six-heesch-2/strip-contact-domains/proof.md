# Complete contact intervals and a forced E2 half-turn

six-heesch-2, researcher. Author-checked exact computer-assisted lemmas and an
ordinary unformalized proof. Independent review is pending. No historical
priority or Heesch record is asserted.

## Scope and literal tile

For integer k>=6, in axial unit-hex coordinates put

```text
T_k = {(0,0),(-2k,k-1),(-2k-1,k)}
      union, for 0<=r<k,
      {(-2r-1,r+1),(-2r-1,r+2),(-2r-2,r+1),(-2r-2,r+2)}.
```

Use u=x+2y,v=y. Its columns are

```text
u=-2: v=k-1;  u=-1: v=k;
u=0: 0<=v<=k; u=1: 1<=v<=k;
u=2 and3: 2<=v<=k+1.
```

The area is4k+3. The [earlier column/frame proof](../parametric-strip-obstruction/proof.md)
shows connectivity, absence of holes and a unique D6 frame for k>=2.
A pose (M;a,b) acts on (u,v) by M(u,v)+(a,b). All copies here are registered
integer translations of the twelve D6 orientations, with reflections allowed.
Write M=(alpha,beta,gamma,delta) in row-major order. Four matrices have beta=0;
eight have beta=+/-3.

E0 consists of all disjoint root contacts. For r>=0, E_(r+1) consists of g in
E_r for which the fixed pair T_k,g(T_k) has a disjoint whole-copy halo cover
and every contact among fixed and added copies has its relative pose in E_r.
Holes are allowed in this local test. These are the registered local domains
of [the preceding conditional lemma](../parametric-strip-obstruction/proof.md).
The [all-motion registration/pair-depth bridge](../proof.md) is separate.
No new corona upper bound is claimed below.

## Statements

For every integer k>=6:

1. E0 has exactly 96k+184 poses. A complete disjoint description consists of
   522 affine integer rectangles in the coordinates specified below. Every
   rectangle with a varying side has a unit-width other side, so it is an
   integer interval family rather than a two-dimensional growing family.
2. The open-halo notch N=(-1,k-1) has exactly the nine suppliers in the table
   below, among all registered copies disjoint from T_k.
3. For the identity pose g_b=(I;6,b), raw contact holds exactly for
   3-k<=b<=3. If g_b belongs to E1, then b is3-k or4-k. Inverse contacts
   satisfy the corresponding restriction by isometry covariance.
4. The pose Q=([[2,-3],[1,-2]];5,3) is outside E1.
5. Every E2 halo cover for the fixed pair with g=(I;6,4-k) contains
   R=(-I;5,3), the half-turn about (5/2,3/2) in these coordinates.

The last statement is a necessary neighbor, not an exclusion of g from E2.
The full all-k E2 subset A2 hypothesis of the preceding conditional upper-three
lemma remains unproved. Finite-five regular-cell polyhex construction remains open.

## Complete raw-contact reduction

Let W be T_k together with its six cell-neighbor translates. Represent W by
the 42 unmerged shifted column intervals; overlap among them does not matter.
A translation is a raw contact exactly when its image intersects W and does
not intersect T_k. On the regular hexagonal lattice, boundary contact implies
an adjacent cell pair, so these cell tests also cover vertex contacts.

For a nonparallel matrix write beta=3s, s=+/-1. Every integer translation a
has a unique representation a=3t+r, r in{0,1,2}. Set z=b-delta*s*t.
For source column c with heights[l_c,h_c] and target column d with heights
[L_d,H_d], column intersection requires

```text
C = (d-alpha*c-r)/beta is an integer;
v = C-s*t;
l_c <= C-s*t <= h_c;
L_d <= gamma*c+delta*C+z <= H_d.
```

If C is not an integer, that column pair is empty. Otherwise these are exactly
an integer rectangle in(t,z). For s=1 its t range is[C-h_c,C-l_c]; for s=-1
the range is[l_c-C,h_c-C]. Its z range is
[L_d-gamma*c-delta*C,H_d-gamma*c-delta*C]. All endpoints are affine integers
in k. This argument has no truncated translation range or empirical premise.

For beta=0, a must equal d-alpha*c. The b range is
[L_d-gamma*c-max(delta*l_c,delta*h_c),
 H_d-gamma*c-min(delta*l_c,delta*h_c)]. This is an integer interval.

Take the union of these regions for W and subtract the union for T_k. All
regions have affine half-open boundaries. Comparisons of boundary positions
are linear predicates A*k+B>=0. Their integer critical cuts give a finite
exact parameter decomposition. In this raw-contact problem it has only the
cut6: the order is stable throughout[6,infinity), as the reader reconstructs.
Consequently each selected arrangement cell is valid for the whole range.

The reader reconstructs the selected cells using interval-count sweeps rather
than the producer's point coverage tests. It checks all 36 root column pairs,
all shifted halo columns, all orientations/residues/parallel translations,
and every selected rectangle. Exact interval-length products sum to the
polynomial184+96k, with zero quadratic coefficient. It additionally verifies
the unit-width assertion for each growing rectangle. Frame uniqueness makes
pose counts equal to geometric-copy counts.

Unit-edge enumeration in axial coordinates independently agrees at
k=6,7,8,9,12, giving760,856,952,1048,1336 contacts. Those checks validate
the implementation; the rectangle identity and stable endpoint order prove
the all-k result. No count is inferred by fitting a polynomial to samples.

## Exact notch suppliers

N is missing from T_k and is adjacent to column0. A copy covering N has a
unique preimage cell(c,v). For each matrix and each source column enumerate
all v in that column. Its translation must be

```text
a = -1-alpha*c-beta*v;
b = k-1-gamma*c-delta*v.
```

Root overlap excludes a union of source-height intervals. In the nonparallel
case, intersection with source column j and root column d has

```text
C = (d+1-alpha*(j-c))/beta;
w = v+C;
image height = k-1+gamma*(j-c)+delta*C.
```

Divisibility is constant. When the displayed image height belongs to the root
column, forbidden v lie in [l_j-C,h_j-C]. The parallel case is direct interval
overlap. The 72 matrix/source-column systems and their affine endpoints again
have only critical cut6. Their allowed height intervals are nine singletons,
yielding the following complete atlas J(k).

| Matrix M | Translation(a,b) |
|---|---|
| [[-2,3],[-1,2]] | (-3k-3,-k-2) |
| [[-1,0],[0,-1]] | (-3,2k-2) |
| [[-1,0],[0,-1]] | (-1,k-1) |
| [[-1,3],[-1,2]] | (-3k-2,-k-2) |
| [[1,-3],[0,-1]] | (-1,k-1) |
| [[1,-3],[1,-2]] | (-1,k-1) |
| [[1,0],[1,-1]] | (-4,k-2) |
| [[2,-3],[1,-2]] | (-1,k-1) |
| [[2,-3],[1,-1]] | (-1,k-2) |

The reader uses a separate forbidden-interval event sweep and critical-cut
calculation. Materialized point alignment in axial cells independently
reconstructs all nine suppliers at the stated comparison parameters.

## The side restriction

The raw rectangle calculation for(I;6,b) gives3-k<=b<=3. Its notch is
(5,k-1+b), which is outside the root. Every added copy covering it is g_b*h
for some h in J(k). Intersecting each of those nine copies with T_k gives
forbidden b intervals, with exact critical cut6. The union of surviving
integer b values is exactly{3-k,4-k}. Thus the necessary E1 restriction
eliminates k-1 of this family's k+1 raw contacts. It does not prove existence
of an E1 cover at either remaining value.

At b=4-k the only root-disjoint suppliers of this notch are
R=(-I;5,3) and Q=([[2,-3],[1,-2]];5,3).

## A complete finite collar excludes Q

For the fixed pair T_k,Q(T_k), require these six open-halo cells:

```text
(-3k+6,4-2k), (-3,-2), (-1,k-1), (-1,0), (4,3), (-2,-1).
```

To prove supplier completeness, use the same point alignment for an arbitrary
affine point P. For each source column c and height v the pose is
(M;P-M(c,v)). To test overlap with a fixed copy f(T_k), transform to the root:
use relative matrix f^-1*M and point f^-1(P). The source-height computation
above then gives all forbidden v intervals. Take their union for both fixed
copies. Affine comparisons and activation conditions are partitioned exactly.

In the unbounded parameter ranges every surviving height interval has bounded
constant length. A few bounded exceptional parameter classes have a varying
length; its maximum on that bounded class is used to include a conservative
finite list of affine poses. Unioning the pose lists across all parameter
classes therefore contains every possible supplier for every k>=6. Extra
poses outside their source class are harmless and are filtered or relaxed.
The resulting union has 46 affine poses. No private finite closure census is
an input to this completeness argument.

For those poses, the reader reconstructs coverage, overlap with fixed copies,
and pairwise packing conflicts from exact affine column predicates. The 239
nonconstant atoms have period1 and cuts6,7,8,9,10,11,12; the last representative
stands for the whole unbounded range. Every demanded point is checked to lie
in the open halo for every class. Materialized cell sets audit every matrix.

Union the available/supplier incidence masks across classes and intersect the
conflict masks. Every actual cover at every parameter gives a cover in this
conservative finite relaxation. A16-node rejection DAG excludes it. At each
node, branching on a remaining demanded cell considers every available
supplier. Selecting it removes its covered demands and overlapping poses;
every child must be a certified smaller-demand state. Leaves have no supplier.
The search-free reader checks all branches and the root. This proves Q is
outside E1, even with holes allowed and with no further restrictions on added
copies beyond disjoint packing.

## Forced half-turn and remaining gap

In an E2 cover of the pair(I;6,4-k), the notch(5,3) must be covered. The
side calculation leaves only R or Q. This point is adjacent to root cell(3,2),
which exists for every k>=6, so either supplier touches the root. Every contact
in an E2 cover must belong to E1. The Q exclusion therefore forces R.

This does not establish that the resulting three-copy configuration is
impossible, nor that it extends to an E2 cover. That is a concrete remaining
subproblem. In particular the full 32-pose E2 inclusion and all-k unconditional
upper-three conclusion have not been established here. A plane-tiling or
finite-five construction has not been claimed.

## Validation, dependencies and reproducibility

Run the serial command in [README.md](README.md). Normal/optimized mathematical
evidence agrees. Six damage controls alter a raw system, a raw endpoint, a
collar breakpoint, a relaxed eligibility mask, a DAG node, or a supplier list;
all are rejected. Guards raise operational exceptions and never count as
mathematical rejections. The source is standard-library Python with the three
pinned previously published geometry files in [expected.json](expected.json).
Generated certificate files are ignored and need not be downloaded.

The all-k reduction is an ordinary unformalized argument. The affine/height
kernels are shared between producer and reader; the separate sweeps, cut
reconstruction and direct materialized audits are same-author validation,
not independent peer review or proof-assistant formalization.

Primary context:[Kaplan2022](https://arxiv.org/abs/2105.09438) and the
[author's census](https://cs.uwaterloo.ca/~csk/heesch/). The
[earlier conditional strip proof](../parametric-strip-obstruction/proof.md)
supplies the literal definitions, column/frame argument and shared exact
affine code; its source41bf6af8891df8c07f5a71db1c81a40b52c7b4ca / graph9321
remains conditional. The[T5 source](../strip-t5/proof.md) supplies the
separate unit-edge geometry module used for audits. The
[registration/pair-depth source](../proof.md), sourcecf3b672f2bf53a076c057b44a6f1a087ef028fcd /
graph8585, explains the separate all-motion bridge; no record or new global
corona conclusion is imported from it.
