# A fixed-Moser three-copy family is four-colorable at every angle

Let `A` be the archived Parts `v159e646` point set, with vertex 0 at the
origin, and set

\[
t=\frac{5+i\sqrt{11}}6,\qquad B=A\cup tA.
\]

**Theorem.** For every Euclidean isometry `g` fixing the origin, the strict
unit-distance graph on `B union g(A)` is four-colorable. The family has at
most 450 vertices. Both rotations and reflections, at arbitrary angles, are
covered.

The multiplier `t` is fixed in this theorem. Other relative placements of
the first two copies, different shared vertices, and mixed gadget types
are not asserted to be excluded.

## 1. Exact construction and field dependency

Use the restricted complex field

\[
E=\mathbb Q(i\sqrt3,i\sqrt{11})
  =R(\alpha),\quad R=\mathbb Q(\sqrt{33}),\quad\alpha=i\sqrt3.
\]

The four rational coefficients of a point mean
`a+b sqrt(33)+c i sqrt(3)+d i sqrt(11)`. Both `A` and `B` lie in `E`.
The multiplier is a unit since `(25+11)/36=1`.

Exact reconstruction from the hash-pinned coordinates gives:

| Quantity | Value |
|---|---:|
| Vertices / strict unit edges of `A` | 159 / 646 |
| Overlaps of `A` and `tA` | 26 |
| New edges between those copies | 18 |
| Vertices / strict unit edges of `B` | 292 / 1,251 |

Label `B` by first retaining `A` in its input order, then appending previously
unseen points of `tA` in the same source order. The shared origin remains
vertex 0. These conventions specify the coloring-certificate indices.

