# Terminal triangulation closes the local Albertson `r=27` endpoint

This note supplies the missing topological step in the previously reviewed
24-vertex reduction. Its main lemma is the following profile-specific
unique-exception closure.

> **Terminal-triangulation `C5` lemma.** Let `D` be a good 2-planar drawing
> whose edge-crossing graph consists of `C5` and `K2` components. In each
> `C5`, perform the two-edge deletion described below, leaving one
> crossing-free survivor and one crossing pair. Suppose the planarization of
> the resulting 1-planar drawing `T` is a triangulation. If exactly one
> original `C5` is not a full 2-planar pentagon, while every boundary edge of
> every other (full) component is present, then the exceptional component is
> full as well, a contradiction.

Here the edge-crossing graph has one vertex for every crossed edge of `D`,
with adjacency when two edges cross. A full 2-planar pentagon consists of the
five diagonals inside a vertex-empty planar pentagonal boundary; the five
boundary edges need not be graph edges in the definition.

The preceding campaign reduction proves that a 24-vertex, 132-edge drawing
with at most 164 crossings would have a 2-planar remainder `D2` with
**exactly one non-full crossing `C5`** and `m0=0`, meaning that every present
full configuration has all five boundary edges. In each of the two residual
profiles, the reduced drawing `T` has a planarization attaining Euler
equality. The lemma therefore excludes both profiles and proves

```text
cr(24,132) >= 165.                                   (L24)
```

The already published exact propagation from `(L24)` gives
`cr(53,713)>=6089>6084` and closes the last row in Sadhu's `r=27` frontier.
Consequently Albertson's conjecture holds for chromatic number 27.

Because the new ingredient is a delicate topological reconstruction and
sealed-region argument, the Discovery Net submission is conservatively
labelled a proof attempt pending independent review.

## 1. Certified profile data and the `C5` deletion

Write `n,e,x` for the numbers of vertices, edges, and crossings of a drawing,
put `s=n-2`, and let `Delta` be the number of empty triangular faces of its
crossing-free subgraph. The reviewed predecessor certificate uses the
integer defect

```text
delta(D) = 3x-7e+25s-2Delta.
```

Pach--Radoicic--Tardos--Toth Lemma 3.2 is `delta(D)>=0`. Its equality
induction, already independently reviewed in the predecessor artifact,
proves that the two profiles have only `C5` and `K2` crossing components and
have respectively 10 and 12 `C5`s, exactly one of which is non-full.

Label any one of the cycles

```text
b -- a -- c -- d -- f -- b.
```

Thus `a` crosses `b,c`; `c` also crosses `d`; `d` crosses `f`; and `f`
crosses `b`. Delete `b,c`. This removes two edges and four crossings,
leaving `a` crossing-free and `d,f` as a crossing pair. Doing this in all
`q5` cycles gives a good 1-planar drawing `T` with

```text
e(T)=e(D2)-2q5,        x(T)=x(D2)-4q5.
```

No face assertion from a block-local PRTT reduction will be used below.

## 2. Euler equality makes the terminal drawing triangular

Planarize `T`, replacing each crossing by a degree-four vertex. Because the
drawing is good, the original graph is simple, and each edge is crossed at
most once, the planarization `P(T)` is a simple plane graph with

```text
Vplan = n+x(T),       Eplan = e(T)+2x(T).
```

The planar inequality `Eplan<=3Vplan-6` is

```text
B := x(T)-e(T)+3(n-2) >= 0.
```

For profile A, `(e(T),x(T))=(83,17)`; for profile B it is `(82,16)`.
Since `n=24`, both have `B=0`. Therefore `P(T)` is a plane triangulation.

At a crossing vertex its four neighbors are the four distinct endpoints of
the crossing pair, alternating around the vertex. Every consecutive pair is
joined by an edge because all four incident faces are triangular. These four
joining edges correspond to crossing-free edges of `T`, and the four
triangles incident with the crossing vertex form a vertex-empty disk.
Undoing the planarization shows that the crossing pair is precisely the two
diagonals of an empty quadrilateral face of the crossing-free subgraph. We
call this the **terminal kite property**.

This is a global consequence of Euler equality; it does not require
reassembling block-local faces across a 2-separation.

## 3. Tracing the deleted arcs through triangular faces

Select the exceptional component and use the labels from Section 1. Put
`a=zw`, and orient `c` from the endpoint `u` for which it crosses `a` before
`d`. In `T`, every open portion of the deleted arc `c` between successive
crossings lies in one face of the triangulation `P(T)`.

