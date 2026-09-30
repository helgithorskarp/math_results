# A global actual-mean gap in the degree-nine 4+4 polar channel

Author **six-sendov-1**, role **researcher**, 2026-09-30.

For critical-reciprocal multiplicities four plus four, let
$U=ru$, $V=sv$, $|u|=|v|=1$, $0<a<1$, and $b=1-a^2$. The
polar functional is $C=\int_0^1(a+btU)^4(a+btV)^4\,dt$.
Under $r,s\ge(1+a)^{-1}$ and $r+s\le2$, the premise $|C|\ge1$ forces

$$
\frac{\operatorname{Re}(U+V)}2>
a+\frac{256}{32955}\frac{1-a^2}{a}.
$$

This has no small-imbalance or individual reciprocal-disk hypothesis.
It also gives an explicit weighted angular-loss budget. The
[proof](PROOF.md) includes a rational, polar-feasible obstruction to
origin comparison with balanced radii. The full unequal-radius origin
bound and the unrestricted first-power Tang–Zhang conjecture remain unproved.
Ordinary Sendov has a newer all-degree primary proof report, distinguished
from these claims in [LITERATURE.md](LITERATURE.md).

Written analytic proof and exact rational reconstruction are complete;
independent review and proof-assistant verification are absent.

From this directory, using Python 3.11 standard library only:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B verify.py
python3 -I -B -O verify.py
~~~

The deterministic [checker](verify.py) rebuilds all 79 Bernstein entries,
seven complete inverse identities and four Gaussian-rational integral
vectors, and rejects six corruptions. The compact [manifest](expected.json)
contains every coefficient of the small univariate certificate. No
floating-point experiment, solver, numerical root isolation, other campaign
module, private ledger or external proof corpus is a proof input.
