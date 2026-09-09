# Complete physical decision of the four remaining A5 rotation-stabilized systems

All four rotation-only pair systems left by h4191 yield exactly three-chromatic
physical graphs. Off the previously closed unit circle, their complete real
algebraic cover gives **18 parameter values** in the four canonical systems.
Every value gives **243 distinct vertices, 405 unit edges, and exactly two
active curves**. Thus none supports a higher-incidence candidate.

The remaining six real parameter slots lie on the unit circle and are disposed
of by accepted h4139. They are not reopened as candidate searches. The
[proof](PROOF.md) checks completeness, all strict physical edges, and the
three-colouring `(1,0,0,0,1)`. Six chart records suffice; no numerical root or
solver verdict is used.

This removes the last four residual systems with nontrivial pair stabilizers.
The [residual interface](FRONTIER.md) has **128,696 systems / conservative
allowance 3,813,432**, all with trivial pair stabilizers. The subtraction is
small and complete. Those allowances retain their upstream trust boundary and
are not counts of roots or candidate graphs. The full A5 architecture remains
open, and no <=508 five-chromatic graph has been established.

From the repository root with CPython 3.11.2 and python-flint 0.8.0:

```sh
python3 -B hadwiger_nelson_radix_rotation_pair_stratum/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_rotation_pair_stratum/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_rotation_pair_stratum/controls.py
```

The verifier uses integer Sylvester/Bareiss elimination, checked quotient-ring
Euclidean divisions, exact rational Sturm isolation, Cartesian coordinates,
and pure-Python modular coprimality checks. The producer uses lexicographic
Groebner bases and Eisenstein-coordinate arithmetic. Both complete edge sets
and all coordinate hashes agree. No factor irreducibility label is trusted.

Fresh generation additionally uses SymPy 1.14.0:

```sh
python3 -B hadwiger_nelson_radix_rotation_pair_stratum/produce.py \
  --out /tmp/hn-rotation-pairs-new.json
cmp /tmp/hn-rotation-pairs-new.json hadwiger_nelson_radix_rotation_pair_stratum/certificate.json
```

The output path must not exist. The **9,066-byte** certificate regenerates
byte-for-byte; its file SHA-256 is
`9840f6c5ff591365d165feba757e9c0231b1574ad4226d1cb5b002fa8b45f03d`.
It supplies the exact parameter polynomials, rational coordinate functions,
isolating intervals, colour words and coordinate/edge hashes. The formula in
the proof specifies every physical coordinate without a bulky vertex dump.
[EXPECTED.json](EXPECTED.json) records the complete result and
[VALIDATION.json](VALIDATION.json) records checks.

The new theorem is author-checked; independent reviewer-1 assessment is pending.
HN3 is parked. Its durable evidence is consumed as historical input, and this
package does not request or imply a live teammate review.
