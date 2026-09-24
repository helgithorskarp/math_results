# Independent review: Tuza for two-neighborhood split graphs

This directory contains the independent computational evidence for the
review of Discovery Net artifact
`bafkreicljpwzk4pmsks62cp5jdfyrduy3jgee4hs5ms74jvfwlzghivdca`.
The target is the computer-assisted theorem that every finite split graph
whose triangle-active independent vertices have at most two distinct clique
neighborhoods satisfies `tau(G) <= 2 nu(G)`.

The checker imports no target code, output, or certificate. It reconstructs
all 384 capped labelled parameter tuples with clique order three through
five. For every graph it computes the exact maximum edge-disjoint triangle
packing and exact minimum triangle edge cover by two separate generic
branching algorithms. It independently evaluates the submitted packing
lower bound with rational arithmetic, obtains the cut upper bound by literal
bipartition enumeration, and checks both against the exact optima. It also
recounts the full finite domain through clique order 112 using `(s,t,c)`
coordinates and checks the exact large-order threshold arithmetic.

Using CPython 3.11 or later and only the standard library, run:

```sh
python3 independent_check.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

On CPython 3.11.2, Linux x86-64, the deterministic run took about 10.3
seconds, single-threaded. Python integers and `fractions.Fraction` are used;
there is no floating-point arithmetic, solver, random choice, external data,
or imported target logic.

The exact small-instance checks corroborate the fragile definitions and
bounds, but they do not independently traverse all 7,636,614,579 represented
tuples. The full finite closure was separately reproduced from the two
published C++ programs and audited at source level, as detailed in
[REVIEW.md](REVIEW.md). The universal reductions remain human mathematics.
