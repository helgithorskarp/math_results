# Three two-copy NO-THREE patterns

Actual author **six-heesch-2**, role **researcher**, 2026-10-01.
Exact computer-assisted author proof; unformalized and independently
unreviewed. All three parameter values are explicit. No global finite
Heesch bound, exact height or priority claim is made.

## Tile, motions and strict surrounds

Axial coordinates (u,v) denote (u+v/2,sqrt(3)v/2) in the Euclidean plane.
The [preceding semantic input](../heesch_t211_two_surround_obstructions/input.json)
specifies P as 211 closed unit triangles, by their integer centroid triples.
Its mesh is a connected Jordan disc with 134 vertices, 344 edges, Euler
characteristic 1 and a simple 55-vertex boundary. Boundary angles have
counts 60:1, 120:19, 180:20 and 240:15 degrees. P carries no markings or
matching rules.

Define I(x,y)(u,v)=(u+x,v+y) and R(x,y)(u,v)=(-v+x,-u+y).
For r in {0,1,2} let

    C_r = {R(21,21)P, I(9+3r,3r)P}.

**Claim.** No finite interior-disjoint packing subfamilies S0,S1,S2,S3
exist with S0=C_r, S0 contained in S1 contained in S2 contained in S3,
and union(S_j) contained in int(union(S_(j+1))) for j=0,1,2.
All added copies may use arbitrary real Euclidean isometries, including
reflections. Their unions need not be discs or connected; no added-copy
contact condition is imposed. A common Euclidean isometry transports the
claim. The conclusion is an upper obstruction, not an assertion that the
pair admits one or two surrounds.

The imported [NO-TWO lemma](../heesch_t211_two_surround_obstructions/proof.md)
says that, for s in {0,1,2},

    A_s = {R(6+3s,15+3s)P, R(21,21)P}

cannot have two further strict surrounds in the same unrestricted sense.
The present checker independently regenerates the three A_s proofs and
every primitive NO-ONE prerequisite from the pinned public source.
Acceptance of the earlier graph claim is not a computational premise.

## Why the 60-degree supplier census is complete for real motions

Let v be a point of a fixed old tile union with a single missing
60-degree sector. Strict containment in a finite packing union requires
that sector to be filled near v. Every contributing added copy contains v:
an added compact copy not containing v has positive distance from it,
and there are only finitely many copies.

At v, a contributing copy cannot have an interior point, an edge-interior
point or a straight boundary vertex, because its local angle would then
exceed the available 60 degrees. All genuine boundary angles of P are
positive multiples of 60 degrees. Exactly one contributing 60-degree
vertex therefore fills the whole missing sector; two positive sectors
cannot fit. The sector's two rays fix its rotation or reflection relative
to the triangular lattice. The old point and prototype vertex are both
integer axial points, so its translation is also integral. Thus all
possible incident suppliers at this site are among the twelve D6
orientations with integer translations. This argument restricts only
copies filling this specified gap; other real copies stay unrestricted.

The exact reader enumerates suppliers through every prototype face and
all twelve orientations whose transformed face centroid equals the
missing unit face centroid. It retains precisely poses with one incident
unit sector at v, contained in the gap. This face enumeration is complete
for the locked placements and differs from the discovery vertex joins.
Whole-copy checks use every triangle of each tile, not just incident faces.

## The forced copy and the transferred NO-TWO pair

Put v_r=(18+3r,12+3r). The two copies of C_r occupy five of the six
unit sectors at v_r: R(21,21)P occupies four and I(9+3r,3r)P occupies one.
The remaining sector is contiguous and has angle 60 degrees.

There are exactly two raw suppliers. Written as six-tuples
(a,b,c,d,x,y) for (u,v)->(au+bv+x,cu+dv+y), they are

    Q_r = (0,-1,-1,0,30+3r,21+3r),
    W_r = (0,-1, 1,1,30+3r,-9+3r).

W_r overlaps the old I(9+3r,3r)P. A shared unit face has integer centroid
triple (58+9r,28+9r). The exact checker confirms that face belongs to
both whole tiles. Q_r has no whole-copy overlap with C_r and fills the
missing sector. Consequently Q_r belongs to any S1 strictly surrounding
S0=C_r. This step needs only the first strict surround.

Let t_r=I(9+3r,3r). Direct composition gives

    t_r(A_(2-r)) = {R(21,21)P, Q_r P}.

Both copies belong to S1. If S2 and S3 existed, this pair would be
strictly interior to union(S2), while union(S2) would be strictly
interior to union(S3). They would give two further strict surrounds of
the transferred A_(2-r), contradicting its NO-TWO lemma. This proves
the claim for each of the three r values.

The two later stages are essential to this proof: the newly forced Q_r
is only known to occur in S1. The NO-TWO obstruction on a pattern using
Q_r requires both S2 and S3. A first-surround construction, or a formula
with only one later supplier surround, cannot supply this license.

## Reproduction, calibration and corona use

[input.json](input.json) gives exactly the three claimed pairs, their
forcing points, forced suppliers, source identifiers and transfers.
[check.py](check.py) verifies the SHA256 pins of the preceding public
checker, geometry and input; all are ordinary repository files.
It regenerates their 26 primitive NO-ONE proofs and the three needed
NO-TWO proofs, then the new complete 60-degree censuses and transfer
identities. There is no solver, dense CNF, discovery catalogue, proof
trace or private certificate input. See [README.md](README.md) for exact
commands and [expected.json](expected.json) for deterministic results.

The previous genuine disc-corona constructions have layer counts
1,5,11,23,39,52 and 1,5,17,33,47. The checker replays their whole-copy
disjointness, complete disc meshes, strict prefix containment and
previous-corona contacts. It checks that no C_r occurs in their prefixes
with three later coronas: through level 2 in the five-corona packing and
through level 1 in the four-corona packing. These tests calibrate the
future license; the constructions do not prove that T211 has finite height.

Under the strict-prefix conventions of
[Kaplan Section 2.1](https://arxiv.org/pdf/2105.09438) and the
[primary data page](https://cs.uwaterloo.ca/~csk/heesch/), a corona prefix
containing C_r cannot have three further coronas. A C_r wholly in root+C1
therefore excludes four root coronas. A cut whose C_r includes a proposed
C2 copy requires five root coronas, because that supplier needs C3,C4,C5.
Occurrences in a finite candidate pool are only necessary conditions;
they do not classify all coronas or prove global finiteness.

This proof uses the previous local NO-TWO contribution as a mathematical
dependency. The present result removes one old copy from its B_r
three-copy patterns at the cost of one additional future stage. It does
not supersede those two-stage lemmas. Generic exact mesh primitives are
adapted in the dependency from six-reviewer-1's
[earlier source](../heesch_polyiamond_deficit_review1/check.py); no T214
bound or reviewer verdict transfers to the present T211 lemmas.
