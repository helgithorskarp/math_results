# A421-point heptagon difference graph and42 potential colourings

**Completed result.** An exact heptagon construction gives a421-vertex,
1848-edge unit-distance graph D with a proper four-colouring. A21-potential
colouring construction reduces to84 small XOR constraints and has exactly
42 normalized solutions, in six cyclic symmetry classes. Both geometry
and classification are checked independently.

All these colourings separate every pair at distance sqrt(3). Whether
ordinary four-colourings must do so is **unresolved**. This is not a
certified nonmonochromatic-pair gadget or a record graph.

The seed has no pair at distance3 or sqrt(7), so it cannot directly replace
the corresponding Parts terminal gadgets. Every subgraph of this seed
is four-colourable. This bounded milestone explores geometry distinct from
the Parts and dense506 families; no larger heptagon sum or subsequent
construction phase was started.

## Mathematical content

[PROOF.md](PROOF.md) defines H through21 exact cyclotomic coordinates,
sets D=H-H, proves the general difference-potential criterion, and states
the finite enumeration and its trust boundary. The only imported object
is the21-point motif of
[Haugland, Section2](https://arxiv.org/html/2608.04542v4).
Its coordinates are rewritten in Q(exp(pi*i/21)); no source code,
floating-point path census, or previous SAT claim is imported.

| Exact quantity | Result |
|---|---:|
| Motif vertices / unit edges |21 /42|
| Distinct directed unit differences |84|
| Difference points / unit edges |421 /1848|
| Complete unordered D-pair scan |88410|
| Distance3 pairs / sqrt(7) pairs |0 /0|
| sqrt(3) pairs / cyclic orbits |126 /9 of size14|
| Two-variable / four-variable XOR constraints |42 /42|
| Normalized potential assignments |42|
| Potential rotation classes |6 of size7|
| Primary / independent search nodes |2035 /9426|

The potentials define C(h_a-h_b)=p_a XOR p_b and C(0)=0. Unique nonzero
ordered differences make this well-defined. A unit edge imposes nonzero
XOR on the symmetric difference of its endpoint supports. The normalized
rows fix p_0=0,p_7=1,p_14=2. All42 rows are in
[potentials.json](potentials.json); colour labels are0,1,2,3 as the group
F_2^2. Every lifted edge and every designated sqrt(3) pair is checked.

The independent audit reconstructs geometry in the tensor basis
zeta7^a*omega6^b, rather than the producer's degree12 cyclotomic polynomial
basis. It uses an explicit denominator7 inverse identity, with no imported
producer module, and scans every pair. It then uses fixed variable order
to enumerate the84 constraints, independently of the producer's
minimum-domain search, and compares all42 assignments entrywise.

This class does not contain all proper colourings by definition. A
seven-point control supplies a proper non-potential colouring of a tiny
difference graph; it illustrates the logical limitation of the method,
without making that assertion about D.

## Reproduction

Use Python3.11.2 (tested), standard library only, with assertions enabled.
From this directory in a full checkout choose a fresh external directory:

```bash
python3 -B build.py --work /scratch/fresh-heptagon-difference
python3 -B classify.py --work /scratch/fresh-heptagon-difference
python3 -B audit.py --work /scratch/fresh-heptagon-difference
python3 -B controls.py --work /scratch/fresh-heptagon-difference
python3 -B verify.py --work /scratch/fresh-heptagon-difference
sha256sum -c SHA256SUMS
```

Expected status:
`EXACT421-POINT GRAPH AND COMPLETE42-LIFT CLASSIFICATION VERIFIED`.
The verifier separately reports that ordinary sqrt(3)-pair forcing is
unresolved. Reproduction requires no native SAT solver or proof file.

The expected files record all stable outputs; elapsed times are excluded
from comparison. [validation.json](validation.json) pins the generated
graph and potential-stream hashes and reports measured timings. The
public graph stream and primary solution stream match the original
prototype byte for byte. The complete public audit was replayed after
adding the cyclic-class check. The graph table remains local; it is
regenerated deterministically. The committed42-row certificate is small.

The public build took6.459 seconds, classification about0.10 seconds,
and the final independent audit22.471 seconds. Python peak memory was
not measured. Direct Python loops were sufficient; no native rewrite or
parallel enumeration was warranted. The primary classifier has an
explicit2,000,000-node bound and reports incomplete status if reached;
the completed2035-node result is what is certified here.

Controls check all42 unit roots and their conjugates, proper-divisor order
conditions, exact inverses and zero-inverse rejection, the tiny non-lift
example, and three deliberately invalid421-point colour rows. The new
checks were performed by the author; external review is pending.

## Unrestricted pilot: inconclusive

[pilot.json](pilot.json) records the two bounded native tests for pair
[0,332] in the sorted D table; the origin has label210. An exactly-one
encoding with the terminals fixed to colour0 returned UNKNOWN after
200000 conflicts in CaDiCaL195, accessed through python-sat1.9.dev15.
A second at-least-one encoding pinned an adjacent unit triangle and
returned UNKNOWN after60 seconds in Kissat4.0.4. Neither establishes
infeasibility. The restricted native experiment is superseded by the
complete direct potential enumeration and is not used as a proof of an
ordinary graph relation.

[query.py](query.py) regenerates both ordinary formulas. For example:

```bash
python3 -B query.py --work /scratch/fresh-heptagon-difference --encoding alo --output /scratch/heptagon-pair.cnf
/path/to/kissat --time=60 /scratch/heptagon-pair.cnf /scratch/heptagon-pair.drat
```

The original complete direct input has1684 variables and7817 clauses,
SHA256 `cd4a235652de1ca3d74bc0c8b06d33799a6a0196e360f1531c12f00322dfbcdd`.
Its public regeneration was byte-identical. The onehot option converts
the first query's two positive assumptions into equivalent unit clauses.
These are optional unresolved-query inputs, not part of the proof replay.

The original time-limited run produced a131,841,287-byte incomplete DRAT
trace. It is local, is **not a certificate**, and was not submitted to a
proof checker as one. No graph claim depends on it. No job is still running.
Any later UNSAT claim needs a complete independently checked proof;
matching the partial trace is neither required nor evidence.

## Campaign context and handoff

The primary record calibration remains the509-vertex construction in
[Parts' paper](https://arxiv.org/abs/2010.12665), also identified as the
record by the August2026 Haugland source above, checked live2026-09-05.
No priority claim is made for difference graphs or XOR colour encodings.

The preceding HN-3 pass closed all arbitrary additions through three
points to two fixed dense506 hosts, in the
[three-point extension package](../hadwiger_nelson_dense506_three_point_extension/README.md).
That theorem and its non-field predecessor now have an
[accepted independent review](../hadwiger_nelson_dense506_three_point_extension_review1/README.md).
HN-2's new [rigid-block pilot](../hadwiger_nelson_parts509_rigid_block_core_pilot/README.md)
certifies an869-point relation-restricted block, above its373-point budget.
Neither result is a mathematical premise here; these are distinct lanes.

**Next direction:** test whether a proper colouring of this specific D
can escape the potential construction, starting with a bounded Kempe
perturbation of the42 explicit colourings before extending native runtime.
Such a colouring would falsify a proposed necessity route; its absence
from a bounded perturbation search would not prove necessity. This next
phase has not started. Alternatively reassess the composition if a
compact terminal mechanism remains unsupported. Do not restart Parts
support closures or the closed dense506 repair radii.
