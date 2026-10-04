# Central original-one-double exclusion

Actual author **six-sendov-2**, role **researcher**. This source proves
`C < 47/2` for every actual normalized, odd-moment-zero real eight-vector
with exactly one original double and

```text
0 < D < 1/24,  24(a^2-1/8)^2 < D.
```

[PROOF.md](PROOF.md) gives the complete original-root fibre, a new coupled
cubic-decay cap, the full spectral-mass/Bezout interpretation, all three
continuous-domain positivity boxes and the two remaining D-range payments.
It also proves that any remaining high-value exact-one-double profile
lies on the strict outer branch `d < 0, u < 0`, with
`1/729 < D <= 5/141`; its equality boundary is impossible by the actual
Rolle degree count. Exclusion of that branch and the complex first-power
inequality remain open. This is an ordinary computer-assisted author
lemma, unformalized and independently unreviewed.

## Reproduce

From the repository root, with Python3.11+ (tested3.12.14):

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/central-one-double-exclusion/verify.py --expected round-two/six-sendov-2/central-one-double-exclusion/EXPECTED.json
```

The standard-library Fraction engine regenerates every original polynomial,
moment, Bezout entry, determinant coefficient and Bernstein coefficient,
checks every reverse identity and prints the compact expected record.
It reads the expected fixture only after completing the mathematics.
Repeat with `-O` if desired: mathematical gates use explicit exceptions,
not Python assertions. No CAS or downloaded input is needed for this engine.

An environment with **SymPy1.14.0** can independently reconstruct every
entry via a different determinant and direct-box composition method:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/central-one-double-exclusion/compare_cas.py --expected round-two/six-sendov-2/central-one-double-exclusion/EXPECTED.json
```

Add `--whole /tmp/central-whole.json` to either command to write the entire
1,609,517-byte mathematical record outside the source directory. Add
`--check /tmp/central-whole.json` to the other to compare every byte of
the canonical, fully regenerated record. Its SHA256 is
`d72afbbe7b6a4e89abcde57a8d5d919b864abb0a0456b205dd668f1238de6ec1`.
The complete record is deliberately not committed.

For all four local/cold normal/optimized replays, full record comparison,
and six mathematical damage controls:

```sh
python3 -I -B round-two/six-sendov-2/central-one-double-exclusion/validate.py --scratch /tmp/central-one-double-validation --output /tmp/central-validation.json
```

If SymPy is installed in a separate dependency directory, pass its path
as `--sympy-root PATH`. This inserts only that explicitly selected CAS
dependency; production source and cold copies stay isolated. Each child
is serial with all six native thread variables one and a fixed45-second
guard. No resource setting is raised. A failed/interrupted run is
incomplete evidence and never a nonexistence claim.

## Evidence and trust boundary

[EXPECTED.json](EXPECTED.json) records all 6,786 strictly positive tensor
entries, degrees `(12,28,5)`, exact minima, three entire-box hashes and the
entire mathematical-record hash. These compact fields accompany whole
regeneration and reconstruction, not a sampled sign test.
[VALIDATION.json](VALIDATION.json) records four whole positive replays,
six intended mathematical rejects, complete coefficient agreement, version
and resource measurements. The largest validated child took7.517s and
used69,544KiB. All fit the unchanged1CPU/2GiB/128-task individual scope;
no timeout, resource failure or incomplete enumeration occurred.

Different same-author computations validate arithmetic. They do not
constitute independent peer review. The ordinary root geometry, compression,
full-mass interpretation, cap inequalities, Bernstein partition-of-unity
and cited small-D collar remain written, unformalized mathematical bridges.
[LITERATURE.md](LITERATURE.md) and [DEPENDENCIES.json](DEPENDENCIES.json)
give current problem status, precise prior scopes, exact commitments and
the intended original atomic relations.
