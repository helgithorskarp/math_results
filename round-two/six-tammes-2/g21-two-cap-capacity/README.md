# Twelve-point G20 plus 5-12: two-cap capacity certificate

Actual author **six-tammes-2**, **researcher**, 2026-10-03.
Any finite unit t-code containing the original twelve-label G20 and the
additional contact 5-12 has **at most fourteen points**, throughout the
closed interval I=[14/25,593/1000]. Every additional point is arbitrary;
additional contacts are allowed. The proof requires no thirteenth point,
degree, face, physical cohort, support, proximity or optimizer premise.

This removes the fresh point contacting 2,9,10 required by
[the earlier derived-G24 theorem9966](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/derived-g24-capacity/PROOF.md).
Combined with [9922's two-branch routing](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/g20-five-cycle-routing/PROOF.md),
it eliminates the entire 5-12 branch for fifteen-point original-G20 codes
on I. Their P=(5,7,12,10,9) is consequently an actual undivided pentagon;
all three additional points lie in the complementary eleven-disk.
Only this routing corollary imports9922. The actual-P arbitrary-three
capacity problem, unrestricted original-G20 capacity and global Tammes15
optimality remain open.

Read [PROOF.md](PROOF.md) for the exhaustive two-candidate normalization,
packing exclusion of the second candidate, boundedness, convexity and
two-cap argument. [SYSTEM.json](SYSTEM.json) fixes the literal mask and
all-point quantifier. The certificate covers all364 active-plane triples,
with4 identically singular triples and360 complete closed covers:
367 leaves,31 short and336 opposite-residual exclusions. Both replays
check751 strict signs and73 generic identities. A fourteen-point control
at t=29/50 verifies two actual additions; it is not a new packing record.

Python3.11+ and its standard library suffice. From this directory, run
the following commands **serially**, with one mathematical child at a time:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
python3 generate.py --output /tmp/g21-two-cap-certificate.json
cmp CERTIFICATE.json /tmp/g21-two-cap-certificate.json
python3 -O generate.py --output /tmp/g21-two-cap-certificate-O.json
cmp CERTIFICATE.json /tmp/g21-two-cap-certificate-O.json
python3 check.py --output /tmp/g21-two-cap-check.json
cmp EXPECTED.json /tmp/g21-two-cap-check.json
python3 -O check.py --output /tmp/g21-two-cap-check-O.json
cmp EXPECTED.json /tmp/g21-two-cap-check-O.json
python3 audit.py --output /tmp/g21-two-cap-audit.json
cmp AUDIT_EXPECTED.json /tmp/g21-two-cap-audit.json
python3 -O audit.py --output /tmp/g21-two-cap-audit-O.json
cmp AUDIT_EXPECTED.json /tmp/g21-two-cap-audit-O.json
python3 controls.py > /tmp/g21-two-cap-controls.json
cmp CONTROLS.json /tmp/g21-two-cap-controls.json
python3 -O controls.py > /tmp/g21-two-cap-controls-O.json
cmp CONTROLS.json /tmp/g21-two-cap-controls-O.json
sha256sum --check SHA256SUMS
```

The complete42003-byte [CERTIFICATE.json](CERTIFICATE.json) has SHA256
**b6e46d0f57136128f83bee26b824b542f837f72813e251d675eecefcd8de924e**.
All eight native commands above actually passed in normal/optimized modes;
both whole regenerated certificates and all whole paired outputs agree.
[VALIDATION.json](VALIDATION.json) records actual executions, source pins,
one native thread, one mathematical child, unchanged1CPU/2GiB scope and
50-second internal/55-second subprocess guards. Maximum child wall time
was7.637982seconds; peak child RSS21480KiB. No limit was raised.

Integer Bernstein signs generate the closed covers. Rational Horner/Bernstein
and centered rational Taylor implementations separately replay every sign;
Taylor encloses757 complete subcells with at most one extra split, and the
maximum deflated sign degree is18. These same-author implementations share
the coordinate/Cramer reduction and integer polynomial kernel. They are
arithmetic corroboration, not independent mathematical review.
[CONTROLS.json](CONTROLS.json) records24 damaged scope/cover rejections,
swapped residual orientation, corrupted coordinates and endpoint-zero
rejections in both methods, with three valid schema representations and
two positive-polynomial controls. An incomplete run supplies no exclusion.

[RUNTIME_PINS.json](RUNTIME_PINS.json), [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json),
[DEPENDENCIES.json](DEPENDENCIES.json) and [LITERATURE.md](LITERATURE.md)
record exact source, scope and credit. Four arithmetic/producer files are
copied unchanged from9966 and credited; the new model drops its actual x.
The optional x in the fourteen-point control is never a theorem premise
or cap plane. Floating discovery streams and failed cap proposals are
not proof inputs. No raw expanded polynomial corpus is needed.

[Independent REVIEW9984](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/derived-g24-audit/REVIEW.md)
confirms the earlier thirteen-label theorem and proves its exact feasible
interval and uniform fourteen-point attainment. Its literal mask and
verdict are retained; it does not review this weaker-mask two-cap result.
Independent mathematical review and formalization of the present proof
are pending.
