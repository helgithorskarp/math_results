# Collapsed cutoff: the complete balanced angular quartic coefficient

Author: **six-sendov-2**, role **researcher**.

For n=m+1>=4, fix the marked root at a=(m+2)/(2m) and move the other
m roots from -1 along balanced boundary angles. This source proves the
complete fourth-order coefficient of the critical reciprocal sum:

$$F=\frac{2m}{1+a}-K_m(\theta)E^2+o(E^2),$$

$$K_m=\frac{(m+2)(3m+2)^3}{256m^7}
\left[m(m^2-4m-4)\frac{\sum\theta_j^4}{(\sum\theta_j^2)^2}
+(13m+18)-9(m+2)\eta\right].$$

The invariant eta is the squared concentration of the coupling vector's
weights in the distinct eigenspaces of the Hermitian angular compression.
[PROOF.md](PROOF.md) defines it precisely, handles repeated eigenvalues
and proves continuity and a uniform remainder on the balanced sphere.
A fourth-moment-only formula would fail the published moving-pair check.

For degree nine, the maximum angular coefficient is attained and lies in

$$\left[\frac{560235}{8388608},
\frac{10985}{33554432}(116+28\sqrt{10})\right].$$

The relative width is below **0.267%**. Every nonzero balanced direction
has coefficient at least 164775/8388608, so the cutoff has a strict
quartic deficit throughout this angular slice. The exact optimizer and
an optimal full stability basin remain unresolved; inward disk motions
and nonlinear mean phase have not been reduced to this slice.

Status: complete ordinary author proof and exact symbolic validation;
independent review is pending, with the spectral/analytic bridges
unformalized. [LITERATURE.md](LITERATURE.md) compares the statement with
the quadratic theorem, classical companion matrices, prior local results
and the complementary phase lane. This does not prove the unrestricted
first-power endpoint or claim a new ordinary Sendov proof.

Run from repository root with Python 3.11 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_angular_quartic/verify.py
~~~

Expected: **46 exact symbolic checks and five rejected mutations**.
The checker enumerates ordered contour words, multiplies free block
matrices, contracts formal power sums with the dimension left symbolic,
and checks both previous all-degree profile formulas and the new bound.
Normal and optimized outputs agree with [expected.json](expected.json).
[algebra.py](algebra.py) contains the author's reused exact arithmetic;
no external data, numerical root solving, floating-point proof input or
solver is required. The checker does not independently certify the
written uniform spectral bridge.
