# A fixed nine-type obstruction to centered-cover corrections

The proposed centered-LP cover estimate cannot be repaired by a
subquadratic error even when the number of neighborhood types is fixed.
For every integer `p>=2`, we construct a capped split graph with

```text
k = 4p,       r = 9,       D = sum_i |S_i| = 17p,
|V| = 13p-4,  |E| = 25p^2-6p,
H = nu_c* = nu* = 15p^2/2-2p,
tau = 8p^2-2p = binom(k,2).
```

For `Phi_k(H)=k^2/4-k/2+H-H^2/k^2+1/4`, this gives

```text
tau-Phi_k(H) = p^2/64+p/8 = k^2/1024+k/32.
```

Consequently no fixed-type `o(k^2)` error repairs this bound, including
`cD`, `crk`, or `C(r)k`. At `p=5`, the exact cover number is 190 while
the proposed bound rounds up to 189.

This removes the growing-type limitation of the
[earlier obstruction](../tuza_centered_cover_obstruction/README.md).
It does **not** refute Tuza: an explicit packing of `5p^2` centered
triangles proves `tau<2nu` for every member. It also does not refute the
accepted spoke-saturated theorem. Here the spoke count is `17p^2-4p`,
so `E/2-H=p^2`. No minimality of nine types is claimed.

The construction comes from a general exact identity: complete the core
groups in an independent blow-up of a split graph, and give each group
`p-1` new private centers. Each of `tau`, `nu_c*`, and `nu*` then equals
`p^2` times its seed value plus `s*binom(p,2)`, where `s` is the seed
clique order. The [proof](PROOF.md) uses transversal averaging and
explicit fractional packings, without finite-field restrictions.

The universal proof is complete but unformalized; independent review of
this new result is pending. See [sources and scope](SOURCES.md).

## Reproduce

With Python 3.11.2 or compatible Python 3, from this directory:

```sh
python3 check.py > /tmp/fixed-type-cover-audit.json
cmp /tmp/fixed-type-cover-audit.json AUDIT.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) uses only the standard library. It exhausts the
seed's `2^19` edge subsets, checks exact centered primal and full dual
certificates, explicitly expands all transversals at `p=2,3`, and checks
actual graphs at `p=2,3,5,11,16,31`. Every actual triangle is tested
against the full dual, and actual packing witnesses and edge partitions
are verified. Five damaged certificates must be rejected.

The expected output is [AUDIT.json](AUDIT.json), with environment and
runtime details in [RUN.json](RUN.json). There are no solvers, random
inputs, external datasets, or bulk certificate dependencies. The hashes
serialize the generated packing triangles as ASCII `u v w\n` records in
generator order. Exact finite audits support the implementation; the
universal quantifiers and the large-instance cover lower bound rest on
the proved averaging and completion identities.

The remaining positive research target is more selective. These examples
have `H/k^2 -> 15/32`, above the potentially critical range near `1/4`.
They do not exclude a useful cover estimate restricted to smaller `H`,
or another route to an effective Tuza theorem for fixed type count.
