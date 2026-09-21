# An obstruction for nonuniform Erdős--Szekeres blow-ups

For a convex seed, every feasible Baek--Balko nonuniform `(X,Y)` blow-up
has at most `2^(k-2)` points. The proof classifies all equality profiles
and supplies a sufficient certificate using selected convex intervals
of a possibly nonconvex seed. No smaller-case Erdős--Szekeres conjecture
is assumed.

See [PROOF.md](PROOF.md) for the theorem, exact nonnegative deficit,
and boundary cases, and [SOURCES.md](SOURCES.md) for prior work and the
limited novelty audit. This is a modest obstruction for a named
construction family, not a solution of the general conjecture.
Independent review and formalization are pending.

From the repository root, with CPython 3.11+ and no external packages:

```sh
python3 discrete_geometry/erdos_szekeres_convex_interval_obstruction/verify.py
```

The output must match [expected.json](expected.json), including status
`VERIFIED`. Runtime is approximately several seconds. The checker uses
integer arithmetic only. It exhausts 231,053 feasible active profiles
for convex seeds with `2 <= N <= 6`, `N-1 <= k-2 <= 6`, confirming 96
equality profiles; 5,730 profiles on an exact nonconvex seed; and 780
local allocation/equality checks against counts of actual binary words.
The nonconvex fixture gives both a successful local certificate and a
feasible equality profile outside the sufficient hypothesis.

The all-parameter theorem is proved on paper. Finite enumeration only
corroborates it; no solver, floating point, external dataset, random
search, or omitted large certificate is involved.

File integrity, from this directory:

```sh
sha256sum -c SHA256SUMS
```
