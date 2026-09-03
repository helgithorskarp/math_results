# Majority C-colouring of moderately imbalanced 3D Hamming graphs

This directory proves an exact formula for a broad imbalanced part of the
three-dimensional Hamming-graph problem posed by Bujtas, Dettlaff,
Furmanczyk, and Laskowska.

## The theorem

Let

```text
n1 >= n2 >= n3 >= 2,
Ni = ni - 1,
h = ceil((N1 + N2 + N3)/2).
```

Assume `h >= N1`, and put

```text
r = h - N1,
s = r + 1.
```

Then

```text
chi_bar_ge(K_n1 square K_n2 square K_n3) = floor(n2*n3/s).
```

Here `chi_bar_ge` is the maximum number of colours in a vertex colouring in
which every vertex has at least half of its neighbours in its own colour
class.  Equivalently, each colour class induces minimum degree at least `h`.

The hypothesis is the moderately imbalanced (near-triangle) range

```text
ceil((n1+n2+n3-3)/2) >= n1-1.
```

It contains every balanced triple.  For `n1=n2=n3=n`, the formula becomes
`floor(n^2/ceil((n+1)/2))`, recovering the previously proved balanced result.

The proof also classifies the smallest possible majority sets: every set of
size `n1*s` inducing minimum degree at least `h` is, after permuting tied
coordinates, a coordinate rectangle `K_n1 square K_s` with the third
coordinate fixed.  When `s=1`, this means a full `K_n1` coordinate line.

## 1. Sharp lower bound on a colour-class size

Let `C` induce minimum degree at least `h`, fix `v in C`, and let `ai` be the
number of points of `C` on the `i`-th coordinate line through `v`, excluding
`v`.  Write `A=a1+a2+a3`.  Then

```text
0 <= ai <= Ni,    A >= h.
```

Let `B` be the points of `C` at Hamming distance two from `v`.  A selected
point on line `i` has exactly `ai` possible neighbours among `v` and the same
line.  It consequently needs at least `h-ai` neighbours in `B`.  (These
quantities are nonnegative because `h >= N1 >= Ni`.)  Every point of `B` is
adjacent to at most two selected coordinate-line points.  Double counting
gives

```text
2*|B| >= sum_i ai*(h-ai),

|C| >= 1 + A + (1/2)*sum_i ai*(h-ai).                 (1)
```

For fixed `A`, the sum of squares `sum_i ai^2` is maximised by filling the
largest caps first.  This follows either from majorisation or by repeatedly
moving one unit from a smaller occupied coordinate to a larger unfilled one.

Since `h=N1+r`, first suppose `A=N1+t`, where `r <= t <= N2`.  Substituting
the extremal vector `(N1,t,0)` in (1) and subtracting
`(N1+1)(r+1)` gives

```text
(t-r)*(1 + (N1-t)/2) >= 0.                            (2)
```

If `A=N1+N2+t`, where `0 <= t <= N3`, the value at `t=0` is already at least
the target by (2), and adding the third coordinate increases the right side
by

```text
t*(1 + (h-t)/2) >= 0.                                 (3)
```

These ranges exhaust `A>=h`.  Thus every colour class has at least

```text
(N1+1)(r+1) = n1*s
```

vertices.  Dividing the order `n1*n2*n3` of the graph by this lower bound
proves

```text
chi_bar_ge <= floor(n2*n3/s).                         (4)
```

Equality in the class-size bound forces equality throughout (1)--(3).  Hence
`A=h` and the local profile is `(N1,r,0)` up to an allowed coordinate
permutation.  Equality in both incidence counts says that every distance-two
point is adjacent to both of its coordinate-line projections.  There are
exactly `N1*r` such points, forcing the full Cartesian rectangle.  There can
be no distance-three point because (1) is also sharp.  This proves the stated
classification.

## 2. Rectangular star-partition lemma

The matching construction uses the following independent combinatorial
lemma.

