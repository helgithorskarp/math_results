# Exact residual interface after the h4085 closure

The requested real-root and simultaneous thirteen-failure bridge is complete.
The h4071 list of 800 systems has exactly 1,022 real embeddings.  After exact
alignment and colour-word filtering, 15 injective algebraic components with
48 real embeddings remain.  They occur at representative pair indices

```
5, 6, 20, 30, 33, 36, 83, 85, 101, 109, 115, 194, 322, 347, 360.
```

For each, read the `outcome:"survivor"` component in
`certificate.json`.  Its `polynomial` is in increasing powers of `t`, its
`intervals` select all real embeddings, and the containing pair row gives
`shear`, `relation_a`, and `relation_b`, also in increasing powers.  Reconstruct

```
t = unique root in interval,
y = -relation_b(t)/relation_a(t),
x = t - shear*y,
u = phi(x), v = phi(y).
```

All 48 embeddings are certified nonalignment and injective, so every physical
point set has order 343.  Each survivor component's only identically vanishing
event factors are its two listed pair factors.  The whole architecture now has
at most 48 residual classes relative to the original thirteen-word cover,
although symmetry stabilizers or cross-pair coincidences may reduce this
further.

The final refresh found HN-2's h4085 closure: its stronger 62-word certificate
already proves every one of these embeddings four-colourable and leaves zero
unresolved classes.  Consequently no candidate reconstruction or chromatic
work is requested from this handoff, and the architecture is retired.  The
present data is a complementary exact parameter audit that identifies
precisely where the earlier thirteen words were insufficient.  This internal
certificate is not a reviewer-1 verdict.

HN-2's internal replay found and corrected a root-interval decoder weakness:
duplicate singleton roots passed the old endpoint-order test.  All 1,022
intervals in this certificate were already distinct within their components.
Use the corrected `verify.py` and its duplicate-singleton control for future
certificate replays; the certificate and architecture decision are unchanged.
The follow-up receipt is `HN2_REPLAY.json`.  No candidate work is reopened.
