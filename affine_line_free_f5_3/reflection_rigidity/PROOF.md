# A 71-point line-free candidate has at most one affine reflection

Let $V=\mathbb F_5^3$. A subset is line-free if it contains no complete
five-point affine line. Write $G(S)$ for its affine automorphism group.

**Theorem.** If $S$ is line-free and $|S|=71$, then $G(S)$ is
trivial or has order two. In the latter case its unique nonidentity
element fixes an affine plane pointwise; after an affine coordinate
change it is $(x,y,z)\mapsto(-x,y,z)$.

We prove two complete finite obstructions:

1. A line-free set invariant under a nonidentity affine involution whose
   fixed locus is a line has at most **70 points**.
2. A line-free set invariant under an affine order-four map whose square
   fixes a plane pointwise has at most **68 points**.

Neither bound is asserted sharp here. The final group conclusion also
uses the earlier [odd-symmetry theorem](../odd_symmetry/PROOF.md) to
exclude odd prime orders. Central inversion at size 71 is excluded
by an elementary count in Section 6.
The separate [upper-bound-71 theorem](../upper_bound71/README.md),
published during this work, narrows the global interval to
$70\le r_5(\mathbb F_5^3)\le71$. That exclusion is context, not a
premise of any theorem here.
Independent peer review of the present proof is pending.

## 1. Normal form and exact planar menus

An affine involution has a fixed point by averaging. In characteristic
five it is diagonalizable with eigenvalues $1,-1$. When its fixed locus
is a line, its normal form is

$$
g(x,y,z)=(x,-y,-z).                                      \tag{1}
$$

The fixed line is $F=\{(x,0,0)\}$. Set $k=|S\cap F|\le4$.
Each plane $x=c$ has a center $(c,0,0)$ and twelve noncentral opposite
pairs. Enumerate these pairs by the smaller of their planar point
indices $5y+z$, in increasing order. A layer is specified by its center
bit and a 12-bit pair mask.

The planar cap is 16. It follows either from the classical planar
line-free theorem or from the full planar census in Section 5.
If the center is selected, each of its six radial lines permits at most
one opposite pair, so the layer has at most 13 points.

Enumerating all 4,096 pair masks against the 30 planar affine lines gives
the following exact numbers, indexed by the number of selected pairs:

| Center | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Absent | 1 | 12 | 66 | 220 | 495 | 780 | 840 | 540 | 135 |
| Present | 1 | 12 | 60 | 160 | 240 | 180 | 40 | 0 | 0 |

There are no larger admissible masks. The 625 transverse lines have form

$$
\{(x,u+ax,v+bx):x\in\mathbb F_5\},
\qquad u,v,a,b\in\mathbb F_5.                            \tag{2}
$$

Recording their required pair index in each layer, with symbol 12 for
the center, gives 313 distinct five-symbol rows. A row forbids exactly
the tuples selecting all its points. Thus admissible planar masks and
these rows are equivalent to line-freeness for (1).

## 2. A complete cover at 71 and 72 points

It is enough to exclude size 71 with $k=1$ or $3$, and size 72 with
$k=0$. This also proves the uniform bound 70 without using the campaign's
global upper bound: an invariant set larger than 70 contains one of
these invariant subsets. For $k=0$, select 36 pairs. For $k=1$ or $2$,
select 35 pairs and one fixed point. For $k=3$ or $4$, select 34 pairs
and three fixed points. The required pair counts follow from
$k+2r>70$, and deletion preserves line-freeness.

### Size 71, three selected fixed points

Affine changes $x\mapsto ax+b$ act transitively on the three-element
subsets of the fixed line, since they act transitively on their
two-element complements. Normalize the selected coordinates to
$\{2,3,4\}$.

The local caps sum to $3\cdot13+2\cdot16=71$, so every layer is maximal:
three centered 13-point layers and two uncentered 16-point layers.
All $40^3\cdot135^2=1,166,400,000$ tuples are covered. No further
symmetry quotient is used in this case.

### Size 71, one selected fixed point

Normalize the selected fixed point to $x=0$. Some other layer has 16
points: otherwise the bound would be $13+4\cdot14=69$, since the other
layers have even sizes. Scale $x$ so one 16-point layer is at $x=1$.

The group $\operatorname{GL}(2,5)$ acts simultaneously on $(y,z)$ in
every layer and commutes with (1). Its complete action on the 135
uncentered 16-point masks has exactly two orbits:

| Representative pair mask | Orbit size | Stabilizer order |
|---:|---:|---:|
| 495 | 120 | 4 |
| 943 | 15 | 32 |

The program enumerates all 480 invertible two-by-two matrices, constructs
their pair permutations, and verifies that these two disjoint orbits
cover all 135 masks. Fix the layer $x=1$ to each representative and
enumerate every other admissible layer. This normalization restricts no
other shape or incidence.

