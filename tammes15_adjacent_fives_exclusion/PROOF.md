# The two ordinary fives cannot contact in the conditional Tammes-15 branch

Author: **six-tammes-1**, role: **researcher**, 2026-09-30.
Status: complete author-audited exact computer-assisted lemma with a
written geometric reduction. Independent mathematical review and
formalization are pending.

## Statement

Let fifteen distinct unit vectors have minimum geodesic separation d,
and put c=cos(d). Their **complete** contact graph is assumed to give a
connected cellular sphere decomposition into simple strictly convex
triangles T and quadrilaterals Q, each contained in an open hemisphere.

**Local exclusion.** On the full interval `1/2<c<3/5`, if exactly two
vertices have degree five, each incident to four T faces and one Q,
and the other thirteen vertices have degree four, the degree-five
vertices are noncontacting.

**Eight-Q corollary.** Suppose instead the graph has degrees3..5,
exactly eight Q faces, and `1/2<c<beta`, where beta is the unique root
in `(119/200,3/5)` of

```text
1+4c+2c^2-4c^3-11c^4-24c^5.
```

The [three-five exclusion](../tammes15_three_five_exclusion/PROOF.md),
source `d1f289db096e04d307604aa243d757574ffb998d`, graph
`bafkreifqqkykpc6zwd6xmvvuq4yl7ik6qktmksr6ozase3fqm3hbt6k4fm`
(h7562), supplies precisely the degree pattern in the local exclusion.
Consequently its two degree fives are noncontacting. The two necessary
profiles remain, with the following sharper triangle-component restriction:

| (d41,d42,d51,n3) | n4 | n5 | separated ordinary fours s | inherited H types |
|---|---:|---:|---|---:|
| (4,0,0,0) | 13 | 2 | 1 or 3 | 6 |
| (2,1,0,0) | 13 | 2 | 0, 2 or 4 | 5 |

A separated ordinary four has cyclic sectors T,Q,T,Q; an ordinary
four has two T sectors, a deficit-one four has one, and a deficit-two
four has zero. The eleven inherited H types are unchanged. These are
necessary conditions, not realized packings or a full contact-graph
enumeration. The entire eight-Q branch, larger faces and coverage of
global optimizers remain open. No improved global numerical bound or
Tammes-15 optimality is asserted.

## 1. Original fans and the complete nine-rotation cover

Use the established equilateral-T angle and rhombus notation

```text
alpha=acos(c/(1+c)); x=2*pi-4*alpha;
rho(u)=2*atan(1/(c*tan(u/2))); y=rho(x).
```

The [ordinary-five and rhombus proof](../tammes15_eight_quad_reduction/FIVE_BOUNDARY.md)
and [corner-capacity proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md)
give, throughout `(1/2,3/5)` with ordinary fives explicit,
`alpha<qangle<2alpha`, `alpha<2*pi/5`, `y>x`, and the rule that a
Q never has adjacent ordinary fives. A degree-four vertex cannot have
three or four T faces: its angle sum would be strictly below5alpha
or equal4alpha, both below2pi. Thus it has at most two Ts.

Suppose the two ordinary fives A=0 and B=1 contact. Their edge must
be T-T, with two distinct triangular third vertices S=2,T=3. Two
distinct unit points have at most two common contact neighbors, since
their affine contact planes meet in a line with at most two sphere
intersections (antipodal points have none for c>0). Hence S,T exhaust
the common neighbors of A,B. Their other four neighbors are all
distinct original vertices, labeled4,5,6,7. This is an original
eight-point patch, with no normalized fan copies.

At each ordinary five the four Ts form one linear five-neighbor link.
B occupies position i=1,2,3 in A's link; A occupies j=1,2,3 in B's.
Choose the orientation with S,B,T consecutive at A and T,A,S at B.
The cover in [fans.py](fans.py) constructs all nine possibilities:

| (i,j) | T counts at (S,T) |
|---|---|
| (1,1) | (2,2) |
| (1,2) | (2,3) |
| (1,3) | (1,3) |
| (2,1) | (3,2) |
| (2,2) | (3,3) |
| (2,3) | (2,3) |
| (3,1) | (3,1) |
| (3,2) | (3,2) |
| (3,3) | (2,2) |

All vertices other than A,B have degree four and at most two Ts.
Only `(1,1),(3,3)` survive. They are the same full face/F patch under
boundary dihedral relabeling, checked both by face correspondence and
all pairwise Gram identities. In `(1,1)` its links are

```text
A: 2,1,3,4,5; B: 3,0,2,6,7.
T faces: 012,013,034,045,126,167.
```

There are six Ts and thirteen prescribed contacts. Its boundary
dihedral canonical edge mask is172253945. The face/Gram correspondence,
rather than the mask alone, justifies the one representative.

## 2. Six forced Qs give fourteen original positions

Use an equilateral anchor basis `a1=e1,a6=e2,a7=e3` with

```text
H=(1-c)I+cJ; <u,v>=u^T H v; r=2*c/(1+c).
```

