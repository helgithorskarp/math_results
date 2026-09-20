# The all-forward ordered 3-pattern at the `3m+2` boundary

## Result

Let `m >= 2`, and let `P^(m)` be the all-forward 3-partite ordered
3-matching on `[3m]`, with edges

```text
{j, m+j, 2m+j},                 1 <= j <= m.
```

Then

```text
ex_<(3m+2, P^(m)) = C(3m+2,3) - 10.                 (1)
```

Thus the conjectured formula of Anastos--Jin--Kwan--Sudakov is exact at
the first unresolved excess for the constant orientation in uniformity
three.  The case `m=2` was already covered by the primary paper; the new
range here is `m>=3`.

## Blocker formulation and the upper construction

Put `N=3m+2`.  Every order-preserving copy of `P^(m)` on `[N]` is
specified by its omitted pair.  A set `D` of triples is a *blocker* if it
meets every one of these copies.  Taking complements shows that (1) is
equivalent to

```text
minimum blocker size = 10.
```

There is a blocker of size 10: take all triples

```text
e={e_0<e_1<e_2} with e_1-e_0 >= m, e_2-e_1 >= m,
and e_2 <= N-(m-1).                                      (2)
```

Here the vertices in (2) are numbered from 1 through `N`.  The first edge
of every canonical copy lies in (2): its two internal gaps contain the
other `m-1` copy edges, and at least `m-1` copy vertices follow its last
vertex.  The change of
variables

```text
(e_0,e_1,e_2) -> (e_0, e_1-(m-1), e_2-2(m-1))
```

is a bijection from (2) to the 3-subsets of `[5]`, so there are exactly
10 such triples.  It remains to prove that nine triples cannot block all
copies.

## Occurrence graphs on a cycle

Identify `[N]` cyclically with `Z_N`.  For a triple `e`, let `Omega(e)` be
the graph whose vertices are `Z_N` and whose edges are the omitted pairs
whose canonical copy contains `e`.

If `e` occurs in a copy, each of the three cyclic open gaps between its
vertices has at least `m-1` vertices.  The three gaps contain
`3(m-1)+2` vertices in total, so their two surplus vertices have one of
two forms:

1. Both surplus vertices lie in one gap.  That gap is an interval of
   `m+1` vertices, and `Omega(e)` is the clique on that interval.
2. The surplus vertices lie in two gaps.  Each of those gaps is an
   interval of `m` vertices, and `Omega(e)` is the complete bipartite
   graph between the two intervals.

Consequently all nonempty occurrence graphs, indexed by `s in Z_N`, are

```text
Q_s = K_[s,s+m],
R_s = K_([s,s+m-1], [s+m+1,s+2m]),                 (3)
```

where all intervals are cyclic.  There are `N` graphs of each type.
Thus a blocker is exactly a selection of the graphs in (3) whose union is
the complete graph on `Z_N`.

For a cyclic pair, its *distance* is the smaller of its two clockwise
separations.  A `Q_s` contains only pairs of distance at most `m`.
In particular, all pairs of distance greater than `m` must be covered by
the selected `R_s`.

## The cyclic-gap lemma

We use intervals of integer points, so an interval of length `a` contains
`a` points.

**Lemma.** Suppose selected graphs `R_s` cover every pair of cyclic
distance greater than `m`.

- At least five `R_s` are selected.
- If exactly five are selected, list their starts cyclically as
  `t_0,...,t_4`, and put

  ```text
  h_i = t_(i+1)-t_i                 (cyclically).
  ```

  Then

  ```text
  h_i + h_(i+1) >= m+1             for every i.       (4)
  ```

**Proof.**  For a pair `{x,x+m+1+t}`, where
`0<=t<=floor(m/2)`, direct use of (3) shows that the permissible starts
of an `R_s` are two cyclic intervals of lengths `m-t` and `t`.  Their
complement consists of two intervals, each of length `m+1`.  Conversely,
the complement of any two such `(m+1)`-intervals, whose two intervening
lengths sum to `m`, is the permissible-start set of such a pair.

At distance exactly `m+1`, the permissible starts form one interval of
length `m`.  Hence any family covering the long pairs has every cyclic
gap between consecutive starts at most `m`.

