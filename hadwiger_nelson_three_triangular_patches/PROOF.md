# Exact classification of three pairwise-irrational P48 patches

Put

\[
 \omega=(1+i\sqrt3)/2,\qquad R=\mathbb Z[\omega],\qquad
 K=\mathbb Q(\omega),
\]

and let

\[
 P=P_{48}=\{a+b\omega:a,b\in\mathbb Z,\ a^2+ab+b^2\le48\}.
\]

Every graph below is the **strict** unit-distance graph: every pair of distinct
physical points at distance one is an edge. No planarity assertion is made.

## The theorem

**Theorem.** Let `alpha_0,alpha_1,alpha_2` have complex norm one and suppose

\[
 \overline{\alpha_i}\alpha_j\notin K\quad(i\ne j).
 \tag{1}
\]

Then

\[
 G=\operatorname{UD}(\alpha_0P\cup\alpha_1P\cup\alpha_2P)
\]

has 505 vertices and chromatic number at most four. It has chromatic number
four if and only if some pair of patches has a proper cross edge whose two
endpoints both have residue zero under

\[
 \rho(a+b\omega)=a-b\pmod3.
 \tag{2}
\]

In every other case its chromatic number is three.

This theorem closes the full continuum of rotations satisfying (1), not just
the finite exceptional list used by the computation.

## Physical order and the one-dimensional pair constraint

The patch has 169 points and 456 internal unit edges. If nonzero points
`alpha_i z=alpha_j w` coincided, then
`conjugate(alpha_i)*alpha_j=z/w` would belong to `K`, contradicting (1).
Thus the three copies meet only at their common origin and have
`3*169-2=505` physical points.

The residue map (2) properly three-colours a triangular lattice. The patch is
triangle-connected: after fixing the colours on the central unit triangle,
166 forced third-vertex steps colour every other vertex. Its proper
three-colouring is consequently unique up to a permutation of colours.

For a relative rotation `alpha` outside `K`, all nontrivial cross contacts lie
on one rational contact equation. The two-patch argument proves that there is
an `epsilon` in `{1,-1}` such that every cross edge with two nonzero residues
satisfies

\[
 \rho(z)\rho(w)=\epsilon.
 \tag{3}
\]

The full argument is recorded in the
[two-lattice proof](../hadwiger_nelson_triangular_overlays/PROOF.md). It gives
a four-colouring of the two patches, and a three-colouring exactly
when there is no cross edge joining two residue-zero endpoints. Conversely,
such a zero-to-zero edge forbids three colours by uniqueness of the patch
three-colouring. This is the exact two-patch obstruction used below.

Cross contacts involving the common origin occur for every rotation, but each
is already an internal edge of one patch after the three origin labels are
identified. Call a pair of layers *active* when it has another cross contact,
and form the active graph `H` on the three layer indices.

## Forests of active pairs

If `H` is a forest, choose a vertex incident with every edge of `H`; for a
three-vertex path this is its middle vertex. Give that root patch colours
`A,+,-` according to residues `0,1,-1`.

For each adjacent leaf, use (3) to assign its two nonzero residue classes the
opposite sign colours. Give its nonorigin residue-zero vertices colour `A` if
the interface has no zero-to-zero edge, and a fourth colour `B` if it does.
The shared origin retains colour `A`. This is proper within a leaf because a
residue class is independent. It is proper across the interface by (3); a
mixed zero/nonzero edge has different colour types, while a proper zero/zero
edge has colours `A,B`. Leaves have no mutual cross contacts. Isolated layers
can plainly be coloured from `A,+,-`.

This constructs a four-colouring for every forest. If no active interface has
the zero-to-zero obstruction, `B` is unnecessary and the construction uses
three colours. If an interface does have the obstruction, its two-patch
subgraph proves that four colours are necessary.

## Complete active triangles

It remains to classify the case `H=K_3`. Rotate the entire configuration so
that `alpha_0=1`, and write `alpha=alpha_1`, `beta=alpha_2`. Then `alpha`,
`beta`, and `conjugate(alpha)*beta` must all be exceptional irrational contact
rotations for `P`.

Write a point in Cartesian form as

\[
 z=(X+i\sqrt3Y)/2,
\]

where `X,Y` are integers of the same parity. For ordered nonzero patch points
`z=(X,Y)` and `w=(A,B)`, the equation `|z-alpha*w|=1`, with
`alpha=x+i sqrt(3)y`, becomes a rational line

\[
 ux+vy=k,
\]

where, before primitive normalization,

\[
 u=XA+3YB,\qquad v=3(YA-XB),\qquad
 k=(X^2+3Y^2+A^2+3B^2-4)/2.
 \tag{4}
\]

The line meets the ellipse `x^2+3y^2=1` when

\[
 D=3u^2+v^2-3k^2\ge0.
\]

Putting `S=3u^2+v^2`, its two roots are

\[
 x={3uk\pm v\sqrt D\over S},\qquad
 y={vk\mp u\sqrt D\over S}.
 \tag{5}
\]

The exact Cartesian enumeration finds 834 primitive contact lines. Precisely
360 have positive nonsquare `D`, yielding 720 distinct rotations outside
`K`; the remaining lines are irrelevant under (1). For each nonsquare line,
the verifier substitutes (5) into all `169^2` cross-pair squared norms. This
both reconstructs its full strict cross-edge set and proves that the only
coincidence is the common origin. Across the two conjugate roots this accounts
for 10,281,960 exact norm evaluations.

To test the third interface without floating point, each rotation is stored as

\[
 (x_0+x_1\sqrt d)+i\sqrt3(y_0+y_1\sqrt d)
\]

with squarefree `d`. Products are expanded as rational linear combinations of
square roots of squarefree integers. The verifier enumerates every unordered
pair `{alpha,beta}` among the 720 rotations and retains it exactly when
`conjugate(alpha)*beta` is also in the inventory. This produces 216 complete
active triangles. There are no omitted cases: any proper cross edge supplies
one of the primitive equations (4), and normalization fixed `alpha_0=1`.

All 216 triangles have the following exact properties:

| Quantity | Census |
|---|---:|
| squarefree radicand on all three sides | 21 |
| side chromaticities | `(3,3,3)` in all 216 cases |
| proper cross-edge counts | `(6,12,12)` in all 216 cases |
| strict graph order | 505 |
| strict graph size | 1,398 |
| distinct labelled edge streams | 114 |

The committed certificate contains one 505-digit word over `{0,1,2}` for
each distinct edge stream. The independent verifier rebuilds every one of the
216 strict graphs, requires repeated hashes to have identical edge tuples,
requires the certificate keys to equal the reconstructed inventory, and tests
every edge against its word. All words are proper. Each graph contains an
internal unit triangle, so its chromatic number is exactly three.

Thus an active triangle is always three-colourable. Combined with the forest
construction, this proves the theorem and the stated exact criterion.

## Computational trust boundary

`build.py` uses Kissat only to find the displayed colour words. The theorem
does not trust a SAT answer: `verify.py` uses the Python standard library,
imports no builder code, independently reconstructs the Cartesian geometry
and exact multiquadratic closure, and checks the words directly. The SHA-256
edge identifiers serve as certificate keys; repeated identifiers are also
required to have exactly equal edge tuples, and every word is checked on every
reconstructed occurrence.

`controls.py` prepares the exact inventory once and confirms that seven
independent corruptions are rejected, including a missing graph, an extra
graph, a malformed word, and a deliberately monochromatic strict edge. A unit
triangle supplies an independent eight-assignment check that two colours do
not suffice.

This is a negative construction result. It establishes no five-chromatic
unit-distance graph and no improvement on the 509-vertex record.
