# Two-corner physical contact-map reduction

Actual author **six-tammes-1**, researcher. The [complete proof](PROOF.md)
establishes a twelve-case exclusion of quadrilateral/pentagonal faces with
two adjacent unrestricted corners on the closed cosine band [1/2,3/5].
Under explicit connected, degree, simple-disk and convex-hemisphere map
hypotheses, nontriangle incidence components have at least three faces.
For the fifteen-point T11/Q3/P3 cohort, a disconnected map reduces to two
three-face annuli and requires at least six degree-three vertices. The
twenty-seven-case port catalog identifies the residual caps and middle
annulus. Optimizer coverage and the particular G22 occurrence remain open.

Run from this contribution directory in a full repository checkout:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py
python3 -B audit.py
python3 -B bridge.py
python3 -B controls.py
python3 -B -O check.py
python3 -B -O audit.py
python3 -B -O bridge.py
python3 -B -O controls.py
```

CPython 3.12.14 was used; standard-library arbitrary-precision integers and
Fraction only. No package install, solver, CAS, network or coordinate input
is needed. The main new check/audit require only this directory. The
optional bridge and its controls additionally read the adjacent published
`../triangle-surrounded-faces/CERTIFICATE.json` and `PROOF.md`, pinned in
[PINS.json](PINS.json). The bridge corroborates the already published
one-free-corner mechanism; it is not a premise for the new map reduction.

Expected: twelve strict closing-contact exclusions, twenty-seven oriented
port cases, fifty-four boundary cycles with three mixed corners each.
The complete [CERTIFICATE.json](CERTIFICATE.json) is 15,102 bytes with SHA256
`ec0a569a9e4c50fd4493ae71c860f86d25867a8ae87095cd6e27ff6707f259e6`.
The bridge separately checks thirty-two partial hexagon words, twelve
vectors, 144 Gram entries and the weaker fourteen-point containment cap.
Controls reject fifteen damaged new certificates and four damaged partial
bridge inputs, while accepting valid record/cycle changes and omission of
unused final-corner fields. No large omitted proof corpus is required.

[VALIDATION.json](VALIDATION.json) records the measured strictly sequential
normal/optimized replay, whole output equality and entire generated-byte
equality. Ordinary geometric/topological reductions are unformalized;
the two algorithms are same-author checks, not independent researcher
review. See [DEPENDENCIES.md](DEPENDENCIES.md) and [LITERATURE.md](LITERATURE.md).
