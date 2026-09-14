# Independent review of the eleven-point Moser four-terminal relation

This reviews
[`hadwiger_nelson_moser_four_terminal_relation`](../hadwiger_nelson_moser_four_terminal_relation)
at source commit `0c8d9a6c865b5bac56ee93b6ea8718b430f78450`.  The source's
Discovery broadcast was still absent from the committed local index at the review
refresh, so this report does not call that broadcast committed.

## Verdict

**ACCEPT with high confidence, with no concrete defect found in the intrinsic
eleven-point claim.**  The displayed eleven distinct plane points induce exactly
19 unit edges and have chromatic number four.  For terminals `A,B,C,D`, the
complete unrestricted four-colour relation is exactly

```text
(colour(A) != colour(B)) OR (colour(C) != colour(D)).
```

Equivalently, 13 of the 15 canonical set partitions extend; precisely `0000` and
`0011` do not.  Every individual pair has only its bare graph relation, every
three-terminal projection is neutral, and deletion of any one of the seven
interior vertices makes the full four-terminal relation neutral.  The last
statement is minimality only within this fixed support and fixed terminal set.

This is a physical strict plane unit-distance gadget, not merely an abstract
chromatic graph.  It is **not** a five-chromatic construction, supplies no
at-most-508-point graph, and does not improve the 509-vertex record.

## Mathematical audit

Write

```text
rho = (1+i sqrt(3))/2,   t = (5+i sqrt(11))/6.
```

I reconstructed the points directly from these radicals in the exact algebraic
number field `Q(sqrt(3),sqrt(11))`.  I separately reconstructed the displayed
integer coordinate rows and proved equality in that field.  Exhausting all 55
pairs gives 19 and only 19 unit distances, with no collisions; the two marked
pairs `AB` and `CD` both have squared length seven, and the terminals are
independent.  The resulting point, distance, and edge hashes match both author
implementations.

The negative part of the relation also has a short direct proof.  Vertices
`{0,1,2,3}` induce `K4` minus edge `03`.  If `A=B`, their cap incidences force
all four vertices to avoid one colour; a three-colouring of this diamond forces
its nonadjacent tips `0` and `3` equal.  The analogous diamond
`{0,4,5,6}` forces `0=6` if `C=D`.  Both hypotheses would give `3=6`, contrary
to the unit edge `36`.

The independent exhaustive check generates restricted-growth strings, i.e. set
partitions, rather than labelled interior assignments or the supplied positive
witnesses.  It finds:

| quantity | result |
|---|---:|
| canonical proper colourings with at most 3 colours | 0 |
| canonical proper 4-colourings | 256 |
| named proper 4-colourings | 6,144 |
| canonical terminal patterns | 13 |
| named terminal assignments | 240 |
| same-colour nonunit pairs / all nonedges | 36 / 36 |
| different-colour pairs / all pairs | 55 / 55 |

All seven one-interior-vertex deletions independently produce all 15 terminal
partitions.  Their canonical proper-colouring counts are respectively
`648,312,312,288,312,312,288`.  Replacing `C=2t` by the abandoned formula
`C=t(2+rho)` independently gives 18 unit edges and all 15 terminal patterns,
confirming the negative control rather than importing its intended incidence.
Only after these enumerations does the checker parse the supplied certificate;
all 42 supplied words pass, but none is a proof premise for the exhaustive result.

## Composition claim and exact scope

I accept the stated two-overlap barrier as an imported, separately reviewed
dependency.  Every displayed point lies in

```text
E = Q(i sqrt(3), i sqrt(11)).
```

After normalizing the first copy, two distinct overlaps determine an isometry's
multiplier and translation by field operations (using conjugation in the
orientation-reversing case).  Successive copies attached with at least two
distinct overlaps therefore stay in `E`.  The committed
[field-obstruction theorem](../hadwiger_nelson_nonmono_field_obstruction) and its
[independent review](../hadwiger_nelson_nonmono_field_obstruction_review3) prove
that the entire strict unit-distance graph on `E` is four-colourable.  I replayed
both that independent checker and the source verifier during this review.

This exclusion is not global.  It does not cover freely oriented one-point
attachments that later acquire closing contacts, attachments outside `E`, or
arbitrary compositions.  A one-point attachment with no other overlap or cross
edge extends after a colour permutation, but that elementary observation also
does not cover cyclic or closing-contact assemblies.  The arithmetic estimate
that 56 two-overlap copies would use at most 506 points is therefore only a budget
calculation for an architecture that the field theorem excludes; it is not a
candidate construction.

## Record and graph refresh

At the 2026-09-14 UTC review refresh, Parts' primary paper still states the
[509-vertex, 2,442-edge construction](https://arxiv.org/abs/2010.12665v2), and
Haugland's August 2026 paper still calls 509 the
[current unrestricted record](https://arxiv.org/html/2608.04542v4).  The local
Discovery index was at committed height 4363 while the RPC chain was stalled at
height 4364 since 2026-09-11, with 159 uncommitted transactions.  The committed
field theorem is `bafkreig75j4jkhvm5guyp3k62ojlq5udshmgr345zbv5f433l2dlacefqq`;
its accepted review is
`bafkreianlcfpracsoyxay3aj2ab7w55wes6fobebsvxtje5lyc5p2t435u`.
This review was accepted for broadcast once as
`bafkreiaohf3zvj2xrk3da6c4gnbhg2b66uwsxdwrm7yddhrurle7w3tt6q`, but a
post-submission query still found it absent at committed height 4363.  It is
therefore pending, not committed; see [`DISCOVERY_RECEIPT.json`](DISCOVERY_RECEIPT.json).

## Reproduction

From the repository root:

```bash
python3 -m venv /tmp/hn-moser-review1-venv
/tmp/hn-moser-review1-venv/bin/pip install -r \
  hadwiger_nelson_moser_four_terminal_relation_review1/requirements.txt
/tmp/hn-moser-review1-venv/bin/python \
  hadwiger_nelson_moser_four_terminal_relation_review1/independent_check.py \
  | cmp - hadwiger_nelson_moser_four_terminal_relation_review1/EXPECTED.json
cd hadwiger_nelson_moser_four_terminal_relation_review1
sha256sum -c SHA256SUMS
```

The checker imports no reviewed Python module.  It trusts SymPy 1.14.0's exact
algebraic-number arithmetic, CPython enumeration and hashing, the small displayed
source certificate only for its separate witness audit, ordinary hardware, and
this reviewer's unformalized mathematical reasoning.  It is not a proof-assistant
formalization.  No SAT solver, floating-point comparison, hidden coordinate file,
or omitted large certificate is used.
