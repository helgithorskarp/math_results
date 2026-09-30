# Strict local but nonglobal degree-nine energy minima

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary written author proof; independent review is pending.

For a degree-nine polynomial with simple fixed marked root `a`, eight
other roots in the closed unit disk, and all multiplicities counted, set

```text
v=1/(1+a), E=sum_other_roots |(a-z_j)^(-1)-v|^2,
F=sum_critical_points |a-zeta|^(-1).
```

An explicit unit-circle family of multiplicities **1+3+4** has a smaller
`F` than the previously reviewed stationary singleton/seven branch at
exactly the same sufficiently small energy, uniformly for
`0<=a<=301769/500000`. For every compact
`J subset((10 sqrt(2198)-225)/404, 301769/500000]`, that stationary branch
remains a **strict local but nonglobal minimum** under all eight
original-root closed-disk motions, modulo root permutation and scalar
factors. All energy thresholds remain existential.

The competitor is

```text
Q_(a,s)(z)=(z-a)(z+exp(7 i s))
                 (z+exp(-41 i s/40))^3(z+exp(-157 i s/160))^4.
```

Its exact small positive energy inverse gives `Q_(a,e)`. With `P_(a,e)`
denoting the entire actual nonlinear-mean stationary branch,

```text
F(P_(a,e))-F(Q_(a,e)) >= gamma e^2 > 0,
gamma=723014343439697853/843420355826745088000000000000.
```

This separates local stability from global optimality below `5/8`.
It supplies neither an unrestricted first-power counterexample nor a
classification of the competing global minima or all transition radii.
The earlier global theorem on `[5/8,1]` and the independently reviewed
local theorem retain their stated scopes.

Read [PROOF.md](PROOF.md) for the quantified statements, the complete
active-space spectral formula, original residual-cubic analytic bridge,
exact-energy elimination and uniform dominance argument. Read
[LITERATURE.md](LITERATURE.md) for primary literature, exact dependencies,
method attribution and review limits.

## Reproduce the exact certificate

From this directory, with **CPython 3.11**, standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -O -B verify.py
```

Both commands regenerate and compare every record in the required
[expected.json](expected.json); there is no downloaded input, solver,
floating eigenvalue or numerical sign. The normal output reports:

```text
identity_count: 67
strict_sign_count: 10
complete_record_count: 96
full_matrix_profile_count: 7
direct_original_cubic_radius_count: 3
corruption_control_count: 7
records_sha256:
b6c91a5300b2fd6bde40a978215bf677b08f79644f138ca9ed5cc46b9c2b3e25
```

The fixture-file SHA256 is
`13aa078dc7681647905c1a80989d849b095d2dd7b5da969d0fc0f07dc9d51caf`.
The checker-file SHA256 is
`e66d95a92ae281b5cb9801b8d34dc2cc17a53fe659e313b6a7e587f4cb87e296`.
Observed CPython 3.11.2 times were 3.031 seconds normally and 3.128 seconds
under optimization; the validation harness's peak child RSS was 22876 KiB.
These measurements do not assert uniform performance on other systems.

The certificate uses three different routes:

* Untruncated rational polynomial identities prove the parametric moments,
  active characteristic polynomial, positive squared gap and barrier to
  the proposed stronger Gram slope.
* Full rational eight-by-eight symmetric-commutant projection checks
  spectral pinching on seven profiles, including all three merged-label
  controls. The two-active-eigenvalue formula holds for every real profile
  parameter by the written polynomial argument, not by sampling.
* Direct differentiation of the actual degree-nine polynomial, physical
  residual cubic, reciprocal transformation and exact branch recursion in
  `Q(sqrt(1256647))[i][s]/(s^6)` reproduce the true fourth-order objective
  and exact-energy coefficient at `a=0,301769/500000,5/8`. Both active
  branches, the far branch and all five within-block critical
  multiplicities are retained.

Seven corruption controls reject omission of energy elimination,
within-block multiplicities and spectral pinching, a wrong active gap,
wrong local stiffness, the false strengthened Gram slope and a changed
complete-record digest. Separate harness runs confirmed that missing,
malformed and altered full fixtures fail under `-O`; runtime guards do
not rely on Python assertions.

## Trust boundary

The exact code proves its algebraic identities and signs. The analytic
implicit-function theorem, uniform energy inversion, remainder bounds,
compactness and credited all-disk local theorem are ordinary written
mathematics in the proof and cited sources, outside a formal kernel.
The three direct radius checks do not prove a continuous-radius statement;
that coverage follows from the explicit positive gap, monotonicity and
analytic compactness argument. Author checks and baseline replay are
validation, not independent review of this new result.

The compact fixture contains the complete 96 records. No large corpus,
private state or exploratory computation is required or distributed.
