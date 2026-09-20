# Uniform conditioning and uniqueness for polygon sign codes

For every feasible, strictly ordered half-circle sign code, the closure
Jacobian satisfies the sharp bound

\[
\|Dg(\phi)^T\lambda\|_\infty\geq\|\lambda\|_2.
\]

The constant is independent of the number of vertices and of the code.
It follows that, for every `n >= 3`, each fixed code has at most one feasible
stationary point with perimeter deficit

\[
U_n-F\leq\frac1{400n^5},\qquad U_n=2n\sin\frac{\pi}{2n}.
\]

If a code reaches this superlevel, its global maximum on the closed ordered
angle simplex is unique. At that point the full Lagrangian Hessian is at
least `I/(2n^3)` and the equality KKT matrix is nonsingular.

The model fixes `phi_0=0`, `phi_n=pi`, uses `c_j in {+1,-1}`, and imposes

```text
0 < phi_1 < ... < phi_(n-1) < pi
g(phi) = sum_j c_j (exp(i phi_(j+1)) - exp(i phi_j)) = 0
F(phi) = sum_j 2 sin((phi_(j+1)-phi_j)/2).
```

The conditioning proof uses an odd alternating sum of switch vectors.
An even alternating sum on an arc shorter than `pi/3` has norm less than
one; this prevents feasible free switches from concentrating in such a
projective arc. This is the main structural lemma. The later uniqueness
argument uses the existing strong-convexity/Taylor method with new uniform
constants; see [attribution](SOURCES.md).

For powers of two `n >= 2^17`, Bingane's published `B_n` construction lies
above the threshold. Together with the prior
[uniform saturation theorem](../small_polygon_uniform_saturation/PROOF.md),
this reduces every unrestricted global contender at those orders to a
unique maximum within its own code. It does not select the winning code.
The cutoff is conservative, not an optimized bound.

## Reproduce the supporting checks

Tested with Python 3.11.2, standard library only:

```sh
cd discrete_geometry/small_polygon_code_conditioning
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python runs must print the same JSON, exactly matching
[expected.json](expected.json), with `status: PASS`. They check 255 even
and 256 odd rational short-arc subsets, 60 half-circle cuts, the exact
sharp triangle fixture, 189 Poincare coefficient identities, six positive
rational margins, and controls for infeasibility, an incorrect cut, the
unpinned path kernel, and malformed codes. The run takes under a second
on the development machine. No packages, downloads, numerical solvers,
random seeds, or external data are needed.

[PROOF.md](PROOF.md) carries the universal quantifiers. The checker
corroborates algebra, constants and conventions; it is neither a proof
assistant formalization nor an exhaustive feasible-code computation.
Source publication and matching checks do not constitute independent review.

## Scope

The sharp constant refers to the infinity-norm inequality, not sharpness
of its weaker consequence `sigma_min(Dg) >= 1`. Feasibility is essential.
The uniqueness theorem applies only to the stated high-perimeter region;
it neither excludes lower stationary points nor proves global convergence
of a numerical method. Its uniform threshold does not recover the sharper
published candidate-specific `n=16` certificate. There is no assertion of
uniqueness across codes, a new optimal perimeter, or a classification.

The main theorems are self-contained. Only the original-polygon corollary
uses the earlier saturation theorem and Bingane's explicit construction.
Literature was refreshed on 2026-09-20; the claimed new scope is relative
to the sources searched, without exclusive priority.
