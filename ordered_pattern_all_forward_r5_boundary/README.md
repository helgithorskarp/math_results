# The all-forward ordered 5-pattern at the `5m+2` boundary

## Result

Let `m>=2`, and let `P^(m)` be the all-forward 5-partite ordered
5-matching on `[5m]`, with edges

```text
{j, m+j, 2m+j, 3m+j, 4m+j},             1 <= j <= m.
```

Then

```text
ex_<(5m+2,P^(m)) = C(5m+2,5)-21.                     (1)
```

Thus the conjectured formula of Anastos--Jin--Kwan--Sudakov is exact at
the first unresolved excess for the constant orientation in uniformity
five.  The case `m=2` was already covered by the primary paper; the new
range here is `m>=3`.

## Blockers and the 21-edge construction

Put `N=5m+2`.  Every canonical copy on `[N]` is determined by its omitted
pair.  A set `D` of 5-edges is a *blocker* if it meets every copy.  Taking
complements makes (1) equivalent to

```text
minimum blocker size = 21.                            (2)
```

There is a blocker of size 21.  In one-based indexing, take all
`e={e_0<e_1<e_2<e_3<e_4}` such that

```text
e_(i+1)-e_i >= m for i=0,1,2,3,     e_4 <= N-(m-1).  (3)
```

The first edge of every canonical copy satisfies (3).  Subtracting

```text
(0,m-1,2(m-1),3(m-1),4(m-1))
```

bijects (3) with the 5-subsets of `[7]`, so it has 21 edges.  We prove that
20 edges never suffice.

## Three occurrence-graph types

Identify the omitted vertices cyclically with `Z_N`.  For an active 5-edge
`e`, let `Omega(e)` be the graph whose vertices are `Z_N` and whose edges are
the omitted pairs whose canonical copy contains `e`.

Each of the five cyclic open gaps of `e` contains at least `m-1` vertices.
Their total is `5(m-1)+2`, so the two surplus vertices are either together,
in two adjacent gaps, or in two gaps at cyclic separation two.  Consequently
every nonempty occurrence graph is exactly one of

```text
Q_s = K_[s,s+m],                                      s in Z_N,
R_s = K_([s,s+m-1],[s+m+1,s+2m]),                    s in Z_N,
T_s = K_([s,s+m-1],[s+2m+1,s+3m]),                  s in Z_N.  (4)
```

Conversely, deleting any pair in a graph from (4) leaves exactly `m-1`
retained vertices in every cyclic gap, so the list is complete.  A blocker
is therefore a selection of these occurrence graphs covering `K_N`.

## Private layers and start gaps

Cyclic distance 1 is private to `Q`, distance `m+1` to `R`, and distance
`2m+1` to `T`.  Each graph of the corresponding type covers exactly `m`
pairs in its private layer, while each layer has `N` pairs.  If `q,r,t`
are the selected type counts, then

```text
q >= 6,                  r >= 6,                  t >= 6.       (5)
```

For any selected start family covering its private layer, list its starts
cyclically as `a_i`, put

```text
h_i=a_(i+1)-a_i,             d_i=m-h_i,
```

and note that `1<=h_i<=m`, so `d_i>=0`.

We will use a simple two-arc observation.  If a cyclic point set can be
partitioned into two consecutive blocks, each of cyclic span at most `2m`,
then it lies in two disjoint arcs of `2m+1` points.  The two complementary
block hulls can be enlarged inside their two separating gaps: the available
gap capacity exceeds the total required enlargement by
`N-2(2m+1)=m`, so the two enlargements can be allocated without meeting.
The two complementary arcs contain `m` points in total.  If their smaller
size is `u<=floor(m/2)`,
these complementary arcs are exactly the permissible `T`-starts for a pair
of distance `2m+1+u`: explicitly they are intervals of lengths `m-u` and
`u`.  Hence such a point set fails to cover the high-distance band.

Six `T`-starts always split into two three-point blocks.  Each block spans
at most two start gaps and hence at most `2m`.  Thus

```text
t >= 7.                                                     (6)
```

Only `t=7,8` can occur in a blocker of size at most 20.

## Repairs forced by a `T`-gap

For a gap `h_i=m-d_i` between selected `T`-starts, direct membership in
(4) gives a pair whose permissible selected starts are

```text
T: (a_i,a_(i+1)),
R: J_i=[a_(i+1),a_i+m],                 |J_i|=d_i+1.  (7)
```

The `T` interval is the empty open start gap.  Therefore a selected `R`
start must hit every `J_i`.

### Seven maximal starts

Suppose `t=7`.  Then

```text
sum_i d_i = 7m-N = 2m-2.                                (8)
```

High-band coverage forces

```text
d_i+d_(i+1)+d_(i+2) <= m-1             for every i.     (9)
```

