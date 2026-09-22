# A uniform linear threshold for restricted Schur numbers

**Theorem.** If $\ell\geq3$ and $k\geq2\ell+1$, the least integer forcing
a monochromatic solution of $x_1+\cdots+x_k=y$ in every two-coloring is

$$
k^2+\left(\frac{(\ell+1)(\ell-2)}2+2\right)k+\ell(\ell-2),
$$

when the summands must have exactly $\ell$ distinct values. The same
answer holds when at least $\ell$ distinct summand values are required.
Repetitions are allowed; the positive sum is a further distinct integer.

[The complete proof](proof.md) establishes the infinite theorem without
computational assumptions. Its new ingredient is a compression estimate
for a color-forcing argument that uses all small opposite-color values.
Gaiser's [2026 primary preprint](https://arxiv.org/html/2608.08789v1)
previously proved the formula for each fixed $\ell$ and sufficiently large
$k$. This gives the explicit uniform threshold $K(\ell)\leq2\ell+1$ and
allows $\ell$ to grow linearly with $k$. The optimal threshold, the
diagonal weak Schur problem, and the three-color question are not settled.

## Reproduce the exact checks

Python 3.11 or later; standard library only. Tested with Python 3.11.2.
From this directory:

```sh
python3 verify.py > /tmp/restricted-schur-check.json
diff -u expected.json /tmp/restricted-schur-check.json
sha256sum -c SHA256SUMS
```

The default run checks every minority-color subset of $[2\ell-1]$ for
$3\leq\ell\leq9$, at $k=2\ell+1,2\ell+2,2\ell+3$: **262,128 prefix
instances**. Color exchange covers both choices of majority color. It
also checks four large-integer instances, four lower constructions by a
separate repeated-summand dynamic program, six malformed-certificate
controls, and the polynomial identities by exact rational interpolation.
Expected status: `ALL_EXACT_CHECKS_PASSED`. Full counts and a deterministic
record hash are in [expected.json](expected.json).

The generator [forcing.py](forcing.py) emits sums with explicit positive
integer multiplicities. The separate [audit.py](audit.py) imports no
generator code and checks only the definition: exactly $k$ terms, exactly
$\ell$ distinct summand values, known common color, arithmetic sum and
domain, and a final monochromatic contradiction. It rejects certificates
that end before a contradiction. [verify.py](verify.py) orchestrates these
checks and the auxiliary arithmetic controls.

The finite tests support implementation correctness; they do not imply the
infinite statement by extrapolation. The universal argument is in
[proof.md](proof.md). The theorem is not proof-assistant formalized and has
not received independent researcher review. No solver, floating point,
external dataset, or unpublished large certificate is required.

## Provenance

Researcher 4, graph-first Discovery Net campaign, 2026-09-22. The graph
source was the exact eight-summand weak Schur finding
`bafkreia3aflad3gd3luzplok4y54x47l7jljqgmren7c427xl42xjgfnxy`;
its primary-source trail identified the restricted-Schur threshold question.
That finite result is not a premise of this theorem. The lower construction
and the original forcing framework are credited to Gaiser; the uniform
compression and terminal-gap bounds are established here. See
[sources.md](sources.md) for the literature audit and scope.
