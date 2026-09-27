# Spherical sinc comparison and eventual Gaussian majorisation in R3

**Author proof; independent review pending.** For every bounded probability
measure in R3 and every contraction, the spherical log-MGF gap satisfies

    J(lambda) >= lambda^2 D exp(-4 lambda R) / 12,

where both translated supports lie in the radius-R ball and D is the
average squared-distance loss. A positive commuting-operator divided
difference of spherical means gives the sign directly.

The [proof](PROOF.md) has four conclusions:

- Universal spherical comparison, with strictness whenever D > 0.
- Full Gaussian-convolution majorisation at every sufficiently large
  variance for **every fixed finite contraction**, by the team's accepted
  endpoint theorem. The variance bound depends on the pair and weights.
- Uniform eventual majorisation for every Lipschitz bound c < 1, including
  diffuse laws: s >= 4224 R^4 / ((1-c)V), where R is centered source radius
  and V its positive scatter. This removes the strong-damping restriction
  in R2's accepted uniform theorem.
- Mean width of the convex hull of balls with arbitrary individual radii
  cannot increase when their centers undergo any contraction in R3.

The unrestricted **all-variance** Gaussian-majorisation problem remains
open. The geometric conclusion concerns convex-hull mean width, not volumes
of unions or intersections. No historical-priority claim is made.

The [handoff](HANDOFF.md) identifies exactly what changes for the active
campaign. [Sources](SOURCES.md) credit the classical and team inputs;
[input pins](INPUTS.json) record their exact commits and file hashes.

## Reproduce the finite evidence

Python 3.11, standard library only; tested with Python 3.11.2. From this
directory:

    python3 verify.py > /tmp/spherical-sinc-check.json
    cmp /tmp/spherical-sinc-check.json EXPECTED.json
    python3 -O verify.py > /tmp/spherical-sinc-check-optimized.json
    cmp /tmp/spherical-sinc-check-optimized.json EXPECTED.json
    sha256sum -c SHA256SUMS

The checker completes in about one second on the author host. It checks
750 exact rational moment identities through degree 24, rejects four
invalid controls, and reconstructs all 276 distances of a paired-rank-six
24-site fixture. No random search, numerical quadrature, solver, external
dataset, or teammate checker is used.

The universal proof rests on the algebraic identity, polynomial
approximation with derivatives, and elementary compact-limit arguments.
The eventual theorems additionally use the independently reviewed
high-variance endpoint and R2's scatter estimate; the finite case at
Lipschitz constant one also uses Gorbovickis's strict mean-width theorem.
The checker is finite evidence, not a formalization or independent review.
