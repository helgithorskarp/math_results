# Degree-nine first-power annulus and unequal-light stability

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.

For a degree-nine polynomial with roots in the closed unit disk and
critical multiset $\{H^6,L_1,L_2\}$, if a marked zero $a$ satisfies
$$
 |a-L_1|=|a-L_2|,\qquad |a|\ge43750/46643\approx0.93797569,
$$
the complete author proof establishes
$$
 \sum_{\mathrm{critical}\ \zeta}|a-\zeta|^{-1}\ge8.
$$
It is strict for $|a|<1$; equality is only the boundary binomial
$C(z^9-a^9)$. Multiplicities count, coincidences are allowed and
a critical collision contributes infinity. Heavy phase, radial order
and light-pair center are unrestricted in this annulus.

The new [stability theorem](STABILITY.md) allows unequal light distances
when their reciprocal magnitudes differ by at most
$10^{-40}(1-|a|)^2$. It uses a uniform normalized origin margin
$|I|^2-r^{12}s^4\ge10^{-32}(1-b)^2$ derived from the complete
endpoint coefficient support. Both constants are very conservative.

Read [PROOF.md](PROOF.md) for the complete reduction and
[LITERATURE.md](LITERATURE.md) for the three imported premises,
their review scopes, earlier annuli and precise limitations.
This is an **unformalized exact computer-assisted ordinary author
proof**. Independent review of this new result is pending.
Unrestricted degree-nine first power remains outside the claim.

## Reproduce

CPython3.11+, standard library only; tested with CPython3.11.2.
From the repository root:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B sendov_degree9_equal_light_annulus_first_power/verify.py
~~~

The command checks the core identities and mandatory fixture, then
executes all18 cases in **sequential fresh processes**, with a180-second
timeout for each. A timeout or missing case is an incomplete check.
No such event establishes a mathematical exclusion.
Expected final JSON includes verified=true, complete_cases=18,
complete_tensor_signs=4884500 and full_inverse_identities=18.

For compact core verification, including the whole reference comparison:

~~~sh
python3 -I -B -O sendov_degree9_equal_light_annulus_first_power/verify.py --core-only
~~~

To regenerate an individual complete case:

~~~sh
python3 -I -B sendov_degree9_equal_light_annulus_first_power/verify.py --case G4-nearer
~~~

The18 case names are E1,E2,E3,G1,...,G6, each suffixed -nearer or
-farther. Their union is the complete finite partition.
Individual cases verify their whole mapped polynomial, all tensor
signs, the entire inverse identity,18 exact cube controls and the
full case fixture. E3 and G6 additionally check the strict-support
predicates used in the proof. A selected case alone is not the theorem.

The fixture [expected.json](expected.json) is mandatory. Use --check PATH
only to select a different complete fixture, which is compared literally;
missing or changed fixtures fail. The checker uses explicit exceptions
retained under optimized Python. The documented -B commands create no
tensor files or caches.
All coefficients are regenerated from this directory's compact source.

## What is checked

The core compares complete moment, numerator, norm and angular basis
identities,324 scalar Gaussian integral points with648 signed norms,
their Gram products,42 integer/Fraction evaluation comparisons,
two independently integrated communication examples that distinguish
the exponent16 from18, and the exact annulus cutoff product.
Its E1-nearer reference comparison checks14956 monomials and28120
tensor entries. A damaged positive tensor coefficient is rejected.

The stability derivation adds73 complete one-variable signs and a whole
basis identity, exact rational constant gates and72 direct unequal-radius
integral/mean controls. Its positive u-index0..70 support is verified in
each full G6 run. Arithmetic on compact endpoint metadata alone does not
regenerate those tensors; core-only and selected-case commands remain
partial checks.

The universal sign cover has4884500 exact nonnegative coefficients.
Its18 whole inverse identities are independent of the forward
Bernstein weights. No floating-point sign, external solver,
random search, large proof corpus or previous checkout is required.
The case hashes are regression metadata rather than a substitute for
regeneration and exact proof checks.

The written reductions, imported mathematical premises, coverage,
basis soundness and equality argument remain outside a formal kernel.
Author checks do not constitute independent peer review.

## Resources and artifacts

Verification uses one CPU process at a time, all native threads1.
The source was developed and checked within1CPU/2GiB limits. The final
complete standalone verification, including the stability derivation,
took986.791 seconds and its maximum child peak was463024KiB (about452MiB), under all180-second
case caps. The prior complete integer cases used at most457160KiB; the slower G4
rational baseline used1376216KiB. Those baseline measurements are
distinct from the fresh standalone check. Runtime and peak memory
for the current command are printed in its final JSON; individual
cases are capped at180 seconds and require no resource escalation.

The complete fixture, source, proof and attribution are compact.
Large tensors, private ledgers, keys, logs and scratch checkpoints
are not publication artifacts. [SHA256SUMS](SHA256SUMS) records the
source bytes. Reader-facing links use the repository's main branch;
the separately verified publication commit is recorded in the graph
claim and durable campaign report.
