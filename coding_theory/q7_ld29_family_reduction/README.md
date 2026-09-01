# Family-excess reduction of the Q7 size-29 question

## Theorem

Let `Q_7` be the binary 7-cube.  If `Q_7` has a locating-dominating
code of cardinality at most 29, then it has a cardinality-29
locating-dominating code `C` with all of the following properties.

1. At least 41 vertices have singleton identifying sets.
2. At least 12 codewords are isolated in the induced graph `Q_7[C]`.
3. The induced graph has at most 33 edges.
4. There are at least 24 unordered codeword pairs at Hamming distance two.
5. Some isolated codeword has a non-codeword neighbor whose identifying set
   is the singleton consisting of that codeword.

Consequently a complete search may, after a cube automorphism, impose

```text
0 in C;
e_i not in C                         for 0 <= i < 7;
e_0 + e_j not in C                   for 1 <= j < 7.
```

The graph on coordinates `1,...,6` in which `ij` is an edge when
`e_i+e_j` is a codeword has no isolated vertex and no two-vertex connected
component.  Up to `S_6`, there are exactly 115 such graphs.  Checked DRAT
certificates exclude five dense canonical graphs (indices 110--114, with
12, 13, 13, 14, and 15 edges).  Thus the former four minimum-degree branches
for the size-29 question reduce losslessly to 110 surviving, much more tightly
fixed orphan-local branches.

This is a structural and algorithmic reduction, not a nonexistence proof.
The cases of cardinality 28 and 29 remain open.

## Family-excess proof in the minimum-29 case

Suppose first that 29 is the minimum cardinality.  No codeword `c` can have
all of its seven neighbors in the code.  Otherwise deleting `c` leaves all
old non-codeword signatures unchanged, while the new non-codeword `c` has
the seven neighbors as its signature.  This signature cannot equal an old
one because two distinct radius-one balls in a cube intersect in at most two
vertices.

Use the Honkala--Laihonen--Ranto partition into excess-zero points, codeword
couples, and father/son families.  Let

- `p` be the number of excess-zero points;
- `q` be the number of couples;
- father `j` have identifying-set size `i_j` and `s_j` sons; and
- `D=sum_j(i_j-2)`.

Here `3 <= i_j <= 7` and `s_j <= binom(i_j,2)`.  The total excess is

```text
8*29 - 128 = 104.
```

Counting vertices and excess in the partition gives

```text
128 = p + 2q + sum_j(1+s_j),
104 = 2q + sum_j(i_j-1+s_j),
```

and hence

```text
p = 24 + D.                                      (1)
```

Let `a` be the number of isolated codewords.  A codeword labels at most one
singleton signature of a non-codeword, so `p <= 29+a` and

```text
a >= D-5.                                        (2)
```

Couples use two non-isolated codewords.  Therefore

```text
2q <= 29-a <= 34-D.                              (3)
```

The number `M` of vertices in families satisfies

```text
M = 104-D-2q >= 70.                              (4)
```

Put `d=i-2`.  A family of defect `d` has at most

```text
h(d) = 1 + binom(d+2,2),
h(1),...,h(5) = 4,7,11,16,22,
```

vertices.  Since `h(d) <= 22d/5`, (4) implies `D >= 16`.

The equality case is impossible.  Exact integer optimization shows that the
only defect-16 partition with capacity at least 70 is

```text
q=9, M=70, (d_j)=(5,5,5,1),
```

and every family is full.  Equations (2)--(3) force `a=11`, so the 11
isolated codewords and 18 codewords in couples account for the whole code;
no family contains a codeword.  In particular the three full `F_7` fathers
are non-codewords.

If `x` is a full non-codeword `F_7` father, all seven neighbors of `x` are
codewords, all 21 distance-two vertices are its sons, and every
distance-three vertex is a non-codeword.  Any other non-codeword `F_7`
father must therefore be at distance at least five from `x`.  Three full
`F_7` fathers would be three words of pairwise distance at least five in
`Q_7`, but `A(7,5)=2`: after translating one word to zero, the two other
supports both have size at least five and hence have symmetric difference
of size at most four.  Thus `D>=17`.  Equations (1)--(2) now give

