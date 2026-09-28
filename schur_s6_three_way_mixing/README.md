# A necessary three-colour image in any classical 537-colouring

Let `A_1,...,A_6` be the six classes of the Fredricksen--Sweet 536-colouring
in [baseline536.txt](baseline536.txt).

**Theorem.** Every valid six-colouring `C` of `[1,537]` has an index `i`
such that `|C(A_i)| >= 3`. Thus it is impossible to reach 537 while each
old class uses at most two output colours, even if every old class splits
and arbitrarily many entries change. Output colour names are unrestricted.
All Schur constraints include repeated summands `x=y`.

The result closes an entire class of coordinated recolouring constructions.
It supplies no valid 537-colouring and no new lower or unrestricted upper
bound for `S(6)`. It is a different necessary condition from the earlier
[four-core splitting theorem](../schur_s6_three_colour_trades/CORE_FAMILY.md):
that theorem counts how many sets split, whereas this one requires at least
three colours inside one old class. Neither implication between the two
conditions is asserted.

## General reduction

The reduction works for any hypergraph `H` of chromatic number `k>=2`, an
optimal independent partition `A_1,...,A_k`, and a hypergraph `H+` obtained
by adding one vertex `z`. Its restriction to the old vertices is `H`.
Suppose `H+` has a proper `k`-colouring `C` with `|C(A_i)|<=2` for every `i`.

**1. Match old classes with output colours.** In the bipartite incidence
graph, join class `i` to every colour used by `C` on `A_i`. For any set `I`
of old classes, its neighbour set has size at least `|I|`. Otherwise colour
the union of these classes by the fewer than `|I|` colours supplied by `C`,
and keep one separate colour for each other old class. This would colour
`H` with fewer than `k` colours. Hall's theorem therefore gives a perfect
matching. Globally rename the output colours so that `i in C(A_i)`.

**2. Give each old class one alternative.** Choose `f(i)!=i` with
`C(A_i) subset {i,f(i)}`. If the class is monochromatic, choose any other
label as `f(i)`; allowing an unused alternative is harmless. Let `t=C(z)`.

**3. Retain only the forward orbit of the endpoint colour.** Let `T` be
the forward orbit of `t` under `f`. It is closed under `f`. Keep `C` on
the classes indexed by `T` and on `z`; restore every other class `A_i`
entirely to its original colour `i`.

The retained part uses only colours in `T`. The restored classes use
distinct colours outside `T` and are independent by hypothesis. Thus an
edge meeting both parts cannot become monochromatic, and edges wholly
within either part remain valid. The restored colouring is proper.

**4. Enumerate one path followed by one cycle.** Write the distinct forward
orbit in order as `(a_0,...,a_(r-1))`, where `a_0=t`. Then

```text
f(a_j) = a_(j+1)          for 0 <= j < r-1,
f(a_(r-1)) = a_e          for 0 <= e < r-1.
```

There is no loop because `f(i)!=i`, so `2<=r<=k`. The case `e=0` is a
directed cycle; `e>0` is a path feeding into a cycle. The lists are
`{i,f(i)}` on the classes in this orbit, `{i}` on all other old classes,
and `{a_0}` at `z`. If **all** these list-colouring problems are impossible,
then the proposed colouring `C` cannot exist.

This proves a general criterion for a three-colour image. It requires no
distance bound, palindromic symmetry, fixed prefix, or specified output
names. There are

```text
sum_(r=2)^k (k!/(k-r)!) (r-1)
```

ordered cases; duplicate equivalent cases do not affect completeness.
For `k=6` the counts by orbit length `2,3,4,5,6` are
`30,240,1080,2880,3600`, totaling **7,830**.

## Why the old Schur hypergraph has chromatic number six

The input word is directly checked to be a valid six-colouring of
`[1,536]`. An elementary Ramsey bound rules out five colours already on
`[1,326]`; the exact value of `S(5)` is not needed.

Define `Q_1=3` and `Q_j=j*(Q_(j-1)-1)+2`. Every edge colouring of `K_(Q_j)`
with `j` colours has a monochromatic triangle. At a chosen vertex, one
colour occurs on edges to at least `Q_(j-1)` neighbours. Either an edge
inside those neighbours has that colour, giving a triangle through the
chosen vertex, or the induced complete graph uses at most `j-1` colours
and induction applies. The values are `3,6,17,66,327`.

From a five-colouring of `[1,326]`, colour the edge `{u,v}` of the complete
graph on `{0,...,326}` by the colour of `|u-v|`. A monochromatic triangle
`u<v<w` gives the forbidden triple `(v-u)+(w-v)=w-u`. This includes equal
summands. Hence no five-colouring of `[1,536]` exists, as needed for the
matching argument.

## Finite verification

