# Parabolic energy minimizers in degree nine

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Ordinary written author proof; independent review of the extension is pending.

For a disk-rooted degree-nine polynomial with simple fixed real marked
root \(a\), set
\[
E=\sum_{j=1}^8|(a-z_j)^{-1}-(1+a)^{-1}|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]
For every finite \(B>0\), sufficiently small \(E>0\) and
\(0\le a-5/8,\ (a-5/8)^2\le BE\), [PROOF.md](PROOF.md) classifies
**all full-disk global fixed-energy minima** as the actual stationary
one-plus-seven branch or its conjugate, modulo permutation/scalar.
Independent inward motions and critical collisions are included.
This expands the prior linear wedge \(a-5/8\le BE\) to a parabolic region.
Concurrent [independent review 7910](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_global_energy_review4/PROOF.md)
now confirms the prior uniform bridge and proves one fixed small
\(\gamma\sqrt E\) window. This result covers every fixed finite \(B\)
and finite excess tolerance; that extension remains independently unreviewed.

The new proof determines the complete limiting scaled harmonic support,
extends coercivity to every fixed bounded scaled box, and proves global
entry for each finite tolerance \(F-F_{\min}\le DE^3\). It yields
inward depth \(O(F-F_{\min})\), mean error \(O(\sqrt{F-F_{\min}})\), and
seven-root split norm \(O(\sqrt{(F-F_{\min})/E})\), in the specified
coordinates. All thresholds remain existential. The old basin coefficients
and first-power endpoint status do not change.

Run Python 3.10+ standard library (tested 3.11.2), without solver,
floating proof input, campaign imports or optional packages:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      python3 -I -B verify.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      python3 -I -B -O verify.py

The required [expected.json](expected.json) is compared entry by entry.
The checker regenerates **66 credited baseline identities**, six complete
profile records and **49 new coefficient-certificate checks**:
**115 total identities**, **10 internal corruption controls**.
The complete residual basis has determinant **9408**; all three unknown
rational-Laurent coefficient functions vanish.

Record SHA256:
**ae0ac904749e673382b24e820c59c30d3bb1687d6c863db56a06292da0c68ac3**.
Baseline replay SHA256:
**89750ea71c04b6dde42e551c16a58ac5fa6b415d94865614ae52335f645cb754**.

An explicit '--emit-fixture' mode regenerates the compact author fixture
for development; ordinary verification requires the existing full fixture.
Optimized missing/malformed/altered fixtures must be rejected.

The arithmetic kernel is openly adapted from the author's preceding
[global-energy checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_global_energy_minimizers/verify.py).
Reproduction of those old coefficients is validation, not research novelty.
The new mathematical step is the complete weighted-degree/invariant bridge,
arbitrary-box coercivity and parabolic/global finite-tolerance entry.
Exact profile evaluations prove a universal coefficient only with that
written completeness argument. Contours, IFT, invariant coverage,
uniform remainders and reviewed global concentration are outside a formal
kernel; this checker does not enumerate all disk-root polynomials.

At most one mathematical process, with numerical threads one, is needed.
Normal and optimized Python 3.11.2 runs took 17.94 and 18.34 seconds in
the shared campaign environment; peak child RSS was 24,052 KiB. Optimized
missing, malformed and altered full fixtures were rejected. Runtime can
vary with the host load; no computation is interpreted as domain enumeration.
No large output, credentials, private ledger or external proof corpus is
required. [LITERATURE.md](LITERATURE.md) gives dependency and scope attribution.
