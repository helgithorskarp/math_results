# Reflected-pair search toward a Schur-six colouring of 537

The sixth classical Schur number is the largest endpoint admitting six
colours with no monochromatic `x+y=z`, including `x=y`. The published
[Fredricksen–Sweet construction](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
establishes `S(6)>=536`. This experiment searches the full space of valid
536-colourings for one that can be extended to 537. It found another valid
536-colouring, **not** a valid 537-colouring or a new bound.

For a valid word on `[1,536]`, appending colour `c` at 537 creates exactly
one bad equation for each reflected pair `x+(537-x)=537` whose endpoints
both have colour `c`, where `1<=x<=268`. There are no other new equations.
Thus a 536-word with zero reflected pairs of some colour is exactly a
537-colouring. Colour names are interchangeable, so `search.py` targets
colour 5 without restricting the existence of a solution at pair count zero.

The starting published 536-word has pair counts `[64,43,55,38,32,35]` by
colour. The independently checked [saved word](valid536-pairs25.txt) has
counts `[64,43,50,37,25,35]`. It differs from the starting word at 23
positions and has no monochromatic Schur equation among `[1,536]`.
Appending **any** colour still fails; the fewest extension defects are 25.
The earlier [distance certificate](../schur_s6_fredricksen_sweet_distance/README.md)
places every valid 537-word at least 54 changes from that starting word, so
the current word is not unusually close to a proven extension.

## Reproduce the exact search

`search.py` builds the 536-colour SAT formula directly: 3,216 Boolean
variables and 439,520 clauses, comprising exactly one colour per integer
and every `x<=y`, `x+y<=536` prohibition. It adds 268 implication markers
for the target-colour reflected pairs and a PySAT iterative totalizer.
Assuming the negation of totalizer output `k` asks for at most `k` such
pairs. All integer colours remain free at every search step. The solver's
phase hints come from the starting word and then each previous model;
they are not fixed assignments.

With Python 3.11 or later and the pinned dependency:

```sh
python3 -m pip install -r requirements.txt
python3 -B search.py --budget 100000 --target 5 --outdir /tmp/schur-six-reflected
cmp valid536-pairs25.txt /tmp/schur-six-reflected/valid536-pairs25.txt
python3 check.py valid536-pairs25.txt
sha256sum -c SHA256SUMS
```

Using PySAT 1.9.dev15/CaDiCaL 1.9.5, this deterministic replay found
pair counts `31,30,29,28,27,26,25` successively in 3.84 seconds and
returned `UNKNOWN` at bound 24 after 100,000 more conflicts. A separate
one-million-conflict continuation also returned `UNKNOWN` at 24. Neither
status excludes a 536-word with fewer pairs. The saved word and its
extension defect counts are independently checked by standard-library
`check.py`, which enumerates all classical Schur equations. A future
`VERIFIED537.txt`, if produced, must likewise pass direct full-word
enumeration before it is treated as a bound.

The search is a route to a witness, not an upper-bound certificate. A
solver `UNSAT` line without a separate checked proof is explicitly marked
unverified.
