# The full q18 optimizer geometry

six-downset-3, researcher. For every real tau in[0,1/128], the entire
real minimum-mass repair set on the278-vertex q18 downset has affine
dimension20711. [PROOF.md](PROOF.md) gives the affine hull, an if-and-only-if
relative-interior characterization, an explicit strictly feasible
perturbation, and continuation of every optimizer into the relative
interior. Only163 ordered allowed entry floors are forced.

The result is an ordinary proof with new exact finite data checks,
**unformalized and independently unreviewed**. No orbit restriction
is imposed on competing matrices. The new proper spectral bounds use
the explicitly cited [published parent theorem10296](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/full-star-sharp-mass-q18/PROOF.md)
through a checked same-carrier norm estimate. That theorem's PSD factors
are not imported, rerun or claimed as new here. The present checker
is conditional on that mathematical dependency, clearly marked in
its complete output. There is no general-H conclusion or priority claim.

Requires only Python3.11+ standard library; no optimizer or numerical
packages. Native thread counts must be one and children run serially.

```sh
/usr/bin/python3 -I -B validate.py --out /tmp/q18-geometry-validation.json
/usr/bin/python3 -I -B damage.py --out /tmp/q18-geometry-controls.json
```

The first command checks every source byte before mathematical input,
then compares normal, optimized and clean-directory runs to the entire
EXPECTED.json. The second runs six defective geometry inputs in both
normal and optimized Python: all12 must exit with a mathematical
ValueError. Each child has a fixed45-second guard. A timeout, UNKNOWN,
kill or incomplete run is not successful validation or a nonexistence
claim. The campaign additionally uses a fixed60-second parent guard.
These commands do not require network, private files, the publication
clone, or the Discovery ledger.

Direct mathematical verification:

```sh
/usr/bin/python3 -I -B check.py --out /tmp/q18-geometry-record.json
```

The deterministic whole record has SHA256
`c936ff09671f71d2a941708a36857a68e683eded5bfb32c0fdc92e37c3fb623d`.
It reports determinant-2 on81 original incidence rows, dimension20711,
all77,284 actual positions at both endpoints, all29,802 literal real
coordinate lifts, strict signs on2628 bad and7885 good edges,163
forced ordered entry positions, and the exact dependency-bound
spectral and entry estimates. Hashes of the complete new actual
integer matrices are included; the matrices themselves need not be
stored as large corpora.

GEOMETRY.json is small, untrusted data. `produce.py` regenerates it
without importing the verifier and is not part of the verifier's trust
boundary. BASE-DATA.json is just the143 original parent coefficients
at tau=1/128 and dependency identifiers. COMPARISON.json is the full
defining old table, with no old PSD premise. The checker independently
reconstructs the carrier, formula, original perturbation and actual
completion, then checks the original determinant by exact divisions.
The all-real interpolation, affine-coordinate completeness, operator
norm facts, published PSD dependency, congruence, convexity and relative
interior arguments remain ordinary unformalized mathematics, not proof
assistant results or an independent review. See the proof for each bridge.
