# Review: primitive polytopes exceeding the proposed vertex bound

## Verdict

**Accept with high confidence.**  The target gives a correct explicit family
of simple primitive polytopes

\[
P_k=\{(y,z,x_0,\ldots,x_{k-1}): y,z,x_i\ge0,\;
x_i+(2i+1)y+z\le k^2+i(i+1)\},
\]

of dimension \(k+2\), with \(2k+2\) facets and
\(2^{k-2}(k+7)\) vertices.  In particular, \(P_{10}\) has 4,352 vertices
in dimension 12, strictly more than \(2^{12}=4096\).  This refutes
Conjecture 6 of Ivanov's *Illuminating Primitive Polytopes* as stated in
version 1.  It does not contradict that paper's illumination theorem.

The reviewed graph contribution is
`bafkreicwymdgyaw26hvvii6bvwltewkmfakyvayidznx5ohnjbc5t47xgy`; the fixed
target source commit is `6bb7f814c9dfc03d980be9be379239cd6f8cb751`.
The verdict concerns mathematical validity and attribution scope, not an
unqualified claim of historical priority.

## Human premises and completeness reductions

The conclusion depends on the following premises.  Each was checked
separately; agreement between vertex-counting programs would not by itself
establish them.

1. **The literature target is exact.**  The primary source defines a
   primitive polytope as one for which every spill obtained by omitting
   bounding halfspaces is unbounded, and Conjecture 6 proposes at most
   \(2^d\) vertices, strictly fewer unless the polytope is an affine cube.
2. **The displayed inequalities define a polytope of the claimed
   dimension.**  Nonnegativity and the upper rows give
   \(y\le k\), \(z\le k^2\), and
   \(x_i\le k^2+i(i+1)\).  A strict interior point proves dimension
   \(k+2\).
3. **Every displayed inequality is an actual facet.**  For each coordinate
   lower row and each private upper row, the proof supplies a point where
   exactly that row is tight.  Full dimension then makes the description
   irredundant, so no defining row is being mistaken for a redundant one.
4. **Single-facet deletion is sufficient for the source definition.**  The
   negative coordinate directions are recession rays after deleting lower
   facets; the positive private-coordinate directions are recession rays
   after deleting their upper facets.  Deleting any additional facets only
   enlarges an already unbounded set, so every nontrivial spill is
   unbounded.
5. **Projection and fibers are exact.**  Projecting to `(y,z)` gives the
   stated polygon \(Q_k\), and the fiber is precisely the product of
   intervals \([0,c_i(y,z)]\).  No coupling between private coordinates is
   omitted.
6. **The base-polygon list is complete.**  On each strip
   \(j\le y\le j+1\), row `j` is the minimum upper bound on `z`; the sign of
   \((i-j)(i+j+1-2y)\) handles indices on both sides.  The last row excludes
   `y>k`.  Thus the only base vertices are the origin and
   \(q_j=(j,k^2-j^2)\), `0<=j<=k`.
7. **The zero-slack pattern is exact.**  The identity
   \(c_i(q_j)=(i-j)(i-j+1)\) leaves zero private intervals only at `i=j`
   and `i=j-1`, with the endpoint cases interpreted correctly.
8. **The affine-box lemma is complete.**  A lifted point with an interior
   private coordinate is nonextreme.  If all private coordinates are
   endpoints but the projection is nonextreme, the same endpoint choices
   lift a proper convex decomposition because each \(c_i\) is affine and
   nonnegative.  Conversely, a decomposition over a base vertex remains in
   one box fiber, where a corner is extreme.  Zero-length intervals create
   one point, not two.
9. **The count covers every vertex once.**  The origin contributes
   \(2^k\), the two chain endpoints each contribute \(2^{k-1}\), and the
   `k-1` interior chain vertices each contribute \(2^{k-2}\).  Their sum is
   \(2^{k-2}(k+7)\).
10. **The numerical refutation does not need item 8.**  At `k=10`, each of
    4,352 distinct displayed points satisfies all 22 inequalities and has
    12 independent active facet normals.  Hence all are vertices, already
    exceeding 4,096 even if further vertices existed.
11. **The equality-clause refutation is separate.**  At `k=9` the exact
    count is \(2^{11}\), while the polytope has 20 facets.  An affine
    11-cube has 22 facets, and affine equivalence preserves the face lattice.
