# The cell-template extension lemma

Actual author: **six-heesch-1**, role **researcher**, 2026-10-01.
The proof is author checked, unformalized and independently unreviewed.

Let P be the unit-cell disc polyomino whose counterclockwise boundary is

    (3,0),(8,0),(8,5),(10,5),(10,8),(11,8),(11,9),
    (6,9),(6,7),(3,7),(3,6),(0,6),(0,2),(3,2).

Cells are closed squares [x,x+1] by [y,y+1]. P has60 cells. Let U consist
of P and all unit cells sharing a vertex or edge with P; |U|=104. Let K
be the cells p of P whose full3-by-3 unit-cell neighborhood lies in P;
|K|=25. Their exact coordinates, all signed matrices and all translations
are in the `inputs` object of [certificate.json](certificate.json).

A signed frame (M,t) sends a prototype cell square by z -> Mz+t, where M
is a signed permutation matrix. For a lower-left corner p=(x,y), its image
lower-left corner is Mp+t+(sum of negative entries in row1 of M,
sum of negative entries in row2 of M). This formula handles reflections
without assuming that lower-left corners themselves transform linearly.

The inputs supply three frame lists A0,A1,A2 of sizes1,6,12. For a cell
set S define Ck(S) as the union of its whole frame copies at levels0 through k.
The root frame is the identity. No frame or translation is allowed to change.

**Lemma.** Let K be contained in S and S be contained in U. Suppose the19
specified whole frame copies of S have disjoint interiors, and C0(S) is
contained in the interior of C1(S), while C1(S) is contained in the interior
of C2(S). Then the four supplied periodic frames of S, repeated by the lattice

    L = Z(6,-6) + Z(2,38),

exactly tile the Euclidean plane. In particular |S|=60. Thus any unmarked
disc polyomino in this cell family realizing two admissible coronas in this
copy template is a plane tiler and cannot serve the intended finite-five
non-tiler target. The implication also covers cell unions that are not discs;
no prototype connectivity or area hypothesis is used.

The lemma concerns only U,K and these fixed signed frames. It does not
exclude different first or second copy templates, larger cell pools, removal
of core cells, or changed shapes elsewhere. It proves no finite global Heesch
upper bound. The original P has an actual1/6/12-copy two-disc witness, but
its periodic tiling disqualifies it from the finite-height target.

For orientation reference only, sort the eight normalized D4 cell images of
P lexicographically, numbered0 through7. The original frame lists decode to

    A0: (2,0,0)
    A1: (0,2,6),(0,8,0),(1,-11,-1),(1,-5,-7),(2,-6,6),(2,6,-6)
    A2: (0,-4,12),(0,14,-6),(1,-17,5),(1,1,-13),(1,9,-15),
        (2,-12,12),(3,-17,-3),(3,-11,-9),(3,-5,-15),
        (3,3,17),(3,9,11),(3,15,5).

Here an index chooses a normalized image, followed by the indicated integer
translation. For changed S use the signed frames in the certificate, not
these normalized-image indices. The periodic frames for the original P
have normalized codes (2,0,0),(0,2,6),(1,3,25),(3,3,17).

Give each cell u of U a Boolean variable Xu meaning u is selected in S.
Keep the25 variables for K true. For any physical unit cell reached by two
different copies, prohibit choosing both corresponding prototype cells;
if the same prototype variable would cause both copies to occupy it, that
variable is prohibited. These whole-square clauses are necessary for
interior-disjoint copies and impose no artificial markings.

In the integer unit-cell grid, strict containment Ck in the interior of
C(k+1) requires every unit cell sharing an edge or vertex with a selected
cell of Ck to be occupied in C(k+1). If prototype variable Xu puts such a
cell at p in an inner frame and Oq is the complete set of prototype owners
of the neighboring physical cell q in C(k+1), use the clause

    not Xu OR (OR Xv for v in Oq).

A missing owner list forces Xu false. If Xu is itself a possible owner of q,
the clause is tautological and can be omitted. Every actual prototype
satisfying the lemma's hypotheses therefore satisfies these clauses.
The reader checks complete owner lists geometrically, rather than trusting
the discovery generator's local vertex maps.

The lattice L has determinant240 and the equivalent triangular basis
(2,38),(0,120). Unit-cell lower-left corners have quotient address

    (x mod2, (y - 38*floor(x/2)) mod120).

These240 addresses are a complete set of cell cosets. For the four supplied
periodic frames, enumerate every possible prototype owner of each address,
retaining distinct copy occurrences even when their prototype variable is
the same. Introduce a collision gate for each possible pair of selected
owners of one address; a repeated owner variable uses that variable directly.
Introduce a gap gate equivalent to all owners of an address being unselected.
The full failure condition is the disjunction of every collision and gap.
The reader checks all biconditional gate clauses and exhaustively checks
that every quotient collision and every address gap is represented.

Consequently, any S satisfying the hypotheses but failing to tile in this
periodic pattern gives a satisfying assignment of the397-variable,
1818-clause formula in the certificate, including its failure clause.
The202 certified RUP additions derive the empty clause. Each addition is
checked by assigning its negation and running literal unit propagation on
the existing clause database. No SAT solver or external proof checker is
needed by the public reader. Thus no such S exists.

With no gap and no collision, the four whole periodic copies occupy every
unit-cell lattice coset exactly once. All their lattice translates therefore
have disjoint interiors and cover every unit square of the plane, including
its boundary by closedness. The index is240, so4|S|=240 and |S|=60.

The original P is a non-vacuity control: the reader directly checks whole
copy disjointness, strict surrounds, preceding-prefix contact for every
added copy, connectedness, complement connectivity and absence of vertex
pinches. The three prefixes have60,420,1140 cells. Its four periodic frames
cover240 distinct cosets. The illustration is explanatory; the cell and
quotient checks establish the geometry.

The discovery encoding transformed four vertices of every candidate square
and used an adjugate quotient. The public reader uses the signed affine
lower-left formula and the Bezout triangular quotient above, classifies all
premises geometrically, and checks the proof by direct forward propagation.
This is independent checking by the same author, not an independent review
or a proof-assistant formalization. The reduction from geometry to Boolean
variables and from exact cell-coset coverage to a plane tiling is written here.

[Kaplan's primary paper](https://arxiv.org/abs/2105.09438) and
[author dataset](https://cs.uwaterloo.ca/~csk/heesch/) give the polyform corona
conventions; disc prefixes and an outer corona permitting holes are distinct.
The present implication needs only the two strict containments, so imposing
disc topology and the usual preceding-prefix contact condition strengthens
its hypotheses. It establishes a construction obstruction within a changed
square-cell family, not a new finite Heesch number.

Related team work includes [P17 contact-pattern rigidity](../heesch_polyomino_contact_pattern_rigidity/proof.md)
and the distinct [curved-trapezoid interior obstruction](../heesch_trapezoid_uniform_strip_obstruction/proof.md).
Neither theorem, its negative catalog, nor a phase-collapse theorem is used
in this proof. The supplied cells, frames and RUP certificate are self-contained.
