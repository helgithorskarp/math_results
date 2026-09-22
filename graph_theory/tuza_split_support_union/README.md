# A support-union criterion for Tuza's conjecture on split graphs

Let `G` be a finite simple split graph with a specified clique part `C` of
order `k>=3`.  Let `U` be the union, inside `C`, of the neighborhoods of
the independent-side vertices that lie in a triangle, and put `u=|U|`.
This directory proves an exact, residue-sensitive sufficient condition on
`(k,u)` for Tuza's inequality `tau(G) <= 2 nu(G)`.

Write `p(k)=nu(K_k)`, whose classical exact value is

```text
(binom(k,2)-L(k))/3,
L(k)=0                 if k mod 6 is 1 or 3,
     4                 if k mod 6 is 5,
     k/2               if k mod 6 is 0 or 2,
     k/2+1             if k mod 6 is 4.
```

Define

```text
D(k) = -k^2+2k+8p(k),
u_*(k) = floor((k+sqrt(D(k)))/2).
```

**Theorem.** If `u <= u_*(k)`, then `tau(G) <= 2 nu(G)`.

The statement imposes no fixed bound on the number of distinct
independent-side neighborhoods and allows arbitrary multiplicities.  It is not a two-type theorem
and does not require a bound on the order of `G`.  Moreover

```text
u_*(k)/k -> (1+1/sqrt(3))/2 = 0.7886751345...
```

The proof uses two explicit universal witnesses.  A maximum triangle
packing of the clique gives `nu(G)>=p(k)`.  Put all of `U` on one side of
a clique cut, fill that side toward balance, and put every active
independent vertex on the other side.  Deleting the clique edges internal
to the two sides meets every triangle and costs

```text
binom(k,2) - max_{u<=ell<=k} ell(k-ell).
```

The quadratic inequality comparing these witnesses is equivalent to
`u<=u_*(k)`.  Thus the threshold is exact for this particular universal
certificate.  No assertion is made that graphs beyond the threshold fail
Tuza's conjecture, or that no stronger graph-dependent certificate exists.

## Reproduce

Use standard-library Python 3.10+; tested with CPython 3.11.2.

```bash
python3 verify.py
python3 construct.py 100 78
```

The verifier checks the residue formulas and both sides of the exact
threshold for every `3<=k<=20000` (and every `u` through `k=512`),
performs definition-level checks by enumerating every triangle in 1,344
generated small split graphs, and checks a deterministic set of large binary-sized
arithmetic inputs.  The finite checks audit the implementation; the
universal quantifiers rest on [PROOF.md](PROOF.md) and the classical exact
formula for `nu(K_k)`.

[SOURCES.md](SOURCES.md) records the primary literature and the scoped
status search.  This result has not been proof-assistant formalized or
independently reviewed at initial publication.
