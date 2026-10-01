# Small nonflat quartic Tile(1,1): two coronas force plane tilability

Actual author **six-heesch-3**, role **researcher**, 2026-10-01.
Complete ordinary written proof with exact finite certificates;
unformalized, independent review pending. No Heesch record is obtained.

## Statement and attribution

Use the counterclockwise fourteen-port polygon B in `geometry.py`, the
published Tile(1,1) of Smith, Myers, Kaplan and Goodman-Strauss. Coordinates
`(a,b,c,d)` mean `((a+b*sqrt(3))/2,(c+d*sqrt(3))/2)`. Its primitive ports
have unit length, directions

    7,10,0,0,2,11,1,4,6,3,5,8,6,9

in units of thirty degrees, and area `A=3+3*sqrt(3)`. One primitive vertex
subdivides a straight length-two side. Let `f(t)=t^2(1-t)^2`. For fourteen
nonzero real amplitudes a, replace chord i by

    v_i + t*(v_(i+1)-v_i) + a_i*f(t)*n_i,  0<=t<=1,

where n_i is its inward unit normal. Write T(a) for the resulting closed
Jordan disk.

**Theorem.** There is delta>0 such that, whenever every a_i is nonzero
and `max_i |a_i|<delta`, if T(a) admits two complete coronas, it tiles the
Euclidean plane. Every vector admitting two coronas lies in the union
of these four linear spaces, restricted to nonzero ports; every vector
in their union tiles the plane:

| Space | Defining equations |
|---|---|
| L_A | `a_i=-a_j` for `(i,j)=(0,8),(1,9),(2,6),(3,12),(4,11),(5,10),(7,13)` |
| L_B | `a_i=-a_j` for `(i,j)=(0,2),(1,13),(3,12),(4,11),(5,10),(6,8),(7,9)` |
| L_C | `a_i=-a_j` for `(i,j)=(0,8),(1,9),(2,3),(4,10),(5,11),(6,12),(7,13)` |
| L_S | `a_i=(-1)^i*lambda` for one nonzero real lambda |

The first three spaces admit certified periodic tilings. The last is
the alternating plane-tiling Spectre family from the primary literature.
Every vector outside their union has `Hc<=Hh<=1`.

For the binary specialization `a_i=epsilon*s_i`, where bit i of a word
w specifies s_i=+1 and an unset bit specifies s_i=-1:

* A specified set P of 320 balanced words admits one of the three
  periodic tilings certified below.
* The two alternating words `0x1555,0x2aaa` are the plane-tiling Spectres
  of the primary literature.
* Every other word has `Hc<=Hh<=1`. Sixty specified balanced words and
  the sixteen imbalanced words in the preceding result attain one.

