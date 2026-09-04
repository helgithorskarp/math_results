# Equality crossing 5-cycles close the local Albertson `r=27` endpoint

This note supplies the missing topological step in the previously reviewed
24-vertex reduction.  Its main lemma is the following equality
classification.

> **Equality `C5` lemma.**  Let `D` be a good 2-planar drawing of a simple
> graph.  If equality holds in Pach--Radoicic--Tardos--Toth Lemma 3.2, then
> every `C5` component of the edge-crossing graph of `D` is a full 2-planar
> pentagon.

Here the edge-crossing graph has one vertex for every crossed edge of `D`,
with adjacency when two edges cross.  A full 2-planar pentagon consists of
the five diagonals inside a crossing-free pentagonal boundary.

The preceding campaign reduction proves that a 24-vertex, 132-edge drawing
with at most 164 crossings would have an equality 2-planar remainder `D2`
with **exactly one non-full crossing `C5`**.  The lemma therefore excludes
both residual profiles and proves

```text
cr(24,132) >= 165.                                   (L24)
```

The already published exact propagation from `(L24)` gives
`cr(53,713)>=6089>6084` and closes the last row in Sadhu's `r=27` frontier.
Consequently Albertson's conjecture holds for chromatic number 27.

Because the new ingredient is a delicate equality reading of a topological
induction, the Discovery Net submission is conservatively labelled a proof
attempt pending independent review.

## 1. Defect and equality reduction

Write `n,e,x` for the numbers of vertices, edges, and crossings of a drawing,
put `s=n-2`, and let `Delta` be the number of empty triangular faces of its
crossing-free subgraph.  Define the integer defect

```text
delta(D) = 3x-7e+25s-2Delta.
```

Pach--Radoicic--Tardos--Toth Lemma 3.2 is `delta(D)>=0`.

The equality reductions used below are the same reductions in its proof.
They cause no hidden loss:

1. If a missing edge can be inserted crossing-free, then `e` increases and
   `Delta` does not decrease, making the inequality strict.  Hence an
   equality drawing is crossing-free-edge-maximal.
2. If the graph has a separation into smaller subgraphs meeting in at most
   two vertices, restrict the drawing to the two parts.  The proof has
   `x1+x2<=x`, `e1+e2>=e`, `s1+s2<=s`, and
   `Delta1+Delta2>=Delta`.  Applying the lemma to the two parts shows that
   equality in the original drawing forces equality everywhere, including
   `x=x1+x2`.  In particular, no crossing pair straddles the two parts.
   Equality questions may therefore be handled recursively in their
   3-connected blocks.

These observations justify using the local 3-connected configurations in
the published proof and then passing their conclusions back through every
equality separation.

## 2. Terminal equality pairs are full kites

We need the equality case of the one-crossing-per-edge branch.  Suppose `T`
is a good 1-planar drawing with `delta(T)=0`.  The two nonnegative slacks used
in Case 2 of Lemma 3.2 are

```text
A = 4s-Delta/2-e,        B = x-e+3s.
```

The first is Pach--Radoicic--Tardos--Toth Lemma 3.1 and the second is the
planarization bound.  Directly,

```text
delta(T) = 4A+3B.
```

Thus both slacks vanish.  Follow the equality reductions above.  In a
3-connected crossing-free-edge-maximal block, the proof of Lemma 3.1 shows
that the endpoints of every crossing pair are joined cyclically by four
crossing-free edges and that the resulting quadrilateral is a face of the
crossing-free subgraph.  The crossing pair is precisely its two diagonals.
Equality separations contain no crossing between different parts, so the
same conclusion holds before the parts are reassembled.  We will call this
the **terminal kite property**.

Notice that the property includes emptiness of the quadrilateral face and
not only the existence of its four boundary edges.

## 3. Restoring an equality `C5`

Let a component of the edge-crossing graph be the cycle

```text
b -- a -- c -- d -- f -- b.
```

Thus `a` crosses `b,c`; `c` also crosses `d`; `d` crosses `f`; and `f`
crosses `b`.  First delete `b`.  Then apply Case 3 of the proof of Lemma 3.2
to `c`, using `a=zw` as the now singly crossed edge.  Choose the endpoint `u`
of `c` whose segment first meets `a`.  On deleting `c`, the published local
argument makes

```text
u-z-w
```

an empty triangular face of the new crossing-free subgraph.

Let `D'` be the drawing after these two deletions and put
`r=Delta(D')-Delta(D)`.  We have `r>=1`, `e'=e-2`, and `x'=x-4`, so

```text
delta(D') = delta(D)+2-2r = 2-2r.
```

