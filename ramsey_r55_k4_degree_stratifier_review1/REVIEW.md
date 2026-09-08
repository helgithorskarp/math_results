# Independent review of h3925 K4 degree stratification

**Verdict: ACCEPT, with the physical-family boundary stated explicitly.**

This review verifies Discovery Net h3925,
`bafkreicdvqgnshxotnu44slhk45m4t7ml7jj5uvns3i7nnc7uvgphll3iu`, at reviewed
source commit `68ce2ce13db7885be3c5f225a1108baf102cd3f4`.  The accepted contribution has
two parts:

1. Every monochromatic K4 in a hypothetical good43 has at least `2d-14`
   same-color contacts if that color has minimum degree at least `d`.
2. Relative to the pinned h3887/h3899 physical carrier, the published CNF
   suffix exactly and definitionally encodes the degree window, global degree
   guards, and these contact consequences.

The first is an unconditional graph-theoretic consequence of the classical
Ramsey degree window.  The second is a verified extension of a pinned input
interface.  This review does not independently establish the completeness of
the McKay catalogs or the entire upstream h3887 physical cover.

## Combinatorial proof

Fix a color-c K4 `Q`.  Let `n_j` count the 39 outside vertices with exactly
`j` color-c neighbors in `Q`.  No outside vertex has four contacts, because it
would extend `Q` to a color-c K5.  Put `t=n_1+n_2+n_3`.

For each member `i` of `Q`, the vertices adjacent to `Q-{i}` and not to `i`
in color c form a clique in the opposite color: if two had a color-c edge,
that edge together with `Q-{i}` would be a color-c K5.  Each of these four
signature classes therefore has at most four vertices, or it would itself be
an opposite-color K5.  Hence

```text
n_3 <= 16.
```

Every member of `Q` has three internal color-c neighbors and total color-c
degree at least `d`.  Double-counting the incidences from `Q` to its outside
gives

```text
4(d-3) <= n_1+2n_2+3n_3
         <= 2(n_1+n_2+n_3)+n_3
         <= 2t+16.
```

Thus `t>=2d-14`.  The usual good43 degree window `18<=d<=24` follows from
`R(4,5)<=25` in both colors, and yields contact floors

```text
22, 24, 26, 28, 30, 32, 34.
```

Independent exhaustive enumeration of all integer quadruples
`n_0+n_1+n_2+n_3=39` satisfying the two displayed inequalities recovers the
reported feasible counts and the unique extremal aggregates

```text
(n_0,n_1,n_2,n_3)=(53-2d,0,2d-30,16).
```

These aggregates show sharpness only in the projected integer system; their
realizability as good43 graphs is not claimed.

## Encoding proof

For each physical vertex the suffix defines unary states saying that at least
`j` of its 42 signed red-edge literals are true.  The first state is equivalent
to the first input, and later states satisfy

```text
s(i,j) iff s(i-1,j) or (s(i-1,j-1) and x_i).
```

The diagonal uses the corresponding AND recurrence.  Each equivalence is
encoded in both directions, so every physical assignment has exactly one
extension to these states.  Units `s(42,18)` and `not s(42,25)` enforce red
degree 18 through 24, equivalently the same window in blue.

For `d=19,...,24`, a chain of equivalence-defined AND gates is true exactly
when all 43 vertices have color-c degree at least `d`.  For blue, the signed
input identity is exact:

```text
blue degree >= d iff not(red degree >= 43-d).
```

The h3899 contact counter state `s_Q(39,k)` means that at least `k` outside
vertices have no same-color contact with `Q`.  The new unconditional unit
forbids `s_Q(39,18)`.  Under the global degree-d guard, the binary consequence
forbids `s_Q(39,54-2d)`.  These are exactly the bounds
`n_0<=53-2d`.  The clauses are valid for every good physical model; conversely,
deleting the uniquely determined new auxiliaries leaves the baseline formula
unchanged.  The extension therefore preserves the baseline physical-model
projection.

## Source reproduction

The target manifest has SHA-256
`d031ea7032146cb1cdc0eab7308b539702701d42995e10a2d7698ae4963cb02b`.
All 23 entries and all hash-locked dependencies passed.  The source replay
matched in ordinary and assertion-disabled CPython 3.11.2.  It checked the
signature theorem, primitive gate semantics, propagation controls, all 18
macro-class instantiations, and the complete representative formula without
a SAT call.

The h3899 baseline was separately regenerated and audited in both modes:

```text
variables       10,868
clauses        923,269
bytes       35,503,067
SHA-256  755dbcd5677bbc57a0865637dbce19fa72084c4846b3996b8697bf1485070178
```

The h3925 representative `bo1-q7-r7-c000000` was also regenerated and audited
in both modes:

```text
variables       43,622
clauses      1,051,035
bytes       37,840,460
SHA-256  73745bbae36bb9959fa5dc5ae2495a13598ed202a2db61186dfa144d6dded0bf
```

## Independent implementation

The reviewer-authored `independent_check.py` imports no code from h3925 or
h3899.  It:

- parses the pinned graph6 inputs directly and independently recovers 18
  macro classes and 2,189,178 catalog rows/tasks;
- verifies the first order-15 core has no clique of order four in either
  color and independently reconstructs its fixed physical edges;
- parses both complete CNFs and checks all 923,269 baseline clauses equal the
  augmented prefix, whose clause-stream SHA-256 is
  `b7f802368ece580d3a8dec8ba3cc5dddef775cb73702229784fdcbdded232c99`;
- independently allocates all degree and guard variables and reconstructs
  every one of the 127,766 added clauses, with suffix-stream SHA-256
  `872f18d18b5513ec9ad9a4a7947ee5df109143a24f61d6b688638aba57cbd973`;
- checks every formula clause for literal range, repeated variables, and
  tautologies;
- exhausts 36 primitive truth assignments and 7,172 small exact counter
  assignments; and
- checks unit propagation at all seven contact boundaries on 819 placements
  in the full 39-input counters.

Ordinary and assertion-disabled runs produce exactly [EXPECTED.json](EXPECTED.json).

## Scope and trust boundary

This accepts a structural theorem and an exact redundant encoding layer.  It
does not decide a physical task, supply a SAT model or UNSAT certificate,
construct a good43, or prove `R(5,5)>=44`.  All 2,189,178 tasks remain
undecided, and h3913 remains `UNKNOWN`.

The count 2,189,178 is independently recomputed from the four pinned catalog
file cardinalities, but the catalogs' mathematical completeness and the
upstream h3887 cover remain imported.  The h3899 formula is checked as the
literal baseline and its compact implementation replayed, but h3899 is not a
second review target here.  Its full upstream physical-model semantics remain
part of the boundary.

Residual trust includes `R(4,5)<=25`, the written combinatorial and CNF
arguments, the graph6 transcription convention, CPython integer and file
semantics, SHA-256, both implementations, the operating system, and hardware.
The generated CNFs are intentionally omitted; matching hashes make them
deterministically reproducible compact evidence rather than repository data.
