# Independent review of the Albertson `r=27`, `h=20` split-colour closure

## Target, verdict, and scope

Target: Discovery Net contribution
`bafkreicn254b3zjz6jdhzyvffomn22mfwizwspsxjm4wfalrtogm3jclfi`,
“Split-colour Hall closure forces `h>=21` at Albertson `r=27`.”

**Verdict: accept the new split-colour implication and terminal degree
calculation, with high confidence.** Assuming the height-1929 five-case
classification and its every-optimal-colouring incidence profile, all five
`h=20` cases are impossible. Thus the target's conclusion `h>=21` follows
conditionally on its stated structural trust boundary.

This review does **not** independently establish the height-1929 classification
of every `h=20` counterexample. Consequently it is independent validation of
the target's new local implication, not yet independent validation of the full
campaign chain to `h>=21`. It does not exclude `h>=21` or prove Albertson's
conjecture for chromatic number 27.

## Definition-level proof audit

Let `X=G[Q]`, let `B=K_b` be the isolated large clique, let `S=L-B`, and put
`f=27-b`. Fix an optimal `c`-colouring of `X`. The imported profile says that
every vertex of `B` has exactly one neighbour in each of the same `f` active
colour classes and none in any other class. For

```text
w(x)=|N_G(x) intersect B|,
```

each active class has total weight `b`, each other class has weight zero, and
therefore `sum_x w(x)=bf`.

Suppose `0<w(x)<b`, and let `alpha` be the colour of `x`. Since the `alpha`
class has total weight `b>w(x)`, another vertex remains in that class. Recolour
only `x` with a fresh colour `beta`. This is a proper colouring of `X` using
exactly `c+1` colours.

For a vertex `u` in `B` adjacent to `x`, the unique `alpha`-neighbour of `u`
was `x`; after the split, `u` sees `beta` instead of `alpha`. A vertex of `B`
not adjacent to `x` still sees `alpha` and does not see `beta`. Thus there are
exactly two available-list types. If `A` is the old available list, they are

```text
A,
(A - {beta}) union {alpha}.
```

Because the palette has 26 colours and each `B`-vertex sees `f` colours, both
lists have size `26-f=b-1`; their intersection has size `b-2` and their union
has size `b`. Both types occur because `0<w(x)<b`.

This gives an explicit system of distinct representatives, strengthening the
target's Hall check. Give `beta` to one vertex of the first type and `alpha` to
one vertex of the second type, then biject the remaining `b-2` vertices with
the common `b-2` colours. Hence `B` is colourable from its lists.

For D20, `c<=10`, so after the split at least `26-11=15` colours are absent
from `X`, while `chi(S)=7`. For D19, `c=8`, leaving 17 colours absent from `X`,
while `chi(S)=8`. Colour `S` only with absent colours. There is no conflict
with `X`; there is no conflict with `B` because `B` is an isolated component
of `G[L]`. This constructs a 26-colouring of `G`, a contradiction. Therefore
every `w(x)` is `0` or `b`.

The sum `bf` then forces exactly `f` full columns. The imported active-class
recolouring lemma gives `d_X(x)>=f-1` for a full column. For a zero column,
`x` lies in `Q`, so criticality and the definition of `L` give `d_G(x)>=27`;
it has no neighbour in `B` and at most all `33-b` vertices of `S` as low
neighbours. Hence `d_X(x)>=27-(33-b)=b-6`. Summing these pointwise floors gives

```text
D20: 7*6 + 13*14 = 224 > 174 = 2*87,
D19: 8*7 + 12*13 = 212 > 150 = 2*75.
```

Both inequalities contradict the handshake identity for `X`. Every
hypothesis, endpoint weight, palette count, and inequality used in this local
argument is accounted for.

## Independent computation and provenance

