# Exact crossing number of a star times a triangle: status correction

This directory records a literature-status correction and a short structural
certificate for

\[
  G_m=K_{1,m}\mathbin{\square} C_3 \qquad (m\geq 1).
\]

It does **not** claim a new crossing-number theorem.  Clancy, Haythorpe, and
Newcombe explicitly recorded the exact value in their 2020 survey, explaining
that it follows from the path-product lower bound and a direct drawing.  The
purpose here is to correct a Discovery Net branch that had treated the all-
parameter statement as conjectural, and to give a particularly small
independent lower-bound certificate.

## Exact value

For every integer `m >= 1`,

```text
cr(K_{1,m} square C_3) = floor(m/2) floor((m-1)/2).
```

Write the three copies of the centre of the star as `c_0,c_1,c_2`, and
write the three copies of leaf `j` as `x_(j,0),x_(j,1),x_(j,2)`.
Delete the three edges of the centre triangle and, for every `j`, delete
the edge `x_(j,0)x_(j,2)` of the corresponding leaf triangle.  What remains
is a subdivision of `K_{3,m}`: its branch vertices are

```text
c_0,c_1,c_2 and b_j=x_(j,1),
```

and its three paths from `b_j` are

```text
b_j--x_(j,0)--c_0,   b_j--c_1,   b_j--x_(j,2)--c_2.
```

The paths have pairwise disjoint interiors, including between different
values of `j`.  Since crossing number is unchanged by subdivision and is
monotone under taking subgraphs,

\[
  \operatorname{cr}(G_m)\geq \operatorname{cr}(K_{3,m})
   =\left\lfloor\frac m2\right\rfloor
    \left\lfloor\frac{m-1}2\right\rfloor.
\]

For the reverse inequality, let `H_m=K_{1,1,1,m}`.  Biedl--Chimani--Derka--
Mutzel's maximal-pathwidth-three formula gives

\[
  \operatorname{cr}(H_m)=
  \left\lfloor\frac m2\right\rfloor
  \left\lfloor\frac{m-1}2\right\rfloor.
\]

In a crossing-minimal drawing of `H_m`, replace each degree-three vertex in
the part of size `m` by a sufficiently small triangle, attaching its three
old incident arcs to the three new vertices.  The replacement takes place in
pairwise disjoint crossing-free disks and creates no crossing.  The resulting
graph is exactly `G_m`, so `cr(G_m) <= cr(H_m)`.  Together the inequalities
give the displayed formula.

Keeping the centre triangle in the deletion certificate instead shows that
`G_m` contains a subdivision of `K_{1,1,1,m}`.  Thus the same comparison is
visible entirely at the graph level: `H_m` is a topological minor of `G_m`,
while locally splitting each of its degree-three vertices gives a drawing of
`G_m` with no extra crossings.

## Reproduction

Tested with CPython 3.11.2; only the standard library is required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u expected_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The verifier explicitly constructs the product graph and both subdivision
certificates for a fixed audit suite through `m=1000`, and checks the edge and
vertex identities for every `1 <= m <= 10000`.  It does not compute crossing
numbers.  The universal crossing-number argument is the short proof above;
the code only checks its finite graph-theoretic certificate and arithmetic.

## Scope and trust boundary

- This is a status correction and independent proof packaging, not a novelty
  claim.
- The lower bound uses the published exact value of `cr(K_{3,m})`.
- The upper bound uses the published exact value of `cr(K_{1,1,1,m})` and the
  elementary local vertex-splitting construction.
- The checker uses exact Python integers and sets.  There is no solver,
  floating point, randomness, downloaded input, or exhaustive drawing search.

Bibliographic details and the precise prior-status quotation are in
[SOURCES.md](SOURCES.md).
