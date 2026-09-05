# A full-extension obstruction reduces 197 minority cores to 79

**118 four-versus-seven core classes are excluded from the full
43-vertex Ramsey (5,5) problem.** Their twelve minority vertices
contain a blue K4. A hand proof shows that such a K4 is incompatible
with the seven blue moving triangles and the full color-degree bound.
The 79 remaining classes contain no blue K4 and remain open.

The [proof](PROOF.md) combines the forced fixed signatures with a
simple incidence contradiction:

```text
Each of seven blue triangles is blue to at most one pair-signature
fixed vertex: at most 7 incidences.

Each of six pair-signature fixed vertices needs at least two blue
triangles to keep its red degree at most 24: at least 12 incidences.
```

This goes beyond the preceding local-feasibility result: all 197
cores still have valid 22-vertex extensions with ten fixed vertices.
The obstruction uses the complete seven-triangle moving remainder.
No cross-block phase search, full CNF, SAT solver, selected degree
profile, or fixed-row normalization is required.

The new theorem and census await independent review. **No target,
Ramsey lower-bound improvement, closure of the remaining 79 cases,
or exclusion of all eleven-cycle automorphisms is claimed.** The
two three-versus-eight cores are unchanged.

## Compact certificates and checks

[classification.json](classification.json) lists every excluded
core with a blue K4 witness and every retained core. The 118 excluded
classes cover 63847 locally valid labeled cores; the remaining 79
cover 51696. Orbit multiplicities and completeness of the marked
action cover come from the pinned
[197-class catalog](../ramsey_r55_order3_eleven_four_core).

[attachments.json](attachments.json) lists all 33 possible blue
neighborhoods of one blue triangle within the forced ten-fixed-vertex
graph, for each of its four edge patterns. This is a thirteen-vertex
necessary subsystem, not a claimed extension to the red core.
The producer lists a structural family; the independent checker
constructs all 4096 literal graphs and checks for monochromatic K5s.
It also checks every local red degree and every possible blue-triangle
count against the degree upper bound.

[packing.opb](packing.opb) has 42 variables and 13 inequalities.
[packing_certificate.json](packing_certificate.json) gives a
nonnegative sum of these rows resulting in `0 >= 5`. The checker
reconstructs all variable meanings and adds the rows exactly. This
is an infeasible necessary projection, even over the reals; no solver
or integrality assumption is used for the arithmetic refutation.

For the catalog partition, the producer examines core transversals;
the checker instead enumerates all 495 literal four-sets per core.
Every witness, retained entry, multiplicity and certificate byte is
checked, with identical normal and optimized Python results.
Eight malformed-certificate controls are rejected. Four literal
hypothesis controls and two feasible weakened incidence systems
test the steps of the structural argument.

## Reproduction

CPython 3.11.2, standard library only. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B generate.py --work /scratch/new-r55-blue-k4/production
cmp classification.json /scratch/new-r55-blue-k4/production/classification.json
cmp attachments.json /scratch/new-r55-blue-k4/production/attachments.json
cmp packing.opb /scratch/new-r55-blue-k4/production/packing.opb
cmp packing_certificate.json /scratch/new-r55-blue-k4/production/packing_certificate.json
python3 -B verify.py --source /scratch/new-r55-blue-k4/production --report /scratch/new-r55-blue-k4/verification.json
cmp report.json /scratch/new-r55-blue-k4/verification.json
python3 -B controls.py --source /scratch/new-r55-blue-k4/production --report /scratch/new-r55-blue-k4/controls.json
cmp controls_report.json /scratch/new-r55-blue-k4/controls.json
python3 -B -O generate.py --work /scratch/new-r55-blue-k4/production-O
python3 -B -O verify.py --source /scratch/new-r55-blue-k4/production-O --report /scratch/new-r55-blue-k4/verification-O.json
cmp report.json /scratch/new-r55-blue-k4/verification-O.json
python3 -B -O controls.py --source /scratch/new-r55-blue-k4/production-O --report /scratch/new-r55-blue-k4/controls-O.json
cmp controls_report.json /scratch/new-r55-blue-k4/controls-O.json
```

The scripts default to the pinned sibling `cover.json`; pass `--cover`
to specify a separate copy with the same hash. Work stays outside Git.
The public certificates contain the full small projection, multipliers,
attachment set and core partition. There is no omitted solver proof
or large dataset required for this milestone.

## Dependencies and scope

The hand proof restates all necessary fixed-signature arguments from
the preceding [fixed-vertex theorem](../ramsey_r55_order3_eleven_four_fixed).
It imports no computational enumeration for those steps. Its only
external Ramsey-value input is
[McKay and Radziszowski's R(4,5)=25 theorem](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf),
which gives the degree upper bound 24. That computation is not
reproduced here. The degree bound also appears in the accepted
[eleven-cycle parent](../ramsey_r55_order3_eleven_cycle_obstruction).

The 197-to-79 census additionally imports the catalog's completeness
and full-action normalization, which still await independent review.
The theorem itself needs no catalog or full-formula normalization.
Internal algorithmic independence is not an independent reviewer
verdict. Unformalized proof/code alignment, exact inherited source
bytes, Python/runtime/hardware, SHA256 and the external Ramsey theorem
remain trust boundaries. No formalization or priority claim is made.

This bounded milestone stops after the shared obstruction and its
complete catalog application. No search on the remaining 79 cores,
larger construction, or further proof phase has begun.