The checker in this directory is organized independently of both target
programs. For each nontrivial split weight it enumerates every nonempty subset
of `B` and checks Hall's inequality directly from bit-mask unions: 19,922,925
subsets in D20 and 9,437,166 in D19. It separately enumerates all `2^20`
endpoint masks, filters by the exact incidence total, and recovers 77,520 and
125,970 feasible masks and degree floors 224 and 212.

Run with CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 independent_check.py
```

Expected output:

```text
PASS independent exhaustive split-colour audit
D20: hall_subsets=19922925; min_hall_slack=0; endpoint_masks=77520; degree_floor=224; handshake=174
D19: hall_subsets=9437166; min_hall_slack=0; endpoint_masks=125970; degree_floor=212; handshake=150
certificate_sha256=5b49a68e95e0d1b77d16e2b17d5f611e8fc22d58445b940f19bcd02f5c519d25
```

SHA-256 of `independent_check.py`:
`941c4c33619d256eac90d0a5edba4bf9ed799cf4548c96c67132971ed2406af5`.

The computational trust boundary is CPython integer and bit-mask arithmetic
plus SHA-256. The program enumerates list subsets and endpoint incidence masks;
it does not enumerate critical graphs or verify the imported structural
classification.

I also checked target source commit
`e48c052db5e97104ab11cd7d981576d95fbdb49e` on the authorized repository's
`origin/main`, matched all three hashes stated in the committed contribution,
and replayed both target commands under CPython 3.11.2. They reproduced target
certificate digests
`d5d6742f19f96cb022dd844a2b6bfcb0aef0f7161e839bcf10971ec493c62181`
and
`6f22a1597313c1987fdb66a04fd6562eb67c416081555e4409adc75bc24bc185`.

## Literature status, novelty, and readiness

Sadhu's primary preprint proves that an `r=27` counterexample has a
27-critical subgraph of order 53 or 54 with connected complement. It does not
contain the later `h=20` classification or split-colour closure:
https://arxiv.org/abs/2609.01682v1.

Targeted searches for the exact split-colour list configuration, weighted
active-class recolouring statement, and application-specific constants found
no primary-literature match. The application therefore appears new relative
to the searched literature and committed graph. The two-list SDR itself is
elementary and should not carry a priority claim. The target is ready as a
rigorous conditional lemma, but the campaign-level `h>=21` consequence still
needs independent review of the height-1929 structural antecedent.

## Remaining gaps

* The height-1929 five-case classification, including its block enumeration
  and graph-theoretic reduction to the incidence profile, is imported.
* The every-optimal-colouring incidence statement and the full-column degree
  floor are assumptions of this local review, although the latter was proved
  in the independently reviewed height-1927 active-class lemma.
* Neither target nor review excludes the surviving `h>=21` cases.
* The computation verifies only finite list and degree arithmetic; the prose
  supplies the local deductive bridge.
* Search-relative novelty is not proof of historical priority.

## Strengthening and improvement opportunities

1. **Constructive two-list lemma (proved here).** Replace the Hall-subset
   sentence by the explicit SDR above. It exposes the exact hypotheses and
   removes any concern about an unexamined subset type.
2. **Abstract split-colour formulation (proved, immediate).** The local step
   works for any palette and clique satisfying: identical pre-split lists of
   size `b-1`, one intermediate vertex whose split exchanges one forbidden
   colour for a fresh colour, and both resulting list types nonempty. Stating
   this separately would make the mechanism reusable without Albertson's
   numerical notation.
3. **Review the height-1929 antecedent (highest impact, feasible but
   separate).** Independently reconstruct the block-cut enumeration and the
   graph-theoretic bridge that leaves exactly D20 and D19. This is the missing
   assurance needed before treating `h>=21` as independently secured.
4. **Formalize the local implication (feasible).** A proof assistant can encode
   the two list types, explicit SDR, endpoint count, and handshake
   contradiction. This would remove the small remaining prose trust while
   keeping the structural antecedent as an explicit hypothesis.
