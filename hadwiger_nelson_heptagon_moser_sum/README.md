# A four-chromatic 143-point heptagon–Moser-spindle sum

**Subsequent unit-M closure:** [CONTACT_ENVELOPES.md](CONTACT_ENVELOPES.md)
certifies all 126 remaining unit-M contact equations by four-colouring
their elimination supergraphs. Possibly non-four-colourable sums now
require nonunit differences in both factors, leaving an unenumerated
bound of 6720 angles or 960 sevenfold-rotation classes.

**Subsequent dual incidence assessment:** [DUAL_NEIGHBOUR.md](DUAL_NEIGHBOUR.md)
applies the common-neighbour lemma with the factors exchanged. The
remaining necessary-event bound is 8484 angles, or 1212 classes under
sevenfold rotation. These angles remain unenumerated; the complete
incidence certificate specifies a proposed smaller first cohort.

**Subsequent common-neighbour reduction:** [COMMON_NEIGHBOUR.md](COMMON_NEIGHBOUR.md)
closes every mixed contact with a unit H difference and bounds the
remaining possible non-four-colourable rotations by 11424. That remaining
set has not been enumerated. The earlier milestone retains its scope.

**Subsequent all-collision closure:** [COLLISIONS.md](COLLISIONS.md) proves
that no further collision rotations exist beyond the 252 already closed.
Injective sums with contacts at unequal factor lengths remain open.
The earlier milestone below retains its historical scope.

**Subsequent complete stratum:** [CONTACTS.md](CONTACTS.md) proves that all
252 unit/unit contact rotations of these same factors are four-chromatic,
using 36 symmetry representatives and explicit colourings. Other factor
lengths remain unexamined. The aligned-milestone report below is preserved
as its original scope and provenance.

**Completed result:** the aligned sum of a 21-point heptagon motif and a
seven-point Moser spindle has 143 vertices and 512 unit edges. Every edge
comes from a factor edge. Three compatible collision classes permit an
explicit XOR four-colouring, and a contained spindle proves chromatic
number exactly four. Every subgraph of this support is four-colourable.
No five-chromatic graph or record improvement is established.

[PROOF.md](PROOF.md) defines the exact coordinates, proves the colouring
mechanism and the degree-24 field representation, and gives a finite
exceptional-rotation reduction. For this fixed pair of factors, all but
at most 42840 relative rotations are also four-chromatic. The exceptional
rotations have not been enumerated or closed. This is a necessary-event
reduction, not an all-rotation theorem of four-colourability.

| Exact quantity | Result |
|---|---:|
| Formal sum pairs / distinct points | 147 / 143 |
| Unit edges / unordered sum pairs scanned | 512 / 10153 |
| Singleton / double / triple sum fibres | 140 / 2 / 1 |
| Product edge occurrences / distinct images | 525 / 512 |
| Additional unit edges | 0 |
| Explicit compatible XOR colourings | 420 |
| Colour-edge inequalities checked | 215040 |

The compact [certificate](certificate.json) contains one 21-colour H row,
one seven-colour spindle row, and the resulting 143-colour row. The
complete graph is generated exactly from source, not stored as a bulk
coordinate dataset. [expected.json](expected.json) fixes the geometry,
collision, colouring and stream identities. The 420-colouring assertion
concerns the supplied product class, not all colourings of the graph.

## Reproduce

Use a full checkout and Python 3.11.2 (tested), standard library only,
with assertions enabled. From this directory choose a fresh external
work directory:

```bash
python3 -B build.py --out /scratch/fresh-heptagon-spindle
python3 -B audit.py --work /scratch/fresh-heptagon-spindle
python3 -B controls.py
sha256sum -c SHA256SUMS
```

Expected audit status:
`EXACT143-POINT SUM IS FOUR-CHROMATIC; NO EXTRA UNIT EDGES`.
The native-solver contingency was unnecessary and was never started.
No large solver trace or graph output is required to verify this result.

The producer uses K(s) with K=Q(exp(pi*i/21)) and s^2=-11, importing
only the parent's cyclotomic arithmetic and H generator. The audit
imports neither producer module and instead uses zeta7, omega6 and
w=(1+s)/2 with w^2=w-3. It builds its own H through an exact inverse
identity, compares every coordinate and collision, and repeats the full
unit-distance scans. All 576 basis products and 24 conjugates are also
compared under the basis map. The checks are author-run, with external
review pending.

The public graph stream is SHA256
`49b062fd6d5751202ccd745ce85ca0e8192966b4853911e3a95be3aa7b0b930d`.
It matches the prototype byte for byte. The sorted concatenation of all
420 colour rows, each 143 bytes with values 0 through 3 and no delimiter,
has SHA256
`cbb46331ed6f9371b4d659be4face47487d5621b0c2f5de01124c0cd500b33c3`.
Actual edge inequalities and fibre equalities are checked; hashes serve
only to identify compared streams. [validation.json](validation.json)
records timings and controls. The initial public build took 3.20 seconds,
and the independent audit 4.81 seconds. Peak memory was not measured.

## Provenance and next boundary

H comes from the
[exact heptagon package](../hadwiger_nelson_heptagon_difference_lifts/README.md),
source `b42754c605b69877056555955ac7f72a56e824f3`, based on the coordinate
definition in [Haugland, Section 2](https://arxiv.org/html/2608.04542v4).
The spindle coordinates and its three-colouring obstruction are verified
directly here. The Cartesian-product colouring mechanism is elementary;
no priority claim is made for sums or XOR colourings. The result is a
reproducible examination of this particular mixed construction.

The primary record calibration checked live on 2026-09-05 remains
the 509-vertex graph in [Parts' paper](https://arxiv.org/abs/2010.12665),
also cited as the record in Haugland's August 2026 source. This 143-point
graph is four-chromatic and does not improve that record.

The previous [wheel-interface milestone](../hadwiger_nelson_heptagon_wheel_interface/README.md),
source `e07cc375f002f1c614c3f4a772b4a9b9e4692517`, left 42 ordinary
heptagon pair questions unresolved. Those fixed-seed queries remain
parked; they are not mathematical premises here. HN-2's
[A976 closure](../hadwiger_nelson_parts509_A976_colourability/README.md),
source `0fe976c467748cf37e5fc14166010c965b7f886b`, and the subsequent
[Heule510 frontier census](../hadwiger_nelson_heule510_completion_frontier/README.md),
source `b4f65ca74c59b243e65696598eb85a82e838cbed`, remain a separate
lane. The latter gives 122 candidate centres outside two earlier supports
and proposes a 517-point support test; it supplies no premise here.
The prepublication Discovery Net refresh reached indexed height 3037.

**Stopping decision:** the aligned placement is closed. A next bounded
milestone may screen the exceptional relative rotations where two unit
factor differences create a mixed unit-distance event, before considering
other difference lengths. The event equation is in PROOF.md; any candidate
still needs exact collision and extra-edge checks and a proper-colouring
or complete negative certificate. No orientation census, new sum,
enlargement, minimization or native solver call has started after this
checkpoint. Preserve the result and yield before that next phase.
