# A six-class conditional minimum-eight exclusion

Actual author: **six-covering-2**, role **researcher**.

No distinct covering with minimum exactly eight and moduli dividing 10080
can retain all six classes
`[(8,0),(9,0),(10,1),(14,1),(12,3),(16,1)]`.
Consequently a distinct minimum-eight covering retaining them has actual
LCM at least 15120. The unrestricted period-10080 and period-15120
questions remain open. See [proof.md](proof.md) for the finite reduction.

The standalone standard-library checker verifies an 83-record complete
tree, including all 213 actual branch phases and strict integer capacity
cuts. It requires only the 97336-byte [certificate](certificate.json).

From the repository root, CPython >=3.10:

```sh
python3 -B number_theory/distinct_covering_10080_anchor16_phase1/check.py
python3 -B -O number_theory/distinct_covering_10080_anchor16_phase1/check.py
python3 -B number_theory/distinct_covering_10080_anchor16_phase1/controls.py
python3 -B -O number_theory/distinct_covering_10080_anchor16_phase1/controls.py
```

Compare the final JSON with [expected.json](expected.json), omitting each
case's elapsed `seconds` field. The controls reject nine invalid fixtures
under both normal and optimized Python. Author checks are not independent
review. No private forest, ledger or numerical solver is required.
