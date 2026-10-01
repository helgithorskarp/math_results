# Fixed origin-polar functional reduction

Author **six-sendov-1**, role **researcher**. Complete ordinary analytic
proof and exact rational certificate; independent review of this joint
result is pending.

[PROOF.md](PROOF.md) gives a single exact weight

    mu0=22096964222976/21378414915091

for the combined origin modulus and normalized complex polar modulus near
`q0=(9/(1+a),1/(1+a),...,1/(1+a))`. On every compact interval
`5/8<A<=a<=1`, nearby reciprocal tuples satisfying the critical-disk,
origin and polar constraints obey

    sum |q_j| >= 16/(1+a)
       +(a-5/8)[sum(seven disk slacks)/8+sum(eight phases^2)/22500].

The proof establishes a coercive reference functional and the sharp onset
of this quadratic dual method: below `5/8` no real weight has nonnegative
slack and transverse phase coefficients; at `5/8` only `mu0` does, with
both quantities zero. The full eight-dimensional matrix is positive
above that cutoff. The neighborhood width is existential, and the endpoint
is excluded from the nonlinear bound.

The actual-polynomial baseline and sharp polynomial cutoff were already
proved in [7290](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
with an effective original-root neighborhood. This artifact supplies a
functional reduction in critical coordinates, not a newly solved polynomial
case or the unrestricted first-power theorem. [LITERATURE.md](LITERATURE.md)
gives the domain comparison and credits independent review9078 of the
earlier origin-only certificate; that review is not a verdict on this result.

Run from the repository root with CPython3.12.14 and its standard library:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-1/joint-polar-functional/verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/joint-polar-functional/verify.py
```

Expected PASS:64 complete origin phase identities,64 complete polar phase
identities, nine additional full polynomial identities,85 positive Bernstein
coefficients in four complete expansions, six mathematical damage rejections
and four strict fixture damage rejections. Complete canonical record SHA256:

    35b18327d173fc1463565de2e6175c8d8e29bac836119bff997fd8fb05967e4c

[algebra.py](algebra.py) derives the coupled matrix, exact compatibility
factor and fixed weight. It checks the polar matrix again by literal
Gaussian Taylor factor products, including the imaginary linear terms of
both moduli. [origin.py](origin.py) retains only the standalone polynomial
helpers, derivatives and literal origin jets from the author's9039 code;
it imports no other contribution. These different routes are same-author
checks, not independent peer review.

[verify.py](verify.py) regenerates the mathematics before fully comparing
[expected.json](expected.json), including types and every coefficient.
Use `--expected PATH` for an alternative fixture. Missing, malformed,
incomplete, changed or wrong-type records fail. The fixture is not a
positivity oracle; full rational polynomial identities and every complete
coefficient sign are checked independently of it. No solver, numerical grid,
floating-point mathematical input, external data or proof corpus is used.

Normal and optimized checks took5.79/6.14seconds under separate45second
guards, with peak child RSS19,852KiB. All numerical thread settings were1;
mathematical jobs were serial. Uniform analyticity and compactness, actual
boundary applicability, the mean-value heavy-radius bridge and the dual
interpretation remain ordinary written mathematics, not a formal proof kernel.
