# A partial-cell obstruction in the changed Q17 construction family

Actual author **six-heesch-1**, role **researcher**. This result is author
checked, unformalized and independently unreviewed. The checks below are
different source implementations by the same author, not peer review.

Let a cell coordinate p denote the closed unit square p+[0,1]^2. Let B be the
scale-two subdivision of the seventeen-cell polyomino with rows

    y=0: 2,3; y=1: 1,2,3,4; y=2: 0,1,2,3,4;
    y=3: 2,3,4,5; y=4: 3,4.

This is the OTHER Kaplan seventeen-omino, author coordinate/PDF record193.
The original tile and its three coronas retain Kaplan's 2021/2022 credit.
Define U to be the union of the closed 3-by-3 cell neighborhoods of B, and
K={p in B: the closed 3-by-3 cell neighborhood of p lies in B}. Thus |B|=68,
|U|=116, |K|=28. These are a search domain and a mandatory core; there are no
marks on the tile. The different old P17/record44 upper-four theorem is not
used.

Define the six extra selected cells

    A={(1,4),(7,0),(9,4),(9,7),(9,8),(10,3)}

and the seventeen empty cells

    F={(-1,4),(0,5),(0,6),(1,6),(5,10),(7,10),(8,-1),(8,0),
       (8,9),(9,5),(10,1),(10,7),(10,8),(11,6),(11,7),(12,6),(12,7)}.

Put Q=K union A. Take any unmarked Jordan-disc polyomino S satisfying

    Q subseteq S subseteq U\F.

Let g0 be the identity; let g1(x,y)=(y-9,15-x); and let
g2(x,y)=(9-x,y-5). These formulas act on points of the plane, not on cell
lower-left corners. Their literal signed frames are

    g0: M=((1,0),(0,1)), t=(0,0)
    g1: M=((0,1),(-1,0)), t=(-9,15)
    g2: M=((-1,0),(0,1)), t=(9,-5).

**Claim.** If the three whole copies g0(S), g1(S), g2(S) have pairwise
disjoint interiors, no finite interior-disjoint packing of congruent copies
of S containing them can make their union a subset of its interior. Additional
copies may use arbitrary real translations, rotations and reflections; holes
in the enlarged union are allowed. In particular, a first prefix containing
this pattern cannot have a complete further surround. This is a conditional
pattern obstruction, not a global height bound or classification of S.

For any signed frame (M,t), the cell lower-left map is

    phi_(M,t)(p)_i = sum_j M_ij*p_j + t_i + sum_j min(0,M_ij).

The reader derives the same map independently by transforming all four
vertices of the unit square. If phi_gi(p)=phi_gj(q) for i!=j and q in Q,
then p cannot belong to S: otherwise two old copies share an entire unit
square. Also, if q=p, such a collision forbids p without a second selected
cell. The reader regenerates all these one-cell packing consequences. There
are 27, disjoint from Q and F:

    E={(-1,3),(-1,5),(-1,6),(0,3),(1,1),(1,2),(1,3),(1,5),
       (2,1),(2,6),(3,-1),(3,0),(3,1),(3,6),(3,7),(3,8),
       (4,-1),(4,8),(5,-1),(5,8),(5,9),(7,-1),(7,9),(9,10),
       (10,10),(11,8),(12,8)}.

At v=(-4,6), the three incident cells other than c=(-4,5) are forced
occupied. In fact g1 maps (8,5), (8,4), (9,4) to (-4,6), (-5,6), (-5,5),
respectively; the first two sources belong to K and the third to A. The
identity and g2 have no source in U at c, while g1's source is (9,5) in F.
Thus the old union has an exact 270-degree filled sector at v and a
90-degree gap in the unit square c+[0,1]^2, for every S in the hypotheses.

Suppose a finite containing packing made that old union interior. A
sufficiently small circle about v misses nonincident boundaries and other
vertices. A new Jordan-disc orthogonal tile incident at v has positive local
angle 90,180 or270 degrees, or180 at a nonvertex boundary point. It cannot
contain v in its interior because the old sector already occupies270 degrees.
To fill the remaining90 degrees with disjoint interiors requires exactly one
new tile, incident at a convex90-degree corner, whose two boundary rays match
the gap axes. This forces a D4 orientation. The prototype corner and v are
integer points, so its translation is integral too. The forced owner
therefore contains the whole missing unit square c+[0,1]^2.

Every possible owner is among the following complete finite envelope: choose
one of the eight signed D4 matrices M and a source cell p in U, and use the
unique integer translation t for which phi_(M,t)(p)=c. There are 8*116=928
distinct frame/source pairs. This overincludes sources absent from S and
sources not at the necessary convex corner, which is harmless.

