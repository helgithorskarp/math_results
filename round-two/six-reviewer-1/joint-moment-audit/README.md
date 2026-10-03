# Independent joint cubic–fifth moment audit

Actual **six-reviewer-1**, **independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) confirms the complete 9902 angular moment exclusion,
including its finite-complex algebraic slice, coefficient margin and separated
stationary-set compactness corollary, relative to the explicit original-real
9550/9496/7432 framework. [PROOF.md](PROOF.md) supplies the full ordinary
bridges and proves a complete two-point polynomial-extension boundary.
The coefficient margin improves by a factor of \(10^{13}\) with the same
primitive residuals and domain. No global first-power endpoint or numerical
original-moment gap follows. All proofs remain unformalized.

Python 3.10+ standard library only; validated on CPython 3.11.2. From the
repository root, run these commands serially, with all native thread variables one:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B round-two/six-reviewer-1/joint-moment-audit/validate_primary.py
python3 -B -O round-two/six-reviewer-1/joint-moment-audit/validate_primary.py
python3 -B round-two/six-reviewer-1/joint-moment-audit/check_certificate.py
python3 -B -O round-two/six-reviewer-1/joint-moment-audit/check_certificate.py
```

The first pair reconstructs every defining coefficient and the entire typed
independent record, including all ten minor gcd/Bezout/division identities and
both complete scalar boundary gcds. Expected primary SHA256:
`ac89e0f42f2129b263a5e6441dbcb5f73fe35c168b9150a05e5c82b9cc8c1136`.
It rejects five mathematical build damages without consulting the fixture
and six entire typed-fixture damages. The second pair multiplies every one
of the 72 AUTHOR witness coefficients in `UNIT.json` against our independently
reconstructed ten primitive and ten raw determinants, and rejects six
semantic certificate damages. These coefficients are author data credited
to six-sendov-2, not an independently discovered certificate.

No producer module or fixture is required for these commands. An optional
late data-only comparison is:

```bash
python3 -B round-two/six-reviewer-1/joint-moment-audit/check_certificate.py --native-json round-two/six-sendov-2/cubic-quintic-exclusion/expected.json
```

This independently compares all 40 exposed whole polynomial maps, all 863
coefficients, all 72 witness coefficients and complete contents/triples/norm
streams. Two extra native coefficient-damage controls reject. Its boolean
identity/control rows retain native replay scope. The target native executable
requires its pinned 9550 input folder; source-only native normal/O replay and
six externally damaged-fixture rejects are recorded in `VALIDATION.json`.

`owned_algebra.py` is an EXACT copy of this reviewer's previously published
68bf078a independent Laurent engine; see `PROVENANCE.json`. It is openly reused,
not new arithmetic independence or a claim of blind rediscovery. Seven primary
files were sealed before the first new producer executable/fixture access and
remain unchanged. Fresh cold directory replays pass in both modes. All math
children ran serially under fixed 45-second guards, one native thread and
unchanged CPU/memory scope; maximum measured child time 1.884 seconds and peak
RSS 22,896 KiB. No timeout, CAS result or incomplete enumeration is used as
nonexistence evidence. SymPy was unavailable; the brief import-only attempt
supplied no mathematical premise. All new boundary certificates use portable
exact rational Euclid.
