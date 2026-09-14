# An exact joint palette relation on sixteen plane points

All colourings below are ordinary proper maps to the four colours
`{0,1,2,3}`. A prescribed terminal word is the only additional restriction.
In particular, the complete relation does not assume that a terminal pair is
bichromatic. The separate palette corollary states that hypothesis explicitly.

## Physical construction

In the complex plane set

\[
A=-\tfrac12,\quad B=\tfrac12,\quad
D=\tfrac34+\tfrac{i\sqrt{15}}4,\quad
C=\tfrac{i(\sqrt{15}+\sqrt7)}4,\quad
E=-\tfrac34+\tfrac{i\sqrt{15}}4.
\]

These points form the unit cycle `A B D C E A`. Attach the two equilateral
apices to each of the edges `DC` and `EA`:

\[
X_\pm=(D+C\pm i\sqrt3(C-D))/2,\qquad
Y_\pm=(E+A\pm i\sqrt3(A-E))/2.
\]

Let `S=(A,B,D,C,E,X+,X-,Y+,Y-)`, in this order, and take `G` to be the
strict unit-distance graph on `S union (-S)`. The two copies share exactly
`A,B`, with their roles exchanged. The sixteen points are distinct after
this collision merge. Their coordinates lie in
`Q(sqrt3,sqrt5,sqrt7) + i Q(sqrt3,sqrt5,sqrt7)` and have denominator 8.
The checked coordinate fixture is [points.tsv](points.tsv).

The complete unit graph of `S` consists of its five cycle edges and the eight
spokes from `X+,X-` to `D,C` and from `Y+,Y-` to `E,A`. Thus `S` has 9
vertices and 13 edges. The complete graph `G` has precisely the two copies
of these edges, sharing `AB`: 16 vertices and 25 edges. There are no further
cross edges. The proof checker verifies all 120 unordered physical pairs,
using exact coefficients in the independent square-free radical basis.

Mark the ordered eight terminals

```
T = (X+, X-, Y+, Y-, -X+, -X-, -Y+, -Y-)
  = (5, 6, 7, 8, 12, 13, 14, 15).
```

They induce no unit edges. Each displayed adjacent pair has distance
`sqrt(3)`. Each pair's two unit-circle intersections are exactly its two
core neighbours. All eight nonterminal vertices of `G` are obtained this way.

## Exact elimination of one cell

For a four-terminal word `w`, write `P={w0,w1}`, `Q={w2,w3}`; these sets
may have size one or two. Define `R(w)` to be the following relation on the
ordered colours `(a,b)` of `A,B`:

\[
\begin{split}
(a,b)\in R(w)\quad\Longleftrightarrow\quad &a\ne b,\ a\notin Q,\\
&\exists d,c,e\in\{0,1,2,3\}:\quad
 d,c\notin P,\ e\notin Q,\\
&d\ne c,\ c\ne e,\ e\ne a,\ d\ne b.
\end{split}
\]

These are exactly the thirteen cell edges, grouped by their endpoints;
there is no relaxation. Exhausting the 64 assignments of `(d,c,e)` for each
ordered `(a,b)` therefore computes the complete cell relation. It also gives
a constructive extension whenever a relation entry is present.

The second cell interchanges `A,B` and has no other common vertex or cross
edge. Consequently an eight-terminal word `w` extends to `G` **if and only if**

\[
R(w_0w_1w_2w_3)\cap R(w_4w_5w_6w_7)^\mathsf{T}\ne\varnothing. \tag{1}
\]

This is the full joint relation, including monochromatic pairs and words
using fewer than four colours. Each cell by itself permits every one of its
15 four-terminal patterns up to colour permutation. The coupling through
the shared unit edge is therefore essential to the new eight-terminal relation.

## Complementary-palette corollary

Suppose the two `X` pairs each use a specified two-element colour set `P`,
and the two `Y` pairs each use a specified two-element colour set `Q`.
Orientations within the pairs do not matter. Then these pins extend to `G`
**if and only if `P` and `Q` are disjoint**.

Here is a direct proof, independent of the full pattern count.

