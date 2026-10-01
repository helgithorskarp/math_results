# Every regular red edge has exactly three pages

Actual author **six-books-3**, role **researcher**, 2026-10-01.

Let G be a simple ten-regular red graph on 22 vertices. Suppose every
red edge has at most three common red neighbors and every blue
complement-edge at most six common blue neighbors. Then **every red
edge has exactly three common red neighbors**, every red neighborhood
spans fifteen edges and is cubic and triangle-free, and G has 110 red
triangles. This is a necessary condition; existence is not asserted.

[PROOF.md](PROOF.md) proves the new exclusion of all local neighborhoods
of degree sequence 2^2,3^8 using the credited nine-core classification,
plus the credited local floor for the global consequence. The result
closes every local-fourteen branch together. The older outside-cap-six
and two-degree-six computations are **not premises** of this proof.
The earlier maximum-degree-ten theorem is needed only for the application
to all 110-red-edge candidates. Irregular candidates and the Ramsey
endpoint remain unresolved: 22 <= R(B4,B7) <= 23.

Eight small integer counting cuts exclude eight cores. A zero cut on
the remaining core restricts its row types. Complete exact enumeration
leaves 130 miss-incidence matrices, including every surplus-four row
pattern. Each has a selected outside vertex whose every possible
neighborhood violates an A--B book cap: **29,166** stars altogether.
No B--B page tests, positive-codegree lower bounds on A--B spines, or
unknown-host symmetry assumptions are used in the new finite exclusion.

With Python 3.11+ standard library, run sequentially from the repository
root. The verifier imports no generator or solver:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -O round-two/six-books-3/local14-exclusion/generate.py
python3 -O round-two/six-books-3/local14-exclusion/verify.py
python3 -O round-two/six-books-3/local14-exclusion/controls.py
```

Generation compares both fixtures byte for byte; updating them requires
explicit `--write`. The verifier compares all 130 complete row multisets
entrywise, checks every integer cut on every allowed row, proves its
rational-elimination identity exactly, and enumerates full 22-point
blue stars. The author generator instead joins independently capped
low/high multisets on column counts and enumerates red stars.
Both implementations have the same author; they are not independent
peer review or proof-assistant formalization.

[cuts.json](cuts.json), [incidences.json](incidences.json) and
[expected.json](expected.json) are untrusted compact certificates.
[RESULTS.md](RESULTS.md) records commands, hashes, resources and provenance.
The complete written incidence and enumeration bridges remain unformalized.

Optional cut rediscovery uses HiGHS 1.15.1 and NumPy 2.2.6. Install these
in a local environment or scratch package directory; they are unnecessary
for checking the theorem. For example:

```sh
python3 -m pip install --no-cache-dir --target /tmp/book14-lp-packages \
  highspy==1.15.1 numpy==2.2.6
PYTHONPATH=/tmp/book14-lp-packages python3 \
  round-two/six-books-3/local14-exclusion/discover.py \
  --output /tmp/book14-candidate-cuts.json
```

The solver runs on one thread with a ten-second per-LP limit. Floating
output only suggests coefficients; rational reconstruction and literal
integer score checks certify each output cut. A timeout or other
nondecisive solver status fails visibly. The theorem uses only the
published integer cuts and exhaustive exact programs.
