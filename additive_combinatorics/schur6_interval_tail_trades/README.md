# Minimum tail repairs create a larger Ramsey target

This is a checkable obstacle to one construction direction for the classical
sixth Schur number. **No colouring of `[1,537]`, improved Schur bound, or
impossibility theorem for the construction family is claimed.** All Schur
conditions include repeated summands.

Reserve colour 6 on `T0=[78,154] union [460,537]` and colour its complement
with five colours. This is the free interval model selected in the
[preceding independence calculation](../schur6_interval_ramsey_bottleneck/README.md).
Every complement position has an independent colour choice; there are no
old-class palettes, modular fibres, or reflection equalities.

The exact tail reduction below identifies 15 empty colour lists for an
explicit seed. Moving those points into colour 6 requires deleting at least
43 old reserved points. There are exactly 44 minimum deletion sets. Every
resulting reserved support, even after filling the gaps between the 15
points, would force a triangle-free five-colour complete graph on at least
190 vertices if its complement could be five-coloured. Thus completing
any of these repairs would imply **`R5(3)>=191`**.

This is a conditional implication, not a new Ramsey lower bound. The
[April 2026 survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), Section 6.1.1,
gives `162<=R5(3)<=307`. The record Schur baseline remains `S(6)>=536`,
as used in the [July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034).
The matching argument and difference-colouring implication are elementary;
no historical priority is asserted for those methods.

## Exact completion problem

Write `U=[1,77]`, `V=[155,304]`, and `W=[305,459]`. Fix colours on `U,V`
that already satisfy their Schur rows. For each `z in W`, let `L(z)` contain
the colours not appearing on an equal-colour pair `x,y in U union V`
with `x+y=z`. A colouring of `W` completes the five-colouring exactly when:

1. Each `w(z)` belongs to `L(z)`.
2. For `d in U` and `x,x+d in W`, the three colours
   `u(d),w(x),w(x+d)` are not all equal.

Indeed, all remaining Schur rows have types `UUU`, `UVV`, `UVW`, `UWW`,
or `VVW`. Their respective counts are `1482,8547,3003,8932,5700`.
The first two types are already satisfied; the next and last create lists;
`UWW` gives the binary constraints. A `V+W` sum is at least 460 and a
`W+W` sum exceeds 537. The tail is a general finite list-colouring problem,
not automatically 2-SAT.

`data.json` gives a full valid five-colouring `B` of `[1,160]`, copied from
the earlier construction data, and the seed
`u(d)=B[d]`, `v(154+i)=B[i]` for `1<=i<=150`.
The seed satisfies every `UUU` and `UVV` row. Its empty tail lists are

```
F = {312,313,315,322,326,327,332,334,335,336,340,341,342,347,348}.
```

For example, the colours 1 through 5 at 312 are blocked respectively by
`18+294`, `156+156`, `39+273`, `32+280`, and `52+260`.
Each pair has the indicated common colour. This is a local obstruction to
this seed, not to all choices on `U,V`.

One can also add 155 to the old reserved support: let
`T0(delta)=[78,154+delta] union [460,537]`, `delta in {0,1}`.
Both supports are sum-free. For `delta=1`, discard the seed value at 155;
the same 15 lists are still empty. The result below covers this immediate
enlargement as well.

## All minimum repairs

**Proposition.** Let `Q=F` or `Q=[312,348]`, and permit only additions from
`Q` to `T0(delta)`. The minimum size of a set `C subset T0(delta)` for which
`(T0(delta) minus C) union Q` is sum-free is `43+delta`. The complete list
of minimum deletion sets is

```
C_t = [460,459+t] union [112+t,154+delta],
       0<=t<=43+delta,
```

where an interval with reversed endpoints is empty. After adding the whole
interval `Q=[312,348]`, the remaining support is

```
T_t = [78,111+t] union [312,348] union [460+t,537],  |T_t|=149.
```

After adding just `F` its size is 127, and it is a subset of `T_t`.

**Proof.** The old support and `Q` are each sum-free. Two old lower points
sum to at most 310, below `Q`; two points of `Q` sum beyond 537. The only
new triples therefore have the form `l+q=h`, with `l` in the old lower
interval and `h` in the old upper interval. They give a bipartite graph of
deletion requirements. Its nonisolated vertices are

```
L_i=112+i, H_i=460+i, 0<=i<m=43+delta.
```

The point 348 gives all `m` disjoint edges `L_i H_i`, so at least `m`
deletions are needed. A minimum cover chooses exactly one endpoint of each
of these edges, and no isolated vertex. The point 347 gives every edge
`L_(i+1) H_i`. If `H_(i+1)` was chosen, `L_(i+1)` was not, so `H_i` must
also be chosen. Hence the chosen upper vertices form an initial segment
`H_0,...,H_(t-1)` and the chosen lower vertices are `L_t,...,L_(m-1)`.
Conversely every such choice covers every possible edge: an edge `L_i H_j`
has `j<=i` because `q<=348`. If `L_i` is unchosen, `i<t`, hence `j<t`
and `H_j` is chosen. This proves optimality and the complete classification
for both choices of `Q`.

## Explicit difference witnesses

For each `0<=t<=44`, put

```
b=111+t, p=floor((112+t)/2), r=112+t-p, s=min(78,126-2t),
A_t=[0,p-1] union [b+p,b+p+s-1] union [348+p,347+p+r].
```

All positive differences of `A_t` lie in `[1,537] minus T_t`.
Within a component they are at most 77. Between consecutive components
they lie in `[b+1,311]`: the needed inequalities are
`p+s<=201-t`, `s<=126-2t`, and `r<=75+t`.
Between the first and last component the differences lie in
`[349,459+t]`. These inequalities hold throughout `0<=t<=44`.
The components are disjoint and

```
|A_t| = 190+t  (0<=t<=24),
         238-t (25<=t<=44).
```

Thus the displayed sizes range from 190 to 214. They are lower witnesses
for the auxiliary independence numbers, not asserted exact maxima.
Given a five-colouring of the complement of `T_t`, colour the edge between
`x<y` in `A_t` by the colour of `y-x`. A monochromatic triangle would
give a Schur triple of differences, which is forbidden. Therefore
`R5(3)>=|A_t|+1>=191`. The same argument applies when just `F` is added,
because that reserved support is a subset of `T_t`.

The statement does not cover repairs deleting more old points, adding
different new points, or changing the initial low/middle seed. Those are
the remaining construction freedoms. In particular, these implications
do not exclude any six-colouring of `[1,537]`.

## Reproduce

Python 3.10 or newer, standard library only; tested with Python 3.11.2:

```sh
python3 -B verify.py > /tmp/schur-tail-check.json
diff -u expected.json /tmp/schur-tail-check.json
sha256sum -c SHA256SUMS
```

The independent checker verifies the complete 160-word, every seed sum
and list, all 27,664 target rows, all four deletion graphs, the matching and
chain hypotheses that prove the classification, every reserved support,
and every pairwise difference in all 45 witnesses. It also exhausts small
tail-completion instances and small versions of the matching/chain cover
classification. The proofs above establish the statements; small-instance
checks are implementation audits. No SAT solver or UNSAT status is needed
for any claim in this note.