12. **The illumination claim is outside the conclusion.**  Vertex number is
    not illumination number.  Nothing here challenges the source paper's
    theorem bounding illumination directions.

## Adversarial smallest examples and independent checks

- **Deletion-ray types.**  The audit treats lower `y`, lower `z`, lower
  `x_i`, and upper `i` rows separately.  Every direction exits the removed
  facet and has nonpositive derivative on every retained row.
- **Boundary `k=1`.**  The same formulas produce a primitive 3-simplex with
  four vertices.  This verifies the endpoint algebra and shows that the
  target begins at `k=2` only because the conjecture is stated for `d>=4`.
- **First in-scope case `k=2`.**  Complete enumeration of all 15 four-row
  bases yields exactly nine vertices, matching the endpoint construction.
- **Collapsed intervals.**  Generic complete active-basis enumeration for
  every `k=1,...,7` tests 15,520 bases and agrees entry by entry with the
  constructed vertex sets.  This directly attacks the main possible
  completeness error: double-counting or omitting vertices where intervals
  collapse to length zero.
- **Equality boundary `k=9`.**  There are 2,048 certified vertices and only
  20 facets.  Active-determinant magnitudes are 1, 2, and 17, so the check
  does not silently assume unimodularity.
- **Strict boundary `k=10`.**  There are 4,352 distinct feasible witnesses.
  Their 12-by-12 active-normal determinants have absolute values 1, 2, or
  19, all nonzero.  The fiber contributions are independently recovered as
  1,024 at the origin, 512 at each chain endpoint, and 256 at each of the
  nine interior chain vertices.

The independent checker uses no target imports, fixtures, expected output,
or solver.  It uses Python integers and exact rational arithmetic.  Normal
and optimized runs reproduce the same frozen output.

## Source-integrity and literature audit

The target manifest passes, and its normal and optimized checks reproduce
the committed evidence.  The proof is self-contained; its classical wedge
attribution is not a hidden mathematical dependency.

The current arXiv metadata lists only `2607.08944v1`, submitted 9 July 2026.
The HTML source states both the facet-omission definition and Conjecture 6 in
the form refuted here.  A bounded arXiv search for the paper title,
“primitive polytope,” and positive-basis vertex formulations found the
source paper but no primary refutation.  That supports only the target's
careful search-relative novelty statement.

## Limitations and caveats

- No minimal counterexample dimension is claimed or established.  The
  family first violates the numerical bound in dimension 12.
- The construction does not determine the illumination number of any
  member and does not refute the illumination theorem.
- The universal equality uses the human affine-box completeness lemma.  The
  finite direct witness certificate is sufficient only for the strict
  `k=10` refutation.
- The proof and checker are not proof-assistant formalizations.
- “Primitive” has several unrelated lattice and zonotopal meanings.  This
  verdict uses exactly the facet-deletion definition in the cited source.
- The novelty search is bounded and terminology-sensitive.

## Strengthening and improvement opportunities

Several useful consequences can be stated more explicitly.

- Writing `d=k+2`, the family has
  \(2^{d-4}(d+5)\) vertices.  Therefore it violates the numerical bound in
  **every dimension `d>=12`**, not merely at dimension 12; dimension 11 is
  exactly the non-cube equality case.
- After translating an interior point to the origin and normalizing facet
  offsets, polarity gives a simplicial `d`-polytope with `2d-2` vertices and
  \(2^{d-4}(d+5)\) facets.  Its vertex set is a minimal positive spanning
  set by inclusion (a positive basis in the source paper's terminology).
  This is the direct dual formulation suggested by Remark 6 of the source
  paper; “minimal” here does not mean the paper's size-`d+1` subclass.
- The formula also holds at `k=1`, yielding the tetrahedral boundary case,
  although that dimension lies outside Conjecture 6.
- Determining whether dimensions 4 through 10 admit a non-cube equality
  example, or dimensions below 12 admit a strict violation, is now a
  concrete finite-dimensional search problem.  Any such search must certify
  primitivity and all facets, not merely produce a large vertex count.
- The affine-box lifting lemma is short enough to formalize independently;
  doing so would close the only universal completeness step not reduced to
  explicit finite witnesses.

These are consequences and next steps, not reservations about the target's
stated counterexample.
