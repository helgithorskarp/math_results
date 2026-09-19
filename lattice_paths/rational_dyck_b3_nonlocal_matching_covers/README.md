# Nonlocal matching covers in `D(a,3)`

## Result

Let `a>3`, `gcd(a,3)=1`, and write

```text
a = 3m + epsilon,    epsilon in {1,2}.
```

For every `0 <= z <= m-1`, put `n=m-z` and define the two rational-Dyck
paths by their three `R`-run lengths:

```text
X_z = (a-1-2z, z+1, z),
Y_z = (2m+epsilon-z, z, m).
```

Thus a triple `(r,s,t)` denotes `R^r U R^s U R^t U`.  Then

```text
X_z  <_M  Y_z
```

is a matching-order cover, and both score levels are singletons.  The
Lagrange fibres of the two paths are separated by exactly `m-z-1` steps in
the complete height-three Lagrange chain.  In particular, `X_0 <_M Y_0`
gives matching covers whose Lagrange-fibre distance tends to infinity.
This disproves adjacent-fibre locality for matching covers even in the
fixed-height family `D(a,3)`.

The score gap has the following positive closed form.  If `F_k` and `L_k`
are the Fibonacci and Lucas numbers, respectively, then

```text
5 (M(Y_z)-M(X_z))
 = 2 F_(2z+1) (4 L_(6n+2epsilon-5) + 3 L_(2n+2epsilon-2))
   + 10 F_(2z) F_(6n+2epsilon-4).
```

This supplies `floor(a/3)` explicit covers at every admissible endpoint.
The theorem is a structural bridge from the previously classified matching
orientation of adjacent Lagrange fibres to genuinely global matching-cover
relations; it is not a complete classification of every matching cover in
`D(a,3)`.

The proof is in [PROOF.md](PROOF.md).

## Reproduction

Requirements: CPython 3.11 or later; no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I verify.py --max-a 180
PYTHONDONTWRITEBYTECODE=1 python3 -I independent_check.py --max-a 60
PYTHONDONTWRITEBYTECODE=1 python3 -I test_verify.py
sha256sum -c SHA256SUMS
```

`verify.py` uses the height-three run matrices and checks the closed gap,
the singleton-cover assertion, the layer separation, and the exact
Lagrange-fibre distance over the requested range.  `independent_check.py`
imports none of that code: it generates binary rational-Dyck words directly
and computes matching scores with scalar continuants from the literal
adjacency encoding.

The expected summaries are recorded in [expected.json](expected.json).
The principal output lines are

```text
EXACT VERIFIED D(a,3) NONLOCAL MATCHING COVERS; 4<=a<=180; endpoints=118; paths=221427; covers=3540; max_fibre_distance=58; row_sha256=5d666573c7517dd5332a27c61ad367373902f175cffa955b07bb5343733a4897
INDEPENDENT VERIFIED D(a,3) NONLOCAL MATCHING COVERS; 4<=a<=60; endpoints=38; paths=8607; covers=380; max_fibre_distance=18; row_sha256=1dfc7e32caabff677666c9508c8c2d3b8d52c4875f92861505d72d7a2b640fe1
```

## Dependencies and literature boundary

The proof uses the complete adjacent-Lagrange-fibre matching orientation on
`D(a,3)`, Discovery Net contribution
`bafkreibdaxha2iirytu6khafs6nnaag66ul3anwjop6j4hz7oepqz6qr54`.  The
needed consequences are restated precisely in the proof and checked over
the finite validation range.

Apruzzese and Cong define the two orders and pose cover classification in
[*On Two Orderings of Lattice Paths*](https://arxiv.org/abs/2310.16963).
Li's current public manuscript and source at commit
`845a030e87c39f24990dce48e5aad2e48d569318` give a global exact cover
algorithm and a different nonlocal matching-cover family in `D(n,n-1)`, but
do not state this height-three family:
[lattice-path-orders](https://github.com/crabsatellite/lattice-path-orders/tree/845a030e87c39f24990dce48e5aad2e48d569318).
Targeted primary-source, repository-source, web, and committed-graph searches
found no duplicate of the theorem here.  This is a search-relative novelty
statement, not a claim of historical priority.

## Trust boundary

Universal validity rests on the proved adjacent-fibre orientation theorem,
the displayed Fibonacci matrix formulas, elementary summation identities,
and the layer argument in `PROOF.md`.  The finite runs corroborate rather
than prove the universal statement.  Both checkers are bespoke Python, not
proof-assistant kernels.  Reproduction additionally trusts CPython exact
integer arithmetic, SHA-256, the operating system, and hardware.  There is
no floating point, randomness, solver, external dataset, generated input,
or omitted large certificate.
