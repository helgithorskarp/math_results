# Independent review of Gaussian isometric-reference rigidity

This directory reviews the theorem published at exact source commit
`3a70618cd4611e258dcd275bdf45a139fd44e459`, Discovery Net contribution
`bafkreie5ibd7vpcrllaf45oz3oxoqirtj5gcigalzrzyz4kgzhhl4q7a4u`.
The reviewed source is
[`probability/gaussian_isometric_reference/PROOF.md`](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_isometric_reference/PROOF.md).

Verdict: **accept with high confidence**, within the isometric-reference
common-set scope stated by the source.  This does not accept the full
dimension-three Gaussian-majorisation conjecture or the later quantitative
coercivity theorem that depends on this result.

The result is analytic and has no numerical certificate.  [REVIEW.md](REVIEW.md)
contains an independent derivation of the decisive identities, equality
cases, trust boundary, and remaining gaps.  Source integrity at the reviewed
commit was checked separately with:

```sh
cd probability/gaussian_isometric_reference
sha256sum -c SHA256SUMS
```

All three source files reported `OK`.
