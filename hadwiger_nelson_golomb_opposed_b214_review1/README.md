# Independent review of the opposed-B214 relation gain

Verdict: **accept, with a strict fixed-composition and neutral-completion
limitation**.

An independent exact implementation confirms the complete physical geometry
and the full normalized Golomb four-colour relations of both declared
supports:

| Support | Points | Complete unit edges | Golomb patterns | Chromatic number |
|---|---:|---:|---:|---:|
| two opposed B214 copies | 343 | 1,782 | 66 of 95 | 4 |
| plus native A159 | 359 | 1,893 | 66 of 95 | 4 |

The first support therefore gives a genuine complete-input relation loss. The
pattern `0121212203` has checked full extensions through the left and right
B214 copies separately, but the independently replayed RUP proof excludes it
from their complete physical union. This proves at least one interaction-only
loss; it does not assert that all 29 missing patterns have separate lifts.

The native A159 completion adds 16 physical points and 111 unit edges,
including 32 new contacts beyond the component edge sets, but eliminates no
further Golomb pattern. Its 66 positive full words and the inherited exclusion
proof establish exactly the same relation. This is a useful forcing source
followed by a rigorously neutral finishing operation, not a five-chromatic
construction.

The review additionally checks that both complete physical graphs are
connected, have minimum degree five, and have no articulation vertex or
bridge. Thus the relation loss is not explained by the bridge or pendant
pathologies found in earlier campaign components.

## Independent method

The target uses four-term arithmetic in
`Q(sqrt(3),sqrt(11))` and a watched-literal RUP checker. This review instead
parses the public coordinates into the full ordered basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)
```

and multiplies basis masks by symmetric-difference and repeated-prime
reduction. Every unordered physical pair is scanned exactly. The recovered
point and edge streams agree entry-for-entry with the target hashes.

The review enumerates the 95 normalized Golomb patterns directly. It checks
all 132 published positive full-graph words, regenerates the
1,401-variable/9,823-clause CNF for the other 29 patterns, and replays all
1,382 RUP additions with remaining-literal counts and literal occurrence
lists. This is independent of the target's watched-literal implementation.
New proper colourings of the 343- and 359-point supports differ from the
target words in nine and ten positions respectively.

## Reproduction

CPython 3.11 or later and a complete checkout of this repository are required;
the standard library suffices. From this review directory:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The controls compare the independent RUP engine with definition-level unit
propagation on 10,240 small cases, check 6,561 multiquadratic products, test
cut structures on a path and triangle, and reject hash, colour-word, and RUP
lemma corruptions. See [PROOF.md](PROOF.md),
[PROVENANCE.md](PROVENANCE.md), and [VALIDATION.json](VALIDATION.json).

The target's 52 KB positive certificate and 78 KB RUP trace are referenced by
hash rather than duplicated. No solver binary, floating-point incidence
predicate, private file, ledger, or generated CNF is required.

## Exact scope and record status

The result covers only the isometries

```text
L(x,y)=(x-1/2,y),  R(x,y)=(-x+1/2,y)
```

for the two pinned B214 copies and the single native A159 placement. It does
not classify other frames, phases, copy counts, roots, or finishing gadgets.
The source relation has 66 surviving patterns and no certified route to an
empty four-colour relation within 508 points. Both displayed graphs are
four-colourable, so neither is a record candidate.

Parts's published 509-point, 2,442-edge five-chromatic construction remains
the supported unrestricted order record in the bounded primary-source check,
also identified as current by Haugland's August 2026 paper.

## Sources

- Reviewed target (branch path):
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_golomb_opposed_b214_stop>.
  Exact reviewed revision:
  `42fd5e441e190a4022743479458aabf2ca55a85b`.
- Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- Haugland, [A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane](https://arxiv.org/abs/2608.04542).

The requested `math-review` skill was unavailable. Its independence,
exact-scope, geometric-realization, chromatic-certificate, hidden-assumption,
and source-integrity criteria were applied directly with the available exact
computer-assisted and GitHub research skills.
