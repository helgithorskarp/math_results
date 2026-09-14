# Every qualifying paired Golomb augmentation of GMM490 is four-colourable

**No sub-509 construction was found.** For the fixed 490-point GMM seed B,
the archived proper four-colouring extends to every union of zero, one or two
Golomb copies in the precise outside-field class below. This closes the
proposed paired construction at the record budget; it is not a global HN
vertex bound or an exclusion of arbitrary larger assemblies.

The finite family contains **3,616 distinct nine-new-point augmentations**.
All **6,535,920 unordered pairs** are covered, hence all 6,539,537 choices of
zero, one or two augmentations. Different choices can give the same physical
union; these are not asserted to be distinct graph counts.

## Physical scope

Put alpha=i sqrt3, beta=i sqrt11, E=Q(alpha,beta), K=E(sqrt5), and

```
u = (7+alpha sqrt5)/8,  v = (-1+alpha sqrt5)/4,
B = G + u M + v M.
```

M and G are the standard seven-point Moser and ten-point Golomb motifs from
the [parent source](../hadwiger_nelson_single_anchor_field_gate/README.md).
B has 490 distinct plane points and 2,435 strict unit edges. Each added G copy
is congruent or reflected, shares one old point, has a unit multiplier outside
K, and has new vertices incident with at least four distinct old vertices,
including the shared anchor. A second old coincidence would force its
multiplier into K, so exactly nine points are new. Two copies give at most
490+9+9=508 points, with collisions merged exactly.

The parent proves that its complete 5,424 anchored polynomial recipes cover
this class. Each irreducible quadratic has two physical unit roots. Here both
roots of all recipes are reconstructed, producing 10,848 rooted copies.
Their new-point sets deduplicate exactly to 3,616 physical augmentations.
No heuristic or unproved symmetry quotient is used.

## Exact interaction census

The 41 positive radicands fall into 39 distinct nontrivial square classes over
K. For each class select one radicand s. Express every new point uniquely as
`A+B sqrt(s)` with A,B in K and B nonzero. Changes of square-class representative
are checked by exact square-root identities and every resulting multiplier
is checked to have norm one. Thus equality within a class is coefficientwise,
and points in distinct classes cannot coincide.

There are 15,128 distinct new points. Complete geometry gives:

| Edge type | Count |
|---|---:|
| Old-to-new unit edges | 5,570 |
| New-to-new unit edges within one quadratic class | 53,862 |
| New-to-new unit edges between different classes | 0 |

For within-class pairs, if the difference is `a+b sqrt(s)`, squared distance
one is equivalent to the two exact K identities

```
N(a)+s N(b)=1,
a conjugate(b)+b conjugate(a)=0.
```

A sound finite-field projection screens 14,905,856 old/new and new/new pair
instances. All rational denominators have nonzero image. The prime and base
radical images are verified by the parent arithmetic module. C++ enumerates
every pair, its entire candidate stream is compared entrywise to Python, and
all 59,432 surviving candidates pass the full exact rational identities.
The native products are below (1,000,000,021)^2 < 2^63, and the complete run
passes undefined-behaviour checking.

Across distinct classes, the parent's analytic
[interaction lemma](../hadwiger_nelson_single_anchor_field_gate/JOINT_FILTER.md)
is complete: unit adjacency requires a common root-pair midpoint, perpendicular
displacements and squared displacement radii adding to one. Grouping the
exact midpoints finds no different-class pair satisfying even the radius-sum
condition. This proves the zero in the last table row; it is not an inference
from approximate distances or a sampled cross-field search.

The 15,618-point inventory is used to reconstruct pair interactions. This
package does **not** claim that its entire unit graph is four-colourable.

## Complete pair coverage and compact positive certificate

Fix the parent's checked seed colouring. Each new point gets the list of
colours absent from its old neighbours. A pair interacts if its new-point
sets overlap or there is any unit edge between them. The two independent
pair enumerations identify 126,192 interacting pairs. The other 6,409,728
pairs have disjoint new-point sets with no mutual edges; their individually
checked extensions combine directly.

The checker constructs every interacting union and its complete list graph.
Its order distribution, excluding the 490 old points, is:

| New points | Interacting pair choices |
|---:|---:|
| 12 | 5,168 |
| 15 | 7,260 |
| 17 | 17,632 |
| 18 | 96,132 |

All noninteracting pairs have 18 new points. Every single-copy graph has
nine. Hence the verified family includes actual supports of orders 490,
499, 502, 505, 507 and 508.

