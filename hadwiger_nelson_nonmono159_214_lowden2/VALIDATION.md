# Validation of the mixed denominator-two exclusion

The checked environment was CPython 3.11.2, GCC 12.2.0, and Linux x86-64.
The inherited witness-generation dependency is `python-sat==1.8.dev24`
(CaDiCaL 1.9.5); no SAT solver is used for the checked positive assignments.

## Enumeration

The independent trace-based Python enumerator returns 24 possible orthogonal
maps, 12 supporting at least two overlaps, and 39,004 distinct placements.
Its entire histogram matches `CENSUS.txt`; the sorted placement stream has
SHA-256 `6f61f7c8ff6494ca2ba2b99cadfb6f120d7192d08026a33749658c3d3093c334`.

Every canonical placement row, not just the total, was compared with the
existing directed-segment enumerator's output for these inputs and the
options `--emit-at-least 2 --max-denominator 2`. All 39,004 rows agreed;
there were no duplicates. The old enumerator is
`../hadwiger_nelson_nonmono159_lowden2/enumerate_overlaps.cpp`. This comparison
is supplementary: the new trace proof and Python enumeration establish
completeness without trusting the old enumerator.

## Full coloring check

A full single-core C++ replay checked all 39,004 archived coloring witnesses
and completed successfully in 395.835 seconds including compilation and
checkpoint decompression. The `verify.sh` entry point was also exercised with
an existing plain-text coloring file, so that it independently rebuilt the
entire placement list before checking the witnesses; that end-to-end check
completed successfully in 398.304 seconds. The expected mathematical
output is:

```
graphs=39004
unsat=0
order_range=250-371
edge_range=1207-1787
exact_geometry=true
direct_witness_verification=true
```

The full SAT generation branch was not rerun in this pass. The inherited
solver-produced assignments were verified directly, and the original graph
and coloring streams were hashed; `GENERATED.json` records those hashes.
A hash match is provenance, not a proof.

## Separate geometry sample and rejection check

Run, without Python's assertion-disabling `-O` flag:

```bash
python3 audit_samples.py /absolute/path/to/transforms.txt \
  /absolute/path/to/colorings.txt > /tmp/mixed-lowden-sample.json
cmp expected_sample.json /tmp/mixed-lowden-sample.json
```

Here `transforms.txt` is the canonical output of `enumerate_lowden.py`.
The Python implementation recovers the component edge counts 646 and 977,
then checks full geometry and color validity for the first and last placement
in each supported orientation and one maximum-overlap placement. These 25
samples contain 40,971 strict unit edges. The sample results match
`expected_sample.json`. This is separate geometry evidence for the samples,
not a second full replay of all union edges.

A build with `-O1 -g -Wall -Wextra -fsanitize=undefined,address
-fno-omit-frame-pointer` passed a ten-placement smoke sample without sanitizer
diagnostics. Replacing the first sample coloring by an all-zero assignment
was rejected with a monochromatic-unit-edge error.

GCC reports one inherited warning: the affine enumerator's original `main`
is textually renamed into an unused function that has no final `return 0`.
That function is never called in the verifier. The executed verification path
has no sanitizer finding in the stated sample. All transitive verification
sources and witness-generation inputs are pinned by `SHA256SUMS`.

## Incremental scope

Of the 39,004 placements, 5,308 already lie in the earlier overlap-at-least-20
mixed-gadget closure. The remaining **33,696** are below that threshold.
Together the two results cover 46,880 of the previously enumerated 2,557,868
mixed placements with at least two overlaps, leaving 2,510,988 outside their
combined scope. This arithmetic concerns this fixed two-gadget family only.
