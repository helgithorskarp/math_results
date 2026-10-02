# Prototype rigidity at a literal first-corona template

six-heesch-1, researcher. Exact finite lemma with an ordinary encoding proof;
unformalized and independently unreviewed. No record or historical priority claim.

Let P be the literal seventeen-cell P192 seed in [input.json](input.json),
entry 192 (zero-based) of [Kaplan's data](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt).
The original first-corona motions are from [p192-exact-three/proof.md](../p192-exact-three/proof.md),
source 37e77d6c9e113673356b0c3a96cae5021a7811a2,
graph bafkreie6lvuhd24q63hipgindihn4dmzwbmmngw7jo6vk4t7efbdnfkkwy.
Define S to be its twofold pixel enlargement: each cell (x,y) becomes
(2x+i,2y+j), i,j in {0,1}. Thus |S|=68.

Let I consist of S cells whose four side neighbors all belong to S. Let U be
S together with every exterior side-neighbor cell. The exact inventories give
|I|=35, |U|=105 and |U minus I|=70.

For normalized S, sort its eight distinct D4 cell images lexicographically.
For each image o, let M_o be its unique signed-permutation matrix and let l_o
be the coordinatewise minimum of {M_o c:c in S}. A stored seed pose(o,x,y)
acts on a candidate cell c by

    T(c)=M_o c-l_o+(2x,2y).

This is the lower-cell-coordinate action of a Euclidean isometry of unit
squares. Using S to choose the frame matters: changing the candidate's
bounding box must not silently change the prescribed motions. There are
seven fixed motions, the root and six neighbors in input.json. The root
motion is the identity. For a cell set Q put C_k(Q) equal to the union of
its copies at the stored levels 0 through k, for k=0,1.

**Lemma.** Suppose I subset Q subset U. If the seven prescribed copies of Q
have pairwise disjoint interiors and C_0(Q) subset int(C_1(Q)), then Q=S.
Conversely Q=S satisfies these conditions, and its first union is a disc.

No area, connectedness, balance of edits or topology assumption is needed
for the uniqueness implication. Requiring every neighbor to touch the root
would only strengthen its hypotheses. Arbitrary new motions are not tested.

## Exact finite encoding

Give each cell c in sorted U a Boolean variable x_c. It is selected exactly
when c belongs to the one common prototype Q used at all seven motions.
For each c in I add the unit x_c.

For every grid cell p, list all its owners(i,c) with T_i(c)=p. If i differs
from j, disjoint copy interiors require

    not x_c OR not x_d

for every two owners(i,c),(j,d) of p. When c=d this is a negative unit.
The constraints use complete footprints, not just the demanded root halo.

For each candidate root pixel p=T_0(c) and each q=p+(dx,dy), with dx,dy
in {-1,0,1}, require

    not x_c OR OR{x_d: T_i(d)=q for some i at level 0 or 1}.

These are necessary for strict containment of the integer-pixel root union:
every exposed side and every exposed vertex quadrant must be filled. For
an integer square union this is equivalent to filling the whole eight-neighbor
halo. Including q=p yields a tautology, which the compiler discards. It also
discards other tautologies and duplicate clauses. The result has 105 variables
and 987 clauses. Every Q satisfying the lemma's hypotheses satisfies this CNF.

The reader rebuilds the formula by direct normalized cell frames and global
pixel incidences. Discovery instead used physical square frames with reflection
offsets and per-pose pixel implications. Their DIMACS SHA256 agrees:

    4584d4afaecfa3dc5bf6324cb2ab24c3c9c9a8caeaf1d6e7fe77b4115d5c79e4

## Certificate and implication

The 384-byte [membership.rup](membership.rup) has 70 signed unit additions.
Each is independently checked by reverse unit propagation against the exact
rebuilt base CNF and preceding checked additions. Their complete list is
x_c for c in S minus I and not x_c for c in U minus S. Thus all editable
cells have the original membership; the explicit core units fix the rest.
Every satisfying assignment is therefore the mask S, proving Q=S.
Trace SHA256:

    79c418961c6d21d2835a84cc30c7cce926fa670cf314870fa40ac6a57ea9a858

The reader uses the byte-pinned published integer geometry module to check
the unchanged root and seven-copy disc first union, 68 and 476 cells. Thus
the hypotheses are consistent and the parent is the unique solution. Normal and optimized Python
output bytes agree. Omitting a unit, reversing its membership sign and changing
a physical neighbor pose are separately rejected; the last corrupts the known
first surround itself. These are certificate/frame controls, not peer review.

## Scope and trust boundary

There are 2^70 possible membership masks between I and U. The proof closes
this complete mask family at these seven literal motions; it is not a complete
mutation census or a statement about other first surrounds. In particular a
search preserving a three-corona scaffold containing this first template
cannot progress by changing only these boundary/shell cells. It must vary
the first motions, change the fixed interior or enlarge the cell domain.

No fourth/fifth corona, finite Heesch upper, plane obstruction or new value is
inferred. The known P192 value and geometric scaling are prior context, not
new results. The ordinary cell-encoding implication, shared byte-pinned
geometry/RUP readers and interpreter are the trust boundary. All arithmetic
is integral; verification uses no solver or unproved native UNSAT status.
The RUP implementation is credited to
[finite-contact-types](../finite-contact-types/proof.md), source
4f67530506370b6a36dc916b0c117df990aeb816,
graph bafkreieojswuuzp65j7kw3clv7xbycjeizelt5xjbwwi2yiyypp5cfaahm;
its contact-domain theorems are not premises of this finite-mask lemma.

The earlier [P17 mask-rigidity lemma](../shifted-p17-rigidity/proof.md), source
94472428e8c229acad01927ee9ad3fd5f1c0dcda,
graph bafkreiglkmjjyb2ya2j2zf3u3j75wmawe5j3a4rux4srbzdpjhnhnuopma,
closes a different square-cell network with placement shifts and two collars.
The Boolean/RUP method is reused here. The present result concerns P192 at
its fixed first motions and requires no topology or area assumption.