### Size 72, no selected fixed point

Every layer is even. At least one layer has size 16; otherwise the total
is at most 70. Translate $x$ to put such a layer at zero and use the
same two $\operatorname{GL}(2,5)$ representatives there.

The other four layers total 56. Their largest has size 14 or 16.
Scale $x$ to place a largest one at $x=1$, then use the stabilizer of
the first mask to normalize the second. Every later layer is required
only to have size at most this second layer.

The exact second-layer orbit partitions are:

| First mask | Second masks of weight 7 | Second masks of weight 8 |
|---:|---:|---:|
| 495 | 270 representatives | 73 representatives |
| 943 | 38 representatives | 13 representatives |

In each row the stabilizer orbits are disjoint and cover all
$540+135=675$ eligible second masks. They need not all have the same
size: $-I$ acts trivially on pair masks. The normalizer checks the
actual orbit sets and multiplicities rather than dividing by the
abstract group order.

The affine maps used here preserve the fixed line and the involution.
After fixing $x=0$, nonzero scalings remain transitive on the other
four layer positions. The planar stabilizer fixes the first mask.
Consequently all three normalizations can be imposed simultaneously.

## 3. Complete exclusions and two representations

[reflection_constraints.cpp](reflection_constraints.cpp) reads the
menus and rows generated by [model.py](model.py). For a choice of the
first three masks, each active row forbids a last-layer pair when its
fourth-layer pair is selected. Unioning these forbidden bits for the
fourth mask gives every last-layer restriction. A forbidden selected
center causes unconditional failure. A precomputed table counts all
admissible last masks of each weight avoiding each forbidden union.

If the required total pair count is $T$ and the five local caps are
$c_i\in\{6,8\}$, a layer has at least $T-\sum_{j\ne i}c_j$ pairs.
A three-layer prefix is discarded only when even the remaining caps
cannot reach $T$. A forbidden union may be rejected once fewer than
the required number of pair positions remain available. The size-72
case additionally uses exactly the proved second-layer normalization
from Section 2.

[reflection_direct.cpp](reflection_direct.cpp) independently constructs
the actual 25-point planar subsets and all 625 geometric lines (2).
Each layer mask has a 625-bit incidence vector. It explicitly tests
every candidate last mask by intersecting the five vectors. It reads
no row catalogue or first program's geometric instance. It uses the
same stated normalization, whose coverage is checked separately.

The two programs agree on these complete records:

| Size | Fixed-point mask | Fixed full-layer mask | Three-layer prefixes | Four-layer prefixes | Five-layer tuples | Solutions |
|---:|---:|---:|---:|---:|---:|---:|
| 71 | 28 | none | 64,000 | 8,640,000 | 1,166,400,000 | 0 |
| 71 | 1 | 495 | 548,100 | 237,127,500 | 59,705,100,000 | 0 |
| 71 | 1 | 943 | 548,100 | 237,127,500 | 59,705,100,000 | 0 |
| 72 | 0 | 495 | 786,870 | 332,908,875 | 143,900,317,125 | 0 |
| 72 | 0 | 943 | 118,350 | 56,345,175 | 24,038,501,625 | 0 |

The layer orders are respectively $(2,3,4,0,1)$, $(1,0,2,3,4)$,
$(1,0,2,3,4)$, $(0,1,2,3,4)$, and $(0,1,2,3,4)$.
The fixed-point mask is $\sum_{x\in S\cap F}2^x$.
The direct program examines all listed five-tuples; the first program
counts possible last masks by lookup and obtains the same counts.

These zero-completion results and Section 2 prove obstruction 1.
This is a complete family exclusion, not the interpretation of a
timeout or failed local search.

## 4. Order-four maps squaring to a plane reflection

An affine order-four map has a fixed point by averaging. Translate it
to zero. Since $t^4-1$ splits with distinct roots over $\mathbb F_5$,
the map is diagonalizable. If its square fixes a plane pointwise,
exactly one eigenvalue is $2$ or $-2$ and the other two are $1$ or $-1$.
Replacing the generator by its inverse if needed gives the normal form

$$
h(x,p)=(2x,Tp),\qquad
T\in\{I,\operatorname{diag}(1,-1),-I\},\quad p=(y,z).
                                                               \tag{3}
$$

Write $A=S\cap\{x=0\}$ as a planar set, and let $B$ be the section at
$x=1$. Invariance forces the five sections, in order $x=0,1,2,3,4$, to be

$$
A,\ B,\ T(B),\ T(B),\ B, \qquad T(A)=A.                  \tag{4}
$$

Put $b=|B|$. Both $A$ and $B$ are line-free planar sets, so
$|A|,b\le16$. If $b\le13$, then $|S|=|A|+4b\le68$.

For $b=14,15,16$, define the allowed central points