* If `P=Q`, the path `A E C D` alternates through the two complementary
  colours. Its ends `A,D` differ, so `B`, adjacent to both, lies in `P`.
  Thus `R` directs an edge from `P^c` to `P`; its transpose has no common
  entry, contradicting (1).
* If `P={a,b}`, `Q={a,c}`, with fourth colour `d`, the first cell's relation
  is exactly `{(b,a),(b,c),(d,a),(d,b),(d,c)}`. To see this, `A,E` must use
  the two colours `{b,d}` and `C,D` must use `{c,d}`; their intervening edge
  `EC` gives the five listed possibilities for `AB`. This relation is
  disjoint from its transpose.
* If `P` and `Q` are disjoint, choose `A,B` to be the two colours of `P`.
  Put `E=B` and choose distinct colours `C,D` in `Q`. This colours the first
  cell. Use the exchanged endpoint assignment on the second cell. All
  required edges are proper, yielding a global extension.

The size-two hypothesis matters: all eight terminals may have colour zero
in an ordinary four-colouring. The gadget does not itself force any pair to
be bichromatic, equal-coloured, or to repeat another pair's palette.

## Full relation and essential eight-terminal cases

There are
`S(8,1)+S(8,2)+S(8,3)+S(8,4)=2795` terminal partitions using at most four
colours. Since `T` is independent, all are proper on the bare terminals.
Equation (1) admits **2691** and forbids **104**. A direct proper 16-letter
word is supplied for each admitted pattern; the checker independently
recomputes both signs by (1).

For each forbidden word, delete one terminal pin at a time while retaining
the entire physical graph. Exactly **32** forbidden words have all eight of
these relaxations feasible. They cannot be detected by any proper subset of
the eight pins. One example is `01020102`; the certificate contains eight
full words witnessing its single-pin relaxations.
When a restricted word is normalized, its colour relabelling extends to a
permutation of all four colours. Projection of the certified positive words
therefore proves extension for the original named pins as well.

Complete projection counts provide a further scope check:

| Number of retained terminals | Subsets | Subsets with a forbidden pattern |
|---:|---:|---:|
| 1 | 8 | 0 |
| 2 | 28 | 0 |
| 3 | 56 | 0 |
| 4 | 70 | 0 |
| 5 | 56 | 0 |
| 6 | 28 | 2 |
| 7 | 8 | 4 |

These statements concern the designated eight terminals, not every vertex
subset. In particular they do not assert graph minimality. The graph has a
unit triangle and a checked proper three-colouring, so its chromatic number
is **exactly three**, not five.

## Construction budget and the closed first attachment

If an exact physical host contains an isometric image of all eight terminals,
adjoining `G` adds at most eight vertices. A host on at most 500 vertices
would therefore stay within 508. If every four-colouring of that host induces
a forbidden terminal pattern, restriction proves that the union is not
four-colourable. Coincidences and extra unit edges cannot invalidate that
implication; they must still be merged and included before certification.
No host satisfying this forcing premise is supplied here.

The first host tried was the existing 421-point Haugland difference graph.
[host_gate.py](host_gate.py) reconstructs its 88,410 physical pairs and finds
126 at distance `sqrt(3)`. Both unit-circle intersections of each pair already
belong to the host. Explicitly, for endpoints `u,v` the two roots are

\[
 (u+v)/2\ \pm\ (i\sqrt3)(v-u)/6.
\]

All 252 root occurrences are checked for membership and unit distances to
both endpoints. Therefore **any** isometric terminal attachment of the
present comparator to this host already has every one of its eight core
vertices in the host. No new point or unit edge can result. This conclusion
requires no enumeration of possible eight-terminal frames and no new SAT
query. The attachment is retired. This is not a closure theorem for larger
circle constructions, different hosts, or arbitrary plane graphs.

The elementary odd-cycle list-colouring and equilateral-diamond mechanisms
are standard. No historical priority, smallest-gadget, or record-improvement
claim is made for this explicit source or relation. Its remaining record
obstacle is an economical **physical input-palette forcing premise** at the
specified terminal geometry. Copy counts and phase windows are not increased
in the absence of that premise.
