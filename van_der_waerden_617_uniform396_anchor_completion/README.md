# Uniform 396 edits for all 617 reflection-seam references

Actual author: **six-vdw-3**, role **researcher**, 2026-10-01.
Complete author computer-assisted combinatorial lemma; independent review
of this extension is pending.

Every binary word on 3704 positions avoiding all nonconstant integer
seven-term arithmetic progressions has **396–3302 nonpole edits against
each of the 617 specified QR617 reflection-seam references**. The word
itself is arbitrary: reflection, periodicity and balance are not assumed.
The six or eight undefined reference positions remain free and uncounted.

The new result gives individual **198–1651 edits in each original colour
class** at phases 184, 201, 205 and 269. This completes the previously
published total-floor profile. Individual floors of at least 198 now cover
616 phases; **phase 611 still has an individual floor of 197**. Its earlier
total bound of 396 is imported. No 3704-point colouring, new W(2,7) lower
bound, exact W value, attainment or unrestricted nonexistence is claimed.

From the repository root, CPython 3.11+ standard library suffices:

```sh
python3 van_der_waerden_617_uniform396_anchor_completion/reproduce.py --work /tmp/qr617-anchor-frozen
```

This independently replays all 28 anchor roots, their inherited rigidity
and domain proofs, normal and optimized checker modes, and corruption
controls. Expected status:
`EXACT_QR617_UNIFORM396_ANCHOR_COMPLETION`, uniform total floor `396`,
remaining individual-197 phases `[611]`, remaining total-395 phases `[]`.
The exact result fixture is [expected.json](expected.json).

Optional source-only generation of the nine new root certificates uses
`highspy==1.11.0` and `numpy==2.2.6`, in a separate virtual environment:

```sh
python3 -m venv /tmp/qr617-anchor-env
/tmp/qr617-anchor-env/bin/python -m pip install -r van_der_waerden_617_uniform396_anchor_completion/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /tmp/qr617-anchor-env/bin/python van_der_waerden_617_uniform396_anchor_completion/reproduce.py --fresh --work /tmp/qr617-anchor-fresh
```

Use a fresh work directory for each run. Compute children are serial,
externally capped at 30 seconds, with native LP limits of 15 seconds and
one thread. Regenerated coefficients need not be byte-identical: every
new certificate must pass the separate exact checker and prove the same
complete scope. A missing guide, timeout or unsuccessful bounded proposal
establishes no exclusion. There is no private input or proof corpus.

[PROOF.md](PROOF.md) states the mathematical argument and quantifiers;
[DEPENDENCIES.md](DEPENDENCIES.md) separates fully replayed old root proofs
from the imported other-phase profile; [VALIDATION.md](VALIDATION.md) and
[evidence.json](evidence.json) record the measured checks.
`SHA256SUMS` pins the compact published files.
