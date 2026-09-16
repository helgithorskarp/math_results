# B292/V214 negative-trace nonforest admission stop

The requested construction gate is incompatible with the existing exact
geometry. A quadratic unit rotation over E=Q(i sqrt(3),i sqrt(11)) with
negative local relative trace cannot support a simple alternating unit
cycle on distinct physical points of P union (uQ+h), P,Q contained in E.
Thus its private cross interface is a forest.

A four-cycle forces the relative trace to be zero. Any longer alternating
cycle forces the isometry to preserve E. Neither permits a quadratic
negative-trace rotation. [PROOF.md](PROOF.md) gives the short deduction and
a direct valuation proof for translations in E(u).

For the connected B292 and V214 sources, the 506-label point budget fits,
but the requested negative-trace AND nonforest conjunction has no physical
placement. No graph was constructed or passed to a colouring solver. This
is an admission correction, not a sub-509 candidate, an ordinary non-four
result, or a theorem colouring all remaining negative-trace forests.
No second placement or forest substitute was attempted.

The committed cycle theorem is h2595, artifact
`bafkreibe2izkrcivsfl3rdybfjwqjwby7g24ebbtbg7xiuvsbcbeoat2pa`.
Its four-cycle dependency is h2531, independently accepted at h2535.
The h2595 theorem has no direct review or objection in the queried committed
neighbourhood. We do not relabel it independently reviewed. The separate
valuation derivation here has author checks only.

Run with Python 3.11 or later, standard library only:

```sh
python3 -B check_identities.py
python3 -O -B check_identities.py
sha256sum -c SHA256SUMS
```

The first two commands check their output against `EXPECTED.json` and print
it. `SOURCE_PINS.json` records immutable source hashes and verified remote
links. The proof does not import executable code from those sources.
The symbolic checks supplement the mathematical argument; they do not
certify the geometry of a new physical support.

The sole campaign endpoint remains a complete strict plane unit-distance
graph on at most 508 points with a proper five-word and replayable ordinary
non-four evidence. This note makes no progress claim toward that order.
