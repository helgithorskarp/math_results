# Complete classification of circulant two-colorings of `K_43`

There is no red/blue circulant coloring of `K_43` without a monochromatic
`K_5`.  More precisely, among all `2^21 = 2,097,152` colorings whose edge
color depends only on cyclic distance in `Z_43`, the minimum number of
monochromatic `K_5`s is

```text
43.
```

Exactly 42 colorings attain the minimum.  They are one orbit under the 21
effective multiplicative automorphisms of `Z_43` and color complementation.
Thus Exoo's `Cyclic(43)` length coloring is the unique optimum under these
operations.  This is an exact computer-assisted classification of the full
undirected Cayley family on `Z_43`, not a search near one seed.

This negative result does **not** construct a 43-vertex Ramsey graph and does
not improve the lower bound for `R(5,5)`.  It rules out the whole circulant
family as a source of such a graph and shows that any successful 43-vertex
construction must break translation symmetry.

## Structural reduction

Let

```text
L = {1,...,21}
```

be the undirected cyclic distance classes.  A circulant coloring is specified
by a subset `S` of red lengths; the other lengths are blue.  For a five-set
`A` of vertices, let `lambda(A)` be the set of the cyclic lengths of its ten
edges.  The set `A` is red exactly when `lambda(A)` is contained in `S`, and
blue exactly when `lambda(A)` is contained in `L \ S`.

Translation acts freely on five-subsets of `Z_43`: if a nonzero translation
fixed such a set, primality of 43 would force its size to be divisible by 43.
Consequently the `C(43,5) = 962,598` five-sets form exactly

```text
962598 / 43 = 22386
```

translation orbits.  Write `w(M)` for the number of these orbits whose
distinct-length mask is `M`.  There are 10,437 masks, with multiplicities

```text
1^189, 2^9660, 4^462, 6^42, 8^42, 9^21, 12^21.
```

Define the subset zeta transform

```text
F(S) = sum_{M subset S} w(M).
```

Then the monochromatic-clique count of the coloring `S` is exactly

```text
q(S) = 43 * (F(S) + F(L \ S)).
```

This identity turns the classification into 21 exact zeta-transform passes
followed by evaluation of every one of the `2^21` masks.  No graph search,
randomness, floating point, or solver is involved.

The minimum of `F(S) + F(L \ S)` is one.  It occurs for 42 masks: 21 have ten
red lengths and 21 have eleven.  Their least integer bitmask has red lengths

```text
{1,4,5,6,7,8,9,12,14,17}.
```

Exoo's red length set is

```text
D = {1,2,7,10,12,13,14,16,18,20,21}.
```

Multiplication by 20 modulo 43, followed by color swap, sends `D` to the
displayed canonical minimizer.  The 21 maps induced by multiplication by a
unit (where multipliers `a` and `-a` induce the same distance permutation),
together with color swap, generate 42 distinct images.  The certificate
checks that these images are entry-for-entry the complete minimizing set.

An additional census in `classification.json` gives the exact full histogram
of the integer orbit objective `q(S)/43`.  In particular, values two, three,
and five do not occur; the next objective after one is four.

## Independent verification

`enumerate_circulant43.cpp` is the production proof computation.  It counts
all anchored five-sets `{0,a,b,c,d}` and divides every mask frequency by five,
because each free translation orbit has exactly five translates containing
zero.  It performs the subset zeta transform, evaluates all `2^21` colorings,
and writes the complete objective histogram and all 42 minimizers.

`verify_classification.py` uses a different orbit construction and a different
minimum-classification algorithm:

- it retains the lexicographically least actual translate of each five-set,
  so it obtains 22,386 orbit representatives without division;
- it scans all `2^20` color-swap-normalized length colorings directly against
  the 10,437 weighted masks, stopping only after the objective exceeds one;
- it finds no zero-objective coloring and exactly the 42 certified
  one-objective colorings;
- it directly recounts the red and blue orbit totals of every minimizer and
  verifies the multiplier/color-swap orbit entry-for-entry; and
- separately, it regenerates the ancillary full objective histogram with a
  standard-library Python zeta transform.

The direct bounded-objective scan is independent of the generator's zeta
enumeration for the main minimum and uniqueness theorem.  Both computations
share the mathematical distance-mask reduction and ordinary compiler or
interpreter semantics.

## Reproduction

Requirements: GCC 12.2 or another conforming C++20 compiler, and Python 3.11
or later.  There are no third-party dependencies.  From this directory run:

```bash
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  enumerate_circulant43.cpp -o enumerate_circulant43

./enumerate_circulant43 classification.regenerated.json
cmp classification.json classification.regenerated.json

python3 verify_classification.py classification.json
python3 -m unittest -v test_classification.py
```

Both enumerator and verifier print:

```text
colorings=2097152 five_set_orbits=22386 distance_masks=10437
minimum_orbits=1 minimum_K5=43 minimizers=42 symmetry_orbits=1
```

On the research host, the optimized GCC 12.2 enumerator took 0.24 seconds,
the independent CPython 3.11 verifier took 19.3 seconds, and the three tests
took 3.5 seconds.  The complete enumerator also passed a run compiled with
AddressSanitizer and UndefinedBehaviorSanitizer.  All counters fit in 32 bits:
the largest zeta entry is the total 22,386 five-set orbits; histogram totals
are accumulated in 64 bits.

SHA-256 values:

```text
1732151505c47e63e64943d0d15b24eed928671b69986052d846168a853d66e2  classification.json
cc04171ea072d0d5d304eb71caa0a2de33d069c6e228c24686f6dc2a3a6c029c  enumerate_circulant43.cpp
6aa16132a7d0bdff734446c7d2f5e0d8eccdcd5caa5155a493799160f4818fdc  verify_classification.py
cb4f7b155203f7c7d22eb0ba6efb9f2481c7d927f3344019e254110369e1263a  test_classification.py
```

## Scope, provenance, and literature

The trust boundary is the proved distance-mask reduction, the two source
implementations, standard C++ and Python semantics, and the compiler or
interpreter.  The checked-in JSON is compact evidence, not an opaque external
input.  Completeness of the classification does not depend on the earlier
Cyclic(43) component certificates in this repository.

Exoo introduced the relevant cyclic coloring in
[*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113).
Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
gives its length set, proves that it has 43 red and no blue `K_5`s, and studies
low-multiplicity perturbations.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) supplies the current upper-
bound context.  Neither the inspected primary sources nor the committed
Discovery Net graph stated this complete `2^21` circulant classification.
Novelty is therefore asserted only relative to those searched sources and
the graph, not as a universal historical-priority claim.
