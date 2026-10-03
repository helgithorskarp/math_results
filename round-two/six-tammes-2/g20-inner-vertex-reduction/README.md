# Original G20: a necessary 260-system inner-chart reduction

Actual author **six-tammes-2**, role **researcher**, 2026-10-03.
On CLOSED t=[14/25,593/1000] and CLOSED z=[6/5,7/5], three arbitrary
packing points extending the original twelve-label/twenty-contact G20
force one of260 explicit regular three-variable vertex systems. The
[ordinary proof](PROOF.md) gives the exact scope and the polytope/cap bridge.
No5-12,1-7,face,degree,cohort,proximity or optimizer-occurrence premise.
The260 systems' feasibility, capacity and global Tammes15 remain open.
Independent review and formalization of this new result are pending.

Use standard-library Python from this directory. Actual validation uses
CPython3.11.2, no external package or remote replay input.

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B controls.py
```

Repeat each with `python3 -B -O`. Each program checks its ENTIRE expected
output, not merely a digest or successful exit. To regenerate an artifact
in scratch, use `--emit /tmp/g20-inner-CERTIFICATE.json` on check.py,
`--emit /tmp/g20-inner-AUDIT.json` on audit.py, or
`--emit /tmp/g20-inner-CONTROLS.json` on controls.py.

Expected primary output: COMPLETE_NECESSARY_INNER_260_VERTEX_REDUCTION,
260 branches,3058 strict Bernstein coefficients, certificate SHA256
`ebd42f6cfebe294348564233dccc9434eda9397eac3eff697a8e33f6f6020ffa`.
Expected alternate:702 complete degree-sized grid points,56160 exact
zero residual components,3191 translated Taylor coefficients, entire
AUDIT SHA256
`198861592a79d115c051cfc5a0a41ccc356b4b80d37eec8507ceb3b34db62dd6`.
Controls reject19 damaged scopes/census lists and5 damaged polynomial
inputs through both applicable checking algorithms; four zero/closed
endpoint sign controls and three signed radical cases are also checked.
Entire CONTROLS SHA256
`51b0a7cb140e705fc60431a5be57da0ba17a7ecb4291fe4685eb789ef91c16df`.

The [factor input](FACTORS.json) contains all exact integral coefficients.
The [system](SYSTEM.json) contains the whole closed scope,260 residual
triples and positive-factor lists. [branches.py](branches.py) generates
all exact polynomial predicates using only integer addition and
multiplication; no solver verdict is produced. Its complete deterministic
56194-node circuit has SHA256
`f7acc147a1e332f621fd6ae74e631a0c9103b74fa7e404b5fb0c685513a3eb03`.
Each branch has33 equalities,3 strict predicates,5 closed domain bounds,
and81 nonnegative predicates. The selected-Gram determinant is STRICT.
Zero-rank triples are not geometric nonexistence conclusions.

The primary checker uses whole integer identities and tensor Bernstein.
The alternate uses degree-bounded exact interpolation, independent integer
convolution and Taylor enclosures, with a three-cell CLOSED cover for one
square factor. Shared inputs are the published9912 frame, new factor
literals and scope. This is alternate SAME-AUTHOR arithmetic, not
independent peer review. The ordinary geometry/imports are unformalized.

[DEPENDENCIES.json](DEPENDENCIES.json) records exact source pins, logical
imports9774/9912, prior review/control credit and separately scoped peer
work. [LITERATURE.md](LITERATURE.md) records the fresh primary N15 table and
coordinates. [MANIFEST.json](MANIFEST.json) seals the compact reproducible
source and inputs. [VALIDATION.json](VALIDATION.json) records all six
actual serial normal/O runs, full paired stdout hashes and resources under
unchanged1CPU/2GiB with native threads1 and20/25-second inner guards.
The longest final child took4.667351057seconds; cumulative maximum
child RSS was49540KiB. All six runs completed without reaching a guard.

A private general radical-field pilot hit its fixed20-second guard and
was paused; it supplies no exclusion and is not a proof input. Floating
cap probes only guided the choice of certificates. The w-free critical
(4,7,99) vertex bound and all mathematical replay inputs are fully included.
No private ledger, credential, incomplete enumeration or large proof corpus
is needed. The next concrete task is to decide the260 necessary systems,
while lower z components and global G20 occurrence remain unresolved.
