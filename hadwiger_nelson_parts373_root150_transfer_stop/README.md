# A full small-gadget transfer at receiver vertex150 is a neutral one-vertex sum

This package closes one fixed physical replacement for the independently
accepted Parts373 receiver. Translate the complete 136-point small Parts
gadget so its centre is the retained vertex150. The exact union has **508
points and 2,420 complete unit edges**, but the two parts meet at only that
vertex and have **no other unit contacts**. Consequently every host
four-colouring extends and every projected host relation is unchanged.
The complete graph has chromatic number exactly four.

This is a failed receiver-conditioned construction, not a sub-509
five-chromatic graph. It does not classify other translations or placements.

## Exact frozen support

Use the original Parts509 labels in the hash-pinned `points.tsv`, with
coordinates divided by96 in the basis

    (1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165)

for x and y separately. Put

    H = {0,...,373} minus {310},
    S+ = {0} union {374,...,508},
    t = p150 = (1/2,sqrt3/2),
    W = H union (S+ + t).

The map is this one translation; there is no rotation, reflection, anchor
search, subset choice or completion layer. Its source centre0 coincides with
host vertex150. All135 other translated points are distinct and outside the
entire original509-point set. Thus the merged budget is exactly
373+136-1=508, and the translated source has no second host overlap.

The intended test was whether one complete small gadget, attached at a
neighbour of the omitted star, could supply both functions of the original
136-point deleted module. Its internal constraints are preserved by isometry;
its old receiving-frame relation is **not** preserved by that fact. The point
saving omits the separate star vertex310. No obstruction-preserving saving
was assumed from the shared centre or the point count.

This is outside the [full-gadget two-overlap closure](../hadwiger_nelson_parts_full_gadget_overlap_closure/README.md):
that theorem uses the full374-point large part and at least two overlaps.
The old four-addition one-anchor closure and sealed a=8 pool also do not
cover this wholesale135-point replacement. Being outside a registered
closure was only a scope check, not positive chromatic evidence.

## Complete contacts and universal extension

The independently written sparse-radical checker reconstructs all128,778
unordered pairs. Its complete squared-distance stream agrees with the
producer's subset-mask arithmetic, not merely the final edge count.

| Exact object | Count |
|---|---:|
| Retained host points / unit edges | 373 / 1,856 |
| Translated full small-gadget points / unit edges | 136 / 564 |
| Shared points | 1 |
| New physical points | 135 |
| Complete union points / unit edges | 508 / 2,420 |
| Additional contacts between the private parts | 0 |

The source centre has12edges to new vertices. Those belong to the translated
small gadget. The whole actual host interface is `{150}`, and every unit edge
is inherited from one of the two parts. In graph terms W is their one-vertex
sum.

The certificate contains a proper colouring of the small gadget. For any
proper four-colouring of H, permute the small gadget's colour names to make the source
centre agree with host vertex150. Unite the colourings. Their only shared
vertex now agrees, and the complete contact census leaves no unchecked cross
edge. This proves that **every** proper H colouring extends. In particular,
all468 reviewed boundary orbits survive; no full relation enumeration is
needed to prove the universal extension statement.

A literal508-colour word also checks directly. Its host restriction is the
first row of R1's table, with the23-pin word

    01200021231303000000303

The unchanged host contains the seven-point Moser spindle on original labels
`[0,149,152,312,151,154,314]`; all2,187three-colour words fail on its11edges.
Thus W is exactly four-chromatic. Recolouring the first vertex with colour4
also gives a checked proper five-word, which supplies only an upper bound.

## Reproduce

Python3.11 or later and its standard library suffice. From this directory:

```sh
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

`verify.py` imports neither producer code, sibling mathematical code nor a
solver. It reconstructs the coordinates and every unit edge with exact
integer arithmetic using squarefree-radicand multiplication via gcd, checks
the literal words, and checks a source-colour permutation for each of the
four possible shared colours. Normal and optimized results agree. Controls
reject bad source-edge colours, an incorrect receiver word and an invented
extra-contact count.

Hashes use compact JSON, and the distance stream uses sorted radical keys:

- Points: `1c70557566c47fdd02eff0c2956bb26e72e13d03936bb5371d47cf9e9f25ec59`.
- Complete edges: `03340b2efe798c9d5016b6c10310d0842d08f0ad3733163c100b286b45285fa7`.
- All squared distances: `3dacddb641f3f2b9b2ebec719382a6d191b21152e413cb874a59a1584e8e9dbb`.

The single initial pinned SAT call took about0.044s and returned a checked
model. That solver output is not a premise of the public proof: the positive
word and one-vertex-sum argument are checked directly. The proof trusts the
standard multiquadratic basis, exact Python integers, complete finite loops
and ordinary hardware. This is author verification, not an independent
research review or a proof-assistant formalization.

## Sources and stopping boundary

The [receiver source](../hadwiger_nelson_parts373_receiver_relation/README.md)
is pinned at `0fdb37bb7772a835307f904403589ba1d4676f20`; its
[independent acceptance](../hadwiger_nelson_parts373_receiver_relation_review1/README.md)
is at `d86266c0e09db808865b6c379d68d1c133a86756`. The copied coordinate
file has SHA-256
`f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.
Their negative completeness and parent proofs are context, not premises of
this universal extension certificate.

Retire this fixed transfer. Do not try more anchors, translations, phases,
partial gadgets or added layers from this failure. The Parts373 receiver
remains valid, but this source has no interaction beyond the shared colour.
A genuinely different physical replacement with demonstrated incompatibility
is still missing. G19, a=8 and the completed boundary-lens driver remain banked.

[Parts](https://arxiv.org/abs/2010.12665) gives the509-point/2442-edge record;
[Haugland v4](https://arxiv.org/html/2608.04542v4) still names509 as current.
The present exactly-four graph changes neither that record nor the global
Hadwiger--Nelson bounds.