The eigenvalues1-c,1-c,1+2c are positive. This coefficient space is
isometric to Euclidean R3, preserving all inner products. Starting
from the anchor triangle167, the other fan points are forced as

```text
a2=r(a1+a6)-a7; a0=r(a1+a2)-a6;
a3=r(a0+a1)-a2; a4=r(a0+a3)-a1;
a5=r(a0+a4)-a3.
```

At a contact edge with an old triangular third point o, its two
possible unit common neighbors are o and `r(a+b)-o`. Original
injectivity selects the second when constructing the adjacent T.
The checker separately removes/reinserts polygon ears and compares
all24 coefficient functions with this direct construction exactly.

For a Q with opposite old corner f and its two adjacent corners a,b,
the other opposite corner is forced by

```text
q=2*c/(1+<a,b>)*(a+b)-f.                         (1)
```

Its denominator is positive. For any two points with a unit common
contact neighbor f, Cauchy--Schwarz gives `1+<a,b>>=2*c^2>0`.
The affine-plane/sphere intersection has at most two solutions;
the simple Q's other corner is different from f and selects (1).
All explicit denominator signs are also checked exactly.

The sole Qs at the two Fs are therefore

```text
0,2,8,5; 1,3,9,7.
```

The checker verifies their ten positions are distinct, by unit norms
and strict different-position bounds inherited in the full audit below.
At vertex2, its known faces012,126 and Q0285 form the consecutive
link path `8,0,1,6`. Its four distinct contact neighbors already
exhaust degree four. The remaining sector is between6 and8. Those
points are strictly noncontacting by the exact Gram audit, so this
sector cannot be T and must be a Q. Similarly the remaining sector
at3 is between4 and9. These force

```text
2,6,10,8; 3,4,11,9.
```

Now4 has four distinct neighbors0,3,5,11; its known consecutive
faces034,045 and Q `(3,4,11,9)` leave the sector between5 and11. They are
strictly noncontacting, so this also is Q. Vertex6 similarly leaves
the sector between7 and10. The last two forced Qs are

```text
4,5,12,11; 6,7,13,10.
```

No arbitrary planar completion or connectedness of all T faces is
assumed. Every
new label is justified as an actual Q opposite via (1). The exact
fourteen-position audit proves that it is distinct from every earlier
label, so the two last opposites cannot be an overlooked original alias.

## 3. Only two possible complete core contact patterns

All fourteen positions have unit norm throughout `(1/2,3/5)`, with
no coordinate poles. Of their91pairs, exactly25are identically contact
pairs. Another62have strict packing gaps `c-<ai,aj>>0` on the entire
interval. The remaining four are

```text
class A: (8,12),(9,13);
class B: (10,12),(11,13).
```

The two gaps within each class are **identical rational functions**.
For each of the four pairs the checker proves `1-<ai,aj>>0`, so they
are distinct positions even where their packing gap is negative or zero.
It does not assert all fourteen positions form a packing throughout
the interval. The exceptional packing gaps can change sign; a negative
gap already prevents an actual packing. For an actual packing they
are nonnegative, and only their zeros can create additional contacts.

The25fixed contacts give degrees

```text
5: 0,1;
4: 2,3,4,5,6,7;
3: 8,9,10,11;
2: 12,13.
```

There is exactly one remaining original point, label14, of degree four.
The complete fifteen-point graph has degree sum `2*5+13*4=62` and31edges.
Its four edges at14 leave **27contacts within the fourteen-point core**.
Thus precisely two further core contacts are needed. The only possible
ones are the four exceptional pairs, appearing in identical-gap pairs.
Exactly one whole class A or class B must be contacts.

Definition-level degree counting then forces all four neighbors of14:

| Additional core contacts | Four neighbors of14 |
|---|---|
| class A | 10,11,12,13 |
| class B | 8,9,12,13 |

This uses the complete graph and actual degree pattern. It is not a
bound on unrestricted extensions of an arbitrary fourteen-point code.

## 4. Undivided Cramer residuals and Bezout obstructions

For three necessary neighbors bi of a possible unit point v, put
`ni=H*bi`, let N have those three rows, d=det(N), and let Y be the
three undivided Cramer numerators for right-hand side `(c,c,c)`.
The checker verifies coefficientwise `N Y=d c1` and **every column**
of `adj(N)N=d I`. Hence `Nv=c1` implies `Y=dv`, even if d=0.
Necessarily

```text
G=Y^T H Y-d^2=0.                                (2)
```

No determinant root, singular parameter or rank-deficient case is
divided through or dropped. All rational-function denominator poles
are excluded explicitly.

In class A, let hA be the gap for(8,12) and use the necessary neighbor
triple `(10,11,12)` in (2). In class B, use the gap hB for(10,12) and
the triple `(8,9,12)`. Writing n(f) for the reduced numerator of f,
the checker obtains exact polynomial gcds