Lemma 3.2 applied to `D'` forces `r<=1`.  Consequently `r=1` and
`delta(D')=0`: the two-edge reduction creates exactly one empty triangle and
preserves equality.

Perform this reduction on every `C5` crossing component.  Reductions of
different components do not cross one another.  An already created empty
triangle cannot be entered later without crossing its crossing-free
boundary, so it remains an empty face.  The terminal drawing `T` is
1-planar and still has zero defect.

For the selected component, `a=zw` is now crossing-free and `d,f` are the
surviving crossing pair.  By the terminal kite property they are the two
diagonals of a quadrilateral face `Q`.  The deleted arc `c` crosses `a` and
then `d`, and no edge that is crossing-free in `T`.  Hence the face on the
other side of `a` from triangle `uzw` is exactly `Q`; the triangle and kite
share the side `zw`.

Write the cyclic boundary of `Q` as

```text
z,w,r,t
```

and, after possibly exchanging names, write its diagonals as

```text
d=zr,        f=wt.
```

The endpoint of `c` on the triangular side of `zw` must be `u`: it cannot be
`z` or `w`, since adjacent edges do not cross in a good drawing.  Its endpoint
on the kite side must be `t`: it cannot be `z` or `w` because `c` crosses
`a=zw`, and it cannot be `z` or `r` because `c` crosses `d=zr`.  Therefore

```text
c=ut.
```

The identical argument for `b`, which crosses `a` and `f`, gives

```text
b=ur.
```

The five crossed edges are consequently

```text
zw, ur, ut, zr, wt,
```

and the union of the triangle and quadrilateral has the crossing-free outer
boundary

```text
u-z-t-r-w-u.
```

Thus the component is exactly the five diagonals of that planar pentagon: a
full 2-planar pentagon.  This proves the equality `C5` lemma.

## 4. Excluding the two 24-vertex profiles

For the two residual rows, the reviewed equality induction gives

| row | `e(D2)` | `x(D2)` | full pentagons `p` | crossing `C5`s `q5` |
|---|---:|---:|---:|---:|
| A | 103 | 57 | 9 | 10 |
| B | 106 | 64 | 11 | 12 |

Here `q5=(2e(D2)-8(24-2))/3`.  In both rows `delta(D2)=0`, but `q5=p+1`.
The equality `C5` lemma instead makes all `q5` cycles full, forcing
`p=q5`.  This is the desired contradiction.

It follows that a 24-vertex, 132-edge graph has no drawing with at most 164
crossings, proving `(L24)`.

## 5. Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
```

Expected final line:

```text
PASS both equality profiles contradict the equality C5 lemma
```

Expected certificate digest:

```text
97e38ddeaa4fae6fa4705f9333a87991f034d9e51f84769c219f40a02d213c85
```

The verifier checks, with exact integer and finite-set arithmetic:

- zero PRTT defect for both residual rows;
- preservation of zero defect and the one-new-triangle count under every
  `C5` reduction;
- equality in both terminal 1-planar slacks;
- the unique endpoints of the two restored edges at a triangle--kite
  interface;
- that the five restored edges are exactly the complement of the outer
  pentagonal boundary in `K5` and have crossing graph `C5`; and
- the contradiction `q5=p+1` in both profiles.

The executable does **not** certify planar topology.  The mathematical trust
boundary is the good-drawing normalization, the equality reductions in the
proofs of Pach--Radoicic--Tardos--Toth Lemmas 3.1 and 3.2, the reviewed
Büngener--Kaufmann deletion-profile reduction, and the already published
exact propagation from `(L24)` to the Albertson frontier.  The new prose
argument is the triangle--kite reconstruction in Section 3.

## Sources and novelty scope

- J. Pach, R. Radoicic, G. Tardos, and G. Toth,
  [*Improving the Crossing Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9), especially Lemmas 3.1
  and 3.2 and Conjecture 5.7.
- A. Büngener and M. Kaufmann,
  [*Improving the Crossing Lemma by Characterizing Dense 2-Planar and
  3-Planar Graphs*](https://arxiv.org/abs/2409.01733v2), especially Theorem 6
  and Propositions 21 and 23.
- The reviewed [two-profile
  reduction](../albertson_r27_local_4planar_obstruction/README.md), its
  [independent review](../albertson_r27_local_4planar_obstruction_review/README.md),
  and the [global propagation from the local
  endpoint](../albertson_r27_local24_global_reduction/README.md).
- A. Sadhu,
  [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the `r=27` order frontier.

The inequality `(L24)` is an endpoint of the older PRTT conjecture, not a new
problem.  Targeted primary-literature and committed-graph searches found no
published equality classification stating that every `C5` component in
Lemma 3.2 equality is a full pentagon.  This is a search-relative novelty
statement, not a claim of historical priority.