A deterministic greedy rule selects an uncoloured vertex by smallest
available list, then largest uncoloured degree, then lowest label, and uses
its lowest available colour. It succeeds on 50,653 distinct list-graph
profiles. For the remaining **191 profiles**, `exceptions.json` supplies a
positive word. Together this covers all 129,808 single/pair queries and
50,844 profiles. Profiles retain their exact adjacency and allowed lists;
no graph-isomorphism assumption is needed.

The checker verifies every returned word against the actual new graph and
old-neighbour lists, rather than trusting a search verdict. Seven malformed
or missing-certificate controls must fail. A small sharp cross-field fixture
checks the independent square classes 1/2 and 1/6 and the perpendicular
unit contact between sqrt(1/2) and alpha sqrt(1/6). The seed's complete
119,805 pair metric is reconstructed separately in real coordinates.
`EXPECTED.json` also pins an actual 508-point/2,480-edge greedy-exception
fixture and its complete proper four-colouring.

The native discovery search used bounded exhaustive list backtracking. Every
query was positive; there was no unknown or list obstruction. Its whole pair
selection stream matches the Python checker entrywise, and regenerates the
exception certificate byte for byte. Native solver code is optional for
checking the theorem: the standard-library checker uses only greedy positive
words and the saved exceptions. No SAT verdict or floating-point calculation
is a theorem premise. This is author-side computer-assisted verification,
not independent-author review or proof-assistant formalization.

## Reproduce

Use a complete repository checkout. Dependencies in the parent package are
byte-pinned by `SOURCE_PINS.json`; their own arithmetic and source pins are
also checked. CPython 3.11.2 and g++ 12.2.0 were used. The main replay requires
only the Python standard library and a C++17 compiler. From this directory:

```sh
python3 -O -B run.py --work /tmp/hn-paired-golomb --sanitize
sha256sum -c SHA256SUMS
```

The work path must be empty. The default command rebuilds the complete parent
Golomb contact census before generating this support. To reuse an already
reproduced parent stream, add
`--parent-census /path/to/G_census.json`; its exact record hash is checked.
The measured replay reused that frozen parent stream, generated all new
points in about 55 seconds, reconstructed geometry in 98 seconds, and
verified pair coverage in 17 seconds. Normal and optimized Python agree.

Optional native discovery and byte-for-byte exception regeneration:

```sh
HN_PAIR_RUN_DIR=/tmp/hn-paired-golomb python3 -B discover.py
```

Raw coordinates, modular streams, native pair profiles, logs and binaries
stay under the work path. Only the compact 38,430-byte exception certificate,
source and expected hashes are committed.

## Stopping boundary and bounded successor probe

The prescribed two-copy colour gate is completely neutral. A bounded
follow-up was motivated by two observations: many pairs overlap in six new
points, so three or four overlapping copies might still fit the 18-point
budget; and a common-colouring compression attempt failed with the seed word
fixed in four of the 39 full class supports. Neither observation is a
non-four-colourability claim about an unprecoloured graph.

`probe_overlap.py` optionally repeats the conditional copy-core experiment
using `requirements-optional.txt` (PySAT/CaDiCaL195). Four returned cores used
52, 45, 45 and 89 new points, all exceeding the budget. `OVERLAP_PROBE.json`
records this as **solver observation only**, with no refutation certificate,
no minimum-core-size claim, and no exclusion of other overlapping triples or
larger copy collections. No resulting physical record-sized obstruction was
found, and that bounded probe stopped. No larger geometry was generated.

This result retires the tested paired-Golomb family. It does not close
more-than-two overlapping copies, fewer old contacts, inside-K multipliers,
other motifs, other seeds, or arbitrary subsets of the full inventory.
A next pass should reassess the construction architecture rather than repeat
these pairs or add solver time to their neutral gate. One distinct unstarted
candidate is the fully injective, independently phased 343-point three-Moser
sum, at simultaneous independent contact equations; its collision locus and
correlated-phase subfamily have separate exclusions and must not be repeated.
Fresh graph and team assessment is required before selecting that candidate.

Parts's [509-vertex/2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the primary-source comparison, also stated in
[Haugland's 2026 manuscript](https://arxiv.org/html/2608.04542v4), refreshed
on 2026-09-14. No record improvement is claimed. Repository refresh consumed
the latest H574/q7 and sealed-pool review boundaries, the new R2 six-point/exchange closure and tested alternative rotation,
and the small equal-pair source closure. R2 now proposes three small A159
images; that proposal is distinct from this paired-Golomb lane. These other
lanes remain distinct. Discovery Net was stale at index 4363; pending
broadcasts were not treated as committed or resubmitted.
