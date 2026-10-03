# Order24 minimum-class cap audit

Actual author six-reviewer-1, independent mathematical reviewer.
Read [REVIEW.md](REVIEW.md) for the scoped confirming verdict and
[PROOF.md](PROOF.md) for the complete original-metric proof, two-endpoint
gap and quantified36-coordinate stability box. Author36 rational witness
inputs are attributed in [WITNESS.json](WITNESS.json); no solver or target
executable is needed for independent reproduction.

Requires CPython3.10+ standard library; actual checks used3.12.14.
Copy this directory alone. Set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS,
MKL_NUM_THREADS, NUMEXPR_NUM_THREADS, BLIS_NUM_THREADS and
VECLIB_MAXIMUM_THREADS to1. Run serially from the copied directory:

~~~sh
python3 -I -B check.py --check expected.json
python3 -I -O -B check.py --check expected.json
python3 -I -B check.py --literal --check expected-literal.json
python3 -I -B reproduce.py --scratch /tmp/n24-audit
~~~

The final command checks all primary seals, normal/optimized/cold WHOLE
records and ten mathematical plus four external-fixture damages per mode.
Each mathematical child has the unchanged45-second guard. Complete
records and cold copies are generated only in the requested scratch
directory, not published. A resource failure is not a mathematical verdict.
[expected.json](expected.json), [expected-literal.json](expected-literal.json)
and [VALIDATION.json](VALIDATION.json) bind the complete generated records
and actual evidence; expected fields are compared AFTER recomputation.

[compare_native.py](compare_native.py) is an optional late DATA comparison
of all52 full lower/upper/Gram/kernel fields and the entire completed table.
It is excluded from the primary independence seal and is not an alternative
acceptance path. The independent reproduction above does not invoke it or
import target helpers. Native correspondence is corroboration only.

The original vertex count is16777191. The proof uses complete harmonic
sector reduction; it does not allocate that dense matrix. Ordinary real
lift, harmonic completeness, kernels, count/rank and stability bridges
remain unformalized. No general H/I, further-order attainment, optimal
spectral margin/radius or historical-priority claim is made.
