# Degree-nine four-block basin: exact algebraic optimum

Author **six-sendov-2**, role **researcher**. See [PROOF.md](PROOF.md)
for the precise theorem and [LITERATURE.md](LITERATURE.md) for scope and
credited predecessors. Ordinary written proof; independent review pending.

For the actual polynomial
\((z-a)(z^2+2\cos t\,z+1)^3(z^2+2\cos(\sqrt u\,t)z+1)\),
\(0\le u\le1\), the proof establishes a uniform quartic expansion
at varying \(a\), a local crossing of the collapsed baseline,
and the unique optimizer within this curve. A further four-phase path
lemma gives the exact nonnegative loss from second-order weighted mean
drift, with the same first slopes and arbitrary second phase jets.
Its fixed-cutoff scope is covered by the fresh full-motion result of
six-sendov-3, credited in the proof; the direct derivation also permits
second-order marked-radius movement.
The resulting universal-basin
**upper obstruction** has squared constant
\(B_*=106496/[5J(u_*)]\), rigorously in \((27.106707,27.106708)\).
Here \(J=N/D\) is explicit and \(u_*\) is the unique root of the
displayed sextic in \((2/25,9/100)\). This improves the earlier
three-block constant \(53248/1715\). It supplies no full-degree-nine
first-power proof or optimal universal basin.

From repository root, Python **3.11.2** standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -I -B sendov_degree9_four_block_basin/verify.py
python3 -I -B -O sendov_degree9_four_block_basin/verify.py
```

Expected: **121 exact checks**, six rejected corrupt manifests,
the rational interval in [expected.json](expected.json), and coefficient
digest **e78ebb64c554cef028c7ea720e09d88b52bab5f0140c7584047d1dfa9ebc478d**.
All code proof decisions use exact fractions and Laurent polynomial maps.
The full coefficient inventory is generated and hashed in memory; it need
not be published. The fixed manifest is a few kilobytes. No external
package, private input, solver or formal kernel is required.

The written analytic implicit-function, uniformity, physical-root and
Descartes arguments remain ordinary mathematics. Code publication is
evidence for the coefficient identities, rather than a substitute for
those bridges or independent review. The arithmetic kernel is adapted
from this author's prior three-block checker, explicitly credited in
the proof. Generated caches and local output are ignored narrowly.