[verify.cpp](verify.cpp) constructs every integer Schur edge through 537
directly from addition. A doubling edge has its two distinct vertices;
every other edge has three. For each of the 7,830 cases it assigns the
specified one- or two-colour domains and fixes the new endpoint's colour.

An edge whose initial domains have empty intersection is permanently safe
and is discarded. The remaining solver repeatedly removes a colour from
one vertex when all other distinct vertices of an edge are fixed to that
colour. An empty domain or monochromatic fixed edge refutes that branch.
If propagation stops, the solver chooses a nonsingleton domain and explores
**every** colour in it. Each branch fixes another vertex, so recursion
terminates. There is no cutoff, learned-clause premise, or SAT library.
A terminal model is checked again. Every branch in every case failed:

| Orbit length | Cases | Completed search nodes | Largest case |
|---|---:|---:|---:|
| 2 | 30 | 2,018 | 907 |
| 3 | 240 | 3,532 | 127 |
| 4 | 1,080 | 59,488 | 949 |
| 5 | 2,880 | 462,728 | 5,529 |
| 6 | 3,600 | 1,074,476 | 8,803 |
| Total | 7,830 | 1,602,242 | 8,803 |

The matching and orbit reduction then prove the theorem. The finite check
uses the entire printed partition, not merely the earlier 225 cores; no
extension to every member of the earlier `2^53` family is asserted.

## Reproduction and controls

Python 3.11+ standard library and a C++17 compiler suffice. Tested with
CPython 3.11.2 and GCC 12.2.0. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py
python3 -B verify.py --controls-only --sanitize
```

The Python wrapper compiles in a temporary directory, checks every case
identifier in enumeration order, and compares all row bytes through a
SHA-256 digest, in addition to the compact counts in [expected.json](expected.json).
The full C++ run took about **29 seconds and 11 MiB** resident memory,
single threaded. The release flags are `-O3 -std=c++17 -Wall -Wextra
-Wpedantic -Wconversion -Wshadow`. The checking build uses address and
undefined-behaviour sanitizers. Node-count overflow is explicitly rejected;
colour masks use only six bits, indices are at most 537, and there are
72,092 integer triples. Other integer counters remain far inside 32 bits.

The [control suite](verify.py) compares the solver with literal exhaustive
assignments for **all 19,607** nonempty three-colour domain systems on
intervals of lengths one through five: 16,058 are satisfiable and 3,549
are not. It checks all **93,750** pairs of a no-loop destination map and
endpoint colour, recovering exactly the enumerated 7,830 orbits. All
120 valid three-colourings of `[1,6]` pass the matching and restoration
control relative to the optimal old word `12312`. The 18 corresponding
small orbit models include 16 SAT and 2 UNSAT cases. Seven larger controls
verify the printed 536 word and reject each unchanged one-point extension.
The compiler warnings were clean; representative nontrivial proof cases
were also run under the sanitizers.

Exploratory discovery used a separately encoded one-bit list SAT model.
It agreed on all 7,830 statuses, with at most 132 conflicts in any case.
Its literal list encoder was checked against complete small assignments,
and grouped encodings were compared clause for clause. A separate Python
Boolean enumerator also completed ten six-class cases. None of these
discovery programs or SAT answers is needed to run or trust the published
proof; the direct colour-domain computation above is the finite certificate.

The logical trust boundary is the matching argument, the restoration
argument, literal integer-edge construction, and exhaustive finite-domain
search. No proof assistant is used. An
[independent review](../schur_s6_three_colour_image_review1/REVIEW.md)
confirmed all 7,830 cases with a separate enumerator, using 1,783,338 nodes.
Its scope remains this printed partition and does not change either bound
on S(6). No historical novelty is claimed for Hall's theorem,
the elementary Ramsey bound, or forward-orbit closure. The concrete
three-colour-image obstruction and its complete finite verification are
the claimed increment; a bounded literature check found no exact overlap.

## Input, context, and constructive consequence

The input is the printed Fredricksen--Sweet colouring, with provenance in
the [earlier fixture record](../schur_s6_three_colour_trades/README.md).
Its normalized 536 digits plus newline have SHA-256
`2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d`.
This file is checked both by the wrapper and by direct arithmetic in C++.

The published lower bound is `S(6)>=536`:
[Fredricksen--Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).
The [July 2026 shifted-template preprint](https://arxiv.org/abs/2607.15034)
still uses that bound. Here `S(6)` is the largest colourable endpoint, so
a verified word through 537 would be an improvement.

For construction searches, binary output lists for every old class can now
be discarded altogether. Any successful candidate must permit at least
one old class to use three different colours. Allowing a branching
destination rule is a concrete next family; this theorem neither excludes
that family nor predicts a speedup for unrestricted search.
