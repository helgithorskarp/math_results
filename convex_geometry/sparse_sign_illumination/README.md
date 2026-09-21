# Sparse-sign polytopes: fractional illumination and covering arrays

For `P(n,k) = {x in R^n: |x_i|<=1, sum |x_i|<=k}`, with integer
`1<=k<=n`, we prove the exact formula

\[
 I_f(P(n,k))=
 \begin{cases}(n/k)2^k,&2k\le n,\\2^k,&2k>n.\end{cases}
\]

When `2k>n`, ordinary illumination is **exactly** the minimum size of a
binary covering array with `n` columns and strength `k`. Arbitrary
illuminating directions can be rounded to sign vectors without losing
any illuminated vertices. Consequently ordinary and fractional
illumination agree in this range exactly for `k=n` and `k=n−1`.
They have an unbounded ratio along `n=2k−1`.

The mechanism is explicit: a direction illuminates a signed `k`-support
exactly when it points inward on that support and puts strictly more
than half its absolute-coordinate weight there. Erdős–Ko–Rado bounds
the resulting intersecting family when `2k<=n`; when `2k>n`, equal
weights work and sign projections are precisely covering arrays.

The strict threshold matters. At `2k=n`, sign vectors illuminate no
vertices; the first branch of the formula applies.

This is a scoped structural result, new to the primary sources checked,
with no historical priority claim. The Hadwiger bound for these
1-symmetric bodies was already proved by Sun–Vritsiou. Covering arrays,
their elementary bounds used here, and unbounded illumination gaps in
general convex bodies are established background. See
[the proof](PROOF.md) and [sources and scope](SOURCES.md).

## Reproduction

Python 3.11 or later; standard library only. From the repository root:

```bash
python3 convex_geometry/sparse_sign_illumination/verify.py
python3 -O convex_geometry/sparse_sign_illumination/verify.py
cd convex_geometry/sparse_sign_illumination
sha256sum -c SHA256SUMS
```

The first two commands compare deterministic output with
[expected.json](expected.json) and exit nonzero on disagreement. The
`--emit` option prints fresh evidence without comparing the fixture.
There is no solver, random search, floating-point arithmetic, downloaded
input, or external package. Tested on CPython 3.11.2, about six seconds
per run in the research environment.

The checker independently enumerates 11,776 bases of defining inequality
systems, obtaining the predicted vertices for seven small bodies. It
compares the entering criterion against both active inequalities and
literal rational-step interior membership on 53,344 vertex/direction
pairs, including zero coordinates and exact ties. It checks capacity on
3,123 absolute-value multisets and replays 138,148 incidences of finite
fractional certificates, comparing primal and dual objectives exactly.
It also checks parity arrays, all 272 possible extra Boolean columns
for two small base arrays, eight rejected double extensions, and ten
negative controls.

The compact [ten-row witness](witness.json) verifies `I(P(5,3))=10`,
whereas `I_f(P(5,3))=8`. Its lower bound is proved without a solver.
This is an illustration of the reduction using a classical covering-
array value, not a new parameter-table entry.

Expected status: `pass`. Entrywise validation SHA-256:

```text
c629106f7032c5379af4d5e204b486c032ccdbdc167ab0de4f90c6d6ad9e2227
```

The finite checks validate implementations and certificates. The
all-parameter theorem rests on the written proof and the classical
Erdős–Ko–Rado theorem; no proof-assistant verification or independent
peer review is asserted by this packet.
