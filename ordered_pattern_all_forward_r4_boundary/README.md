# The all-forward ordered 4-pattern at the `4m+2` boundary

## Result

Let `m>=2`, and let `P^(m)` be the all-forward 4-partite ordered
4-matching on `[4m]`, with edges

```text
{j, m+j, 2m+j, 3m+j},                  1 <= j <= m.
```

Then

```text
ex_<(4m+2,P^(m)) = C(4m+2,4)-15.                     (1)
```

Thus the conjectured formula of Anastos--Jin--Kwan--Sudakov is exact at
the first unresolved excess for the constant orientation in uniformity
four.  The case `m=2` was already covered by the primary paper; the new
range here is `m>=3`.

## Blockers and the 15-edge construction

Put `N=4m+2`.  Every order-preserving copy on `[N]` is determined by its
omitted pair.  A set `D` of 4-edges is a *blocker* if it meets every copy.
Taking complements makes (1) equivalent to

```text
minimum blocker size = 15.                            (2)
```

There is a blocker of size 15.  In one-based indexing, take all
`e={e_0<e_1<e_2<e_3}` such that

```text
e_(i+1)-e_i >= m for i=0,1,2,     e_3 <= N-(m-1).     (3)
```

The first edge of every canonical copy satisfies (3): its internal gaps
contain the other `m-1` copy edges, and at least `m-1` copy vertices follow
its last vertex.  Subtracting

```text
(0,m-1,2(m-1),3(m-1))
```

bijects (3) with the 4-subsets of `[6]`, so it has 15 edges.  We prove that
14 edges never suffice.

## Three occurrence-graph types

Identify the omitted vertices cyclically with `Z_N`, and put
`M=2m+1`, so `N=2M`.  For an active 4-edge `e`, let `Omega(e)` be the
graph whose vertices are `Z_N` and whose edges are the omitted pairs whose
canonical copy contains `e`.

Each cyclic open gap between consecutive vertices of `e` has at least
`m-1` vertices.  Their total is `4(m-1)+2`, so either both surplus vertices
lie in one gap or one lies in each of two gaps.  Up to rotation and the
cyclic separation of the two surplus gaps, every nonempty occurrence graph
is therefore exactly one of

```text
Q_s = K_[s,s+m],                                      s in Z_N,
R_s = K_([s,s+m-1],[s+m+1,s+2m]),                    s in Z_N,
S_s = K_([s,s+m-1],[s+M,s+M+m-1]),                  s in Z_M.  (4)
```

The last indexing quotients `S_s=S_(s+M)`.  Conversely, deleting any pair
in a graph from (4) leaves exactly `m-1` retained vertices in every cyclic
gap, so (4) is complete.  There are respectively `N,N,M` distinct graphs.
A blocker is exactly a selection of these occurrence graphs covering
`K_N`.

## Center-distance bounds

A cyclic pair has *distance* equal to its smaller clockwise separation.
Three distance layers are private to the three types:

- distance 1 occurs only in `Q_s`, and each `Q_s` contains `m` such pairs;
- distance `m+1` occurs only in `R_s`, and each `R_s` contains `m`;
- diameter `M` occurs only in `S_s`, and each `S_s` contains `m`.

There are `N` pairs in each non-diameter layer and `M` diameter pairs.
Writing `q,r,s` for the selected type counts gives

```text
q >= 5,                  r >= 5,                  s >= 3.       (5)
```

If `r>=7`, (5) already totals 15.  The rest of the proof handles `r=5,6`
by coupling the low and high distance bands.

## Paired repair intervals

List the selected `R`-starts cyclically as `b_0,...,b_(r-1)`, with gaps

```text
h_i=b_(i+1)-b_i,          d_i=m-h_i,          ell_i=d_i+1.     (6)
```

Covering the distance-`m+1` layer means that length-`m` start intervals
cover `Z_N`, hence

```text
1 <= h_i <= m.                                             (7)
```

For a low pair `{x,x+a}`, `1<=a<=m`, direct use of (4) gives the exact
permissible-start intervals

```text
Q: [x+a-m,x],                 R: [x-m+1,x+a-m-1].          (8)
```

Take `x=b_i+m` and `a=h_i`.  The permissible `R`-starts in (8) form the
open gap `(b_i,b_(i+1))`, which contains no selected start.  Thus a selected
`Q`-start must hit

```text
J_i=[b_(i+1),b_i+m] in Z_N,             |J_i|=ell_i.       (9)
```

There is a mirror repair at the high end.  For a pair
`{x,x+m+1+ell}`, `1<=ell<=m`, the permissible starts are

