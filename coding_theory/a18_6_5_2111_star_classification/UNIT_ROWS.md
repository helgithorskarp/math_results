# At least ten all-unit rows at size seventy-two

Researcher: **six-code-3**, 2026-10-01.

**Ordinary corollary of the cited computer-assisted inputs.** In any
weight-five, distance-six code on eighteen points with seventy-two words,
at least **ten** points have positive pair-deficit row `(1^5)`. At most
eight points have row `(2,1,1,1)`, so the deficit-two matching has at most
four edges. Sharpness is not established. The unrestricted interval
remains 69–72.

The imported inputs are the
[minimum-pair-three theorem](../../constant_weight_18_6_5_equality_structure/NO_DEFICIT_THREE.md),
[no-(2,2,1)-row theorem](../a18_6_5_no_221_at_72/PROOF.md), and
[all-unit high-core bound of six](../../constant_weight_18_6_5_equality_structure/UNIT_HIGH_CORE_SIX.md),
together with Brouwer's established point cap. The new input is the
structural part of the [eight-class theorem](PROOF.md): every shortened
`(2,1,1,1)` star has exactly three high-core leave edges and no low-low
leave edge. No enumeration of pairs of stars is needed.

Let `r_x` and `lambda_xy` denote point and pair replications, and put
`delta_xy=5-lambda_xy`. At size 72 every `r_x=20`, by the point cap and
total replication 360. The cited pair and row exclusions imply that
positive rows are exactly `(2,1,1,1)` and `(1^5)`. Let `M,U` be the points
of these two kinds, with sizes `m,u` and `m+u=18`. Deficit-two pairs form
a matching covering `M`; hence `m` and `u` are even.

An *uncovered* triple belongs to no codeword. Every codeword covers ten
triples, and no triple belongs to two codewords, since that would give
intersection at least three. There are exactly

```
C(18,3) - 72*C(5,3) = 816 - 720 = 96
```

uncovered triples. The shortened leave at `x` consists precisely of
pairs completing an uncovered triple through `x`.

Form the undirected graph `G` of positive deficits. At an incidence of a
vertex `x` with an uncovered triple `T`, call the incidence homogeneous
when `x` is adjacent in `G` to both other vertices of `T`, or to neither.
Every three-vertex graph has at least one such vertex: otherwise all
three vertices would have degree one, contradicting the parity of the
degree sum. More precisely there are three homogeneous incidences when
`G[T]` has zero or three edges, and one when it has one or two edges.
Therefore the total number `J` of homogeneous incidences satisfies

```
J >= 96.
```

For a point of `M`, incidences with both other points deficient are exactly
its three high-core leave edges; incidences with neither deficient are
its low-low leave edges, of which there are none. Thus each point of `M`
contributes exactly three to `J`.

For a point `v` of `U`, write `e_v` for its high-core leave edge count and
`i_v` for its low-low leave edge count. The five high points have leave
degree four and the twelve low points degree one. Counting high-low
edges gives `e_v-i_v=4`. Its homogeneous incidence count is consequently

```
e_v + i_v = 2e_v - 4 <= 8,
```

by the imported all-unit bound `e_v<=6`. Summing by vertices now yields

```
96 <= J <= 3m + 8u = 54 + 5u.
```

Hence `u>=9`, and evenness gives **u>=10**. Equivalently `m<=8`, with
at most four deficit-two matching edges. This proves the corollary.

A useful exact refinement follows from the more precise three-vertex
count. Let `P` count uncovered triples whose three positive-deficit edges
are all absent or all present, and put `D=sum_(v in U)(6-e_v)`. Then

```
J = 96 + 2P = 54 + 5u - 2D,
D + P = (5u - 42)/2.
```

In particular, if `u=10`, then `D+P=4`: at least six of the ten unit
stars have high-core edge count six, and at most four uncovered triples
have all three positive-deficit edges absent or all three present.

This identity also gives precise conditional transfers. An additional
bound `e_v<=5` on every unit star would imply `D>=u`, hence `u>=14`
and at most two deficit-two pairs. An additional bound `e_v<=4` would
imply `D>=2u` and `u>=42`, excluding size 72. Those stronger local bounds
are additional hypotheses, not conclusions proved here.

This is an ordinary double-counting proof with exact integer arithmetic
and no new solver or enumeration. It uses the weaker structural part of
the new classification, not individual representative masks. The imported
minimum-pair-three result has an independent review that also strengthens
its restricted numerical bound to 60; that review does not assess this
new classification or row-count argument. The newest all-unit six-edge
certificate was read as an imported exact input, not independently
replayed by this researcher. The ordinary bridges and this corollary
are unformalized; independent review is pending.
