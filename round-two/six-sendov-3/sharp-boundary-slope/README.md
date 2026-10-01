# Optimal degree-nine first-power boundary coefficient

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Ordinary author proof; independent review of this extension is pending.

For degree-nine disk-root polynomials and marked roots $a$, let

\[
 F_p(a)=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\qquad
 c=\cos(\pi/9),\quad C=\frac83+\frac1{3(1+c)}.
\]

The [complete proof](PROOF.md) establishes

\[
 \lim_{r\uparrow1}\inf_{p,a:\ |a|=r}
 \frac{F_p(a)-8}{1-r}=C
      =2.838515200687628\ldots .
\]

The universal lower slopes below $C$ are credited to
[six-reviewer-2's existing refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_boundary_review2/REFINEMENT.md).
The new result proves sharpness by genuine disk-root polynomials, and
classifies all leading critical profiles of sharp sequences. With

\[
 y=1/(3(1+c)),\quad x=2/3-y,\quad H=14y,
\]

every balanced real eight-vector $h$ with squared norm $H$ is realized
by the explicit family

\[
 a=1-\epsilon^2,\quad m=-x\epsilon^2+\epsilon^3,\quad
 p_{\epsilon,h}(z)=9\int_a^z\prod_{j=1}^8(w-m-i\epsilon h_j)\,dw.
\]

One sufficiently small positive range of $\epsilon$, uniform over all
these profiles, puts every original root strictly inside the disk.
The first-power sum is $8+C\epsilon^2+8\epsilon^3+O(\epsilon^4)$.
The third-order inward correction repairs the four root tangencies.
Conversely sharp sequences have critical energy $H(1-|a|)+o(1-|a|)$,
vanishing normalized real critical energy, and the same first-order
nonagon root motion. Their leading imaginary critical profiles fill the
whole balanced sphere; no critical multiplicity hypothesis is used.

This determines an asymptotic coefficient. The radius is existential;
the full first-power endpoint in the middle annulus, the inequality at
exactly slope $C$, and the second-order optimal margin remain open here.
Multiplicity and zero-denominator conventions are explicit in the proof.

From the repository root, **Python 3.11.2**, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-3/sharp-boundary-slope/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-3/sharp-boundary-slope/verify.py
```

Both reconstruct and compare the complete [expected record](expected.json):
**45 exact checks; six mathematical mutations rejected**. The cubic-field
signs, all **108** terms of the generic derivative jet and all **217**
terms of the anchored polynomial jet are checked at seven independent
balanced profile coordinates. A separate scalar inverse-distance jet is
checked against its defining equation. The complete record SHA256 is

```text
3b1f2fe109fced85b521b04e952ef3e233811ed9ba70befe8ebe117ea2c18e26
```

Missing, malformed and altered fixtures reject under optimized Python.
The development-only `--emit-fixture` flag emits a replacement record;
ordinary verification requires the existing complete fixture. A run takes
about one second and little memory, using one process and one thread.

The universal analytic bridges and credited reviewed inputs are ordinary
written mathematics. The checker does not certify disk containment or the
quantified theorem in a formal proof assistant. No numerical root search,
solver, external data, private corpus or large certificate is required.
See [literature and exact dependency scope](LITERATURE.md).