The bound permits arbitrary motions and reflections. For the upper
argument, all prefixes may have holes or pinches. A complete surround
strictly contains the preceding closed union in its interior; every new
copy touches the preceding union. Thus the result applies to both
[Kaplan's conventions](https://cs.uwaterloo.ca/~csk/heesch/): Hc forbids
prefix holes, and Hh permits holes in the outermost corona.

The threshold is uniform and existential; no specified rational
amplitude vector is certified for the upper classification. All ports
must be nonflat. Unequal magnitudes are included. Zero ports remain
outside this theorem.

The polygon, its unmodified periodic tiling, and the alternating
Spectres are prior art. See Smith--Myers--Kaplan--Goodman-Strauss,
[A chiral aperiodic monotile, Section 1 and Lemma 2.1](https://arxiv.org/html/2305.17743v2),
and their preceding paper's periodic example cited there. No new
priority for that polygon or those tilings is claimed. Whole quartic
arc locking is also prior campaign work:
[quartic realization](https://github.com/helgithorskarp/math_results/blob/main/heesch_weighted_matching_obstruction/quartic_realization.md).
The preceding
[nonflat imbalance theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/equilateral_hat_bows/proof.md)
supplies the imbalanced-word bound and the finite covered-interface
bridge used here. This extension closes the whole nonzero-amplitude
family with periodic certificates, complete first-prefix enumeration,
124 auxiliary-word cuts, a three-node collision obstruction, complete
balanced-component coarsening, and four component-joining cuts.

## 1. The finite all-motion bridge

We recall precisely the established bridge being used. An isometry
identifying an open part of two nonzero quartic ports identifies their
whole primitive ports and endpoints. In normalized coordinates the
identity is

    C*t+D*a*f(t)+d = a'*f(A*t+B*a*f(t)+c).

Its degrees force B=0; orthogonality gives C=0 and A,D in {+1,-1}.
The remaining coefficients give `c=0` or `1`, d=0, and equal absolute
amplitudes. Opposite tile interiors then require `a_i=-a_j`.

In a fully covered copy, every open port has a unique whole-port
partner. Polynomial arcs with no open coincidence have only finitely
many intersections, so finitely many such arcs cannot cover that port.
At a covered vertex every incident copy has a primitive vertex there:
a regular interface would already have its two whole-port partners
occupying the two sides and leave no room for the corner. The cyclic
adjacency of the filled star propagates the thirty-degree
rotation/reflection group to every incident copy, including a copy
touching only at the vertex.

Normalize the root pose to identity. Its neighbours lie in the finite
vertex-alignment set R: align one of fourteen prototype vertices with
one of fourteen root vertices using one of twenty-four linear motions.
After removing identity and duplicates there are 3,412 poses. In a
hypothetical two-corona patch, all first-prefix copies are fully
covered. Every second-layer copy used to cover a first-prefix boundary
point therefore lies in the finite two-step set

    U={compose(r,t): r,t in R union {identity}}.

Smallness makes positive reference-interior overlap a necessary
rejection. Indeed, for each overlapping reference pair from finite U,
choose a point a positive distance inside both reference interiors.
The least such distance is positive. Bow displacement is at most
epsilon/16, so a sufficiently small boundary homotopy preserves winding
number at every chosen point. Combine this with the positive Jordan
threshold for the single prototype. This supplies a uniform positive
epsilon_0 for all nonzero amplitude vectors, without enumerating U squared or evaluating
epsilon_0 numerically.

Between a fully covered copy and any incident copy, a proper reference
vertex/chord T contact is impossible: the covered reference star, or
the chord's full partner, would force a positive reference overlap.
Likewise a shared full reference chord must carry opposite signs, by
uniqueness of the covered copy's physical port partner. These conditions
apply between two first-prefix copies and between a possible second
copy and every first-prefix copy.

They are **not** imposed between two unfilled final-corona copies in
our upper certificate. The three-node certificate tests only their
positive reference-interior overlap and their occupied angles at old
vertices. It permits outer gaps, partial contacts, T contacts, holes
and pinches. Optional fillers cannot fix a missing covered sector and
are included whenever they could cover a tested sector.

## 2. Three complete periodic certificates

A pose is `(angle,flip,txa,txb,tya,tyb)`, where angle is in units of thirty
degrees and flip reflects the y coordinate before rotating. I denotes
identity. The certified repeated base copies and lattice vectors are:

| Packing | Base poses | U | V |
|---|---|---|---|
| A | I; `(1,1,-1,-3,-1,-1)` | `(3,-1,-3,-1)` | `(6,4,0,2)` |
| B | I; `(7,1,-2,0,2,0)` | `(3,-1,-3,-1)` | `(6,4,0,2)` |
| C | I; `(1,1,-1,-3,-1,-1)`; `(6,0,0,0,4,0)`; `(7,1,1,3,5,1)` | `(6,-2,-6,-2)` | `(6,4,0,2)` |

Here the lattice vectors use the same four-coordinate convention as
points. The determinant is `6+6*sqrt(3)=2A` for A and B, and `12+12*sqrt(3)=4A`
for C. Thus each cell has exactly the total area of its base copies.

The checker proves completeness of a tiny collision window. For every
difference d of a vertex from either base polygon and a vertex from
either other base polygon, it verifies

    |cross(d,V)| < 2*det(U,V),
    |cross(U,d)| < 2*det(U,V).

Every point difference of the polygons lies in the convex hull of these
vertex differences. If two translates intersect, the translation nU+mV
equals such a point difference. Hence integer |n|,|m|<2. The checks for
n,m in {-1,0,1} therefore include every possible intersection, even a
boundary contact. There are 34,34,140 ordered nonidentity comparisons
for the three packings. Exact triangle separation proves no positive
overlap, and exact segment tests exclude all proper T contacts.
Every base port has exactly one whole-port partner (28,28,56 partners),
and every base vertex has all twelve angular sectors occupied.

The periodic packing is locally finite. Its covered area on the
lattice torus equals that torus's area. The complement of its closed
union is open; if nonempty it has positive area. It is therefore empty,
so the reference polygons tile the plane.

The checker forms the port graph from **all** shared chords in each
complete collision window. A binary profile transfers precisely when
every graph edge has opposite signs. Each graph gives 128 words. Their
union P contains 320 different words, is closed under complementation,
and excludes both alternating Spectre words. P is generated exactly by
these three compact fixtures; no list of purported tilers is trusted.

The seven opposite pairs defining each periodic port graph give exactly
L_A,L_B,L_C in the theorem. Every amplitude vector satisfying those
equations transfers to its packing. For all sufficiently small
`epsilon=max_i |a_i|`, uniformly over these vectors,
the periodic edge graph deforms to the prescribed bowed graph. On the
torus there are finitely many edge and vertex neighbourhoods. Disjoint
nonincident edges have positive separation, outgoing rays retain their
order, and endpoint displacement is O(epsilon*t^2). Each shared edge
receives a single identical curve from its two copies. Choose disjoint
thin edge strips and small vertex disks; extend the graph deformation
over those neighbourhoods and over the complementary disk faces. This
is an ambient isotopy of the torus beginning at identity. Its lift is
lattice-equivariant and is an ambient isotopy of the plane. It takes
every reference polygon face to the Jordan disk determined by its bowed
boundary. These congruent bowed copies therefore tile the plane.
The finitely many edge and vertex types in the three embeddings, with
the uniform displacement and endpoint estimates, give a common positive
transfer threshold without a lower bound on the nonzero amplitudes.
L_S tiles by the primary Spectre construction for sufficiently small
|lambda|; its tilability is attributed, not inferred from a finite patch
picture. P is used as an auxiliary colour set in the remaining proof.

## 3. Complete first-prefix reduction outside the tilers

The preceding imbalance theorem already gives Hc,Hh<=1 for the 12,952
unbalanced words. It remains to test the 3,432 words with seven plus
ports. Opposite-sign equations are invariant under complementing all
fourteen bits. Use the 1,716 representatives with w<8192. Remove the
160 periodic representatives and the one alternating representative.
The reader tests every one of the remaining 1,555 words.

For a hypothetical second corona, Section 1 makes all first-prefix
copies fully covered. Against the root the exact geometric inventory
has 664 admissible reference neighbours. Their occupied sectors at
fourteen root vertices must fill the 96 missing root sectors without
overlap. A touching first copy contributes a positive sector; once all
root stars are filled, another touching copy would overlap locally.
Thus exact cover of these sectors includes every possible first prefix,
also when holes, pinches or optional fillers are permitted. Pair tests
check the full polygon footprint, all protected T incidences, and all
shared-port equations, including contacts away from the root.

Two complete searches over all 1,716 balanced representatives agree on
every pose set and its full word set:

* A signed-component search uses a graph on fourteen labels and a fixed
  sector order, with reversed candidate order. Its bipartite components
  supply all sign choices, filtered by seven plus bits.
* A separate word-domain search carries bit sets of all 1,716 words and
  branches on the sector with fewest available candidates. Its word
  rules do not use signed-component traversal.

Both generate the same 842 first prefixes and 382 words counting both
complements. Removing P and the alternating pair leaves 106 first
prefixes: 26 with seven copies and 80 with eight, including the root.
There are 125 remaining prefix/word pairs and 30 representatives.
Every such union has one simple oriented
boundary cycle and is independently checked to be a reference disk.
No intermediate-hole or disk prune enters either search.
Node and pair counts are regenerated in `expected.json`.

## 4. Local cuts and one short collision tree

For 124 pairs, the certificate gives an old vertex and a missing sector.
The reader independently generates every one of the 336 poses aligning
a prototype vertex there, using direct complex multiplication as a
control on repeated thirty-degree rotation. It rejects a sector-covering
pose only by occupied angles, protected reference geometry, or a
protected sign mismatch. Of 17,856 poses covering the named sector,
16,854 overlap occupied angles, 464 fail reference geometry, and 538
fail a port equation. None survives. No test between outer copies is
needed for these cuts.

The remaining word is `0x1569` (with complement `0x2a96`). It has one
seven-copy first prefix, specified literally in the certificate. Its
obstruction is the following complete decision tree, in four-coordinate
world vertices:

1. At `(-2,-2,2,-2)`, sector 10, the only admissible covering pose is
   `(7,1,-2,-2,2,-2)`.
2. After adding that forced copy, at `(-3,-2,2,-1)`, sector 1, the only
   admissible covering pose is `(0,1,-6,-2,4,0)`.
3. With both forced copies present, at `(-1,1,5,1)`, sector 8, no
   admissible covering pose exists.

At each node the reader regenerates all 336 anchors directly. It checks
the exact set of admitted poses against the declared branches, then
recurses into every branch. Across the three nodes there are 1,008
anchors, including 108 covering the missing sector without overlapping
its already occupied angles before other tests. Old-copy interactions
use the fully covered conditions of Section 1. Interactions with earlier
chosen outer copies use only positive polygon-interior overlap and
occupied sectors at old vertices. No outer sign condition or proper-T
ban is used. A real second corona must contain one of the admitted
covering poses at every node; the exhausted leaf is a contradiction.
The same tree works for the complement because all protected equations
only test opposite signs and all outer tests are sign-independent.

This excludes every balanced auxiliary word outside P and the
alternating pair. These same obstructions apply when the physical
amplitudes are unequal: only the reference geometry and the
opposite-colour equations on protected ports enter any upper test.

## 5. From auxiliary words to all nonzero amplitudes

In a hypothetical two-corona patch, let G contain every whole reference
port relation for which at least one copy belongs to the fully covered
first prefix. Include all fourteen labels, even isolated labels. Every
edge imposes `a_i=-a_j`. Nonzero amplitudes make G bipartite. Write W(G)
for all its binary opposite-colour assignments, with independently
chosen colours on each connected component.

Every component of G has equal bipartition sizes. Otherwise choose the
larger side of each component as positive; this gives more than seven
positive labels. It is an auxiliary word obeying all protected
relations of the actual patch. The earlier proof's complete
positive-imbalance enumeration and cuts exclude precisely this
necessary reference prefix/word configuration. This uses the
auxiliary-word certificate in Sections 4--6 of the preceding proof,
rather than inferring a physical amplitude-class imbalance. Thus every
word in W(G) is balanced.

The cuts in Section 4 now imply

    W(G) subset D := P union {0x1555,0x2aaa}.

Let G0 be the port graph of the extracted first prefix. G extends G0
by adding protected equations. Its components are balanced coarsenings
of those of G0: whole old components may merge, with their bipartitions
aligned or reversed, and no old component may split. Every possible
such coarsening has a binary word cube obtained by independently
flipping its whole component label sets.

The reader exhausts these coarsenings for **every one of the 842 first
prefixes**. Start with a base word in W(G0) intersect D, choosing its
representative below 8192. Partition the fourteen labels into whole
merged components. At each step the next component contains the
smallest unassigned label. Its mask must equal the difference between
the base and another permitted word. Require the mask to be a union of
old components, disjoint from earlier masks, and require every new cube
vertex to remain in W(G0) intersect D. Continue until all labels are
assigned. Flipping a balanced component leaves seven positive labels;
conversely a flip preserving seven positives has equal positive and
negative parts in that component. These conditions enumerate every
balanced coarsening. A leaf contained in any single one of the three
periodic colour sets or the alternating pair already implies a tiler.

For the nontrivial domains, this finite enumeration visits 32 nodes.
Only four first prefixes admit a coarsening whose cube is not contained
in any one tiler class. In each case the only such coarsening is its
original two components:

    {0,6,10} | {5,9,13},
    {1,3,7,11} | {2,4,8,12}.

The vertical bar separates opposite bipartition sides. Their sizes are
3+3 and 4+4, and their full colour set is
`{0xccb,0x1555,0x2aaa,0x3334}`. Their literal first poses are in the four
`refinement_cuts` fixtures; their identity is checked against the
regenerated complete frontier, not an external index list.

Each of those four prefixes has a sector that cannot be covered while
the port graph retains those two components. For the first two the
tested vertex is `(-3,1,3,1)`, sector 6; for the other two it is
`(6,-1,-1,-2)`, sector 7. The reader generates all 336 anchored poses at
each sector. A survivor must pass the covered old geometry, and every
protected relation must already be entailed by G0. No survivor remains.
An equation not entailed by G0 either connects two labels in the same
bipartition part (forcing zero, impossible) or joins the two components.
Consequently every real second surround must merge them, removing the
only exceptional coarsening. No assumption about the other outer
copies is used.

It follows that W(G) is contained in one periodic colour class or the
alternating pair. If two labels have opposite colours in every word of
W(G), they lie in opposite parts of the same component of G: independent
flips of different components prove the converse. Therefore containment
in a periodic class forces every corresponding equation `a_i=-a_j`
defining L_A,L_B or L_C. Containment in the alternating pair forces G
to have one component and gives exactly L_S. The actual amplitudes thus
belong to one of the four spaces, which tile by Section 2. This proves
the general theorem.

## 6. Attainment, thresholds and scope

Each of the 106 first reference disk patches matches every shared port
for its declared word. Its filled root stars and primitive whole-port
interfaces put the root strictly inside the union. The finite embedded
edge graph deforms by the same strip/vertex isotopy used above, preserving
that disk and the strict surround. Therefore all 30 listed
representatives and their complements have Hc=Hh=1 for sufficiently small
epsilon. The sixteen imbalanced sharp examples are inherited from the
preceding theorem. No zero-versus-one decision for every remaining word
is asserted.

Take delta smaller than the inherited finite-U/Jordan threshold,
the three periodic transfer thresholds, the two primary Spectre
thresholds, and the finitely many first-witness isotopy thresholds.
Each is strictly positive, so their minimum is strictly positive. This
is a rigorous uniform existential threshold for arbitrary nonzero
amplitudes, with no lower bound on their magnitudes. Floating-point sampling
and solver status play no role.

The trust boundaries are the inherited analytic covered-interface
bridge, the written uniform-smallness and isotopy arguments, the
primary Spectre theorem, and exact integer arithmetic in Q(sqrt(3)).
The new reader is standard-library Python; it imports no search output,
solver, external patch atlas or private ledger. Ten malformed certificate
controls reject, including deleted or altered forced branches; three
additional damaged component-joining fixtures reject. The
full certificate is 24,412 bytes. The first-prefix, port-graph and
collision checks finish exhaustively and contain no timeout.

The general finite-seven target remains open. The all-nonflat Tile(1,1)
quartic lane is now excluded for sufficiently small bows, including
unequal magnitudes.
The previously certified
[flat-port family](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/equilateral_flat_witness/proof.md)
has two coronas and a finite upper bound; flat phases and different
reference polygons remain separate frontiers.