Indeed, if a triple sum were at least `m`, the four corresponding starts
would span at most `2m`; the complementary three starts span at most two
gaps, also at most `2m`.  The two-arc observation would give an uncovered
high pair.

The repair intervals `J_i` are pairwise disjoint.  Adjacent repairs could
meet only if `d_i+d_(i+1)>=m`, contrary to (9).  Repairs at cyclic index
distance at least two would require deficit at least `2m`, contrary to (8).
Consequently

```text
t=7  implies  r>=7.                                    (10)
```

### Eight maximal starts

Suppose `t=8`.  Now `sum d_i=3m-2`.  Again form the eight repairs `J_i`.
Their intersection graph has a seven-vertex independent set.

To see this, first note that `J_i` can meet only `J_(i+1)` or `J_(i+2)`:
greater cyclic index distance would consume deficit at least `3m`.
An intersection with `J_(i+2)` makes four consecutive starts span at most
`m`; adding the next gap gives a five-start block of span at most `2m`,
and the other three starts also span at most `2m`.  This would miss a high
pair, so such an intersection is impossible.

It remains to rule out two vertex-disjoint adjacent intersections.  Rotate
the first to `J_0 cap J_1`.  Up to reflection, the second begins at index
2, 3, or 4.

- At index 2, the five starts `a_0,...,a_4` span at most `2m`; the other
  three span at most `2m`.
- At index 3, the two four-start blocks with internal gap sets
  `{3,4,5}` and `{7,0,1}` each span at most `2m`.
- At index 4, the same two blocks work.

Each case again contradicts high-band coverage.  Thus all adjacent
intersection edges share one `J_i`; deleting that interval leaves seven
pairwise disjoint repairs.  Hence

```text
t=8  implies  r>=7.                                    (11)
```

## The tight `t=r=7` propagation

Assume now that exactly seven `T` and seven `R` graphs are selected.  The
seven disjoint intervals in the `t=7` case contain exactly one selected
`R`-start each.  Write

```text
b_i=a_(i+1)+u_i,                    0<=u_i<=d_i.         (12)
```

The `R`-start gap from `b_i` to `b_(i+1)` has deficit

```text
e_i=d_(i+1)-u_(i+1)+u_i.                                (13)
```

For each `R` gap, the analogous low-distance pair forces a `Q`-start into

```text
K_i=[b_(i+1),b_i+m],                 |K_i|=e_i+1.        (14)
```

Adjacent `K` intervals cannot meet, because (9), (12), and (13) give

```text
e_i+e_(i+1)
 = d_(i+1)+d_(i+2)+u_i-u_(i+2)
 <= d_i+d_(i+1)+d_(i+2)
 <= m-1.                                                   (15)
```

Nonadjacent intervals cannot meet because `sum e_i=sum d_i=2m-2`.
Thus the seven `K_i` are pairwise disjoint, and

```text
t=r=7  implies  q>=7.                                  (16)
```

## Completion

Suppose a blocker had at most 20 edges.  By (5) and (6):

- if `t>=9`, then `q+r+t>=6+6+9=21`;
- if `t=8`, (11) gives `q+r+t>=6+7+8=21`;
- if `t=7`, (10) gives `r>=7`; if `r>=8` the total is already 21, while
  `r=7` invokes (16) and gives `q+r+t>=7+7+7=21`.

This contradiction proves the lower bound in (2).  The blocker (3) proves
equality and hence (1).

## Scope and literature status

The primary source is Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny
Sudakov, *Extremal, enumerative and probabilistic results on ordered
hypergraph matchings*, Forum of Mathematics, Sigma 13 (2025), e55
([DOI](https://doi.org/10.1017/fms.2024.144),
[open manuscript](https://arxiv.org/abs/2308.12268)).  Its Theorem 1.18(1)
gives the blocker construction, and its Conjecture 1.20 proposes the exact
formula for all partite patterns and parameters.  Its Theorem 1.17 settles
matching size two.

A targeted primary-literature and web search through 2026-09-20 found no
later resolution of this `r=5`, all-forward `5m+2` case.  This is a
search-relative status statement, not a claim of priority.  The argument
does not settle the all-forward case for `r>=6` and `m>=3`, or any larger
excess.

## Reproduction

Requires Python 3.11 or later and uses only exact standard-library integer
and set operations.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

The checker reconstructs every canonical copy directly from its omitted
pair for `2<=m<=12`; verifies the complete `Q/R/T` occurrence-graph
classification, the 21-edge blocker, and all private layers; and exhausts
the six-, seven-, and eight-start deficit signatures through the stated
audit boxes.  It independently checks the two-arc implications, repair
intersection graph, and tight propagation formulas.  The computation
corroborates the definitions and boundary cases.  The parameter-uniform
argument above proves the theorem.
