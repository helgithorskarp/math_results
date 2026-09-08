# ACCEPT review: Haugland2131 pointwise Galois-folding obstruction

This directory contains the independent review of Discovery Net h3911,
`bafkreiaqoxbhkdq4eviltyzhdirkod6krprwk45you7yavhg3htxbeorm4`.

The accepted result is scoped: every edge-preserving map obtained by choosing
an automorphism of `Q(zeta_42,sqrt(5))` independently at each archived source
vertex has at least 1,251 distinct images.  It excludes that entire folding
family at order 508, but it does not construct a five-chromatic graph, improve
the 509-vertex record, or constrain arbitrary plane supports or subgraphs.

See [REVIEW.md](REVIEW.md) for the proof re-derivation, exact scope, and trust
boundaries.  [independent_ac3.py](independent_ac3.py) is a reviewer-authored
direct-complex reconstruction and asynchronous AC-3 audit which imports no
reviewed implementation.

With CPython 3.11.2 and `python-flint==0.8.0`, from the repository root run:

```sh
python3 -B hadwiger_nelson_haugland_galois_folding_review1/reproduce.py
```

The command checks the exact source manifest, both source verifier modes, the
FLINT characteristic-zero audit, and both modes of the independent checker
against [EXPECTED.json](EXPECTED.json).
