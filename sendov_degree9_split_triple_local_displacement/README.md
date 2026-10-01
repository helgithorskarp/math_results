# Degree-nine split-triple local displacement stability

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary written author proof with exact rational continuous-domain
certificates; unformalized, independent review pending.

For the credited balanced angular functional J, consider

    theta=(1-alpha_1,1-alpha_2,1-alpha_3,-1,-1,-1,S/2+x,S/2-x),
    alpha_i>=0, S=sum alpha_i<=1/100, x>=0, 1/16<=u=x^2<=1/9.

The new result proves

    j(u)-J(theta)>=200S,
    J_*-J(theta)>=200S+450(u-u_*)^2,
    dist(theta/sqrt(mu_2),O_*)^2<=(J_*-J(theta))/40.

The scalar j,u_*,J_* and the scalar curvature coefficient 450 are
credited inputs. Equality J=J_* occurs only at the credited optimizer
multiset. One unit triple stays fixed; the other three deficits vary
independently and can produce six actual slope values. All collisions,
permutations and reflections are included. This larger restricted tube
complements the previous unrestricted local tube; it does not establish
the whole six-level maximum or the degree-nine first-power endpoint.

[PROOF.md](PROOF.md) proves the ordinary matrix and analytic steps and
specifies the complete polynomial certificate.
[LITERATURE.md](LITERATURE.md) distinguishes inputs and complementary work.

## Reproduce

CPython 3.11.2, standard library only, was used. From this directory run
sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Each must report `status: PASS`, **30,332 checks**, **21,120 bound signs**,
**8,512 determinant signs**, **seven full defining-matrix controls**, and
canonical regenerated-record SHA256

    b0e62075b18a14bcb1b42e0e5d4b7853251a0a7764607390ca4cb3f9213fcddc

Every polynomial and every Bernstein coefficient is rebuilt exactly.
Both complete inverse Bernstein conversions are checked. The seven
full-matrix controls recover Psi by a separate symmetric-commutant
projection with multiplicities intact. No solver, floating-point proof
input, network input, private module or large certificate is required.

Both commands passed in 14.871 and 15.635 seconds, respectively. Across
the sequential author validation the maximum child RSS was 44,380 KiB.
Four altered or absent manifests (a sign summary, the deficit domain, a
defining Psi control and the missing file) were rejected under optimization.
Runtime varies with host load; one CPU mathematical job at a time suffices
within the unchanged two-GiB scope, with all native threads one.

`expected.json` is required and compared in full. `--manifest PATH` checks
an alternative manifest; an absent or altered manifest must fail even
under `-O`. `--write-manifest PATH` is an explicit author-generation mode,
not verification. Ordinary arguments in PROOF.md, exact-arithmetic Python
and the implementation are the trust boundary; this is not a proof-assistant
formalization or independent review.
