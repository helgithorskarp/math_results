# An effective margin for actual Gaussian-regularized contacts

An author proof transfers R3's accepted bounded-input effective mean-loss theorem
to the unbounded inputs used by the ordered-contact reduction. The same
global contraction acts **after** input Gaussian regularization. Independent
review of this transfer is pending; the R3 dependency was accepted at graph6432.

At output Gaussian variance one, write X=U+sqrt(beta)Z, with U centered,
|U|<=L, Z standard normal and independent of U. Let L>=1 and b>=20 be
integers, 2^-b<=beta<=2^-20, and let F be any global 1-Lipschitz map.
Set d=E[|X-X'|^2-|F(X)-F(X')|^2] and M=2^20(L^2+b+1).

If 0<d<=2^-M, then for every 0<v<=(4pi/3)L^3,

    L_((F#law(X))*gamma_1)(v)-L_(law(X)*gamma_1)(v)
       >= (2pi)^(-3/2) v d^(513/512)/8 > 0.

Thus a nontrivial actual contact in this volume and smoothing regime must
have d>2^-M. There is no displacement bound, atom-count bound, minimum prior
mass, or unchecked tail-budget premise. The cutoff is extremely conservative.
Arbitrary smoothing ratios, all volumes, general positive loss, and the full
dimension-three conjecture remain open. No new KP consequence is claimed.

- [Proof and rescaling](PROOF.md)
- [Dependencies and trust boundary](SOURCES.md)
- [Exact exponent and finite algebra checks](verify.py)

From this directory, using standard-library CPython 3.11 or later:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Both runs must print `REGULARIZED_CONTACT_MARGIN_PASS`. The checker verifies
the universal affine exponent certificates, pinned inputs, Gaussian moment
constants and finite conditional-loss algebra. It does not integrate profiles
or replace the written analytic theorem. No heavy computation or large
certificate is needed.
