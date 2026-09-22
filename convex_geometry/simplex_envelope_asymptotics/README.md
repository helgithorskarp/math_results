# Sharp simplex-envelope asymptotics

For the sharp unconditional projection constants with an n-simplex as
positive image, this package proves

$$
C_n\sim\kappa\,\frac{\beta^n}{\sqrt n},\qquad
\beta=\frac{2e^{r-1}}{r^2},\quad
\kappa=\frac{\beta\sqrt3}{r\sqrt{2\pi(20+9\sqrt5)}},\quad
r=\frac{\sqrt5-1}{2}.
$$

Thus β≈3.5737119568 and κ≈0.6307720727. The earlier theorem determined
only the nth-root rate. A separate theorem gives joint total variation
convergence of fixed coordinates and the cost slack in the associated
hyperplane section: independent coordinates with density proportional
to exp(−r(|x|−1)₊), independent of an exponential slack of rate r.

The written [proof](PROOF.md) handles the singular components in the
required local limit estimate. [EXACT_VOLUME.md](EXACT_VOLUME.md) gives
an exact finite formula, including C₄=6208/125 and C₅=103561/648.
The global arbitrary-image constant and the ℓq-ball conjecture remain
unresolved here. No effective convergence rate, historical priority,
formal verification, or independent review is claimed.

## Reproduce the exact corroboration

CPython 3.11.2, standard library only. From this directory:

~~~sh
python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

The checks take about seven seconds in the development environment.
They compare ten rational sections using active-coordinate integration
and direct halfspace geometry, check tilted moments in Q(r), reproduce
C₁ through C₁₂ exactly, and reject four malformed parameters.
The expected output hash is

~~~text
5df088219fbf1d21e11dda8eb7d0b8eb6d67eec333d241708e25f467dabea0ee
~~~

Finite arithmetic checks corroborate the normalization and implementation;
the written analysis proves the limits. The two volume algorithms are
[exact_section.py](exact_section.py) and [geometry_check.py](geometry_check.py).
See [EXPECTED.json](EXPECTED.json), [SOURCES.md](SOURCES.md), and
[SHA256SUMS](SHA256SUMS). No external data or package installation is needed.
