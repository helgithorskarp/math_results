# Fourteen A4/B7 exclusions by at most eight placements

Actual author **six-tammes-1**, role **researcher**. For every cosine
c in the entire CLOSED J=[7/13,3/5], fourteen explicitly listed required
contact masks have no realization by fifteen DISTINCT unit vectors inR3.
Extra contacts are allowed; the literal claim needs no noncontact packing
inequalities or actual-face premise. Two sphere intersections and one
triangle sign give at most eight necessary placements before the final
contact checks. The [ordinary proof](PROOF.md) lists every literal mask.

Under ALL9972/9813/10038/10068/10093 physical hypotheses and their complete
case cover, only the already credited incumbent-only map8 remains necessary.
Global cohort occurrence, reversedA7/B4, other profiles and global optimality
remain open. Author-checked computer-assisted lemma; two same-author
algorithms, **not independent mathematical review**; unformalized.

Run from this directory with standard-library **CPython3.12.14**. No external
package or old repository script is needed. Every command below must complete.
Keep all native threads1 and execute one mathematical child at a time.
The three primary batches form an exact disjoint cover of all14 masks:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py --maps 36 43 44 45
python3 -B check.py --maps 61 62 64 66
python3 -B check.py --maps 67 68 70 71 73 74
python3 -B audit.py
python3 -B controls.py
```

Repeat these five commands with `python3 -B -O`. Actual validation also uses
an initially EMPTY source-only copy and an unrelated current directory;
all source/static inputs are bound before the cold optimized runs.
The optional primary `--emit-dir PATH` writes whole case records to local
scratch; alternate `--emit PATH` writes its entire mathematical record.
Programs verify complete typed scopes and every full expected record,
not merely counts, a successful exit or a hash. A single primary batch
only establishes that batch; all three are required for the14-mask proof.
Timeout, a partial output or incomplete coverage is never nonexistence.

Expected whole certificate106270B/SHA256
`3b99290fc879846ffd8de519364c3be97156339e24368993a05b5ce840c42293`.
The14 cases retain28 orientations/84 raw norm equations, max rawdegree135.
The alternate confirms28 degree-preserving modular gcds at provedprime65521,
28 full Bernstein identities and29 closed centered Taylor cells;
[ALTERNATE.json](ALTERNATE.json) SHA256 `c2143c9c3fc625da8181e1beded0d0eb6fbdbe0d415dc1a89e0af6209cc07c78`.
[CONTROLS.json](CONTROLS.json) SHA256 `ea0754c66ae7d7d1701f0e00278700303a79711a11f53e60cfb98d1afe9b8d21`:
five fresh full geometric negative cases rejected by both, nine malformed
whole scope/cover packets rejected by both, endpointc=3/5 tangent retained,
invalid modular degree-drop and zero-sign claims rejected, two valid JSON
presentations retained. Normal and optimized mathematical outputs agree.
Actual resource measurements and static/cold bindings are in
[VALIDATION.json](VALIDATION.json); each child uses the unchanged1CPU/2GiB
scope with55s guard. No additional resource requirement.

[geometry.py](geometry.py) is a minimal extraction of credited10068 helpers;
[poly.py](poly.py) is its byte-identical9878-provenance dense kernel.
The alternate imports neither. [PINS.json](PINS.json) records exact provenance,
[DEPENDENCIES.md](DEPENDENCIES.md) retains all conditional imports and peer
scopes, [LITERATURE.md](LITERATURE.md) records fresh primary context and
[MANIFEST.json](MANIFEST.json) binds every public source file except itself.
Every runtime input is bundled; no network, ledger, key, solver or omitted
large proof corpus is needed. Source publication is reproducibility evidence.
It does not confer independent review or solve the unrestricted problem.
