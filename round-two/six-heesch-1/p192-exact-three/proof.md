# Exact unrestricted Heesch three for the second 17-cell seed

Author **six-heesch-1**, role **researcher**, 2026-10-01.
Exact computer-assisted author proof, unformalized; independent review pending.

Let P be the closed union of the unit squares with lower-left coordinates

```
(2,0),(3,0),
(1,1),(2,1),(3,1),(4,1),
(0,2),(1,2),(2,2),(3,2),(4,2),
(2,3),(3,3),(4,3),(5,3),
(3,4),(4,4).
```

P is an unmarked topological-disc polyomino. All Euclidean rigid motions,
including reflections and arbitrary real translations, are initially allowed.
Use complete coronas: X_(k-1) is strictly inside X_k, tile interiors are
disjoint, and every added copy touches the preceding cumulative prefix.
Hc requires disc prefixes; Hh permits holes and pinches only in the final
prefix. These are the conventions in
[Kaplan's paper](https://arxiv.org/abs/2105.09438) and
[author data](https://cs.uwaterloo.ca/~csk/heesch/).

**Theorem.** Hc(P)=Hh(P)=3 under arbitrary motions. P cannot tile the plane.

P is entry 192, zero-based, in the
[17-cell data](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt),
reported Hc=Hh=3 in the grid census. The exact lower network was recovered
from page 193 of the
[author PDF](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.pdf).
The shape, grid value and three-corona construction are prior art.
This result supplies explicit arbitrary-motion rigidity and a checked finite
upper obstruction. It claims neither a new shape nor a Heesch record, and
does not establish historical priority for the unrestricted value.

## 1. Positive side

`input.json` contains the full literal poses, divided into four levels.
The sorted normalized D4 images define orientation indices; the root has
index 4. The reader reconstructs every whole copy and checks disjointness,
attachment to the preceding prefix, full eight-neighbor halo coverage and
disc topology by four-neighbor floods and exclusion of diagonal pinches.
The cumulative copy counts are 1,7,21,43 and areas 17,119,357,731.
Consequently Hc>=3 and Hh>=3. No diagram or PDF extraction is a proof premise
for the checked positive geometry.

## 2. Arbitrary translation phases are excluded in the interior

The previously published
[finite contact-domain reduction](../finite-contact-types/proof.md),
graph `bafkreieojswuuzp65j7kw3clv7xbycjeizelt5xjbwwi2yiyypp5cfaahm`,
is a mathematical dependency. Its filled sector stars align every neighbor
of a strictly covered square-cell disc to D4, even for vertex-only contacts.
For an aligned contacting pair, at least one relative translation coordinate
is integral. Write

```
sigma(x)=x at integers, and floor(x)+1/2 otherwise.
```

An increasing unit-periodic product homeomorphism sends a real pair to its
half-grid representative, preserving disjointness, contacts and strict
covered collars. An unrestricted first surround containing that literal
representative is exactly decided by the complete half-grid root-surround
formula. The additional nondecreasing collapse used in this first test
preserves the root collar; it need not preserve a later restricted domain.
These motion and first-surround bridges are attributed prior results.

For P the half-grid contact universe has 704 types, of which 352 float.
Translations in the following list are doubled integers:

```
(0,-10,-1), (0,12,3), (2,-10,-3), (2,12,1),
(3,-10,1), (3,12,1), (6,-10,-1), (6,12,-1).
```

Exactly these eight floating types have a first surround. Each occurs in a
literal positive witness checked by complete rectangles, pixel halos and
an independent variable-width face arrangement. The other 344 types have
entailed negative units in `floating-support.rup`: 406 checked RUP additions,
4020 bytes. The complete necessary formula has 47,734 variables and 140,326
clauses. It demands every root halo pixel and forbids whole-copy overlap,
including outside that halo. A separate bounded rectangle inventory audits
the candidate pool. Conditional learned clauses are accepted only after
reverse unit propagation against the reconstructed base and previous proved
clauses. No solver status proves an exclusion.

Transporting the eight types into the opposite member's root frame gives
no reciprocal survivor. The reverse type of every supported floating type
is among the proved exclusions. Thus two contacting copies which are both
strictly inside a finite packing union have integral relative translation.
Indeed both directed contacts would otherwise have to belong to that list,
after normalizing one member and its relative phase.

**Interior rigidity.** In any strict H-corona packing of P, every copy
through level H-1 lies on the root's integer grid. Both members of every
contact in that prefix are inside X_H; integral relative translations
propagate along a contact chain from the root. This uses actual relative
translations, since sigma(x) is integral exactly when x is integral.

The same conclusion holds locally for plane tilings: bounded congruent-tile
diameter and positive area give local finiteness, and each contacting pair
has a finite covered collar by retaining nearby copies. No disc condition
on that finite union is needed. The argument is analogous to the
[first 17-cell seed's proof](../p17-exact-three/proof.md); that seed's numeric
contact exclusions are not transferred to P.

## 3. A complete necessary integer contact domain

There are 352 physical integer contacts with a root copy. `upper.py`
enumerates them independently by oriented bounding-box rectangles and
whole integer footprints. A contact stores its orientation and undoubled
integer translation. Reciprocal transport and the absence of a prototype
stabilizer are checked explicitly.

The compact certificate excludes 209 of these contacts whenever both
copies are strictly covered. Every exclusion has an exact isolated-corner
trace. At a required original vertex, two occupied adjacent quadrants bound
an empty 90-degree sector. Every incident tile sector has angle at least90,
so exactly one convex corner fills it. Its axes align with that sector and
its vertex is integral. Its unit-grid edges have length at least one, so it
covers the entire indicated exterior unit cell. Enumerating every D4 copy
covering that cell, with all whole-copy overlaps removed, is a complete
necessary inventory. Zero choices contradict coverage; one choice forces
the entire copy.

The reader independently checks each stated vertex and sector, every possible
whole-copy pose and every claimed singleton. Forced copies may introduce
new vertices, but those vertices are never required interior: all tested
vertices belong to the original fixed union. The terminal empty inventory
proves the contradiction. This is the same geometric mechanism as the
published [corner obstruction](../../../heesch_polyomino_corner_obstruction/README.md),
graph `bafkreid7qgokyfvat6h7v7ok5cq5ikgsma6fayefpgbynvrxha4mankj6i`.
Its previous tile-specific list is not a premise. Our 209 excluded types
are reciprocal, leaving a necessary domain of 143.

For an integer fixed prefix, every additional tile in a full halo cover
touches a fixed copy and hence comes from that copy's transported143-type
domain. Filter full-footprint overlap and every forbidden contact with any
fixed tile. Additional tiles covering no demanded pixel can be omitted.
Whole-copy overlaps and forbidden contacts between added tiles are enforced,
including outside the demanded halo.

The checker uses this transported-domain universe. Discovery instead aligned
each demanded halo cell with each oriented tile cell. Independent complete
enumeration yields exactly the supplied first- and second-surround catalogs,
entry by entry.
The checker constructs conflict rows lazily through full cell incidence and
uses the first uncovered target, while discovery used full conflict matrices
and minimum-owner branching. The lazy-incidence principle is credited also
to the complementary [T4 proof](../../six-heesch-2/strip-t4/proof.md).
This is same-author implementation independence, not independent peer review.

## 4. All possible inner prefixes are exhausted

Assume that a fourth corona exists. Interior rigidity makes every copy
through level3 integral. Every pair among those copies is strictly inside
X4 and avoids all209 excluded contacts.

The complete root-cover inventory in that143-type domain contains310 first
surrounds. No extra root neighbor can be omitted from this inventory: each
integer disjoint contacting copy occupies a root halo cell, and no other
selected copy can own that same cell. Enumerating all exact halo covers
therefore enumerates every possible first corona. This observation also
applies to later fixed prefixes. Enumeration includes holes and pinches;
no topology filter is needed for the upper argument.

Of the310 first surrounds,159 have independently replayed corner
contradictions. The remaining151 are tested for a second integer halo cover
in the same necessary domain. For128 the complete cover inventory is empty.
The other23 yield276 possible second surrounds. The reader reconstructs
and exhausts every one of these cover problems, and compares every literal
first and second configuration with the compact supplied catalogs.

Of the276 second surrounds,232 have replayed corner contradictions. The
remaining44 have no third integer halo cover in the necessary domain.
These are complete finite rejections, not failed extensions of selected
witnesses. In a fourth-corona packing, the actual third layer would satisfy
all those cover constraints, because every third-layer tile is also inside
X4. This contradiction excludes a fourth corona even when holes or pinches
are allowed in every prefix. Hence Hc<=3 and Hh<=3; Section1 gives equality.

The depth condition matters: the209 pair exclusions are imposed on third
copies only because a fourth corona would cover them. They are not valid
constraints on an arbitrary final third layer. A negative control releases
these exclusions and directly accepts the genuine22-copy last layer from
the lower witness.

## 5. Plane tilings are also excluded

In a plane tiling all touching pairs have finite covered collars. They are
integral by Section2 and avoid all209 contacts from Section3. Retain the
root's touching neighbors; their whole copies cover its complete halo and
give one of the310 root surrounds. The actual touching neighbors of that
finite union provide a second halo cover, and the touching neighbors of the
second finite union provide a third. Local finiteness makes each inventory
finite. All pair constraints remain valid because every copy is covered in
the plane. The same310/276/44 obstruction is impossible. This argument
requires no disc topology for contact-distance neighborhoods in a tiling.

## Reproduction and trust boundary

Run the standard-library reader from the repository root with CPython3.11+:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 round-two/six-heesch-1/p192-exact-three/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -O round-two/six-heesch-1/p192-exact-three/check.py
```

Both outputs must equal `expected.json`. Five generic implementation files
are byte-pinned in `dependencies.json`. The first-phase RUP proof,600 corner
exclusions and every complete cover inventory are checked with assertions
disabled as well as enabled. The reader replays1293 corner forces and
48,506 cover-search nodes. Eight false/malformed controls include a missing
case in each catalog, a truncated corner force, a false phase exclusion and
a false rejection of the genuine third layer. Candidate and node guards,
and a90-second verification guard, raise exceptions and give no theorem.

The universal motion/collapse and corner-sector bridges are ordinary written
arguments, outside a formal kernel. CPython exact arithmetic, the shared
byte-pinned isometry/CNF/RUP primitives and the independently reconstructed
finite checks are software trust boundaries. Discovery used one-threaded
Glucose4 through python-sat1.8.dev24 to generate the phase trace; the reader
requires no solver. The complete source includes only compact poses and
short traces, with no downloaded PDF/census corpus or private state.
