# Independent n26 transport-cut audit

**six-reviewer-1 / independent mathematical reviewer.** Confirms the complete
original rank-nine certificate of LEMMA10123/0, authored by six-downset-2.
Every real six-deficit repair of the exact fixed thirty transported proper
coefficients is excluded. The full real 36-coordinate face remains open.

[Review](REVIEW.md) · [ordinary proof](PROOF.md) ·
[defining input](INPUT.json) · [credited n24 input](N24_INPUT.json) ·
[provenance](PROVENANCE.json) · [validation](VALIDATION.json).
The proof also derives exact negative-eigenvalue and necessary normalized
proper-motion bounds. The ordinary proof is unformalized. Written proof and
signed certificate were exposed; this is not a blind review. Six fresh
primary files were sealed before the new native n26 executable was opened.

Python 3.10+ standard library; actually checked with CPython 3.12.14.
No primary external executable, solver, floating arithmetic, harmonic decoder,
or downloaded numerical input is required. From this directory run:

```sh
python3 -B reproduce.py --out /tmp/n26-independent-audit
```

This cold-copies sealed primary source, regenerates the entire 280967-byte
original affine record and 12486-byte literal-control record in normal and
optimized mode, compares every field and every byte, and checks 18 semantic
rejections. The hashes recorded in VALIDATION.json follow the full comparisons.
One math child runs at a time; all six native thread variables are set to 1;
each child has a fixed 45-second guard. A timeout is an operational failure.

Exact expected principal values:

- rank of the original PSD dual: 9; original minor determinant: -1575;
- transported pairing: -274356636025866281341291/98175000000;
- trace of Y: 37557180749050;
- negative eigenvalue gap rho: 274356636025866281341291/3687176220037983750000000;
- necessary normalized proper-entry motion Gamma: 823069908077598844023873/574439993048321693800000000.

Optional *late native corroboration*, from a checkout also containing the
nine target files and three hash-pinned n24 files listed in PROVENANCE.json:

```sh
python3 -B corroborate.py --native ../../six-downset-2/six_deficits_n26 --primary /tmp/n26-independent-audit/check.py.json --out /tmp/n26-late-native
```

That step cold-copies the author's public source and compares the complete
6690-byte native record in both modes against the explicit fresh/credited
comparison. It is corroboration, not the primary proof. Its old n8 literal
control is credited author evidence, not an independent new n8 audit.

The literal primary n7/n9 controls are arbitrary signed affine matrices,
not PSD/H witnesses. Generated records are reproducible outputs and are
not published. The input JSON files are compact defining mathematical data.
