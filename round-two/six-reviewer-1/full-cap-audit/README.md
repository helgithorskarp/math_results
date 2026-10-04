# Independent full actual equality-cap audit

six-reviewer-1 / independent mathematical reviewer. Read REVIEW.md for the
verdict and PROOF.md for the complete relative proof and strengthening.
The full moving trace, original motion and actual lower-family premises are
credited in DEPENDENCIES.json. The first-power global conjecture remains open.

CPython3.12.14; standard library only. Run from this directory:

```bash
python3 -B check.py --output /tmp/full-cap-independent-record.json
python3 -B -O check.py --output /tmp/full-cap-independent-optimized.json
python3 -B reproduce.py /tmp/full-cap-independent-validation
```

The validation directory must be new. All six native thread environment
variables are set to1 by reproduce.py; children run serially with45-second
limits. The first two commands should also use native thread settings1 when
the local environment loads numerical libraries; this code imports none.

Expected:81 complete records,34 nonzero whole cost monomials,21906 complete
record bytes, SHA2561580b2f28526707a303a5ed5223f8a0dc37ff48d972825da92aafba2aef81f56.
Four whole local/cold normal/optimized records agree. Six equation-level
faults reject in both modes. VALIDATION.json records the observed run, not a
mathematical input. PRIMARY_SEAL.json seals the defining source after checks.

No producer program/data or parent checker was opened or executed. The fresh
exact cubic-field and sparse polynomial implementation is contained in check.py.
It pays only the declared finite identities/signs; the ordinary uniform/IFT/
supremum/physical bridges are in PROOF.md. Repeated digest checks do not
formalize those bridges. Generated records and runtime state are omitted.
