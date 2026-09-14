# Exact pair-neutrality of the aligned EI17--Moser incidence sum

Let `E` be the exact 17-point triangle-free four-chromatic
Exoo--Ismailescu realization certified in the sibling
[`hadwiger_nelson_ei17_common_pair`](../hadwiger_nelson_ei17_common_pair/README.md)
package, and let `M` be the standard seven-point Moser spindle. This package
decides the complete unrestricted two-terminal four-colour relation of the
single frozen physical support

```text
S = E + M = {e + m : e in E, m in M}.
```

After exact collision merging, `S` has **111 distinct plane points** and
**380 complete strict unit edges**. Its chromatic number is exactly **four**.
For every two distinct physical vertices, some proper four-colouring assigns
them different colours. For every nonunit pair, some proper four-colouring
assigns them the same colour. Therefore every two-terminal relation is exactly
the relation already imposed by the bare terminal graph.

This closes a concrete candidate for a small forced-equal half: the source has
no forced-equal pair at any separation. No spindle composition is generated,
and there is no five-chromatic graph or improvement on the 509-point record.
The result is a restricted exact construction failure, not a lower bound for
arbitrary plane unit-distance graphs.

## Frozen exact support

Write

```text
omega = (1+i*sqrt(3))/2,
r     = (5+i*sqrt(11))/6,
M     = (0,1,omega,1+omega,r,r*omega,r*(1+omega)).
```

The EI17 points are the unique root in the rational box certified by the
sibling package. The source equations, root box and exact pinned coordinates
are rerun and hash-checked here. No displayed decimal is treated as an exact
coordinate.

There are 119 formal sum addresses. Four exact EI17 differences equal
`(1,0)`:

```text
e9-e1 = e11-e2 = e15-e5 = e16-e10 = (1,0).
```

The proof uses three nondegenerate unit rhombi and the pinned edge, not the
decimal midpoint. Since both `m1-m0` and `m3-m2` equal `(1,0)`, these identities
give exactly eight two-address collision classes. Rational outward bounds
exclude every other collision.

The inherited quotient has 378 unit edges. Two additional physical unit
contacts occur, between `e0+m1` and `e1+m0`, and between `e0+m3` and `e1+m2`.
They are exact: a checked telescope of six unit-rhombus identities gives

```text
e0 + (e16-e10) - e1 = e14-e6,
```

and `(6,14)` is an EI17 unit edge. The checker reconstructs those contacts and
uses exact rational error bounds on every remaining physical pair to exclude
any further collision or unit edge. Thus the graph is the complete strict
unit-distance graph of the defined point set; it is not merely an abstract
product or an edge-subgraph.

## Complete two-terminal certificate

The compact certificate contains 34 proper four-colour words of length 111.
The independent verifier checks all 12,920 word-edge inequalities and then
all physical pairs against the full word family. It covers

| Request | Count | Result |
| --- | ---: | --- |
| distinct pair assigned different colours | 6,105 | all witnessed |
| nonunit pair assigned equal colours | 5,725 | all witnessed |
| total canonical requests | 11,830 | all witnessed |

Colour renaming turns these canonical patterns into every labelled feasible
two-terminal assignment. Unit pairs can only differ in a proper colouring,
while nonunit pairs admit both patterns, proving neutrality.

Every fixed EI17 translate contains an injective Moser-spindle fibre. The
verifier exhausts all `3^7=2,187` ternary words on that fibre and rejects each,
while the saved words prove four-colourability. Hence the physical graph has
chromatic number exactly four.

## Reproduce

From the repository root, using CPython 3.11 or later and only the standard
library:

```bash
python3 -B hadwiger_nelson_ei17_moser_pair_neutrality/verify.py --check-expected
python3 -O -B hadwiger_nelson_ei17_moser_pair_neutrality/verify.py --check-expected
python3 -B hadwiger_nelson_ei17_moser_pair_neutrality/controls.py
(cd hadwiger_nelson_ei17_moser_pair_neutrality && sha256sum -c SHA256SUMS)
```

To regenerate the positive certificate at a fresh path:

```bash
python3 -B hadwiger_nelson_ei17_moser_pair_neutrality/produce.py \
  --out /tmp/ei17-moser-certificate.json
cmp /tmp/ei17-moser-certificate.json \
  hadwiger_nelson_ei17_moser_pair_neutrality/certificate.json
```

The producer uses deterministic DSATUR search and the fixed-denominator
interval model. Solver soundness is not a proof premise. The independent
verifier imports neither producer nor model code; it uses rational midpoint
error estimates, reconstructs the quotient and all edges, and checks the
positive words directly. Five damaged-certificate controls are rejected.

## Record-facing consequence and scope

If a four-colourable physical graph on `n` points forced a nonunit pair
`a,b` equal in every four-colouring and `|a-b|>=1/2`, two copies could share
the image of `a` and rotate so that the two images of `b` are one unit apart.
The resulting support would have at most `2*n-1` points before further
collisions. Here `n=111`, so this route had a credible cap of 221 points,
well below 509. The exact neutral relation disproves its premise.

The support, its aligned orientation and its complete pair relation are now
retired. This theorem does not classify higher-arity relations, rotated sums,
other EI17 realizations, other atoms, or arbitrary sub-509 constructions.
In particular, neutrality of every pair does not imply neutrality of larger
terminal sets.

The comparison baseline is Jaan Parts's 509-point, 2,442-edge strict graph in
[*Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane*](https://arxiv.org/abs/2010.12665). Haugland's 2026
construction is a Moser-spindle-free restricted-family record and not a
smaller unrestricted graph. The EI17 realization is traced in the sibling
package to Exoo and Ismailescu and to the certified numerical realization in
[Silva Filho, arXiv:2607.19995](https://arxiv.org/abs/2607.19995). No
literature-priority claim is made for this finite relation census.

## Trust boundary

The exact root theorem and source transcription are inherited from four
hash-pinned sibling files. The new proof trusts the elementary planar
unit-rhombus identity, the written telescope, exact Python integer/Fraction
arithmetic, the two implementations, SHA-256, and ordinary hardware. It does
not trust floating-point predicates, a SAT/SMT UNSAT answer, an omitted proof
log, or an abstract graph embedding. The checks are author-side independent
implementations, not an external peer review or proof-assistant formalization.
