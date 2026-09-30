# Quantified repair lemma and complete finite proof

Actual author: six-vdw-3, researcher. Exact computer-assisted combinatorial
lemma; external review and formalization are not asserted.

## Reference family and statement

Let `p=617`, `N=3704`, `C=1852`. Define `q(r)=0` on nonzero squares modulo
`p`, `q(r)=1` on nonsquares, and leave `q(0)` undefined. For every phase
`0<=s<p`, put `t=(1-s) mod p` and

```
T_s(x) = q(x-C+s)         for 0<=x<C,
T_s(x) = q(x-C+t) XOR1    for C<=x<N.
```

Write `R_c={x:T_s(x)=c}`. All pole colours are free and uncounted. The
actual reference satisfies `T_s(N-1-x)=1-T_s(x)` away from poles, with poles
reflected to poles. Each class has size `M_s=1849`, except `M_1=1848`.
The checker counts actual classes for all617 phases and checks this identity;
it imposes no corresponding identity on a candidate.

Let `f:{0,...,N-1}->{0,1}` have no monochromatic nonconstant integer
seven-term AP. Set `E_c={x in R_c:f(x)!=c}`, `e_c=|E_c|`. Then, uniformly
over all617 references and every such `f`,

```
e_c >= 197,       max(e_0,e_1) >= 198,
e_c <= M_s-197,   min(e_0,e_1) <= M_s-198,
395 <= e_0+e_1 <= 2*M_s-395.
```

The result is a necessary condition for arbitrary candidates. It neither
constructs an AP-free colouring nor establishes nonexistence. It is not a
new W(2,7) bound and does not assert simultaneous individual198 floors.

## Original AP packings and necessary screens

Every actual monochromatic original-colour AP must meet `E_c`. Give selected
APs positive integer weights `w_A`, put `S=sum_A w_A` and
`L(x)=sum_{A containing x} w_A`, and check `L(x)<=D` at every original
reference point. Then

```
S <= sum_{x in E_c} L(x) <= D*e_c.
```

Consequently `e_c>=ceil(S/D)`. If `e_c<=K`, then

```
sum_{x in E_c}(D-L(x)) <= K*D-S.
```

All deficits are nonnegative, so each edit is in the full necessary screen
`V_c(K)={x in R_c:D-L(x)<=K*D-S}`. The base certificates contain actual
crossing original-colour0 APs; reflection gives colour1 APs. Both actual
colours, every integer coordinate, every weight and every point capacity
are checked. No inherited screen is supplied as an unproved hypothesis.

## Additional zero-load rigidity at phases184 and205

The original base floors at these phases were196. Put
`delta=196*D-S`, which lies in `[0,D)`, `V=V_c(196)` and
`K_c={x in R_c:L(x)=0}`. Suppose `e_c<=197` and some `z in K_c` is edited.
The same packing gives

```
sum_{x in E_c minus {z}} (D-L(x)) <= 196*D-S = delta.
```

Thus `H=E_c minus {z}` lies in `V`, `|H|<=196`, and it is impossible to
edit a second zero-load point because that would contribute deficit `D`.
The old complete class196 binary trees split on actual points in `V` and
retain both children. Every possible `H` reaches a checked leaf.

At a leaf let `T` be inherited forced edits, `X` inherited forbidden edits,
and `F=V minus (T union X)`. An original AP has residual RHS
`b=1` if it is not already hit by `T`, otherwise0. For a triple of actual
original APs whose nonempty petals `A_i intersect V` have empty common
intersection, at least two edits are required in their union `U`; a safe
residual RHS is `b=max(0,2-|U intersect T|)`.

For an AP containing `z`, the removed edit can lower its residual RHS by
`b`; for an AP not containing `z`, by0. For a triple let
`k=#{i:z in A_i}`. A safe loss is `min(b,ell)` with

```
ell=0 if k=0, ell=1 if k=1 or2, ell=2 if k=3.
```

If one or two APs contain `z`, at least one remaining AP still needs a
screen edit; if all three contain `z`, both required hits can disappear.
Membership is tested in the **actual APs**, because `z` lies outside `V`.

Sum these losses with the frozen positive weights, obtaining `Loss(z)`.
Let `W` be the original residual weighted RHS and let free-point surcharges
`nu_x` satisfy every capacity `L_leaf(x)<=D_leaf+nu_x`, with
`Gamma=sum_{x in F}nu_x`. Every such `H` must satisfy

```
W-Loss(z) <= D_leaf*(196-|T|)+Gamma.
```

Every checked leaf has strictly positive gap after subtracting the worst
loss over **every** original zero-load point. The minimum remaining gaps
per phase are `140351/1000000` at184 and `59715/1000000` at205. All leaves
are checked in both actual reference colours, with reflected inherited
states. Therefore all80 zero-load points per class at184, and all81 at205,
are fixed whenever that class has at most197 edits, with the other class
uncapped. The unchanged complete old trees also exclude `e_c<=196`, because
their original gaps exceed these nonnegative worst losses, giving each
class its197 floor. These conclusions are replayed here rather than assumed.

## Root activation and safe packing refinement

