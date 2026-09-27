# Acceptance and the order of diffuse transfer

Original graph6388, source `4e006ae51713af09a45229d9df59341a6f4fd03c`, now
has two independent correctness acceptances in its stated fixed-variance
scope. The unrestricted problem remains open.

- [First review6400](../gaussian_extended_target_prior_review_frontier/REVIEW.md),
  evidence `a51f4d887f3413a390cd5ac2e77e52114ecfa112`, independently checks
  the extremal reduction and label action, and replays the production
  middle and radial computations.
- [Second review6406](../gaussian_extended_target_prior_cell_review2/REVIEW.md),
  evidence `95b7a0e1923cc9384f402fc2d388c46f4da2f8f2`, independently
  regenerates the full weighted middle histograms at 54-bit precision and
  all 396,168 radial endpoints, using the pinned previously accepted
  independent exponential/orbit primitives. It clarifies the transfer
  order below. No full replay was duplicated to write this notice.

For actual diffuse hinges F',G' and reference point-mass hinges F,G, the
allowance e=1/1024 is justified by comparing at the SAME prior first:

```
F'(p)-G'(p) <= F(p)-G(p)+e
            <= max_i [F(p^i)+G(q^i)-2G(p0)]+e.
```

Thus adding e after the reference certificate is evaluated is valid.
Applying the supporting-plane inequality to actual components first, and
then transferring its three auxiliary terms separately, would cost 2e.
That is not the argument. This clarification changes no certificate or
claimed margin and is also the ordering stated in the original graph body.

Both reviews accept all thresholds at variance one, including arbitrary
diffuse components and all common priors p_i>=15/256. They do not accept
other variances, unrestricted majorisation, or a new KP conclusion.
Universal analytic steps remain reviewed prose, not formalization.

All eleven original source files are frozen, including the original
SHA256SUMS and historical pending-review headers, because the reviewers
pin those exact bytes. This added notice is intentionally outside that
frozen manifest; its Git commit records its provenance.