The independent reader regenerates the entire envelope using four-square
vertex images. It regenerates every owner and rejects it by one of these sufficient rules:

* source p is in F:136 records;
* source p is in E, with a checked old/old packing witness:216 records;
* a source a in Q of the prospective owner and a source b in Q of an old
  copy have exactly the same physical unit square:576 records.

All928 frame/source pairs are covered, with no duplicate or omitted pair.
The last rule yields a positive-area interior overlap whatever other cells
of S are selected. Hence no forced owner exists, proving the claim.

The literal checked Q50 first-disc fixture is a nonvacuity control: its50
selected cells meet Q and avoid F and E; its three old copies do not overlap
and occur in the independently checked one-root/six-copy first prefix. Its
prefix areas are50,350 and perimeters44,178. It is noncongruent to B. This
demonstrates that the obstruction applies to an actual changed disc first
construction. It does not classify other Q50 first prefixes or prove global
Q50 finiteness. The generic raw decoder ID601 is not the fixture identity:
this fixture is explicitly candidate2101/Q50.

There are65 cell bits unspecified by Q and F, and38 after the27 one-cell
packing consequences E. These numbers count unspecified bits, not the number
of valid discs or admissible arrangements. No optimum-size condition set is
claimed. The conditions were found by greedy weakening of a seed pattern;
the proof uses the final finite envelope, not the greedy search.

In a constructor with compulsory K and identity root, let X_p mean p in S,
and T1,T2 mean that the two specified nonroot whole frames were chosen. A
sound necessary condition for any further surround is

    (OR_{p in A} NOT X_p) OR (OR_{p in F} X_p) OR NOT T1 OR NOT T2.

This25-literal cut replaces the exact Q50 cell/frame block's118 literals.
It constrains the prototype/frame arrangement; a different shape or a
different arrangement of the same shape may survive. Survival of this and
other single-corner owner tests does not construct a compatible next corona.

A second checked variant uses only g1 and g2, with no root-packing
implications. It retains the same Q but takes the following35 empty cells:

    F2={(-1,3),(-1,4),(-1,5),(-1,6),(0,3),(0,5),(0,6),(1,1),
        (1,2),(1,6),(2,1),(3,-1),(3,0),(3,7),(3,8),(4,-1),(4,8),
        (5,10),(7,-1),(7,10),(8,-1),(8,0),(8,9),(9,5),(9,10),
        (10,1),(10,7),(10,8),(10,10),(11,6),(11,7),(11,8),
        (12,6),(12,7),(12,8)}.

With Q subseteq S subseteq U\F2 and the two old whole copies interior-disjoint,
the same claim holds for their union alone. The three occupied quadrants and
missing cell remain fixed. Among the928 owners,280 have source in F2 and648
have a collision between compulsory Q cells. This gives a43-literal
prototype/two-frame cut and leaves47 cell bits unspecified. Its proof uses
no compulsory root. The root-context variant above trades that stronger old
pattern for fewer explicit cell hypotheses. Both apply to the same literal
Q50 first prefix.

`data.json` is the complete1728-byte parameter and nonvacuity fixture. The
standard-library reader `check.py` derives the cell maps from four square
vertices, reconstructs U and K, enumerates all D4/source joins, derives the
packing-implied absent cells, and checks the literal changed first corona.
It imports no solver, native inventory or search generator. It emits hashes
of the deterministically regenerated geometric witnesses; no large corpus
or native CNF is needed.

Run from the repository root:

    python3 heesch_polyomino_partial_corner_filter/check.py
    python3 -O heesch_polyomino_partial_corner_filter/check.py

The outputs agree with `expected.json`. Nine damaged parameter/geometry
controls reject, and benign cell-order reversal passes. The separately
implemented private reader also checked the full928-record generator packets,
including eleven damaged root-context certificate controls. These are checks
by the author; they do not constitute independent review or formalization.
No native UNKNOWN result is used as a mathematical negative.

The sector-to-integral-owner step reuses the elementary filled-contact
argument already credited in
[the earlier motion bridge](../heesch_polyomino_motion_bridge/proof.md).
The new result is this concrete partial-cell obstruction and its root-packing
weakening, not a new general motion theorem. Primary convention/reference
context is Craig S. Kaplan,
[Heesch Numbers of Unmarked Polyforms](https://arxiv.org/abs/2105.09438) and
[the author's Heesch dataset](https://cs.uwaterloo.ca/~csk/heesch/). The other
seventeen-omino is in the author's
[coordinate file](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt)
and [PDF](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.pdf).
No priority claim or current Heesch record is asserted. The assigned
finite-five square-cell construction remains unresolved.
