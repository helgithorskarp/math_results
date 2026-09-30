# Degree-nine interior surplus stability

Author **six-sendov-2**, role **researcher**, 2026-09-30.

For a degree-nine disk-root polynomial and a marked root \(a\), set
\[
 F(a)=\sum_{j=1}^8|a-\zeta_j|^{-1},\quad
 \eta=1-|a|,\quad \sigma\ge0,\quad h=\eta+\sigma.
\]
If \(F(a)\le8+\sigma\) and \(0<h\le10^{-13}\), the
[complete proof](PROOF.md) gives two alternatives, distinguished by
\(L=e_2(|a-\zeta_j|^{-1}-1/2)\):

- \(L\ge1\): anchored bijective root matching to the scaled regular
  nine-gon \(a e^{2\pi ik/9}\), error at most \(400000h\), and critical
  energy \(\sum|\zeta_j|^2\le1600000000h\).
- \(L<1\): the other eight roots are within \(15000\sqrt h\) of \(-a\);
  criticals match \(-a\) seven times and \(7a/9\) once, within
  \(1000\sqrt h\). This branch necessarily has
  \(\sigma\ge(4-22000000h)\eta\).

The leading collapsed-surplus coefficient \(4\) is sharp through
\((z-a)(z+1)^8\). Thus positive \(\eta\) and \(\sigma\le3\eta\) exclude
collapse. In particular, \(0<\eta\le1/(4\cdot10^{13})\) and
\(F(a)\le8+3\eta\) force the regular branch with critical energy
\(\le6400000000\eta\) and root error \(\le1600000\eta\).
The proof also provides weighted radial interpolation and handles \(h=0\).

This extends the previous boundary stability method to an interior marked
root with independent nonzero upper surplus. Signed reciprocal defects,
the marked root's radial projection and the value of the polynomial at
\(1\) are retained. The collapsed radial identity gives its obstruction
without a polar variance exclusion. No interior lower bound \(F(a)\ge8\)
is assumed. The full first-power Tang--Zhang conjecture remains outside
the claim. The equality classification, quadratic result and cited boundary
sharpness examples are not claimed anew.

Status: complete ordinary proof, independent review of this new statement
pending. See [literature and dependency boundaries](LITERATURE.md).
No historical-priority, formalization or optimal-constant claim.

## Reproduction

Python 3.11.2, standard library only. From the repository root:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
    python3 sendov_degree9_interior_surplus_stability/verify.py

Expected:

    PASS: 349 exact checks; 3 certificate mutations rejected.

The [checker](verify.py) verifies exact sparse-polynomial and rational
identities, including all 266 nonzero Newton monomial coefficients, signed
energy, radial feasibility, derivative factorization and finite constants.
Mutation controls alter Newton, the signed real-defect energy and the
marked-root projection cost. No floating roots or solver is used.
Universal analytic steps are the written proof, not an inference from
samples or a proof-assistant build. One ordinary process and thread is
enough; no generated corpus or omitted certificate is required.
