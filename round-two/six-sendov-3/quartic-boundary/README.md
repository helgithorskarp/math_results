# Sharp second-order degree-nine boundary surplus

Author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof; independent review is pending.

For a degree-nine polynomial with all original roots in the closed unit
disk, marked root $a$, and eight critical points counted with multiplicity,
write $F_p(a)=\sum|a-\zeta_j|^{-1}$. Put $c=\cos(\pi/9)$,
$C=8/3+1/(3(1+c))$ and

\[
 B_*=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2
     \in(-0.754160683222,-0.754160683221).
\]

The main result is

\[
 \lim_{r\uparrow1}\inf_{p,a:\,|a|=r}
 \frac{F_p(a)-8-C(1-r)}{(1-r)^2}=B_* .
\]

The proof covers arbitrary competitors with bounded above second-order
surplus, through a new real-energy rate estimate. Equality selects six
zero imaginary coordinates and one opposed imaginary pair at the leading
$\sqrt{1-r}$ scale, together with a unique real correction at scale $1-r$.
An explicit six-plus-pair derivative construction attains
$8+C(1-r)+B_*(1-r)^2+O((1-r)^3)$ with every original root strictly
inside the disk. Since $B_*<0$, the exact-$C$ straight-line boundary
inequality fails arbitrarily close to $r=1$.

Read [PROOF.md](PROOF.md) for the theorem, completeness and stability;
[LITERATURE.md](LITERATURE.md) records the prior inputs. The first-order
coefficient and reviewed concentration/bootstrap are credited prior results.
The full first-power endpoint, an effective annulus radius and the
inequality at exact coefficient $B_*$ remain open here.

## Reproduction

Use Python **3.11** standard library only (tested with 3.11.2), from
repository root:

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
      python3 -I -B round-two/six-sendov-3/quartic-boundary/verify.py

Expected:

    PASS: 69 exact checks; 6 mutations rejected.
    Complete record SHA256: d1ea22c0de70c3e9dc36bf5cfdeae9df4cbad6e463ecc79f2092d38e19da149a

The printed rational coefficient enclosure equals the interval above.
The normal and optimized Python runs agree, and missing, malformed and
altered fixtures fail under optimization. Generating a fixture uses
the --emit-fixture option; ordinary verification requires the complete
[expected.json](expected.json) to match every record.

The full generic balanced calculation has **536 derivative terms** and
**1110 anchored polynomial terms**. It covers arbitrary correction
coordinates through fourth order, rather than sampled profiles.
The explicit construction uses a separate cubic-field bivariate kernel
and exact quadratic Gaussian root arithmetic. It verifies the third-order
inward original-root correction from the defining derivative factors.
Rational bisection certifies all algebraic signs.

The checked run used about **4.1 seconds** and **25,000 KiB maximum RSS**
on the campaign machine, with one process and one thread. These timings
are descriptive. There is no solver, external package, imported data,
numerical root search or large certificate.

Finite algebra is checked by the author executable. The vector inequality,
uniform analytic remainders, compactness and all-root containment are
ordinary arguments in PROOF.md. They are not machine formalized and the
author checks are not independent mathematical review.
