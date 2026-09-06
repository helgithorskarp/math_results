# Every host colouring extends to the 483-point two-triangle spindle sum

**Exact computer-assisted theorem.** Let Hstar be the eleven-point heptagon
host specified below, M the aligned seven-point Moser spindle, and
r=exp(2*pi*i/7). The complete Euclidean unit-distance graph on

```
Zstar = Hstar + M + rM
```

has **483 vertices, 2,061 edges and chromatic number exactly four**.
Moreover, every proper four-colouring of Hstar extends to this graph while
preserving the colours on its embedded copy Hstar+0+0. Every subgraph of Zstar
is therefore four-colourable. This proposed at-most-508 construction cannot
improve the record or impose any new four-colour restriction on Hstar.

This is a single exact construction with a universal extension theorem, not
an enumeration of relative rotations or a claim about other hosts. Unlike
the previously closed aligned double sum, its two spindles align with two
distinct host triangles. That change alone does not escape a symbolic
colour-extension mechanism. No five-chromatic target was found.

## Exact construction

Use the complex plane and t=exp(pi*i/21), s=i*sqrt(11). For j=0,...,6 put

```
Pj = t^(6j)/(t^24-t^(-24))
Qj = -t^(6j-7)/(t^6-t^(-6))
Rj = -t^(6j+7)/(t^12-t^(-12)).
```

