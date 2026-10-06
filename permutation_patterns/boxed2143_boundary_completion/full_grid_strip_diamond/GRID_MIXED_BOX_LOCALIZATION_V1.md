# Localizing the remaining mixed boxes in the original half-grid

Lyra, literature-researcher-2, 2026-10-06. NEW author uniform argument,
pending the existing Sage check. This is separate from621's exact pending
packet and from609's accepted dead-parent scope. It is a reduction of the
same unproved P compatible-mass problem, not a replacement target or a
density theorem. Full agreed target410 remains UNSOLVED.

Use the original parity-p vertices, p in{0,1}, with decreasing guard order
in EVERY horizontal and vertical guard band. Old component permutations
avoid boxed2143. The following statements hold for every r>=2.

1. Every boxed2143 occurrence has one or two selected guards.
2. Two selected guards share a guard row OR a guard column. They are
   precisely the first two or last two selected positions, hence one
   descent pair of2143.
3. Any selected old pair shares an old row or old column, or occupies
   diagonally opposite cells across ONE missing checkerboard vertex:
   both coordinate differences are1 and the lower-left gap parity is1-p.
4. With one selected guard, the three old selected cells are either in
   one old row, in one old column, or three corners of a2x2 cell square
   whose central vertex is missing (parity1-p).

## Empty pair rectangles, with all selected points accounted for

Every pair of selected points of2143 has no OTHER selected point inside
its open bounding rectangle. The two descent pairs use consecutive
selected indices. For the four ascent pairs, inspect the roles a,b,c,d
with b<a<d<c: pair(a,c) excludes b by value and d by position;
pair(a,d) excludes b,c by value; pair(b,c) excludes a,d by position;
pair(b,d) excludes a by position and c by value. A pair rectangle is
contained in the whole selected position/value rectangle. Therefore any
unselected point inside ANY selected pair rectangle already shades the
whole putative occurrence. No selected point may be silently counted as
a blocker. This is the elementary geometry behind the previously checked
signed-cover/K4 correspondence, used here directly.

For guards in different rows i,ell and columns j,k, an old point with row
min(i,ell)+1 and column min(j,k)+1 lies strictly inside their pair rectangle.
It exists, is unselected by the preceding fact, and blocks. Thus any two
selected guards share a row or a column, regardless of their orders.
In the fixed decreasing orders, a same-band guard pair is decreasing in
position/value order. The only decreasing pairs in2143 are(a,b),(c,d).
Any three selected guards would contain an increasing pair, since no
three selected roles of2143 form321. That pair is impossible: different
rows/columns are blocked, and same-band guards are decreasing. Thus at
most two guards are selected.

The old-only exclusion is the uniform monochrome lemma in the EXACT621
packet: any old pair spanning two distinct old rows/columns has an
interior vertex rectangle; either half shades it unless it is a single
missing vertex. Four old points in the resulting2x2 arrangement cannot
have order2143, and a single old row/column is protected by component
avoidance. This proves the lower bound of one selected guard. Guard-only
occurrences are also excluded by the same-band monotonicity and old-grid
shading. The621 lemma is an explicit author proof dependency, not an
inherited independent verdict.

For any two selected old points in distinct rows and columns, all guard
vertices of their open pair rectangle have indices
min(i,ell)<=h<max(i,ell), min(j,k)<=v<max(j,k). If that rectangle has
at least two vertices, an adjacent pair supplies both parities, hence an
occupied unselected blocker. With one vertex it must be missing. This
gives statement3, including diagonally increasing and decreasing pairs.

For three old cells not all in a common row or column, there must be a
diagonal pair. By statement3 it occupies opposite corners of one2x2
square across a missing vertex. A third cell compatible with both endpoints
can only be one of the other two corners. Indeed, in normalized coordinates
for endpoints(0,0),(1,1), a cell sharing row0 with the first must either
be(0,1), duplicate(0,0), or be(0,2); the last possibility crosses the
adjacent occupied vertex(0,1) with the second endpoint. The column case
is identical. A cell diagonal to the first has offsets(+-1,+-1); apart
from the second endpoint, it either has a gap of2 to that endpoint or
crosses an adjacent occupied vertex. Endpoints(0,1),(1,0) give the same
argument after reflection of the column coordinate. Checkerboard parity
changes only the choice of missing/occupied vertices, not adjacency.
Thus the three old cells are precisely three corners of that missing
square. This proves statement4; it is not a claim that every such local
configuration produces a box.

## Exact bounded classification and the remaining weight problem

`grid_mixed_box_localization_controls_v1.py` enumerates the complete
46656 ordered old-component tuples at r3 for EACH checkerboard half.
All components have size3, hence avoid. It scans the FULL literal occurrence
set of each output and checks all four geometric statements, with exact
tag positions and the missing-vertex parity. It streams every full output,
occurrence set and classification; first representatives with COMPLETE
occurrence sets are retained. This is not an all-size inference.
The pinned report contains the complete class counts and stream hashes.
At r3 each guard band has one point, so a two-guard occurrence is impossible;
these controls cannot establish a nonvacuous larger-r two-guard count.

Both small half layouts have EXACTLY66096 full occurrences, with the same
eight class totals: each guard-role/old-L type8748, and each of the four
remaining row/column types7776. Nevertheless their compatible tuple counts
are8100 for parity0 and13036 for parity1. Thus even identical complete
type totals and mean17/12 do not determine joint avoidance. The full
classification streams are

    parity0 e3d579d46faa79aa20416f48b712babd840b61aba82758e7dc2583a46c7304f9
    parity1 9b43d9f09fe254b27a903b3ae1839b38c311f920d0086f1835c1f89daa45e505

The recorded run takes20.710910s/16748KiB. These finite observations do not
select a new target or prove that one parity is better at larger sizes.

The next all-size obligation is to pay for the actual weighted avoiding
population under these remaining local types: one guard with an old-row,
old-column or missing-square triple, and a same-band descent guard pair
with its two old points. Rows, columns, descendants and future extension
multiplicities still count as inputs. An occurrence count, an absent
monochrome type or a local necessary condition alone gives no lower bound
for the joint avoidance probability. In particular the future parent law
remains the product of Evalue and Eposition in590/605; favorable parents
must not replace weighted averaging. AggregateP is still open even though
the every-parent Q is false609.

No uniform mixed-type mass estimate, positive density, new K aggregate
bound, full410 proof, novelty claim or standalone source/original is
supplied. The exact independent check is requested before using this
localization as accepted proof evidence. Earlier artifacts remain unchanged.
