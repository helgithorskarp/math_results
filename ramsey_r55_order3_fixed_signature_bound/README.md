# A sharp fixed-signature bound for ten moving triangles

A hypothetical Ramsey `(5,5;43)` graph with an order-three automorphism
of type `1^13 3^10` must have **at least three fixed vertices blue to
the entire twelve-vertex minority core**, after naming the minority
internal color red. Equality forces all ten nonempty fixed signatures
to occur once: four singletons and six pairs of minority triangles.

The standalone lemma is stronger in scope: for any Ramsey `(5,5)` graph
containing the explicit core H, at most ten external vertices that are
uniform to each of H's four triangles can have a nonempty red signature.
The hand proof adds two incidence inequalities. Read [PROOF.md](PROOF.md).

The [25-vertex fixture](sharp25.edges) attains this bound and contains
no monochromatic K5. It establishes sharpness only for the core and
fixed vertices. Six majority triangles have not been added. The ten-cycle
type and the four full-extension cases remain open; no target graph or
Ramsey-bound improvement is claimed.

The additional exact census leaves **1,868 necessary multiplicity vectors**
under all blue-clique constraints forced by the core and signatures.
They are not asserted graph realizations or surviving full solver leaves.
The separate hard-branch degree-profile counts are unchanged.

## Reproduction

From this directory, using Python 3.11.2 and its standard library:

```bash
python3 verify.py --report /tmp/r55_fixed_signature_report.json
cmp report.json /tmp/r55_fixed_signature_report.json
python3 -O verify.py --report /tmp/r55_fixed_signature_optimized.json
cmp report.json /tmp/r55_fixed_signature_optimized.json
sha256sum -c SHA256SUMS
```

The verifier pins and checks the sibling minority-core edge list against
its explicit definition. It checks every one of the 59,049 multiplicity
assignments both by signature-family capacities and by constructing and
searching the actual forced-blue graph. It compares entry-level decisions,
not merely totals. It also directly checks all 53,130 five-sets of the
literal sharp fixture and the complete order-three action.

Negative controls detect three repeated singleton signatures, four
intersecting signature copies on three indices, and a red edge added
inside a minority triangle's common red neighborhood. The clique routine
is checked in 5,120 small definition-level cases. Exceptions keep all
checks active in optimized Python.

Expected stdout is in [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt); the
full compact output is [report.json](report.json). The reference run
took about five seconds and 16,488 KiB peak resident memory. No solver,
network connection, generated CNF, omitted trace or external dataset is
required. The literal witness was discovered with Kissat 4.0.4, but its
correctness depends only on the published edge list and direct check.

The unique-core dependency has an
[accepted independent conditional review](../ramsey_r55_order3_ten_cycle_phase_sweep_review1).
The older internal-color split remains an explicit imported dependency.
This new result has been internally checked, not independently peer
reviewed or formalized. The unformalized hand proof, exact Python
execution, source correctness and hardware remain the local trust boundary.

## Completed milestone

The signature bound, equality description, complete forced-blue census
and sharp 25-vertex fixture are finished. The next useful step is actual
compatibility of these signatures with six majority triangles, especially
the equality pattern. No further extension phase is included here.