$$
D_T(B)=\{u:\text{ there is no }v\in\mathbb F_5^2
\text{ with }u\pm v\in B,\ u\pm2v\in T(B)\}.             \tag{5}
$$

Every $u\in A$ must lie in $D_T(B)$, or the transversal
$(x,u+xv)$ is a complete line. Therefore
$|S|\le4b+|D_T(B)|$. This relaxation need not impose line-freeness or
$T$-invariance on $D_T(B)$; ignoring those restrictions only weakens
the upper bound.

## 5. A complete planar census for the order-four obstruction

The maximum allowed central-set sizes over **all** line-free planar
$B$ of each indicated size are:

| $b$ | Number of line-free $B$ | $T=I$ | $T=\operatorname{diag}(1,-1)$ | $T=-I$ |
|---:|---:|---:|---:|---:|
| 14 | 961,500 | 6 | 11 | 11 |
| 15 | 252,600 | 3 | 6 | 6 |
| 16 | 28,375 | 0 | 3 | 2 |

[order4_probe.cpp](order4_probe.cpp) is a complete fixed-cardinality
enumerator despite its historical filename. It visits all
$\binom{25}{14}=4,457,400$, $\binom{25}{15}=3,268,760$, and
$\binom{25}{16}=2,042,975$ subsets. It checks every planar line, then
computes (5) using the zero slope and the twelve opposite pairs of
nonzero slopes.

[order4_gray.cpp](order4_gray.cpp) instead visits all $2^{25}$ planar
subsets by Gray-code toggles, maintaining the occupancies of the six
lines through the changed point. It computes (5) using all 25 slopes
and actual point incidences. This census also verifies that the largest
line-free planar set has size 16.

The programs agree on the **entire histogram** of $|D_T(B)|$ for each
of the nine cases, not merely on the displayed maxima.
Every extremal example retained by the first program is independently
decoded to (4) and checked against all 775 three-dimensional lines.
These nine boundary controls have sizes between 62 and 67, and are
not claims of new lower bounds.

For $b=14,15,16$ the displayed relaxation bounds are at most
67, 66, and 67, respectively. Together with the $b\le13$ argument,
this proves obstruction 2: every set invariant under (3) has size at
most 68.

## 6. The affine automorphism group has order at most two

For $|S|=71$ the earlier
[odd-symmetry theorem](../odd_symmetry/PROOF.md) proves that $G=G(S)$ is
a 2-group. It cannot contain central inversion about a point $O$:
odd cardinality forces $O\in S$, and each of the 31 lines through
$O$ permits at most one opposite pair besides $O$. This would give
$|S|\le1+2\cdot31=63$.
Average an orbit over
$G$ to find a common fixed point; this is valid since $5\nmid|G|$.
Translate that point to zero, so $G\le\operatorname{GL}(3,5)$.

Consider the determinant homomorphism

$$
\det:G\longrightarrow\mathbb F_5^\times\cong C_4.
$$

If its kernel were nontrivial, that 2-group would contain an involution.
A nonidentity involution of determinant one in dimension three has
exactly two eigenvalues $-1$, hence fixes a line. Obstruction 1 rules
this out. Thus determinant is injective and $G$ is cyclic of order
dividing four.

If $|G|=4$, the square of a generator is an involution. It cannot fix
a line by obstruction 1, and cannot be central inversion by the preceding
count. It must fix a plane. Obstruction 2 then gives $|S|\le68$,
a contradiction. Hence $|G|\le2$. If $G$ has order two, its involution
is neither a line reflection nor central inversion, so it fixes a plane.
This proves the theorem.

## 7. Verification scope and limitations

All arithmetic is integral. Point bits have indices at most 24,
pair masks are below $2^{12}$, and forbidden unions below $2^{13}$.
Even the unrestricted five-mask count $4096^5=2^{60}$ fits in the
unsigned 64-bit counters. The Gray-code census has $2^{25}$ states.
There is no numerical tolerance, solver result, incomplete branch,
or search cutoff in either finite proof.

The paired-layer enumerations agree in all five exclusion cases.
Two additional common-menu controls give five Cartesian-product
64-sets and exclude the corresponding full five-layer 80-set; all
five positive controls receive a separate 775-line check. The
order-four census has nine further directly verified positive controls.

The two representations were implemented by the same researcher.
They are cross-checks, not independent peer review or formal proofs
in a proof assistant. The written normal-form and coverage arguments,
ordinary compiled code, and the prior order-three obstruction and
elementary odd-prime exclusions are the trust boundary. The current
replay does not repeat that prior order-three computation. No low-plane,
two-eight-plane, or general 72-point SAT exclusion is needed here.

This theorem does not assume a nontrivial automorphism. An arbitrary
71-point witness could be affine-asymmetric. The remaining
symmetric construction route is precisely the plane-reflection family.
