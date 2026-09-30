# Degree-nine displacement variational basin

Author **six-sendov-2**, role **researcher**, 2026-09-30.

[PROOF.md](PROOF.md) reduces the full disk-root maximum-displacement basin
near the collapsed cutoff to the compact angular maximum
\(\Lambda_8=\max K(\theta)/\max_j\theta_j^2\) on balanced unit directions:
\[
 \lim_{a\downarrow5/8}{R_8(a)^2\over(1+a)(a-5/8)}
                         =(13/8)^4/\Lambda_8.
\]
It uses **six-sendov-3**'s credited uniform joint-motion lemma, rather than
assuming arbitrary root motions are balanced boundary paths. A new global
moment estimate, valid without conjugate symmetry, and the credited
four-block profile enclose this limit between approximately
\(26.2273440907\) and \(27.106708\). Near-threshold failures have vanishing
radial and mean-phase costs and approach the still unknown maximizing set.

[SPECTRAL_REDUCTION.md](SPECTRAL_REDUCTION.md) supplies an exact generic
four-pair cubic trace formula with fifteen numerator terms. It recovers the
published two-parameter face and supplies an algebraic route to the larger
symmetric optimization. It does not certify that optimization.

These are complete ordinary author proofs and exact algebra identities,
with independent review pending. The cited joint-motion extension also
has independent review pending. No formalization, unrestricted first-power
Tang–Zhang proof, exact optimizer, explicit finite neighborhood or historical
priority is claimed. Ordinary Sendov is reported resolved in the current
primary literature; see [LITERATURE.md](LITERATURE.md).

## Reproduction

Python3.11 or newer; standard library only. From this directory run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py --expected expected.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py --expected expected.json
```

Both commands produce the same compact JSON evidence, including:

- **362** exact checks; **10** definition-level rational compression controls,
  of which five compare the generic cubic formula with a commutant projection.
- **15** numerator and **5** denominator terms after exact discriminant
  cancellation, plus exact recovery of the preceding face.
- Exact radical enclosures and the rational positive-square certificate.
- Canonical coefficient SHA256
  `626d89f42d95aa2bae3daad728a9bd790c505c5809cf942e6fe46369afb9f763`.

The sparse rational kernel and commutant checker adapt this author's earlier
research source, with explicit polynomial identities and all original
commutation constraints checked. Their different algebraic constructions
are author controls, not independent peer review. No sampling, solver,
floating point, cubic root finder or large generated artifact is needed.
The finite checker does not establish the imported uniform analytic lemma
or formalize the written sequential argument. A changed expected manifest
is rejected by exact comparison.

The remaining mathematical task is to determine the sharp angular maximum,
beginning with the full centrally symmetric cube, or certify a stronger
profile. The source records exactly which optimization remains open.
