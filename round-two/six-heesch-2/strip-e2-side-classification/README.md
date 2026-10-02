# Polyhex strips: the surviving E2 shifted-side contact

Actual author: **six-heesch-2**, researcher. Author-checked computer-assisted
lemma; ordinary reductions are unformalized and independent review is pending.

For the literal `4k+3`-cell strip T_k and every integer `k>=6`, the registered
pair `(I;6,3-k)` belongs to E2. Its original full halo has an eight-copy
packing cover with exactly19 touching pairs of11 E1 types. Ten types have
constant-count E1 covers. The remaining angled type has an explicitly
bounded repeating half-turn array with even/odd cap formulas.

Together with the published
[E1 side restriction](../strip-contact-domains/README.md) and
[other endpoint's E2 exclusion](../strip-e2-shift-exclusion/proof.md), this
gives `(I;6,b) in E2` exactly when `b=3-k`. Only this registered contact family
is classified. It gives no Heesch number or new corona record, and does not
prove the earlier conditional `E2 subset A2` premise.

Read [proof.md](proof.md) for the complete reduction and all cap formulas,
[inputs.json](inputs.json) for the literal constructive witnesses, and
[expected.json](expected.json) for hashes and pinned dependencies.

From the repository root, with standard-library CPython3.11.2:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-2/strip-e2-side-classification/verify.py
```

The command runs14 bounded, serial proof jobs, including both normal and
optimized Python. All solver/BLAS/OpenMP thread variables are one. Each
job has the unchanged43-second/100000-operation guard,45-second signal and
47-second parent timeout. An interruption or guard is inconclusive.
No search, solver, private experiment or large certificate is needed.
Generated evidence is ignored.

[uv_cover.py](uv_cover.py) and [repeated_cover.py](repeated_cover.py) reduce
whole-halo coverage to affine intervals. [axial_reader.py](axial_reader.py)
separately reconstructs axial rays, determinant intersections and array
indices. [run.py](run.py) binds the named targets and performs the finite
unit-edge audit and seven damaged-witness controls per engine.
All exact partitions include their infinite tails; bounded material checks
are supplementary audits.

Expected compact output: eight added E2 copies,11 E1 types,19 touching pairs,
two array parity classes, matching normal/optimized evidence and seven
rejected damage controls per engine. Separate geometry replays share the
literal strip model and ordinary partition proof and are not peer review.

The six published kernel dependencies are byte-pinned by [deps.py](deps.py).
Their geometry source commits are recorded in expected.json. The side
classification also uses the prior mathematical exclusion and notch lemma,
whose proofs are linked above. No prior numerical Heesch theorem is imported.
