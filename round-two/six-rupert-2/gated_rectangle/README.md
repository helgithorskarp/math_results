# Exact J74 canonical rectangle and gated source certificate

six-rupert-2, actual role researcher. The ordinary proof and exact certificate
recover the old closed phase-crossing receiver-box classification using a
new receiver-independent realization of the actual full-body canonical source
cover. The global J74 Rupert question remains open. This is author checked,
unformalized and independently unreviewed.

Read [PROOF.md](PROOF.md) for the exact domains and canonical-only gauge
semantics. Use a checkout of the repository preserving relative directories;
[DEPENDENCIES.json](DEPENDENCIES.json) pins all direct source imports before
execution. Those imports pin their transitive original model/ordered-field
helpers. The old phase-crossing local/contact data is required; its former
millions-of-signs full-source conclusion is not an input premise.

Requirements: CPython3.11+ with the standard library only. Run from this
directory. One numeric-thread, sequential reproduction in ordinary mode:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
mkdir -p .generated/normal
python3 check.py --local > .generated/normal/local.json
python3 check.py --bridge > .generated/normal/bridge.json
python3 check.py --controls > .generated/normal/controls.json
for i in $(seq 0 29); do
    printf -v name 'chunk-%02d.json' "$i"
    python3 check.py --chunk "$i" > ".generated/normal/$name" || exit 1
done
python3 check.py --assemble .generated/normal > .generated/normal/aggregate.json
```

Each default job compares its entire record against [expected.json](expected.json)
and raises an explicit exception on any failure. Run the same sequence with
`python3 -O` and `.generated/optimized`, then compare every complete record
with its ordinary counterpart. A45-second per-child guard was used for the
reported audit; do not run multiple intensive children simultaneously.

All30 source chunks are necessary. Chunk size128; the last chunk contains103
leaves. The complete cube partition has3815 leaves and3814 midpoint nodes,
3437 actual physical cuts,369 conditional canonical gauge rejects and9 local
holes. Required strict exact signs:865323. These counts and the complete
ordered coefficient-stream hashes appear in the aggregate output.

`--emit` performs every mathematical check but omits comparison to frozen
expectations. `--chunk 0 --profile 32 --emit` is explicitly a PARTIAL profile
and cannot be used for complete assembly. Reusing saved journal JSON does not
independently re-establish the exact signs. Run all jobs from the source.

Source code and the91KB integer forest are compact; coefficient streams are
hashed in full and discarded. No private logs, search state, large proof
corpus, credentials or external oracle are needed. Consult [VALIDATION.json](VALIDATION.json)
for actual full modes, hashes, bounded resource data and the publication
reproduction check. The larger outer rectangle keeps cuts at bidegree(2,2);
this does not prove a universal runtime improvement or global non-Rupertness.
