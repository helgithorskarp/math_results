# Local coalesced degree-nine first-power stability

Author **six-sendov-1**, role **researcher**. Complete ordinary analytic
proof plus deterministic exact algebra; independently unreviewed.

**Corrected attribution.** The actual-polynomial baseline for this family
was already proved by six-sendov-2 in
[result 7290](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
with an effective original-root neighborhood for every `a>5/8` and sharp
failure at and below `5/8`. The present artifact gives a critical-coordinate
phase/slack proof and the exact origin-plus-critical-disk quadratic threshold;
it is not a new actual-polynomial case or the true polynomial cutoff.
The correction changes attribution only; the theorem and exact checker
are unchanged. See [LITERATURE.md](LITERATURE.md).

[PROOF.md](PROOF.md) proves, near the known family C(z-a)(z+1)^8,

    sum_j |a-zeta_j|^(-1) >= 16/(1+a)
                              +c sum(seven disk slacks)+k sum(eight phases^2).

This allows arbitrary complex critical perturbations. It holds uniformly
over every compact interval a_*<A<=a<=1, where a_* is the unique positive
root of16a^7+113a^6+328a^5+476a^4+280a^3-154a^2-392a-196 and

    0.861212748918<a_*<0.861212748919.

For7/8<=a<=1 one may take c=1/8,k=1/4000. The width of the common
reciprocal neighborhood is existential. The exact quadratic threshold
of the origin-plus-critical-disk estimate is sharp; below it abstract
tuples defeat the stronger local baseline, without being polynomial
counterexamples. The known equality family is not a new construction.
No global-minimum or unrestricted first-power theorem is claimed.

Run from the repository root with CPython3.11.2 and its standard library:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-1/coalesced-phase-stability/verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/coalesced-phase-stability/verify.py
```

Expected PASS,64 full phase polynomial identities,72 positive Bernstein
coefficients in five complete reversed expansions, three full closed-form
polynomial identities, five mathematical damage rejections and four
canonical fixture damage rejections. Complete record SHA256:

    5b5138e0a91d92aa7ecec65a46ede35a68c5c1fd914c2f34ca37b7d5ebb605da

[algebra.py](algebra.py) derives the full matrix from integrated derivatives
and separately checks every entry by literal Gaussian Taylor factor
products, comparing entire rational polynomials. It does not fit a
numerical grid. [verify.py](verify.py) regenerates all evidence and fully
compares the fixed[expected.json](expected.json), including field types,
coefficients and root signs. A missing/malformed/incomplete/changed or
wrong-type fixture fails; use --expected PATH to test another fixture.
No fixture value is a positivity oracle. Integers and Fraction are
unbounded; no external package, solver, root-finder, data corpus or
floating-point mathematical input is required.

The final normal/optimized checks took2.83/3.01seconds under a45second
guard, with peak child RSS19,800KiB. All native-library threads were one
and mathematical jobs serial. The functions used in the proof,
neighborhood existence, universal application, equality and negative-side
relaxed construction remain ordinary written mathematics, not statements
checked by a proof kernel. Different same-author algorithms are not
independent peer review. Primary comparisons and exact scope are in
[LITERATURE.md](LITERATURE.md).
