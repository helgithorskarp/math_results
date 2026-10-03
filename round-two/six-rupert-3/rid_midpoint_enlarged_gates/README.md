# RID: larger companion-set gates and a full source frustum

six-rupert-3, actual role **researcher**, 2026-10-03.
Complete ordinary intermediate proof with exact controls; author checked,
unformalized and independently **UNREVIEWED**. Global RID Rupert status:
**OPEN**.

For the entire closed receiver segment \(r=(x,0,1)\),
\(2\phi-3\le x\le2-\phi\), the physical relative gate
\(\sqrt{d_x^2+d_z^2}<2\phi-3, |d_y|\le1/4\)
admits precisely the parent and moving companion rotations, with original
translation0 and scale1. The whole closed source frustum
\(\operatorname{conv}(F/3,F)\) enters this gate automatically.
Closed centered/set radius1/5 and open companion-set radius\(2\phi-3\)
corollaries retain the companion explicitly. Every fit touches receiving
supports, so no strict passage follows. See [PROOF.md](PROOF.md) for all
quantifiers, metric forms, proper body actions and the exact branch formula.

Runtime: CPython **3.11.2**, standard library only. From this directory:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I verify.py --output record-normal.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -O -I verify.py --output record-optimized.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I verify.py --controls --output controls-normal.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -O -I verify.py --controls --output controls-optimized.json
```

Use fresh output names. Every mathematical field must match between modes;
timings, peak RSS and the `optimized` flag may differ. Checkers hash all
declared inputs before importing the arithmetic and again after computing.
Every exact inequality and semantic requirement raises explicitly under -O.
Generated complete records are ignored and stay outside publication.

Expected production SHA256:
`6aba27528591e36b0acbd82bce8d62f87edbbd4477b60fff6339eb9e7ac2e082`.
Expected semantic-control SHA256:
`9ab70597a6e8f2a7e91964bf2e66c7e95bb5b2561bdcd76fe97e9563573f9423`.
Canonical JSON uses sorted keys and separators `(',', ':')`.
[EXPECTED.json](EXPECTED.json) contains all complete section hashes;
[EXACT_CONTROLS.md](EXACT_CONTROLS.md) gives every literal source entry bound;
[MANIFEST.json](MANIFEST.json) pins runtime source and compact expected inputs;
[DEPENDENCIES.json](DEPENDENCIES.json) names the sole mathematical premise
and prior published credit. [VALIDATION.json](VALIDATION.json) records full
normal/O comparisons and fresh empty-directory relocation.

The three semantic false controls reject a wider alpha1/4 source frustum,
the wrong **proper body** half-turn HU in the companion formula, and an
unsupported uniform metric radius1/4 certificate. They check the indicated
certificates; rejection does not prove every larger region false. Source
pin-damage checks additionally test declared code/expected inputs before
arithmetic import in both modes.

Exact field signs are decided by rational comparisons of A² and5B² for
A+B√5. The trust boundary is Python integer/Fraction arithmetic and the
written convexity, quaternion, support and covariance proof; no proof
assistant or independent verifier is claimed. Older10074 is used only for
the fixed parent converse. The independently reviewed single-center
threshold is credited as prior art, with no verdict transfer.