If four starts covered all long pairs, group them into two consecutive
pairs.  Each pair fits in an interval of length `m+1`, because its internal
gap is at most `m`.  Enlarge the two pair-hulls, inside the two separating
gaps, to disjoint intervals of length `m+1`.  This is always possible:
the required enlargements use exactly `m` fewer points than the two
separating gaps contain.  The `m` points left over form the permissible
start set of a long pair, but contain none of the four starts, a
contradiction.

Now suppose there are five starts and (4) fails, say
`h_i+h_(i+1)<=m`.  Three consecutive starts then fit in one interval of
length `m+1`; the other two fit in another, because their internal gap is
at most `m`.  Enlarge these two hulls to disjoint intervals of length
`m+1`, exactly as above.  Again the `m` leftover points are the permissible
starts of an uncovered long pair.  This contradiction proves (4).  `□`

The enlargement assertion used twice is just a two-bin allocation.  If
the two hulls have `a+1` and `b+1` points, their required enlargements are
`m-a` and `m-b`; the two separating open gaps contain
`3m-a-b` points.  Thus the total capacity exceeds the demand by exactly
`m`, and each individual demand is no larger than the total adjacent
capacity.  Allocating from the two ends of each separating gap gives the
claimed disjoint enlargements.

## Five disjoint repair arcs

Assume for contradiction that a blocker has at most nine triples.  A
`Q_s` covers exactly `m` pairs of cyclic distance one, and no `R_s` covers
such a pair.  Since there are `N=3m+2` distance-one pairs, at least four
graphs `Q_s` are needed.  The cyclic-gap lemma requires at least five
graphs `R_s`.  Hence a blocker of size at most nine would have exactly four
`Q`-graphs and exactly five `R`-graphs.

Use the five starts `t_i` and gaps `h_i` from the lemma.  Since the
distance-`m+1` pairs are covered, `1<=h_i<=m`.  Consider the low-distance
pair

```text
p_i = {t_i+m, t_i+m+h_i}.                              (5)
```

For a general pair `{x,x+d}` with `1<=d<=m`, (3) gives the exact
permissible-start intervals

```text
Q-starts: [x+d-m, x]              (length m-d+1),
R-starts: [x-m+1, x+d-m-1]        (length d-1).         (6)
```

Substituting (5) into (6), the permissible `R`-starts are precisely the
open cyclic gap

```text
(t_i,t_(i+1)).
```

It contains none of the selected starts.  Therefore `p_i` can be covered
only if a selected `Q`-start lies in the repair arc

```text
J_i = [t_(i+1), t_i+m].                                (7)
```

But (4) gives

```text
t_i+m <= t_(i+2)-1,
```

so

```text
J_i is contained in [t_(i+1),t_(i+2)-1].
```

These five half-open cyclic sectors are pairwise disjoint.  The five
pairs `p_i` therefore require five distinct `Q`-starts, contradicting the
assumed four.  Every blocker has at least ten triples; (2) supplies ten,
and (1) follows.

## Scope and literature status

The primary source is Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny
Sudakov, *Extremal, enumerative and probabilistic results on ordered
hypergraph matchings*, Forum of Mathematics, Sigma 13 (2025), e55
([DOI](https://doi.org/10.1017/fms.2024.144),
[open manuscript](https://arxiv.org/abs/2308.12268)).  Its Theorem 1.18(1)
gives the blocker construction, and its Conjecture 1.20 proposes the exact
formula for all partite patterns and parameters.  It already settles
uniformity two and matching size two.

A targeted primary-literature and web search through 2026-09-20 found no
later resolution of this `r=3`, all-forward `3m+2` case.  This is a
search-relative status statement, not a claim of priority.  The argument
does not settle the all-forward case for `r>=4` and `m>=3`, or any larger
excess.

## Reproduction

Requires Python 3.11 or later and uses only exact standard-library set and
integer operations.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

The checker reconstructs every canonical copy directly from its omitted
pair for `2<=m<=12`; verifies the occurrence-graph classification, the
ten-edge blocker, the permissible-start formulas, and every step of the
cyclic-gap/repair-arc certificate; and compares a deterministic record
with `EXPECTED.json`.  The finite audit checks the definitions and proof
identities.  The parameter-uniform argument above proves the theorem.
