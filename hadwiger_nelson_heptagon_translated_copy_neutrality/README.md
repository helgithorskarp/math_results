# A one-point heptagon interaction has neutral complete component relation

Take Haugland's exact 21-point heptagon motif `H`, choose one motif point
`h_0`, and rotate a second copy through `-2*pi/7` about `h_0`.  Exact
collision merging and a complete unit-distance scan give a **41-point,
105-edge** strict plane unit-distance graph.  The copies share exactly
`h_0`; beyond their 84 factor-edge images there are 21 genuine closing
unit edges.

Despite those contacts, the complete unrestricted component relation is
neutral: **every proper four-colouring of either retained component extends
to the full graph**.  Up to colour renaming, all 327,180 colourings are
enumerated and extended in each direction.  Every physical nonedge also admits both equal and
different endpoint colours.  The graph is exactly four-chromatic.

This was the frozen exact preflight required before any wider component
cohort.  It fails the positive-signal gate and retires this architecture:
there is no basis here for adding rotations, copies, collars or a host.  The
result is a restricted physical construction exclusion, not a five-chromatic
graph and not progress below the 509-vertex record.

## Reproduce

CPython 3.11 or later and the standard library suffice.  From the repository
root, with assertions enabled or disabled:

```bash
python3 -B hadwiger_nelson_heptagon_translated_copy_neutrality/verify.py --check-expected
python3 -O -B hadwiger_nelson_heptagon_translated_copy_neutrality/verify.py --check-expected
python3 -B hadwiger_nelson_heptagon_translated_copy_neutrality/audit.py --check-expected
python3 -B hadwiger_nelson_heptagon_translated_copy_neutrality/controls.py
```

The primary verifier uses `Q(t)` for `t=exp(pi*i/21)`.  The audit imports no
primary code and instead uses `Q(zeta_7,omega_6)`.  Both reconstruct the
coordinates, exact collision quotient and all 105 physical edges, then use
different component-pattern and extension orders.  The controls compare the
42 formal coordinates across bases and exhaust 7,775 small pinned-colouring
queries against literal brute force.  See [PROOF.md](PROOF.md) for the exact
definitions and argument.

The checkers generate their 654,360 projection-extension witnesses in memory
one at a time and commit only stable hashes.  No SAT solver, floating-point distance
predicate, omitted negative trace or external data file is used.  The two
implementations and controls are author-side validation, not independent
peer review or proof-assistant formalization.

The motif is from Section 2 of
[Haugland's manuscript](https://arxiv.org/html/2608.04542v4).  The current
published comparison remains Parts's
[509-vertex, 2,442-edge graph](https://arxiv.org/abs/2010.12665).  Only the
motif coordinate formula is imported; neither paper supplies this finite
relation computation.  No literature-priority claim is made.