```text
gcd(n(hA),n(GA)) = c^2*(1-3*c^2+2*c^3);
gcd(n(hB),n(GB)) = c+4*c^2-6*c^3-34*c^4+7*c^5
                  +86*c^6-18*c^7-80*c^8+40*c^9.
```

The first is positive on the interval: `1-3*c^2+2*c^3=(1-c)^2*(1+2c)`.
The second is strictly negative. Its degree-nine Bernstein coefficients
on `[1/2,3/5]` are

```text
-3/16, -11/48, -3127/11520, -17581/56000, -897823/2520000,
-278609/700000, -109677/250000, -672073/1406250,
-362252/703125, -214896/390625.
```

All are negative, so there is no real zero anywhere in the interval.
Every gcd is additionally audited using an independently implemented
Fraction Euclidean algorithm that constructs exact polynomial Bezout
coefficients s,t and verifies `s*n(h)+t*n(G)=gcd` coefficientwise.
This shares the two computed polynomials, but uses a different algorithm
from the integer primitive pseudoremainders. The gcd and Bezout hashes
are in [EXPECTED.json](EXPECTED.json); no external polynomial corpus
or CAS is required.

The additional contact requires h=0 and the fifteenth unit point
requires G=0. Their Bezout identity would make the nonvanishing gcd
zero. Both classes are impossible, completing the local exclusion.

## 5. Triangle-component corollary

In the inherited eight-Q branch write p=d42 and let s count separated
ordinary fours. The [triangle-fan component lemma](../tammes15_eight_quad_reduction/ALL_ONE_TWO.md),
source `470c27913d3a51edba5af295120a04bfb1b920f3`, gives, at n3=0,

```text
K_T >= (5-p+s)/2; 15+p-s is even.
```

Here triangles are adjacent when they share a T-T edge. The two Fs
are now noncontacting, so no T contains both. Their two connected
four-T fans comprise eight distinct Ts, leaving only two other Ts.
Therefore `K_T<=2+2=4`, regardless of whether the fans meet, share
original vertices, or connect through other triangles. Combining this
with the bound and parity gives `s in{1,3}` for p=0 and `s in{0,2,4}`
for p=1. No triangle connectedness or disjointness of original fans
is assumed.

## Reproduction, primary context and trust boundaries

```sh
python3 -B tammes15_adjacent_fives_exclusion/check.py | cmp - tammes15_adjacent_fives_exclusion/EXPECTED.json
python3 -B -O tammes15_adjacent_fives_exclusion/check.py | cmp - tammes15_adjacent_fives_exclusion/EXPECTED.json
(cd tammes15_adjacent_fives_exclusion && sha256sum -c SHA256SUMS)
```

CPython>=3.11, standard library, one mathematical process and all native
threads one. The checker does not read its expected output, private
pilot data, coordinates, network, solver output or any ledger. Its
certificate only declares the compact two-case table, which is checked
against exhaustive paired-fan generation, all91pair identities/signs,
original degree counts and exact symbolic residuals. Thirteen controls
include rejection of missing/altered contact classes and required
neighbors, zero rational denominators/divisors, an invalid gcd, and
positive tests for singular ranks, nontrivial gcds and sign changes.
Explicit exceptions remain active under `-O`.

The fan code and direct/ear coordinate mechanism are adapted from the
three-five source cited above. The integer polynomial/rational kernels
are attributed adaptations of **six-tammes-2**, researcher,
[the overlap reduction](../tammes15_bridge_overlap_reduction/PROOF.md),
source `34d5a62d025ea9ade24e17c9ba848d297469063f`, graph h7488. Sharing
these kernels is not an independent arithmetic audit of the whole proof.
The Fraction Bezout audit checks a narrower arithmetic bridge.

Complementary [decagon reductions](../tammes15_decagon_extension_reduction/PROOF.md)
and [the first-core cap exclusion](../tammes15_decagon_type0_cap_exclusion/PROOF.md)
were read as context. They concern different prescribed ten-point
families; neither external-ear occurrence nor their exclusion theorem
is transferred to these fourteen positions. Their checkers were not
replayed for this result. The earlier
[independent rhombus review](../tammes_15_triangle_quad_exclusion_review1/README.md)
supports inherited face geometry, and does not review this result.

The current [Cohn table](https://cohn.mit.edu/spherical-codes/) still lists
the unstarred N15 cosine0.59260590292507377809642492233276 with known
quintic `13c^5-c^4+6c^3+2c^2-3c-1`. The
[coordinate archive](https://spherical-codes.org/data/3/15) remains890bytes,
SHA256 `1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
[Musin--Tarasov1410.2536](https://arxiv.org/abs/1410.2536) solvesN14.
Bounded primary/source/graph searches found no matching adjacent-five
exclusion; no exhaustive priority claim is made.

Written rhombus geometry, original-vertex injection, cyclic contact-star
correspondence, Q completion and the inherited component lemma remain
unformalized. The exact checks do not constitute independent mathematical
review, a full graph enumeration or a proof of global optimizer coverage.
All computations finish normally; no timeout, incomplete search or
floating-point failure is used to infer mathematical nonexistence.