```text
p >= 41, a >= 12.                                (5)
```

## Why the reduction also covers a minimum-28 code

The published lower bound is 28.  If the true minimum is 28, use the
previously proved size-28 family-excess theorem: there is a size-28 code with
at least 50 singleton signatures and 22 isolated codewords.  Adding any
non-codeword preserves location-domination and gives size 29.  Only the eight
identifying sets in the added word's closed ball change, and at most seven
old isolated codewords acquire a codeword neighbor.  The enlarged code
therefore has at least 42 singleton signatures and 15 isolated codewords,
which are stronger than (5).  Hence the stated size-29 search reduction is
lossless whether the unknown minimum is 28 or 29.

## Edge, distance-two, and orphan consequences

All induced code edges lie on the at most `29-12=17` non-isolated
codewords.  Splitting an `n`-cube subset between two coordinate layers gives
the inductive upper bound

```text
E_n(m) = max_{r+s=m} (E_{n-1}(r)+E_{n-1}(s)+min(r,s)).
```

Starting with `E_0(0)=E_0(1)=0` gives `E_7(17)=33`, proving the edge bound.

Write `b=29-a` and let `o=p-a` be the number of singleton signatures on
non-codewords.  At most `b` of these are labeled by non-isolated codewords.
Thus at least

```text
o-b = p-29 >= 12
```

isolated codewords have an orphan neighbor.  For such an isolated codeword
`c`, form a graph `H_c` on the seven coordinate directions, with edge `ij`
when `c+e_i+e_j` is a codeword.  The orphan direction is isolated.  Every
other direction has positive degree, and `H_c` has no two-vertex component,
or the two corresponding neighbors of `c` would have equal signatures.
The other six vertices therefore span at least four edges.  Double counting
the resulting distance-two codeword pairs yields

```text
A_2(C) >= 2(p-29) >= 24.
```

Choosing one orphan pair `(c,c+e_0)` gives the displayed normalization.  The
same local graph argument leaves a six-vertex graph with no isolates and no
two-vertex component.  Exhausting its `2^15` labeled edge sets and quotienting
by all `6!` permutations gives 115 canonical branches.  Five of these
branches are excluded by the finite certificates below.

## Reproducibility

The standard-library verifier checks the defect partitions, the unique
defect-16 frontier, `A(7,5)=2`, the edge recurrence, and the 115 local graph
orbits:

```bash
python3 verify_reduction.py
```

The PySAT program preserves the exact search.  A compact canonical branch
can be generated and attacked, for example, by

```bash
python search_q7_ld29.py \
  --no-structural --local-graph-index 0 \
  --build-only \
  --write-cnf /scratch/q7-ld29-local-000.cnf
```

The `--no-structural` input still contains domination, all essential
distance-two separation clauses, exact cardinality 29, the complete orphan
normalization, and all 15 unit clauses fixing the selected local graph.
Omitting the option additionally encodes the proved singleton, isolation,
edge, and distance-two bounds; `--no-pair-bounds` omits only the last,
largest cardinality block.  Solver timeouts on the 110 surviving branches are
not results.  Proof logs must remain under `/scratch`.

### Certified exclusion of branches 110--114

The two densest branches need only the compact core encoding.  Branches
110--112 use the proved singleton, isolation, and edge bounds, but not the
large distance-two cardinality block.

| branch | local edges | variables | clauses | CNF SHA-256 |
|---:|---:|---:|---:|:---|
| 110 | 12 | 10,432 | 183,619 | `adc66a1c31ba6334298dc8f34dc1637deddaebdf947cd42e30b7e889990d518f` |
| 111 | 13 | 10,432 | 183,619 | `a74e12f6668af46325b504a7dbb412ededa6a7e7cdbc40d80cd4e235c85505b1` |
| 112 | 13 | 10,432 | 183,619 | `869c77eecec11ca81d3a8bca45618c874474f7d45d82441c4bc49733ae39d692` |
| 113 | 14 | 1,920 | 19,551 | `139bb5a16c3bea20b9b42fa2d1f66cc42a7690b6deb6e7c90350400928eed6c3` |
| 114 | 15 | 1,920 | 19,551 | `e3b076f86f91ef7b77705a0dce5e8bc6be387507dff0d28d78bd95687aa717a6` |

