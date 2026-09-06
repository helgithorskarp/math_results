# An arc-classification obstruction to the Paley(49) switching family

**Theorem, using the published Hill–Love classification.** Every graph obtained
by taking any 43 vertices of Paley(49) and applying an arbitrary Seidel switch
has a clique or independent set of order five. Thus the entire six-deletion,
arbitrary-switch family is excluded, including every relabeling and color
reversal. No automorphism, degree profile, catalog parent, or neighborhood
constraint is imposed on the resulting graph.

The proof establishes the stronger intermediate statement that every
22-vertex induced subgraph of the **unswitched** Paley(49) has a monochromatic
five-set. Splitting a switched graph into its two switch classes then bounds
the order of a Ramsey subgraph in this switching family by 42. Neither upper
bound is claimed sharp. There is no construction on 42 or 43 vertices here,
no bound improvement for R(5,5), and no exclusion of arbitrary rank-26 graphs.

The finite certificate is 714 physical five-set witnesses. The only imported
mathematical classification is:

In the form used here: up to projective equivalence, PG(2,7) has three types
of 22-point sets meeting every line in at most four points.

This is the published result of Ray Hill and Chris P. Love,
[On the (22,4)-arcs in PG(2,7) and related codes](https://www.sciencedirect.com/science/article/pii/S0012365X02008129),
Discrete Mathematics 266 (2003), 253–261,
DOI [10.1016/S0012-365X(02)00812-9](https://doi.org/10.1016/S0012-365X(02)00812-9).
The paper treats the type without 2-secants geometrically and uses a MAGMA
classification for the remaining two types. **That classification is not
recomputed here.** The checker verifies three inequivalent representatives
and the whole subsequent affine reduction, relative to this published theorem.

## 1. The graph and the geometric reduction

Write F49 = F7[t]/(t²−3), encoding x+yt as x+7y, with 0≤x,y<7. Since 3 is a
nonsquare modulo 7, this is a field. Distinct field elements u,v are adjacent
in Paley(49) precisely when u−v is a nonzero square. Red denotes adjacency.

Every affine F7-line is monochromatic: its nonzero differences are c·d with
c in F7*, and all such c are squares in F49. Consequently a subset with no
monochromatic five-set has at most four points on each affine line. A
22-point such subset, embedded in PG(2,7), would be a four-arc whose line at
infinity is empty.

The certificate supplies three literal 22-point projective sets. Coordinates
are normalized so their first nonzero entry is 1. A projective line has the
same coordinate convention and incidence is the vanishing dot product.
Checking every one of the 57 lines gives these profiles; the entries count
lines meeting the set in exactly j points:

| Representative | j=0 | j=1 | j=2 | j=3 | j=4 |
|---|---:|---:|---:|---:|---:|
| 0 | 7 | 1 | 0 | 21 | 28 |
| 1 | 6 | 2 | 3 | 16 | 30 |
| 2 | 4 | 4 | 9 | 6 | 34 |

Each is therefore a four-arc. Distinct line profiles imply projective
inequivalence. The imported three-class theorem now ensures that these three
literal sets represent every 22-point four-arc. Their labels or construction
history are not needed by the checking kernel.

[build.py](build.py) obtains the representatives from a conic: its internal
points are modified by selected conic points and diagonal points.
[check.py](check.py) imports no producer code and checks only the literal
coordinates, incidence, sizes and three distinct profiles. It does not need
to trust that construction.

## 2. Why exactly 714 coordinate cases cover all affine embeddings

Fix a representative C and a projective image of it lying in the affine
plane. Pull the line at infinity back to a line L disjoint from C. The table
shows that there are 7, 6 or 4 choices for L, respectively.

For L=(l0,l1,l2), let k be the largest index with lk≠0, and let i<j be the
other coordinate indices. The canonical chart is

    P ↦ (Pi/(L·P), Pj/(L·P)).

Its three defining linear forms Pi, Pj and L are independent, so it is a
projective coordinate change with L as infinity. Its restriction maps the
49 points outside L bijectively onto F7². Any other projective map carrying
L to infinity differs from this chart by an invertible affine map.

In field coordinates, such an affine map has the form

    (x,y) ↦ a·x + b·y + c,

where a,b are independent over F7. In particular a≠0 and z=b/a lies outside
F7. Translation by −c preserves all differences. Multiplication by a⁻¹
either preserves every Paley edge color or reverses every color, according
to its quadratic character. Both operations preserve the existence of a
monochromatic five-set. It therefore suffices to check

    (x,y) ↦ x + z·y,   z∈F49\F7.

There are 42 values of z, encoded as 7..48. No arbitrary GL(2,7) map is being
assumed to preserve the Paley graph; all of them are covered by these 42
normalized choices after removing the valid scalar and translation factors.
The complete case count is

    (7+6+4)·42 = 714.

For each case, [certificate.json](certificate.json) gives a color and five
distinct indices in its representative. The checker reconstructs the image
and verifies all ten physical pairs by the independent norm formula

    x+yt is a square iff (x²−3y²)³ = 1 mod 7.

For nonzero x+yt, its norm x²−3y² is nonzero; the criterion follows from
Norm(z)=z⁸ and z²⁴=(z⁸)³. The producer instead enumerates squares by field
multiplication. Every expected case occurs exactly once. The certificate
contains 702 red and 12 blue witnesses, with no missing or extra case.

Thus no 22-point four-arc image can be an induced Ramsey subgraph of
Paley(49). Together with the monochromatic-line argument, this proves the
22-point lemma for **every** subset, including those that are not four-arcs.

## 3. The complete switching-family obstruction

For selected points U and switch bits s, a physical edge has red indicator

    Puv XOR su XOR sv.

Within each of the two sets su=0 and su=1, the induced graph is unchanged.
If |U|≥43, one class has at least 22 points. Choose 22 of them. The preceding
lemma supplies a monochromatic five-set in the unswitched graph, and all its
edges retain their colors after switching. This is the required obstruction.

The argument covers every subset U and every switch. For a fixed 43-point U
there are 2^42 distinct switches because global bit complementation has no
effect. We do not claim that the graphs obtained from different U remain
distinct after relabeling. Color reversal is also covered: multiplication of
all field points by a nonsquare reverses every base color.

The extractor accepts a JSON object with 43 distinct field labels in `points`
and 43 binary entries in `switch`. It takes the first 22 indices of a largest
switch class and directly searches its five-subsets. Its output includes the
complete sorted red-edge list and the actual forbidden five-set.
[verify_witness.py](verify_witness.py) imports no graph-construction or
extraction code; it checks the literal edges and all ten witness pairs.
The fixture is deliberately non-Ramsey and is not a claimed candidate.

## 4. Reproduction and evidence

From the full `math_results` checkout, with Python 3.11 or later:

```sh
python3 -B ramsey_r55_paley49_arc_obstruction/reproduce.py
python3 -O -B ramsey_r55_paley49_arc_obstruction/reproduce.py
```

Both modes print
`VERIFIED_PALEY49_SWITCH_OBSTRUCTION_WITH_HILL_LOVE_PREMISE`, with
714 affine cases and 7,140 physical witness pairs. No SAT solver, native
compiler, network, proof trace or private input is required. The optional
prior-family separation checks use the small existing catalog fixture in
the adjacent public `ramsey_r55_catalog_switch_extensions` directory;
the main obstruction does not depend on it.

For the main certificate alone, the directory is self-contained apart from
the stated published mathematical premise:

```sh
cd ramsey_r55_paley49_arc_obstruction
python3 -B build.py | cmp - certificate.json
python3 -B check.py certificate.json
python3 -B extract.py fixture.json | cmp - fixture_witness.json
python3 -B verify_witness.py fixture_witness.json
sha256sum -c SHA256SUMS
```

Controls verify the factorization of all 2,016 invertible linear maps on
all 49 points (98,784 identities), 56,448 scalar edge-color transfers, all
57 complete affine charts, and all 2,401 base field-pair colors. They also
check extraction in 64 full 43-vertex graphs, including color reversals
and reordered labels, against all 57,792 physical pairs. Six certificate
mutations, eight malformed extractor inputs, and one altered physical
witness are rejected. Normal and assertion-disabled runs agree exactly.
These controls validate the implementations and coordinate transport; they
do not replace the imported projective classification.

The complete proof comprises the published classification, the displayed
geometric reduction, and the finite physical witness certificate. Trust
remains in that published theorem, the unformalized reduction, exact Python
implementations and integer semantics, and ordinary hardware. This is
author validation, not external peer review or proof-assistant formalization.
The preliminary direct and reduced SAT calls returned UNKNOWN; neither
their outputs nor their incomplete traces is a premise of this proof.

## 5. Distinction from prior construction families

The early checks in [separation.py](separation.py) establish that both binary
adjacency ranks of Paley(49) are 24. Switching adds a matrix of rank at most
two, and principal submatrices cannot increase rank. Thus both color ranks
of every new-family graph are at most 26.

The known seven-defect cyclic graph has color ranks 40,42; the cyclic seed
has 42,42, and the primary two-defect graph has 42,40. All 328 supplied
42-vertex catalog parents have both color ranks at least 36, so their
switches and arbitrary one-vertex extensions have rank at least 34 on a
principal block. These named families are therefore disjoint from this one,
under arbitrary relabeling and color reversal. No catalog-completeness
assertion is needed for this finite comparison.

The Paley(41) switching family needs another invariant: its binary rank is
20. Direct integer checks give Sn²=nI−J for the Seidel matrices at n=41,49.
For any 41-point principal block T of a switch of S49, partitioning off the
other eight points gives

    T²−49I = −w·wᵀ−B·Bᵀ,

of rank at most 9. For a switch of S41 the same expression is −8I−z·zᵀ,
which has rank 41. Hence the full Paley(41) switch-plus-two family is also
disjoint. These comparisons do not claim separation from every state of
every old cyclic sublevel component.

Paley graphs, switching, four-arcs and the Hill–Love classification are
established mathematics. A limited targeted literature and Discovery Net
search found no matching Paley(49) Ramsey-switching obstruction. This is
not a historical-priority claim. The new contribution is the 22-point Paley
consequence, its full switching-family use, and its compact reproducible
physical certificate. The inherited symmetry and global degree-profile
frontiers are unchanged; R55-3's global-exclusion lane is separate.
