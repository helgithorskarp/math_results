# Exchange family and a star-type odd-cycle obstruction

Actual agent: **six-heesch-2**. Role: **researcher**.

This is a computer-assisted exclusion of a particular finite family, together
with a local obstruction that succeeds after pair closure has stabilized.
It does not produce a finite-five polyhex or assert a new Heesch record.

## Statement and conventions

Let `S` be the seventeen-cell polyhex in [seed.json](../seed.json), the known
Heesch-four example from Kaplan's census. Consider every eighteen-cell union

`(S \ {d}) union {a,b}`,

where `d in S`, the two additions are distinct and outside `S \ {d}`, and
the final union is connected and hole-free. Reintroducing `d` is allowed.
The deletion intermediate need not be connected. Identify shapes under all
twelve honeycomb orientations and translations.

There are **4,990** such free shapes: **495** tile periodically; every other
member has `H_h <= 2`. More precisely, 3,471 have `H_h=0`, 1,008 have `H_h=1`,
two have checked `H_h=2`, and fourteen have `1 <= H_h <= 2`. Exact values for
those fourteen are not supplied. In particular no finite member of this
family can meet the finite-five polyhex target.

The root is level zero. A new copy touches the previous corona, and each
cumulative prefix is contained in the interior of the next prefix. `H_c`
requires every cumulative union to be a disc. `H_h` permits holes only in the
last cumulative union. Boundary-point contact counts; reflections and all
real Euclidean motions are allowed. The computation relaxes local holes
when proving upper bounds. The standard polyhex angle/edge argument in the
[parent proof](../proof.md#geometric-bridge) locks complete coronas, including
the last, to the honeycomb grid. Thus these are all-motion upper bounds.

Plane tiling is excluded separately for every finite classification, without
assuming a plane tiling's contact balls meet the disc-prefix convention.

## Exact generation

After fixing a deletion, every connected final union has one added cell
edge-adjacent to an old cell. The second addition is adjacent to an old cell
or the first addition. Otherwise the component of the two additions would
be isolated from the sixteen old cells. This remains valid if the old cells
have multiple components. Sequential halo additions therefore enumerate
every permitted shape. Connectivity and outside flood-fill reject invalid
final unions; canonicalization removes free congruences.

The independent generator uses a uniform radius-two pool about `S` and every
unordered pair, rather than a sequential growth order. Each addition in a
connected final union is at distance at most two from an old cell. Exact
integer honeycomb vertices determine all full-edge cell incidences and a
union/find component count. For these honeycomb cell unions, connectedness
and Euler characteristic one are equivalent to a disc: each vertex meets
one, two or three of its three hexagons, so there are no point-only pinches.
The Euler characteristic of a connected union is `1 - number_of_holes`.

The two generators agree on every canonical member. They check respectively
6,080 and 26,236 raw sets. Both share the integer canonicalization primitives;
the topology and enumeration routes are different. The family SHA256 is
`8d6fb52b9f5db3f8fdc7ebd3458022b96feb3425fadeb08fd7af787f45f6d3fe`.

Exactly 26 members are the already published one-cell grafts. The other 4,964
do not embed the earlier sixteen-cell growth seeds or articulation remainders,
as checked by all orientations/translations in the parent family code.
This is disjointness from those specific published families, not a historical
novelty assertion about every individual eighteen-cell polyhex.

## Necessary contact domains

The [parent pair-peeling proof](../proof.md#complete-finite-contact-universe)
defines `E_0` as all disjoint contacts and retains a pair in `E_(r+1)` exactly
when its two copies can be jointly halo-surrounded by a disjoint
`E_r`-compatible packing. Compatibility tests every contacting pair,
including contacts between added copies. Domains are stabilizer-invariant
and reciprocal, and the source checks both properties.

The depth lemma is: in an `H`-corona patch, every contact between copies of
levels at most `H-r` lies in `E_r`. Consequently an `E_r`-compatible root
surround failure excludes `r+1` coronas. In a plane tiling every actual
contact lies in every `E_r`, by induction on its finite neighbor stars.

There is also a cheaper depth-one domain. Let `F` consist of contacts
appearing in any unrestricted full root surround. Let `D` be the reciprocal
part of `F`. Every contact between two interior copies belongs to `D`,
because both copies have their actual complete unrestricted stars. In a
two-corona patch the root and its first neighbors are interior, and every
contact among them belongs to `D`. Failure of a `D`-compatible root surround
therefore gives `H_h <= 1`. The same failure excludes plane tiling.

Every exclusion used to construct `F` is DAG-audited. When forming `E_1`,
`D` restricts only the tested fixed pairs; candidate new neighbors still
come from **all `E_0`**. Filtering those candidates to `D` would consume an
extra interiority condition and invalidate this depth accounting.

The complete replay uses 3,471 root failures, 993 `D` root failures, fifteen
`E_1` root failures, fifteen `E_2` root failures, the single obstruction
below, and 495 periodic certificates. Every positive first surround is
checked as a geometric corona construction before a finite case is assigned
a positive lower bound. Fourteen upper-two cases retain only a one-corona
lower certificate in this classification.

## Odd-cycle obstruction after pair stabilization

For a general sound domain `E_r`, a copy of level `ell <= H-r-1` has a
complete `E_r`-compatible star: every neighbor has level at most `ell+1`,
so all contacts of the star are covered by the depth lemma. Several such
stars whose centers have levels at most `q` have an `E_r`-compatible union
whenever `q+1 <= H-r`.

If a compulsory odd contact cycle has centers at levels at most `q`, their
complete stars admit exactly two well-defined types, and equal types at
each successive edge have an inadmissible union, then `H >= q+r+1` is
impossible. An odd cycle cannot be colored with two alternating types.
The geometric frames must agree around the cycle; this is explicitly
checked in the application. This is elementary local-rule parity with a
corona-depth interface, not a claim of priority for odd-cycle coloring.

The exceptional shape is canonical index **3598**, with cells

```
(0,0) (0,1) (1,-4) (1,0)
(2,-5) (2,-4) (2,-3) (2,-1) (2,0)
(3,-4) (3,-3) (3,-2) (3,-1)
(4,-4) (4,-2) (4,-1) (5,-2) (5,-1)
```

Its tile SHA256 is
`2e36052b2e2a0fbe68f13106d550bdea0b51aa7822b80c9a37fb2a4f7864f0e6`.
It has no nonidentity stabilizer. The unrestricted contact inventory has
549 members; audited pair closure gives `549 -> 11 -> 10 -> 10` and still
permits a root surround. This is a concrete reason stabilization alone
cannot establish tiling or infinite Heesch number.

There are exactly **two** `E_1`-compatible full stars, of degrees five and
seven. `parity.py` independently enumerates all `2^11` contact subsets and
checks coverage, whole-footprint disjointness and contact compatibility,
then compares the complete star sets with the exact-cover enumeration.

Use the integer isometry

`g(x,y) = (y+1, -x-y-1)`.

It has order three. Both stars contain `gS` and `g^2 S`; hence the three
distinct copies `S,gS,g^2S` are a compulsory contact triangle. The stars are
expressed in the unique physical frames `1,g,g^2`, whose product closes to
the identity. For each of the two types, the union of its root star and its
same-type image at `gS` is rejected by a direct overlap/contact-domain check.
Transport gives the same rejection at the other two edges. Thus every edge
of this triangle requires opposite types.

If three complete coronas existed, the triangle's three centers would have
levels zero or one. Their full `E_1` stars would exist and all their star
copies would have levels at most two, which equals `H-r`. The equal-type
rejections therefore apply to these actual stars. Alternation on a triangle
is impossible. This proves **`H_h <= 2`**. All plane stars likewise satisfy
`E_1`, so the same triangle separately rules out plane tiling.

A checked construction has new-copy counts `1,7,14`, cumulative cell counts
`18,144,396`, and hole-cell counts `0,0,4`. It proves two complete `H_h`
coronas and one complete `H_c` corona. Therefore **`H_h=2`** and
**`1 <= H_c <= 2`**. The exact `H_c` value is not asserted. The other exact
two case, index 3602, is the previously published graft case 18, reproduced
here rather than claimed as new.

## Evidence and limits

Every negative exact-cover decision is checked by the parent cell-incidence
auditor, including support exclusions and pair exclusions. It rebuilds
coverage and full-footprint/contact conflicts, then verifies the complete
acyclic failed-state DAG. Positive covers are checked directly. The node
guard raises `Incomplete`; an interrupted, timed-out, guarded or missing
case never becomes a negative mathematical verdict.

The 495 periodic certificates have one, two or four copies per fundamental
domain (84,345,66 cases respectively). Their integer lattice bases and copy
poses occupy about 39KB. The independent lattice-difference checker tests
every pair of occupied cells modulo the proposed lattice. Exactly as many
distinct classes as the lattice index prove nonoverlap and full coverage.
No minimum period size is claimed. Failed period proposals were used only
for exploration and have no role in the upper proof.

The implementation, integer-isometry primitives, geometric bridge and depth
argument are unformalized trust boundaries. The two enumerators and auditors
share those primitives. Internal checks are not independent peer review.
Raw rejection DAGs and exploratory JSONL data are regenerated and omitted.
An optional private checkpoint resumes already completed source checks; it
is operational state, not a standalone proof certificate. The default
command regenerates every decision without such state.

Primary background: Kaplan, *Heesch Numbers of Unmarked Polyforms*,
[arXiv:2105.09438](https://arxiv.org/abs/2105.09438), and the
[author's census](https://cs.uwaterloo.ca/~csk/heesch/).
The unrestricted-size finite-five polyiamond premise is already satisfied
by the attributed Mann construction; see
[Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf) and the
[published realization](../../../heesch_polyiamond_hexapillar/README.md).
The retained constructive frontier here is a finite-five **polyhex**.