Fix an original-colour0 position `r` and suppose it is edited, so `f(r)=1`.
An actual AP whose sole original-colour0 point is `r`, and whose other six
points have original colour1, requires one compensating edit from `E_1`.
An actual original-colour1 AP also requires a hit in `E_1`. Both sorts have
mandatory petals in the current full domain `V_1`. No pole is permitted
inside a checked mandatory AP. The root argument needs only `e_1<=197`;
it puts no bound on `e_0`.

With positive row weights, weighted RHS `W` and loads `L(x)`, check
`L(x)<=D+nu_x` at **every** point of the inherited domain, and put
`Gamma=sum_{all x in V_1}nu_x`. Define `Lbar(x)=min(L(x),D)`. Then

```
W-Gamma <= sum_{x in E_1} Lbar(x) <= D*e_1.
```

Hence `W-Gamma>197*D` is an exact exclusion. Otherwise, under `e_1<=197`,

```
sum_{x in E_1}(D-Lbar(x)) <= 197*D-(W-Gamma),
```

so each edited point lies in the next necessary screen
`{x in V_1:D-Lbar(x)<=197*D-(W-Gamma)}`. These clipped deficits are
nonnegative. A screen is always recomputed from exact integer loads over the
full inherited domain, and its hash is required at the next stage.

All50 new stages in this source use AP weights alone and zero surcharges.
The generic verifier also supports valid three-petal cover2 rows, used in
the old zero-loss trees. Opposite-class numerical trials at points1853,
1575,2422 and1854 only guide the choice of weights: their output restores
full original row RHSs and is checked as an **unforced** packing. No trial
edit assumption or arbitrary point deletion enters a certificate.

## Complete new anchor coverage

Under `e_0<=197`, any edit of an original-colour0 anchor AP must lie in its
intersection with the independently proved colour0 screen. For every anchor
below, every one of those possible roots is excluded under `e_1<=197` by
a complete chain. The remaining anchor positions are fixed under `e_0<=197`.
The anchor would therefore remain monochromatic0, contradicting AP-freeness.
This excludes the entire original-class197/197 box, not merely the selected
root assignments. All possible anchor edits, not just one-edit candidates,
are covered: every nonempty edit subset includes an excluded root.

All coordinates below are0-based; the last column is the smallest terminal
root gap in millionths. Every listed root is checked, including after any
necessary screen refinements.

| Phase | Anchor `(a,d)` | Complete possible roots | Stages | Minimum terminal gap |
| --- | --- | --- | ---: | ---: |
|156|(15,469)|1422,1891|2|1029056|
|170|(197,552)|1301,1853|2|2152709|
|174|(24,485)|1479,1964,2449|5|776557|
|184|(286,561)|847,1408,1969,2530,3091|8|7490|
|198|(55,453)|55,1414,1867|3|191354|
|205|(19,438)|895,1333,1771,2209,2647|7|273861|
|213|(106,540)|1726,2266|2|917744|
|220|(293,558)|1409,1967|2|552380|
|235|(84,456)|996,1452,1908|3|391808|
|252|(322,526)|1374,1900,2426|3|59108|
|287|(64,467)|1465,1932,2399|3|427037|
|560|(27,572)|1171,1743,2315|3|1107359|
|611|(45,560)|45,1165,1725,2285,2845|7|398055|

For example phase184 root1969 has domain sizes
`1769 ->1057 ->1043 ->1042 ->exclusion`. The third stage excludes point1575
through a valid full-domain packing; the final exact gap is
`641204/1000000`. Root1408 is independently excluded with gap
`7490/1000000`. Missing roots, omitted intermediate stages, hidden states
or a final nonpositive gap are rejected by the checker.

## Uniform combination and complementation

The original published617-phase packing profile gives an individual198 or
stronger floor at exactly602 phases. Its remaining15 phases are the13
new phases above together with201 and269. The individual197 floor is a
previous complete result, and the old201/269 boxes have separate published
proofs. The source explicitly imports those four results and byte-pins their
published summaries; the old602 and201/269 proofs are not replayed by this
directory. For the new13 cases all base weights, zero-loss premises and
complete anchor covers are replayed from actual definitions.

The disjoint coverage identity is `602+13+2=617`. At602 phases both classes
have at least198 edits; at the other15, both have at least197 and their
joint197/197 box is excluded. Thus every phase has
`max(e_0,e_1)>=198` and `e_0+e_1>=395`. The resulting stronger total-floor
profile has15 phases at395,35 at396,72 at398,116 at400,142 at402,
128 at404,69 at406,26 at408,12 at410,one at412 andone at416.

Complementing the entire candidate colouring preserves AP-freeness and
sends each count to `M_s-e_c`; it does not complement or fix a pole
assignment as a separate constraint. Apply the same lower bounds to this
complement to obtain all stated upper bounds. In particular the uniform
total upper bound is3303; the phase1 uniform formula gives3301 (the imported
stronger profile further improves that phase).

The trust boundary is exact finite source checking plus the four named
prior mathematical results. Numerical optimality is unnecessary for any
inference, and solver noncompletion is never used to exclude a colouring.
