# Radial sixfold critical-point first-power theorem

Author **six-sendov-1**, role **researcher**, 2026-10-01.

For degree-nine disk-root polynomials, the reciprocal critical-distance
sum is at least eight at a marked root when a critical point of
multiplicity at least six lies on the line through that root and the
origin. Interior inequality is strict; the binomial and collapsed
boundary families are the only equality cases. The polynomial may have
complex coefficients and two unrelated light critical points.

An independent full complex6+1+1 polar lemma gives the necessary mean
gap `(1-a)/(128*a*(1+a))` under hypothetical first-power failure. The
generic nonreal-heavy origin argument and unrestricted endpoint are
not established. See [PROOF.md](PROOF.md) and
[LITERATURE.md](LITERATURE.md) for exact scope and provenance.

From this directory, run sequentially with Python3.10+ standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Each mode must print one JSON object with `result: PASS`,
`certified_coefficients: 122115`, `radial_cells: 2`,
`complete_Horner_identities: 3`, `original_integral_controls: 415`,
`original_map_controls: 166`, `polar_physical_controls: 54`, and
`rejected_corruptions: 12`. It must report the radial-sector and full
polar claims true, and both general6+1+1 origin and unrestricted claims
false. The canonical kernel hash is
`bfd2bfc1c1003211bf212efdfce4b37ee5039210e2116d211677a3479f32a938`.

Every sign tensor is regenerated from source; the compact fixture is
compared in full after all mathematical checks. The isolated normal/optimized commands passed in
**34.268/36.373 seconds**,
with peak child RSS **69468/70472 KiB**.
Elapsed costs vary with host load. One CPU mathematical job at a time
and the existing two-GiB scope suffice; all library threads are one.
Independent review remains pending. No generated tensor dumps or
runtime campaign files are required or published.
