# Gaussian replica interaction

An author proof retains the interaction between iid added replicas to show

    B_(m+ell)/B_m >= (B_(m+1)/B_m)^[ell(m+ell-1)(m+1)/(m(m+ell))].

In particular B_4^4 B_2^5>=B_3^9. Exact scalar certificates turn this into
two unrestricted R3 Gaussian beta signs:

    b_(9,0)>=sqrt(2)d_2/10,
    b_(12,0)>=13 sqrt(2)d_2/1000.

They hold for every bounded-support law, contraction and positive variance,
strictly with any support distance loss. Independent review is pending.
Full Gaussian majorisation, complete later beta rows, the unrestricted
quartic/Hankel sign and new Kneser--Poulsen consequences remain unproved.

Read [PROOF.md](PROOF.md) and [SOURCES.md](SOURCES.md). Reproduce with
standard-library Python 3.11 or later:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Expected status: `REPLICA_INTERACTION_PASS`; 1376 positive rational Bernstein
coefficients, two subdivision algorithms agreeing entry by entry, eight
damaged-certificate rejections, and exact variance/constant controls.
[EXPECTED.json](EXPECTED.json) includes coefficient hashes and minima.

There is no floating sign test, solver, quadrature, external dataset, omitted
large certificate or installed-package dependency. Universal Jensen and
Gaussian integration arguments remain written mathematics.