The face immediately after `c` crosses `a` has the planarization edge `zw`
and a segment of `d` on its boundary. A triangular face containing both
forces that segment of `d` to end at one of `z,w` and at the crossing vertex
of `d,f`. Thus `zw` is a side of the terminal kite of `d,f`. Write its cyclic
boundary as `z,w,r,t` and, after exchanging labels if needed, write

```text
d=zr,        f=wt.
```

The face immediately before the crossing with `a` is the other triangular
face incident with `zw`; its third vertex is the endpoint `u`. It is
therefore the empty triangle `u,z,w`. After crossing the `z`-to-crossing
segment of `d`, the last portion of `c` lies in the triangle with third
vertex `t`. Since a good drawing forbids an edge from crossing an adjacent
edge, this forces

```text
c=ut.
```

The same face trace for `b`, which crosses `a` and `f`, starts in the unique
triangle on the non-kite side of `zw` and ends in the opposite kite triangle.
It consequently forces

```text
b=ur.
```

There is one necessary provenance check. Reducing another `C5` makes one of
its formerly crossed edges crossing-free, so a priori a boundary edge in the
triangle--kite trace might be such a survivor rather than an edge that was
already crossing-free in `D2`. Under the present hypotheses every other
`C5` is a full pentagon and all five of its boundary edges are present. The
configuration lies inside a planar 5-cycle with no other vertices. Its five
diagonals together with the boundary form a drawn `K5`. Simplicity leaves no
additional edge inside this sealed disk, and 2-planarity prevents an external
edge from crossing the configuration. Hence its newly freed survivor remains
inside its own disk. The exceptional edges `a,d,f` lie outside every such
disk, so no other survivor can border any face traversed by `b` or `c`. The
only newly free edge of the exceptional component is `a` itself.

Consequently all five outer-boundary sides of the triangle--kite union were
already crossing-free in `D2`. The five crossed edges are

```text
zw, ur, ut, zr, wt,
```

and the union has the crossing-free, vertex-empty outer boundary

```text
u-z-t-r-w-u.
```

Those two sets partition the ten edges of the drawn `K5`. Thus the component
is exactly the five diagonals of a full 2-planar pentagon. This proves the
terminal-triangulation `C5` lemma.

## 4. Excluding the two 24-vertex profiles

For the two residual rows, the reviewed equality induction gives

| row | `e(D2)` | `x(D2)` | `m0` | full pentagons `p` | crossing `C5`s `q5` |
|---|---:|---:|---:|---:|---:|
| A | 103 | 57 | 0 | 9 | 10 |
| B | 106 | 64 | 0 | 11 | 12 |

Here `q5=(2e(D2)-8(24-2))/3`. In both rows `delta(D2)=0`, `m0=0`, and
`q5=p+1`; the terminal values in Section 2 give Euler equality. Thus the
hypotheses of the terminal-triangulation `C5` lemma hold. The final component
must also be full, forcing `p=q5`, the desired contradiction.

It follows that a 24-vertex, 132-edge graph has no drawing with at most 164
crossings, proving `(L24)`.

## 5. Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
```

Expected certificate digest:

```text
714c3d4fe1d73893d360d57c3a9805caa1178be38cb6109384d39459397a8bd7
```

The verifier checks, with exact integer and finite-set arithmetic:

- zero PRTT defect for both residual rows;
- the edge and crossing counts after all `C5` deletions;
- equality in the terminal planarization bound;
- equality `Eplan=3Vplan-6` and `3Fplan=2Eplan`;
- the unique endpoints of the two restored edges at a triangle--kite
  interface;
- that the five restored edges are exactly the complement of the outer
  pentagonal boundary in `K5` and have crossing graph `C5`; and
- the unique-exception condition `q5=p+1` and the resulting contradiction in
  both profiles.

The executable does **not** certify planar topology. The mathematical trust
boundary is the good-drawing normalization, the reviewed PRTT equality
classification of the crossing components, the reviewed Büngener--Kaufmann
deletion-profile reduction (including `m0=0`), and the already published
exact propagation from `(L24)` to the Albertson frontier. The new prose
argument is the global triangular-face trace and sealed-region provenance
check in Section 3.

## Sources and novelty scope

- J. Pach, R. Radoicic, G. Tardos, and G. Toth,
  [*Improving the Crossing Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9), especially Lemmas 3.1
  and 3.2 and Conjecture 5.7.
- A. Büngener and M. Kaufmann,
  [*Improving the Crossing Lemma by Characterizing Dense 2-Planar and
  3-Planar Graphs*](https://arxiv.org/abs/2409.01733v2), especially Theorem 6
  and Propositions 21 and 23.
