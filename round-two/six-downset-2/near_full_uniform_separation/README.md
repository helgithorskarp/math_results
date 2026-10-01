# Uniform near-cube centered cap separation

Author **six-downset-2**, role **researcher**. For every integer **n>=16**,
no real centered capped H matrix on D(n,n-2) can have all noncomplementary
disjoint couplings with both set sizes at least3 equal to zero. Singleton,
two-set and complementary couplings remain unrestricted. Read
[PROOF.md](PROOF.md) for the precise definitions, hypotheses and proof.

Two rational rank-one upper duals cancel every real free complement
coordinate. Universal coefficient identities and a binomial moment bound
prove the negative sign for all n>=17; one exact rational check covers n16.
This extends only the negative clause of the credited
[finite separation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md).
It does not give an all-order cap construction or settle general H/I.
The author proof is ordinary and unformalized, with no independent review
claim. No solver or floating arithmetic is a proof input.

From this directory, run:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python -B verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python -B -O verify.py
```

The portable checker uses only the Python standard library; tested on
CPython3.12.14. Both commands report ok=true, uniform_n_at_least16,
symbolic_moment_domain n>=17, finite_boundary_n16, literal_order57,
controls4, and canonical result SHA256
`2ea6748b7a2ddf67adcaccceb234372440674c45bd3f263f5c57c7ffdba3e9d9`.

The **file-byte** SHA256 of the pre-existing frozen [expected.json](expected.json)
is `ca203a3c3256a8443b44c62d8a643873dc0344a0bbccc6cdbd68f7ea20c88c58`.
Normal and optimized final replays matched the frozen record and each other's
stdout:0.6858/0.9829seconds, measured peak RSS18076/22308KiB, one thread,
unchanged60second guards. Finite RREF checks at n6,7,16,17,20 and the literal
n6 affine control validate the code; they do not provide the unbounded sign
bridge. The affine literal control is not asserted to be PSD.

Source files:

- [certificate.py](certificate.py): direct affine completion, physical forms,
  closed rational dual profiles and scalar.
- [poly.py](poly.py): exact sparse two-variable coefficient arithmetic over Q.
- [verify.py](verify.py): universal identities, exact moments, all positive
  shift coefficients, separate RREF, literal loop/support/star/form checks
  and four corruption controls. Explicit exceptions survive Python optimization.
- [expected.json](expected.json): compact deterministic coefficients,
  boundary constant, hashes and test records; no full large matrix is stored.

Optional discovery derivation with SymPy1.14.0:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python -B derive_sympy.py
```

[derive_sympy.py](derive_sympy.py) operates over the characteristic0 rational
function field Q(n,x,T) and matches its P,Q against the portable checker.
It does not infer inequalities. This optional dependency is outside the
portable proof replay. No private ledger, credential, solver output, proof
corpus or large generated data is required or included.
