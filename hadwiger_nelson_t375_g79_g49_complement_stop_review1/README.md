# Independent review: one T375--G79--G49 complement stop

## Verdict

**Accept and strengthen at the stated one-architecture scope.** The exact
construction at target commit
`fe8d17ab505eb283244bcacb5ff55e082615f006` is a genuine plane
unit-distance realization. Its complement has 126 physical points and 346
complete unit edges; its union with T375 has 466 physical points and 1,966
complete unit edges. The supplied four-colour words are proper on those
complete graphs, including all 47 unit contacts not inherited from the two
named component edge sets.

The review adds a conclusion absent from the target report: complement
vertices

```text
44, 40, 50, 45, 41, 51, 47
```

induce exactly the standard seven-vertex, 11-edge Moser spindle in that order.
An exhaustive check of all `3^7` assignments finds no proper three-colouring,
while the target word restricts to the proper four-colouring
`1,2,3,0,2,3,1`. Thus the 126-point complement itself has chromatic number
exactly **4**. Its 466-point supergraph also has chromatic number exactly 4.

This is not a five-chromatic graph or a record improvement. The nonmonochromatic
pin colours `0,0,3` are a direct positive stop for the intended complement
obstruction.

## Independent exact reconstruction

`independent_check.py` imports no executable source or target module. It
hash-pins the 109-row appendix, the T375 retained-index certificate, G40, G49,
the target certificate, and the architecture frozen before the target result.
It then:

1. closes the appendix under the specified 120-degree rotation and y-axis
   reflection, obtaining 627 reference points;
2. selects the 375 certified T375 rows;
3. independently forms G79 using multiplication by
   `(119+3 i sqrt(247))/128`;
4. translates G49 and applies the final map `(x,y) -> (x,2/3-y)`;
5. collision-merges exact coordinates and examines every unordered physical
   pair in both resulting point sets.

All coordinates are represented in the basis

```text
1, sqrt(3), sqrt(11), sqrt(33), sqrt(247), sqrt(741),
sqrt(2717), sqrt(8151)
```

with common denominator 4,608. The square classes of 3, 11, and 247 are
independent, so this is a linearly independent basis and coefficient equality
is physical equality.

For edge completeness, the review uses an algorithm distinct from the target's
direct exact scan. It sends the three square roots to checked roots in each of
the prime fields of orders 10,007 and 10,067. Any exact unit pair must satisfy
the resulting modular norm equation, so rejecting a pair on either congruence
cannot discard a real unit edge. Every survivor is then confirmed by exact
eight-coefficient multiplication over the integers. The two sieves leave
exactly 346 of the `C(126,2)` complement pairs and 1,966 of the `C(466,2)`
union pairs; every survivor confirms exactly.

The resulting canonical point and edge hashes match the target. In particular,
the independent reconstruction also recovers:

- T375: 375 points and 1,661 complete unit edges;
- complement/T375 overlap: 35 physical points;
- incidental union contacts beyond inherited edges: 47;
- complement points using `sqrt(247)`: 39;
- checked complement pins: `0,0,3`.

## Chromatic certificate audit

The full 126- and 466-symbol words are checked against the independently
reconstructed complete edge sets. The complement word is also checked to be
the exact restriction of the union word under the independently derived point
embedding.

For the lower bound, the checker derives the subgraph on the seven displayed
indices from the complete edge set and requires it to contain exactly the 11
Moser edges. It enumerates all named three-colour assignments and obtains zero.
As a sensitivity control, deleting any one of those 11 edges produces 12
proper named three-colourings; the witness check rejects every corresponding
edge deletion.

## Reproduction

Python 3.11 or later, standard library only, from this directory:

```bash
python3 -B independent_check.py --check-expected
python3 -O -B independent_check.py --check-expected
python3 -B controls.py --check-expected
python3 -O -B controls.py --check-expected
sha256sum -c SHA256SUMS
```

The trust boundary is CPython exact integer arithmetic and file semantics,
the inspectable finite searches, SHA-256 identity, Git, and ordinary hardware.
No SAT solver, floating-point predicate, target executable, private search
state, or omitted large certificate is used. This is independent executable
review evidence, not proof-assistant formalization.

## Exact scope and record context

The accepted claim covers only the frozen architecture: one exact G79, one
translated G49 decoder, one specified final frame, and their union with the
specified T375 copy. It does **not** exclude other G40 pairs, G49 triangles,
decoder counts or frames; arbitrary relative isometries; multi-complement
assemblies; non-lattice attachments; or any other T375 wrapper. It also does
not enlarge the separately reviewed family of 10,012 high-contact native-field
completions: 39 points here lie outside that native field.

The unrestricted published vertex record remains Parts's
[509-vertex construction](https://arxiv.org/abs/2010.12665). Haugland's 2026
[manuscript](https://arxiv.org/abs/2608.04542) still describes 509 as the
unrestricted record. A 466-point four-chromatic plane graph does not challenge
that five-chromatic record.

At review time the local committed Discovery index remained at height 4,363
and the RPC at 4,364, with the last block dated 2026-09-11. The target receipt
is CheckTx-zero but pending and unindexed; this review does not relabel it as
committed or resubmit it.

## Sources

- Reviewed target: [one T375--G79--G49 complement stop](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_t375_g79_g49_complement_stop),
  target commit `fe8d17ab505eb283244bcacb5ff55e082615f006`.
- Required exact dependency: [T375 small-triangle forcer](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_small_triangle_forcer375),
  dependency commit `f88d7ee5b1d0b5c640750dc287bda159b8775423`.
- Historical component construction: Exoo--Ismailescu,
  [arXiv:1805.00157v1](https://arxiv.org/abs/1805.00157v1).