For branches 110--112 use

```bash
python search_q7_ld29.py --no-pair-bounds --local-graph-index 110 \
  --build-only --write-cnf /scratch/q7-ld29-branch110.cnf
```

Change the index as required.  For branches 113 and 114 replace
`--no-pair-bounds` by `--no-structural`.  Each CNF was solved by the Debian
CaDiCaL 1.5.3 binary with a plain DRAT trace, for example

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-branch114.cnf \
  /scratch/q7-ld29-branch114.drat
drat-trim \
  /scratch/q7-ld29-branch114.cnf \
  /scratch/q7-ld29-branch114.drat
```

DRAT-trim returned `s VERIFIED` for all five inputs.  The proof hashes were

```text
branch 110  f6775c805ea0337dcdd4a60e337e408dbaec9b0feb6ec676c70d07b521f6381b
branch 111  87c4f6cfef93610e92d8dcb85f2a0cd6ec8789e6d7e5d5061264d2773ea004c9
branch 112  a97b7b188681dc6ccd44cbda908ce902c33a606ed94709f5d81d6db8c8d528c0
branch 113  109c2f7da60a149fd14ca5a8ba48d43139d9bbae9b309ead99e6d07f5aa45eeb
branch 114  10ec9899bb2cf019620c6bd2650c04f28a90ebff95c3571fb21773d40336738e
```

The proof files (82, 37, 40, 16, and 12 MiB respectively) are deliberately not
committed.  They are quickly regenerated from the versioned CNFs and are
kept only under `/scratch`.  As a solver-level cross-check, PySAT's independent
Kissat 4.0.4 binding also returned UNSAT on the same five formulas.  The
DRAT-trim Debian package used for the certificate audit was version
`0.0~git20240428.effa1dc-2`; its package SHA-256 was
`a2613ed11f3b2ee1a183ed64ba265a7d88b9b892cef1a40a9097132ccabcc31f`.

Versions used:

```text
Python 3.11.2
python-sat 1.9.dev15 (CaDiCaL 1.9.5 binding)
pypblib 0.0.4
CaDiCaL 1.5.3 (standalone proof-producing solver)
DRAT-trim 0.0~git20240428.effa1dc-2
```

The canonical branch-zero input without the optional structural blocks has
1,920 variables, 19,551 clauses, and SHA-256
`d4a73055e91fec272fa338cd40af5246ab1463bda4918cfa4e6b767ada9f1b52`.
Source SHA-256 values are

```text
requirements.txt     639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
local_graphs.py      35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4
search_q7_ld29.py    3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614
verify_reduction.py  7efbb7e98775f7ffca78a3284b5bf7fa2eecd60ef71c6f3060376e2fa52e70c9
```

The verifier uses only Python's standard library.  The structural theorem is
hand-checkable; computation is used only for small finite arithmetic and
orbit enumerations, each of which is explicitly reconstructed by the source.

## Scope and novelty

Honkala, Laihonen, and Ranto introduced the family partition and proved the
general lower bound.  Junnila, Laihonen, and Lehtila still listed the Q7
interval as 28--32 in 2021/2022.  The graph now contains a verified 30-word
construction, so the unresolved interval is 28--30.  Targeted primary-source
searches through 2026-09-01 found no size-29 specialization forcing 12
isolated codewords, an orphan-pair normalization, or the 115 local graph
branches.  The reduction is therefore apparently new relative to the
searched sources, not a historical-priority claim.

- I. Honkala, T. Laihonen, S. Ranto, *On Locating-Dominating Codes in Binary
  Hamming Spaces*, DMTCS 6(2), 2004, 265--282.
  <https://doi.org/10.46298/dmtcs.322>
- V. Junnila, T. Laihonen, T. Lehtila, *Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces*, Designs, Codes and
  Cryptography 90 (2022), 67--85.
  <https://doi.org/10.1007/s10623-021-00963-8>
