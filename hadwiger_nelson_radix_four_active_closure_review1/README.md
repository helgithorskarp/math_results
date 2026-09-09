# Independent review of the four-active complex-radix closure

**Verdict: ACCEPT with high confidence.** The h4151 contribution correctly
proves that every injective, off-unit-circle member of

```text
A5(z) = T + zT + z^2 T + z^3 T + z^4 T,
T = {0,1,(1+i sqrt(3))/2},
```

with at most four active noncircle distance-event curves is four-colourable.
Combined with the independently accepted collision and unit-circle theorems,
any non-four-colourable member of this architecture must be injective, lie off
the unit circle, and have at least five active curves.

This is an intermediate branch closure, not the campaign target. It constructs
no five-chromatic graph and does not improve the 509-vertex record.

## Independent finite check

[independent_check.py](independent_check.py) imports no target or ancestor
module. The submitted 3,006-entry forbidden-incidence export is used only as a
declarative witness: the checker independently reconstructs its curve IDs and
checks every asserted edge before using it.

The independent implementation differs materially from both submitted paths.
It generates the 2,801 displacement classes from all `7^5-1` rows rather than
grouping label pairs, expands event equations in the real/imaginary basis
`z=x+i sqrt(3)y`, audits all actual label pairs afterwards, and verifies the
K4 part by certificate-set containment rather than searching for a first
clique separately in every failing quartet.

It obtains:

```text
labels / unordered label pairs                 243 / 29,403
unit-normalized displacement classes                 2,801
noncircle curves / circle curve                 2,796 / 1
off-circle universal edges                            243
circle-only monomial edges                            972
noncircle-event edges                              28,188
realized affine F4 hyperplanes                         336
projective normals / eligible normals              85 / 81
eligible quartets                                 960,768
F3-linear-colourable quartets                     934,632
quartets excluded by a planar K4                   26,136
unresolved quartets                                     0
```

The support-stratified counts also agree entry for entry:

| Tail support | Eligible | F3-colourable | Impossible K4 |
|---:|---:|---:|---:|
| 2 | 2,304 | 1,656 | 648 |
| 3 | 73,728 | 67,680 | 6,048 |
| 4 | 884,736 | 865,296 | 19,440 |

Every one of the 29,403 actual label pairs is used to check the independently
derived F3 and F4 failure masks. Every edge of every one of the 3,006 submitted
K4 certificates is then recomputed from its four labels. The checker verifies
that no claimed clique uses the excluded circle curve or an undeclared event.

## Written-proof audit

Reducing the Eisenstein coefficient ring modulo 2 gives `F4`. After normalizing
the coefficient of the first digit, there are 256 affine linear label words.
For a noncircle displacement row, the bad words form an affine hyperplane in
`F4^4` of size 64. The independent checker verifies all pairwise intersections:
two realized hyperplanes with different projective normals meet in 16 words,
whereas distinct constants for one normal are disjoint.

Therefore at most three active curves cannot defeat every word. Four can do so
only by supplying all four constants for one normal. Conversely, those four
hyperplanes partition all 256 words. The 81 normals for which all constants
occur give the complete eligible list. The support formulas are

```text
number of normals: C(4,s) 3^(s-1),
bucket sizes:      2^(s-1), 2^s, 2^s, 2^s,
```

for `s=2,3,4`; they independently sum to 960,768 quartets. Support one is
ineligible because its zero-constant row is the excluded circle monomial.

For the 934,632 coloured quartets, reduction modulo 3 with `omega -> -1`
provides a directly checked proper linear three-colouring. For each remaining
quartet, the checked certificate supplies four distinct labels whose six
pairs are universal or belong to the declared active curves.

Four pairwise unit-distance points cannot lie in the plane. Taking one as the
origin, the other three vectors would have Gram matrix with diagonal entries
1 and off-diagonal entries 1/2. Its independently recomputed determinant is
1/2, hence its rank is three, while three planar vectors have Gram rank at most
two. The six unit edges also force the four physical points to be distinct, so
label coincidence cannot evade the obstruction.

Thus every physically possible eligible quartet is three-colourable, and every
noneligible set of at most four active curves retains an F4 word. This proves
the stated injective off-circle theorem.

## Independent strengthening

The submitted export contains 2,376 three-curve K4 certificates and 630
four-curve certificates. An exhaustive containment sweep shows that the
three-curve certificates alone cover all 26,136 failing eligible quartets.
All 2,376 triples are used by the deterministic greedy coverage, and zero
four-curve certificates are needed. The 630 four-curve witnesses remain valid
but are redundant for this closure proof. This sharpens the reusable interface
without changing the accepted theorem.

## Reproduction

From the repository root, generate the submitted witness and run the independent
checker:

```sh
review_tmp=$(mktemp -d)
python3 -B hadwiger_nelson_radix_four_active_closure/verify.py \
  --export-interface "$review_tmp/interface.json"
python3 -B hadwiger_nelson_radix_four_active_closure_review1/independent_check.py \
  --interface "$review_tmp/interface.json"
python3 -O -B hadwiger_nelson_radix_four_active_closure_review1/independent_check.py \
  --interface "$review_tmp/interface.json"
```

On CPython 3.11.2, the independent normal and optimized runs took 24.82 and
24.87 seconds on one CPU and produced byte-identical output with SHA-256
`c9d16bb292c1f452b1adbc50f590570726942180de091fae55494c176b4635ff`.

The submitted normal and optimized verifiers also agreed byte for byte. The
producer regenerated the 2,275-byte public certificate and the 100,080-byte
interface exactly; the independent submitted verifier accepted both. Target
controls rejected malformed clique and certificate cases, and the HN3 handoff
checkpoint replayed.

## Trust boundaries

The finite checks trust CPython exact integer and rational arithmetic plus code
inspection. They use no floating point, CAS, SAT solver, network data, or
uncommitted raw search artifact. The physical edge reduction, affine-hyperplane
argument, and Gram-rank obstruction were independently re-derived but are not
proof-assistant formalizations.

The full-architecture corollary imports h4119 (collision closure) and h4139
(unit-circle closure), both independently accepted by reviewer-1. The h4105
curve inventory is reconstructed independently here. The h4117 and h4135
global-system counts are checked only as exact handoff bytes and remain imported
trust boundaries; they are not premises of the accepted four-active theorem.

## Strengthening and improvement opportunities

- Replace the published 3,006-set handoff by the sufficient 2,376-triple
  interface and use those lower-arity constraints first in higher-incidence
  parameter pruning.
- Independently review h4117 and h4135 before treating the reported 131,788
  global representatives, 7,780,224 allowance, and 2,528 obligations as
  independently certified rather than imported.
- Formalize the finite-field hyperplane lemma and Gram-rank bridge if this
  reduction becomes load-bearing for a claimed record graph.
- Continue with the genuinely unresolved branch: simultaneous activation of
  at least five noncircle curves at an injective off-circle parameter.

## Provenance

Target Discovery ref:
`bafkreidulncimzcgkped4pqbiisxq7vpprsbm5vuvygsmeno5ldlqvaz34` (h4151).
Target source commit:
`6f58bd6f3fa5a5da0cf549de345facd89e9f19a3`.
Machine-readable results and hashes are in [EVIDENCE.json](EVIDENCE.json).
