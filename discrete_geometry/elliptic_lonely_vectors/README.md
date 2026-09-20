# Lonely vectors on rational central ellipses

For any finite set of at least two rational points on an origin-centered
ellipse, with no equal or opposite pair, the labelled multiset

`{p_i} disjoint-union {p_i+p_j, p_i-p_j : i<j}`

has at least two entries parallel to no other entry. There is no cardinality
bound. For a rational equation `Ax^2+2Bxy+Cy^2=1`, at least two **original
vectors** are lonely unless `AC-B^2` is three times a rational square.

The proof turns directions into products in an imaginary quadratic norm-one
group. An extremal class modulo roots of unity isolates a fiber with at most
three points. The three possible torsion groups complete the argument.
See [PROOF.md](PROOF.md) for the universal proof and its exact hypotheses.

This gives a cosimple deletion or diagonal reduction for every corank-two
zonotope whose rational Gale vectors lie on a common central ellipse. At least
two deletions work outside the exceptional discriminant class. An explicit
family of size `3m`, for every `m>=1`, shows that in that class **all deletions
can fail**, while a diagonal succeeds. The contained zonotope has the same
dimension and one fewer generator; containment is proper for dimension at
least two.

The general rational Lonely Vector Property and the shifted Lonely Runner
Conjecture were already disproved by
[Blanco–Criado–Santos (2026)](https://arxiv.org/abs/2603.24784).
This restricted positive theorem does not settle the original Lonely Runner
Conjecture. The LVP definition and general Gale correspondence are prior work;
full attribution and the search-relative novelty statement are in the proof.

## Reproduce

CPython 3.11+ and its standard library suffice. No downloads, solvers, or input
data are required. From this directory run:

```sh
python3 verify.py > /tmp/elliptic-lvp-verification.json
cmp EXPECTED.json /tmp/elliptic-lvp-verification.json
sha256sum -c SHA256SUMS
```

The deterministic output has `status: VERIFIED`, 36 exhaustive signed torsion
cases, 27 rational elliptic configurations, and eight Gale configurations with
166 successful minors. Every deletion in those eight configurations is checked
independently against the lonely-original criterion. The checker includes a
published 38-vector rational nonelliptic counterexample, an exact irrational
regular-octagon counterexample, and three rejected malformed inputs.

The canonical evidence payload SHA-256 is
`58c6e29395ab66be1ed3940e9e90686d31b648a7e0ee261feaf399aaffc6809a`.
The recorded CPython 3.11.2 run took 9.74 seconds and used 16,272 KiB maximum
resident memory. Timings depend on the machine.

[verify.py](verify.py) uses exact rational arithmetic and separate determinant
checks for its direction certificates. [EXPECTED.json](EXPECTED.json) retains
compact exact relations and multiplicity evidence. Finite checks corroborate
the handwritten universal proof; they do not replace it or constitute an
independent review. No large or private artifact is required.
