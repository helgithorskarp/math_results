# Complete source classification on one whole receiving cell

six-rupert-1, researcher. All proper source orientations, arbitrary original
translation and scale>=1 are classified on the closed pentagon in PROOF.md.
Only proper body symmetries, scale1, translation0 fit. Global Rupert status
remains OPEN; author checked, unformalized and independently unreviewed.

From this directory in a checkout of the repository:

```bash
python3 reproduce.py
python3 reproduce.py --optimized --compare .generated/complete_normal.json
```

Tested: CPython3.11.2 and NumPy1.24.2. NumPy is used for proposals only;
the exact proof code uses the standard library. All subprocesses are
sequential and all numerical libraries have one thread. Each proposal
has the unchanged40s/10000-node/depth18 guard; each exact preparation,
local replay and700-leaf batch has a separate unchanged45s guard.
An incomplete range, different fingerprint or undecided sign is a failure
to reproduce, never mathematical nonexistence.

The commands replay the pinned whole local lemma, reconstruct fresh actual
geometry and the complete proper source quotient, regenerate the private
source forest, verify every midpoint and all349380 coefficient signs,
run independent algebra/damage controls and require a complete aggregation.
The second command compares the entire compact proof record byte for byte.
The old local theorem is an explicit dependency, not silently strengthened.

Generated forests, caches and detailed proof records stay in ignored
`.generated/`; no bulky proof corpus is distributed. A generator fingerprint
is a reproducibility guard. Its floating signs never replace exact checks.
configuration.json pins the existing local files; geometry.py in that
dependency additionally pins the three actual named-model files before
import. expected.json contains small output fingerprints and exact extrema.

Expected:108 source roots,1833 midpoint nodes,1941 leaves,349380 exact
coefficients, positive affine weights and all coefficients strictly negative.
The new outer shell together with LEMMA9283 proves the all-source statement.
Normal/optimized whole compact record SHA256:

`2bb853347af5e8d66d2678a865d4faa347e8d585055c6f91ed729be420bd7a8e`.
