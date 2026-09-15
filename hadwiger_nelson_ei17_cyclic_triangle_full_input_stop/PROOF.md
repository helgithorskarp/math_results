# Proof and certificate semantics

## 1. Exact source

The sibling source checker defines a point set `P={p_0,...,p_16}` as the unique
root, inside a rational radius-`10^-18` box, of 30 independent squared-unit
equations after pinning one source edge.  A contraction argument proves
existence and uniqueness in the box.  Exhaustive interval tests prove that the
17 points are distinct and that their complete strict unit graph is exactly
the 31-edge graph in `seed_edges.json`.  Exhaustive three-colour search and a
proper four-colouring prove `chi(P)=4`.

This package checks the SHA-256 digest of every reused source file and reruns
that certificate.  It relies on the exact root selected by the box, not on the
decimal midpoint or a conjectured number field.

## 2. Cyclic frame enumeration

Fix an ordered source edge `(i,j)`.  Since `|p_j-p_i|=1`, exactly two plane
isometries take it to the ordered segment `AB`: the orientation-preserving map

```text
z -> conjugate(p_j-p_i) * (z-p_i)
```

and the orientation-reversing map

```text
z -> (p_j-p_i) * conjugate(z-p_i).
```

Both formulas are evaluated by outward rational interval arithmetic.  The
images of the anchor endpoints are replaced by exact `A,B` boxes; this is an
exact consequence of the source unit equation and prevents dependency
widening.  Reversing the source edge, reflecting or not, and choosing any of
31 edges gives all 124 labelled frames in the declared architecture.

Multiplication by `zeta=(-1+i sqrt(3))/2` followed by translation by 1 cycles
the equilateral vertices `A -> B -> C -> A`.  Applying this map twice supplies
the other two copies.  Their anchor boxes are likewise replaced by the exact
equilateral vertices.

## 3. Collisions and complete contacts

The construction declares exactly three two-label collision groups:

```text
A: (copy 0,i)=(copy 2,j)
B: (copy 0,j)=(copy 1,i)
C: (copy 1,j)=(copy 2,i).
```

For every two labels in distinct declared groups, at least one coordinate interval
is disjoint.  Hence no other collision is possible.  Each frame therefore has
exactly `51-3=48` physical points.

For every unordered pair of physical groups, the checker encloses squared
distance for every representing label pair.  If every enclosure excludes one,
the physical pair is a certified nonedge.  Otherwise the pair is placed in the
conservative edge set.  Thus the actual complete strict unit graph is a
subgraph of the checked conservative graph, and no physical unit contact is
ever omitted.  All 93 inherited source edges are checked to occur.  There are
116 frames with no possible extra pair and eight with three possible extra
pairs.  Resolving the latter equalities is unnecessary: a proper colouring of
the larger graph is proper on every possible actual graph.

The 93-edge inherited union is connected and remains connected after deletion
of any single vertex or any single edge.  This is checked directly for all 124
frames, so the negative result is not explained by an articulation or bridge.

## 4. Complete source-colouring projection

`verify.py` enumerates colourings in restricted-growth form: colour labels are
introduced in order, so exactly one representative of every orbit under the
global `S_4` action occurs.  A separate fixed-vertex-order enumeration in
`controls.py` confirms the count 85,088.

For a source word `w`, write `a=w(i)` and `b=w(j)`.  They differ because
`ij` is an edge.  Choose any `c` different from both.  On copy 1 apply a colour
permutation taking `(a,b)` to `(b,c)`; on copy 2 apply one taking `(a,b)` to
`(c,a)`.  The three words agree at `A,B,C` and remain proper within their
copies.  This proves extension whenever there is no cross-copy edge, covering
116 frames.  The checker instantiates and verifies the formula for all 85,088
source words.

For each of the eight remaining conservative graphs, copy 0 is fixed to each
source word.  The other 31 physical vertices receive four-bit colour domains
after deleting colours used by fixed neighbours.  Unit propagation plus finite
branching returns a concrete colour for every new vertex.  Every returned word
is checked directly against its initial domains and all new--new edges.  This
gives `8*85088=680704` checked extensions.  Since global colour permutations
preserve properness, the orbit representatives cover all labelled complete
source four-colourings.

Consequently the projection of the composite four-colouring relation onto the
entire first EI17 copy equals the complete source relation.  Every physical
graph is at most four-chromatic.  It contains copy 0, which is four-chromatic,
so its chromatic number is exactly four.

## 5. Arithmetic and trust boundary

Coordinate intervals have integer endpoints over `Q=2^100`.  Addition and
subtraction are exact on this grid; multiplication, division, and square root
round outwards using integer arithmetic.  Pair separation and exclusion of
squared distance one are integer comparisons.  Python integers do not overflow.

The proof trusts Python's integer and `Fraction` arithmetic and the checked
interval formulas.  The extension algorithms are used only to find positive
witnesses, which are then verified edge by edge.  No negative solver answer is
used.  Optimized Python follows the same `require` checks; no proof obligation
depends on `assert`.