The previously proved [field-coloring theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
four-colors the entire complex field `E`. This is an essential mathematical
dependency for the in-field branch. It is not a coloring theorem for the
larger Cartesian plane `Q(sqrt(3),sqrt(11))^2`.

## 2. Complete reduction for two different components

Write `g(z)=uz` or `g(z)=u conjugate(z)`, with `|u|=1`. In the two parities,
let `A'` be `A` or `conjugate(A)`, preserving source labels. Its labeled
internal graph is unchanged.

If `u in E`, then `B union uA'` is a subset of `E` and the field-coloring
theorem applies, including every additional overlap and edge.

Suppose `u not in E`. A nonzero coincidence `b=ua` with `b in B`, `a in A'`
would imply `u=b/a in E`. Thus the origin is the sole overlap, and there are
exactly `292+159-1=450` distinct vertices. Their internal edges number
`1251+646=1897`; the two internal edge sets are disjoint after identifying
only the origin. Edges incident to the origin are already internal.

If there is no new cross edge between nonzero points of the components,
proper component colorings can simply be permuted to agree at the origin.
Otherwise, fix such an edge `|b-ua|=1` and put

\[
c=\overline b a,\qquad S=|b|^2+|a|^2-1,\qquad
\Delta=4|b|^2|a|^2-S^2.
\]

Here `c != 0`, `c in E`, and `S,Delta in R`. Expanding the edge equation and
using `u conjugate(u)=1` gives

\[
cu^2-Su+\overline c=0.
\]

For `Delta<0` there is no unit root. For `Delta>=0`, the roots are
`(S +/- sqrt(-Delta))/(2c)` and have modulus one. For positive `Delta`, a
root lies in `E` exactly when `Delta/3` is a square in `R`: a square root of
the negative real number `-Delta` inside `E` must have the form
`alpha y`, with `y in R`. The double-root case `Delta=0` also lies in `E`.

After discarding these already-settled cases, each pair defines an
irreducible monic quadratic

\[
P_{b,a}(X)=X^2-(S/c)X+\overline c/c\quad\text{over }E.
\]

Two monic quadratics have an outside-`E` root in common exactly when they
are equal, by uniqueness of that root's minimal polynomial. Therefore each
class consists of the **complete** new cross-edge set at either of its two
distinct unit roots. It is neither a subset of selected edges nor an angle
sample. Conversely, both roots realize every edge in the class. Different
classes in one parity have disjoint multiplier sets.

This is the [earlier fixed-origin quadratic reduction](../hadwiger_nelson_nonmono159_origin_pencil/PROOF.md)
applied to unequal components `B` and `A`. Its argument does not require
them to be congruent. The implementation now uses their different sizes,
norm lists, internal graphs, and coloring libraries explicitly.

## 3. Exact census and positive certificate

There are `291*158=45,978` nonzero labeled pairs per parity. In both parities,
the exhaustive rational-arithmetic classification is:

| Pair class | Count |
|---|---:|
| Negative discriminant | 5,747 |
| Unit roots in `E` | 22,966 |
| Two unit roots outside `E` | 17,265 |

The final row groups as follows:

| Parity | Quadratic classes | Labeled isometries |
|---|---:|---:|
| Rotation | 2,391 | 4,782 |
| Reflection | 2,216 | 4,432 |
| Total | 4,607 | 9,214 |

The classes have between 1 and 30 new cross edges. Their strict graphs
therefore have 450 vertices and between 1,898 and 1,927 edges. The full
histograms are in `expected.json`. There are 4,605 distinct labeled
cross-edge sets across the two parities. No quotient by geometric symmetry
or abstract graph isomorphism is used.

`colors_A.txt` contains five proper colorings of `A`; `colors_B.txt` contains
three of `B`. Every coloring has color 0 at the origin, and every internal
edge is checked. For each class, the verifier finds a pair of rows `f,h`
and one of the six permutations `pi` of four colors fixing 0, with

\[
f(b)\ne\pi(h(a))\quad\text{for every new cross edge }(b,a).
\]

The resulting union coloring agrees at the origin, respects both internal
graphs, and is checked on every new cross edge. All 4,607 classes have a
witness; there are zero residuals. These positive certificates complete
the last branch of Section 2 and prove the theorem.

The eight coloring strings total 1,679 bytes. Discovery started with four
previously certified `A` colorings and two residue colorings of `B`. One
satisfiable 450-vertex graph-coloring query supplied one additional row for
each component. It used CaDiCaL through `python-sat==1.8.dev24`. Verification
does not invoke a solver or assume its soundness; every positive witness is
published and checked directly.

## 4. Independent checks and trust

`verify.py` uses the published four-dimensional field arithmetic and the
exact real-sign and real-square criteria from the previous census. These
decisions use arbitrary-precision rationals and integer square roots.

`audit.py` imports none of that implementation. It reconstructs `B` using
the alternative `E=R+alpha R` arithmetic from the previous independent audit,
with `t=5/6+alpha sqrt(33)/18`. It groups by `c/S` when `S!=0` and by the
real projective direction of `c` when `S=0`. This avoids the main
leading-coefficient normalization. Its canonical hashes agree for every
pair classification and every edge-group partition. It independently
checks both internal graphs, the inner overlaps, all coloring rows, and
coverage of every class.

`check_example.py` independently constructs the four placements
`u=(5 +/- i sqrt(39))/8` in both parities. It uses the eight-element real
radical basis of `Q(sqrt(3),sqrt(11),sqrt(13))` at integer scale 288 and
directly rebuilds every strict edge. Both rotations have 1,907 edges and
both reflections 1,905 edges, always on 450 points; actual union colorings
are verified. It imports neither enumeration nor other arithmetic code.

All three checks passed. The continuous-to-finite bridge and the field
coloring remain ordinary unformalized mathematics. The finite certificate
trusts exact Python arithmetic, the published programs, and hash-pinned
coordinates. No numerical unit-distance test, UNSAT verdict, omitted large
certificate, or proof-assistant formalization is claimed.

Since `A subset B`, the new theorem also implies the prior two-copy
fixed-origin exclusion by restriction. It does not imply a general theorem
about arbitrary three-copy placements. No graph improving the 509-vertex
record is produced, and no priority claim is made for the elementary
quadratic or color-permutation methods.

The original gadget is from [Parts' graph-minimization work](https://arxiv.org/abs/2010.12665);
its exact archive provenance is in [SOURCE.md](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md).
The 509 benchmark is also identified in the introduction of
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
