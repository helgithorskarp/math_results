# Validation and resource bounds

The proof uses Python3.11+ and its standard library only. Original run:
CPython3.11; no SAT, MIP, floating-point arithmetic or randomized inference.
Exact integer bitsets and finite AP positions carry all mathematical checks.

Each child is serial, limited to30 wall seconds and200,000 declared cases.
Each coverage slice has at most32 cut rows; baseline slices have at most
190,000 actual APs. Direct residual checking has2,899 APs/20,293 term checks
and87,785 conservative combined cases. Positive generation uses at most
8,000 AP tests and32 finished points per child, d<=64, and512 child windows.
The surrounding process remains within the authorized1CPU/2GiB scope.
Environment variables constrain OpenMP/BLAS libraries to one thread.
Timeout, failed child, allocation failure or incomplete prefix ends visibly
without a family-exclusion conclusion. No larger limits are retried.

The original selected-AP pilot checked all128 binary patterns/4,608 gap cells
per mode, plus24 slices totaling190,464 actual cut/pattern pairs per mode.
A duplicate-rectangle corruption fixture initially exceeded its own count
bound before reaching the intended duplication check. The fixture was fixed
by replacement rather than appending; the failed fixture and unchanged old
sources were preserved privately, and the full pilot reran. This was not a
certificate acceptance defect. The theorem uses the independently checked
actual APs and exact full-domain coverage, not pilot extrapolation.

The reproduction starts from the supplied compact source and proof data.
It audits every base bit against the stated QR formula and checks all
1,141,450 original integer APs in7 slices. A separate small exhaustive test
compares the rank enumeration with an a-major definition for every binary
word of lengths7 through12. The frozen baseline checker uses assertions:
only this checker runs in normal mode with PYTHONOPTIMIZE=0. The three
proof checkers use explicit exceptions and run both normally and under -O.

For every row, sorted unions and bitsets must agree, and their exact exported
complement must equal all supplied mandatory residual cuts. Positive point
checking runs in both modes;12 cover and14 point corruptions per mode must
hit the specified mathematical defect, giving52 rejection checks. A fresh
small-step positive search must regenerate exactly all2,899 supplied APs.
No private search state, prior candidate word or solver proof is loaded.
Completed-stage source/input/output hashes support resumability. Individual
case, time and peak RSS records and the complete journal stay in the local
output directory; they are intentionally not published as a raw corpus.

This is an implementation-checked finite lemma, with same-author independent
algorithms and no asserted external reviewer acceptance or proof-assistant
formalization. The trust boundary is the ordinary Python runtime, these
transparent source files and the finite literal inputs. The full mathematical
claim remains exactly the fixed one-interval family.