**Lemma.** If `m >= n >= s >= 1`, the cells of an `m` by `n` rectangle can be
partitioned into exactly `floor(m*n/s)` pieces, each of at least `s` cells and
each contained in a single row or a single column.

**Proof.** Write `n=a*s+b`, with `0 <= b < s`.  In every row, reserve `b`
cells.  The other `a*s` cells split into `a` row pieces of size `s`.  It
remains to choose the reserved cells so that their `m*b` cells split into
`q=floor(m*b/s)` column pieces.

The case `b=0` is finished.  Otherwise, let

```text
p = floor(m/s),    m*b = q*s+t,    0 <= t < s.
```

Choose

```text
u = max(b, ceil(q/p)).
```

We have `b <= u <= min(n,q)`.  Indeed `q>=b`; and, on writing `m=p*s+v`,

```text
q = p*b + floor(v*b/s) <= n*p.
```

Choose integers `1 <= kj <= p` on `u` columns with `sum kj=q`.  Their total
unused capacity is

```text
sum_j (m-s*kj) = u*m-q*s >= b*m-q*s = t.
```

Thus choose `0 <= ej <= m-s*kj` with `sum ej=t`, and prescribe column degrees
`dj=s*kj+ej` on those `u` columns and zero on the others.

There is a simple bipartite graph with all `m` row degrees equal to `b` and
these column degrees.  To see this directly from the Gale--Ryser criterion,
for every `1 <= k <= m`,

```text
sum_j min(k,dj) >= sum_j k*dj/m = k*b.
```

The graph selects the reserved cells.  Column `j` has `s*kj+ej` selected
cells, which split into `kj` pieces of size at least `s`.  The total number of
row and column pieces is

```text
m*a + q = floor(m*n/s).
```

This proves the lemma.

## 3. Matching majority colouring

Apply the star-partition lemma to the `n2` by `n3` grid with the above `s`.
The hypotheses imply `s<=n3`: indeed

```text
r = ceil((N2+N3-N1)/2) <= ceil(N3/2) <= N3.
```

For every row or column piece `D`, use `[n1] x D` as a colour class.  These
sets partition the Hamming graph.  Each induces `K_n1 square K_|D|`, so every
vertex has at least

```text
N1 + (|D|-1) >= N1+(s-1) = h
```

same-colour neighbours.  There are `floor(n2*n3/s)` classes, meeting (4).

## Reproduction

The checker is deterministic, uses only exact Python integers and sets, and
has no third-party dependencies.

```bash
python3 verify.py --max-side 24 --direct-max-side 8
python3 -m unittest -v test_verify.py
```

The first command prints

```text
VERIFIED triples=1475; shell_profiles=2322698; direct_triples=71; max_side=24; sha256=afa452e4f97e12496cffaaf1576d09cc85189bc5ea2f054a4ab5f7d743af5916
```

`verify.py` constructs every relevant star partition through the requested
range, checks coverage, line support, piece sizes, class counts, every local
shell inequality, and direct definition-level majority colourings for the
smaller range.  The program prints a canonical SHA-256 digest of its summary
records.  The computation corroborates the construction and catches boundary
or indexing errors; the universal theorem rests on the proof above.

Tested with CPython 3.11.2.  No floating point, randomness, solver verdict, or
external data is used.

## Literature and scope

The primary source is:

- C. Bujtas, M. Dettlaff, H. Furmanczyk, and A. Laskowska, *Majority
  C-coloring in Cartesian products*, arXiv:2608.27669v1 (2026),
  https://arxiv.org/abs/2608.27669

Its Open Problem 2 asks for the three- and four-dimensional imbalanced Hamming
graphs.  Proposition 15 supplies general lower bounds but not this exact
formula.  This result solves the stated three-dimensional problem in the
range `h>=N1`; it makes no claim about the more strongly dominant range
`h<N1` or about four dimensions.
