# Binary Gaussian coupling under two rigid component motions

For two fixed bounded component laws whose rigid images shorten every
cross distance, the [author proof](PROOF.md) produces **one Markov kernel
mapping both Gaussian-smoothed component laws to their images**. It holds
in every dimension and at every positive common variance, with arbitrary
unequal anchored norms. The same kernel works for every mixture weight of
these two fixed laws. Independent mathematical review is pending.

The proof orders every weighted overlap `integral min(alpha f_A,beta f_B)`.
Gaussian covariance interpolation cancels the norm drift exactly through
degree-one homogeneity; convex order then yields the common kernel. The
kernel may depend on the component laws and is not known to preserve
Lebesgue measure. This proves neither full Gaussian majorisation nor the
joint-superlevel comparison or a Kneser--Poulsen consequence.

For the accepted two-body contact frontier this signs every ray integral
of the actual joint-level difference. Its sign at each threshold pair,
and the anti-diagonal integrals needed for mixture hinges, remain open.
The distinction from the older universal-prior channel obstruction is
explicit in Section 5 of the proof.

From the repository root, using Python 3.11 or later (checked with
CPython 3.11.2; standard library only):

```sh
python3 probability/gaussian_two_component_binary_coupling/verify.py
python3 -O probability/gaussian_two_component_binary_coupling/verify.py
cd probability/gaussian_two_component_binary_coupling
sha256sum -c MANIFEST.sha256
```

Both Python commands print the JSON in [EXPECTED.json](EXPECTED.json),
with status `EXACT_BINARY_COUPLING_CONTROLS_PASS`. These are exact algebra
and finite-kernel controls, not computational substitutes for the analytic
proof. No large artifact or numerical integration is needed. See
[SOURCES.md](SOURCES.md) for primary literature and durable dependencies.