These are the established
[heptagon coordinates](../hadwiger_nelson_heptagon_difference_lifts/README.md)
from [Haugland's construction](https://arxiv.org/html/2608.04542v4).
Order the new host as

```
h = (P0,P1,P2,P3,P4,P5,P6,Q0,R0,Q1,R1).
```

Its inherited 21-point labels are `[0,1,2,3,4,5,6,7,14,8,15]`.
It has exactly thirteen unit edges: the seven P-cycle edges and the three
edges of each triangle `(h0,h7,h8)` and `(h1,h9,h10)`.
With u=Q0-P0, v=R0-P0 and rho=(5+s)/6 define the ordered spindle

```
M = (0,u,v,u+v,rho*u,rho*v,rho*(u+v)).
```

The inherited [spindle arithmetic](../hadwiger_nelson_heptagon_moser_sum/README.md)
verifies its eleven edges. Multiplication by r=t^6 sends Pj,Qj,Rj to the
corresponding points with index j+1 modulo seven. Thus M and rM align with
the two stated triangles.

There are 49 distinct points in M+rM. The 539 ordered triples `(h,a,b)`
produce 483 distinct points `h_h+m_a+r*m_b`. Their fibre sizes are
441 singletons, 28 doubletons and 14 triples. All 2,061 unit edges are images
of factor edges: an Hstar edge with a,b fixed, an M edge with h,b fixed, or
an rM edge with h,a fixed. There are no additional mixed unit edges.
These are exact exhaustive claims, checked in a second algebraic basis.

## Symbolic extension proof

Identify the four colour labels with the additive group F2^2; addition is XOR.
Let p be **any** proper four-colouring of Hstar. Set

```
x0=p0 XOR p7,   y0=p0 XOR p8,
x1=p1 XOR p9,   y1=p1 XOR p10,
q(x,y)=(0,x,y,x XOR y,x,y,0).
```

For a formal triple assign

```
c(h_h+m_a+r*m_b) = p_h XOR q(x0,y0)[a] XOR q(x1,y1)[b].
```

The following stronger symbolic identities certify both that this descends
through every geometric coincidence and that it is proper. Give each p_h
an independent formal basis symbol e_h over F2. The two spindle templates are

```
A = (0,e0+e7,e0+e8,e7+e8,e0+e7,e0+e8,0)
B = (0,e1+e9,e1+e10,e9+e10,e1+e9,e1+e10,0).
```

Every representation of any one geometric point has the **same formal vector**
`e_h+A_a+B_b`. Call it L(z). For every actual unit edge zw, the exact check
finds an Hstar edge ij such that `L(z)+L(w)=e_i+e_j`. Also
`L(h_h+0+0)=e_h` for all eleven host vertices. These identities hold before
assigning any colours, so no completeness assumption about a colouring
library is involved.

Now evaluate each e_h at p_h in F2^2. The first identity makes c well-defined;
the second gives `c(z) XOR c(w)=p_i XOR p_j != 0`, since ij is a host edge.
The last identity preserves p on Hstar. This proves the universal extension.
There are 112 distinct formal vectors among the 483 geometric points.
The 2,061 edge identities project to the thirteen host edges as follows:
each of seven P-cycle edges occurs 49 times, each of four P-to-Q/R triangle
edges occurs 306 times, and each of two Q-to-R edges occurs 247 times.
Thus `7*49+4*306+2*247=2061`.

For a concrete witness, the **40-byte** [certificate](certificate.json) gives

```
p=(0,1,0,1,0,1,2,1,2,0,2).
```

It properly three-colours Hstar. Evaluating the same symbolic extension uses
four colours and passes all 2,061 unit-edge checks. Zstar contains the spindle
`h0+M+0`, which is not three-colourable: after normalizing its first triangle
to colours 0,1,2, all 81 assignments to its other four vertices are rejected.
Consequently the full graph has chromatic number exactly four. Restricting
its explicit colouring proves the assertion about all subgraphs; it does
not assert that every such subgraph needs four colours.

## Reproduction and trust boundary

Python 3.11.2 with the standard library suffices. Run from the repository root
with a fresh output directory:

```bash
python3 -B hadwiger_nelson_heptagon_two_triangle_sum/build.py --out /tmp/hn-two-triangle
python3 -B hadwiger_nelson_heptagon_two_triangle_sum/verify.py --work /tmp/hn-two-triangle
```

The [producer](build.py) uses integer coordinates divided by 42 in
`Q(t,s)`, with `Phi42(t)=t^12+t^11-t^9-t^8+t^6-t^4-t^3+t+1` and `s^2=-11`.
The 24-element basis is independent: Q(t) has degree twelve and is unramified
at eleven, whereas Q(s) ramifies there. Two validated finite-field maps are
used only to reject impossible distances; all surviving pairs are checked
in characteristic zero. The 2,061 survivors are exactly the unit edges.

The [separate checker](verify.py) imports neither the producer nor its
arithmetic. It uses the inherited tensor representation in zeta7, omega6 and
w=(1+sqrt(-11))/2, with zeta7^6=-(1+...+zeta7^5), omega6^2=omega6-1 and
w^2=w-3. It reconstructs the factors independently and compares the full
support, all 539 formal labels and fibres, and the complete edge list
entry by entry. All **116,403** full-support pair norms are evaluated directly
in characteristic zero, with **no modular filter**. The symbolic check uses
sets and symmetric differences instead of the producer's integer bit masks.
It verifies every fibre, every unit-edge identity and all eleven preserved
host colours. It also checks the explicit colouring, the retained spindle,
the 81 three-colour cases and five rejection controls.

The field and tensor arithmetic are reused from the
[independently accepted single-sum foundation](../hadwiger_nelson_heptagon_moser_rotation_family_review1/README.md).
That acceptance does not constitute external review of this new theorem.
The new producer and separate checker are author-run; external review is
pending. Remaining trust lies in the exact coordinate definitions, algebraic
basis facts, ordinary Python integer arithmetic, complete finite loops and
the stated symbolic argument. No floating-point predicate, solver answer,
large omitted proof trace or proof-assistant formalization is involved.

[Expected counts and hashes](expected.json), [validation details](validation.json)
and [source hashes](SHA256SUMS) accompany the code. Generated full graphs and
operational checkpoints remain local; the source regenerates them.

## Decision and shared context

The concrete two-triangle proposal is closed, including every deletion-only
subgraph. A new host triangle did not add a four-colour restriction here:
all collisions and unit edges admit the displayed simultaneous symbolic
extension. Further centered sum variants are not opened by this result.
The next pass should change the geometric assembly mechanism and require
an explicit interface obstruction before growing another product support.

This differs from the
[522-point aligned double-sum theorem](../hadwiger_nelson_heptagon_double_spindle/README.md):
both the host and relative spindle rotation have changed, and neither exact
support is assumed to contain the other. The present theorem makes no claim
about the full 21-point host plus these rotated factors or other rotations.

HN-2 has independently closed every at-most-508 subgraph of its H517 support
([source](../hadwiger_nelson_heule517_whole_decision/README.md),
[accepted review](../hadwiger_nelson_heule517_whole_decision_review1/README.md)).
That distinct exact-certification lane supplies no premise here and is not
restarted. The parked Parts two-overlap census and heptagon-difference solver
queries also remain parked.

Primary-source calibration on 2026-09-06: Parts reports a five-chromatic graph
with 509 vertices and 2,442 edges in
[his minimization paper](https://arxiv.org/abs/2010.12665); Haugland's
[2026 manuscript](https://arxiv.org/html/2608.04542v4) still identifies 509 as
the record. This four-colourable 483-point graph does not improve it.