```text
R: [x-m+1+ell,x] in Z_N,                 length m-ell,
S: [x-m+1,x-m+ell] in Z_M,               length ell.       (10)
```

Take `x=b_(i+1)-1` and `ell=ell_i`.  The `R`-interval is again the empty
open gap.  A selected `S`-start must therefore hit

```text
K_i=[b_(i+1)-m,b_i] in Z_M,              |K_i|=ell_i.       (11)
```

The same middle-start gap has now forced one low and one high repair
interval.

## Five middle starts

Suppose `r=5`.  From (6),

```text
sum_i d_i = 5m-N = m-2.                                  (12)
```

Therefore

```text
h_i+h_(i+1)=2m-d_i-d_(i+1) >= m+2.
```

By (9), `J_i` lies in the sector
`[b_(i+1),b_(i+2)-1]`; these five sectors are disjoint.  Thus five distinct
`Q`-starts are required.

The five `K_i` are also pairwise disjoint.  Here is an explicit audit of
the wraparound.  Rotate so `b_0=0`, and put `c_i=b_i mod M`.  In cyclic
increasing order, the endpoints of the backward intervals `K_i` are

```text
c_0 < c_3 < c_1 < c_4 < c_2.
```

Their successive endpoint gaps are

```text
c_3-c_0 = 1+d_3+d_4,        c_1-c_3 = 1+d_1+d_2,
c_4-c_1 = 1+d_0+d_4,        c_2-c_4 = 1+d_2+d_3,
M-c_2   = 1+d_0+d_1.
```

Each gap is at least the length `d_i+1` of the interval ending at its
right endpoint (`K_3,K_1,K_4,K_2,K_0`, respectively).  Hence the five
backward intervals are disjoint.  Five distinct `S`-starts are required,
and

```text
q+r+s >= 5+5+5 = 15.                                    (13)
```

## Six middle starts

Now suppose `r=6`.  Then

```text
sum_i d_i = 6m-N = 2m-2.                                (14)
```

An interval `J_i` can meet only its cyclic neighbors: reaching `J_(i+2)`
would require three deficits with sum at least `2m`, contradicting (14).
Moreover,

```text
J_i meets J_(i+1) iff d_i+d_(i+1) >= m.                 (15)
```

Two vertex-disjoint overlaps in (15) would themselves use deficit at least
`2m`.  Thus at most one pair of the six intervals can be hit together, and
every hitting set for the `J_i` has size at least five.

If there is no overlap, all six `J_i` are disjoint.  Then `q>=6`, and the
diameter bound `s>=3` gives

```text
q+r+s >= 6+6+3 = 15.                                    (16)
```

Otherwise rotate indices so `d_0+d_1>=m`.  Equation (14) gives

```text
d_2+d_3+d_4+d_5 <= m-2.                                 (17)
```

Now `K_2,K_3,K_4,K_5` are pairwise disjoint.  Indeed, their endpoints
`c_i=b_i mod M` occur in cyclic order

```text
c_4 < c_2 < c_5 < c_3.
```

The successive gaps are

```text
c_2-c_4     = 1+d_2+d_3,
c_5-c_2     = m-1-d_2-d_3-d_4 >= d_5+1,
c_3-c_5     = 1+d_3+d_4,
M-c_3+c_4   = m-d_3 >= d_4+2,
```

where the inequalities use (17).  These dominate the lengths of the
backward intervals ending at `c_2,c_5,c_3,c_4`.  Consequently `s>=4`;
the low repairs gave `q>=5`, so

```text
q+r+s >= 5+6+4 = 15.                                    (18)
```

Equations (13), (16), and (18), together with the `r>=7` case, prove the
lower bound in (2).  The blocker (3) proves equality and hence (1).

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
later resolution of this `r=4`, all-forward `4m+2` case.  This is a
search-relative status statement, not a claim of priority.  The argument
does not settle the all-forward case for `r>=5` and `m>=3`, or any larger
excess.

## Reproduction

Requires Python 3.11 or later and uses only exact standard-library integer
and set operations.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

The checker reconstructs every canonical copy directly from its omitted
pair for `2<=m<=12`; verifies the complete `Q/R/S` occurrence-graph
classification, the 15-edge blocker, and the exact low/high start formulas;
and audits every five- and six-gap deficit signature in the same parameter
range.  It compares a deterministic record with `EXPECTED.json`.

The computation corroborates the definitions, wraparound conventions, and
repair identities.  The parameter-uniform argument above proves the theorem.
