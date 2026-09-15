# Native Heule133 does not amplify the opposed-B214 source

The single exact support below has **476 distinct plane points and 2,341
complete unit edges**. It is the reviewed 343-point opposed-B214 source,
together with the 133 noncentral points of Heule's native small part.
**Every complete four-colouring of the source extends.** All 12 contacts
between the two parts meet the source origin, so colour permutation on the
attached part gives a direct universal-extension proof.

This fixed interaction is exactly four-chromatic. It is retired at the
separating-vertex gate, without a colour search, another frame, extra copy,
receiver test or completion layer. It is not a record candidate.

## The selected source and new premise

The independently accepted opposed-B214 construction reduces the complete
normalized Golomb relation from 95 to exactly 66 patterns, through genuine
private contacts. It is a different input from the earlier Parts374 module.
Its one native-A159 completion was already proved neutral and is not repeated.

Here the new fixed complement is the small part from Heule's physical
553-point positive parent. The point accounting is

```text
343 + (134-1) = 476.
```

This was a source-conditioned attempt to use the newly demonstrated input
loss. It did not begin with a Parts receiver demand table. The old
Parts374–Heule133 substitution was used only as a pinned coordinate source
for the 133 Heule points, not rerun or varied.

The composite has 146 points outside that old 507-point support, so its
failure is not inferred from containment in the earlier fixed stop. Complete
geometry instead gives the stronger, elementary reason below.

## Exact coordinates and complete contacts

Represent a point by 16 integers divided by 288, the first eight for x and
the next eight for y, in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

Let G be the native ten-point Golomb graph. For the published B214 point
set B, use exactly

```text
L(x,y)=(x-1/2,y),  R(x,y)=(-x+1/2,y),
S=G union L(B) union R(B).
```

Keep G first, then append unseen points of L(B) and R(B) in source order.
This gives the reviewed ordered 343-point source. Its original coordinate
hash is checked against the accepted package. To obtain H, take the 133
points not fixed by changing the sign of sqrt(5) in the pinned old507 table.
This selects exactly Heule's noncentral small side in the displayed frame.
Append H in its source table order, with no transformation.

The source and H have no collision. All **113,050 unordered point pairs**
are tested exactly, giving

| Unit-edge class | Count |
|---|---:|
| Inside S343 | 1,782 |
| Inside H133 | 547 |
| Between S343 and H133 | 12 |
| Total | 2,341 |

Every one of the twelve cross edges has source endpoint 0, the origin.
There are no contacts with any of the other 342 source vertices. The
134-point graph C consisting of H plus the origin therefore has 559 edges,
and the whole graph is precisely S and C joined at that one vertex.

The verifier uses integer multiquadratic multiplication. For basis indices
encoded by the three radical bits,
`sqrt(D_i)*sqrt(D_j)=D_(i&j)*sqrt(D_(i xor j))`.
The eight square classes are independent, so coefficientwise equality
decides both collisions and squared distance one. No floating-point
incidence or inherited-only edge graph is used.

## Universal extension and ordinary chromaticity

[certificate.json](certificate.json) contains a proper four-word on C whose
origin has colour 0. For any complete proper four-colouring c of S, transpose
colours 0 and c(0) in this fixed C word. It now agrees at the origin and
remains proper on every C edge. Since there are no other contacts, it extends
c to the complete 476-point graph.

Restriction in the opposite direction is automatic. Thus the entire
four-colour projection onto all 343 source vertices is unchanged. This is
stronger than checking the 66 saved Golomb-prefix witnesses or a selected
set of source words. In particular the reviewed 66-pattern Golomb relation
remains exactly 66. That numerical source count is an **imported reviewed
result**; no source RUP proof or terminal census is rerun here.

A full proper four-word and a full proper five-word are checked directly on
the complete physical graph. The retained Golomb subgraph has no proper
three-colouring, verified by all 3^7 assignments after fixing its unit
triangle. Hence the whole graph has chromatic number exactly four. The
five-word does not establish five-chromaticity.

## Replay, input boundaries and scope

A checkout of this repository, Python 3.11 or later, and the standard library
suffice. From the repository root:

```sh
python3 -B hadwiger_nelson_opposed343_heule133_origin_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_opposed343_heule133_origin_stop/verify.py --check-expected
python3 -B hadwiger_nelson_opposed343_heule133_origin_stop/controls.py
(cd hadwiger_nelson_opposed343_heule133_origin_stop && sha256sum -c SHA256SUMS)
```

[inputs.json](inputs.json) pins the two existing coordinate files, totalling
27,949 bytes, and their verified remote versions. They are reused rather than
duplicated. The positive words are small and checked independently of their
generation history. No parent non-four theorem or negative solver verdict is
needed to prove this stop.

The producer's sparse radical-gcd expansion and the checker's bit-indexed
square formula agree entry by entry on every point pair and every edge.
Normal and optimized runs agree. Controls accept valid evidence first, then
reject improper source/whole words, a broken origin-edge colouring and an
additional non-origin source contact that would invalidate the extension
rule. [VALIDATION.json](VALIDATION.json) records these author-side checks;
this new package has no independent-author review.

The theorem concerns only S343 and this exact native Heule133 placement.
It is not an arbitrary-complement, Heule-family or global HN exclusion.
The source's previously proved strict loss remains valid, but this operation
cannot amplify it. No neighbouring source/complement frame, phase, root,
copy count, deletion or remaining-32-point sweep follows.

Source and review:

- [Opposed-B214 source](https://github.com/helgithorskarp/math_results/blob/42fd5e441e190a4022743479458aabf2ca55a85b/hadwiger_nelson_golomb_opposed_b214_stop/README.md).
- [Independent source review](https://github.com/helgithorskarp/math_results/blob/5ed67074e4008c0549f8c2e35dc1bf2e86485891/hadwiger_nelson_golomb_opposed_b214_review1/README.md).
- [Heule's physical positive-parent construction](https://arxiv.org/abs/1805.12181).

[Parts](https://arxiv.org/abs/2010.12665) remains the supported 509-point
unrestricted record, also identified as current by
[Haugland v4](https://arxiv.org/html/2608.04542v4). No Discovery submission is
made for this fixed universal-extension stop.
