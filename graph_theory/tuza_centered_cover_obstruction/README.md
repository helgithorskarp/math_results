# A quadratic obstruction to a centered-LP triangle-cover bound

Let `G` be a split graph with clique part of order `k`, and let `H=nu_c*`
be its maximum fractional packing of triangles containing an independent
vertex. The proposed extension of the spoke-saturated cover estimate,

```text
tau(G) <= Phi_k(H) := k^2/4-k/2+H-H^2/k^2+1/4,
```

is false without extra hypotheses, even after adding a uniform `o(k^2)`
error or rounding the right side up to an integer.

For every `k=4^d`, `d>=1`, an explicit split graph satisfies

```text
q = k(k-1)/2,        B = k(k-1)/12,
tau(G) = q,         H = 11q/12,        nu_c(G) = 5q/6,
tau(G)-Phi_k(H) = (k-1)^2/576+(k-1)/24.
```

There are `5B` distinct neighborhood types, each with multiplicity one and
neighborhood size two or three. Thus the construction respects the usual
multiplicity cap `m_i<=|S_i|-1`. Its type count grows quadratically with `k`.
It leaves open an error depending on a fixed number of types, including
an `O(rk)` correction. This is a counterexample to the displayed research
route, not to Tuza's conjecture or to the prior conditional theorem.

The proof uses a nine-vertex gadget and the affine lines of `F_4^d`.
It is a complete author proof, with independent review pending. No
minimality or optimal counterexample constant is claimed.

| Clique order | Types | Centered fractional optimum | Triangle cover | Proposed bound |
|---:|---:|---:|---:|---:|
| 4 | 5 | 11/2 | 6 | 375/64 |
| 16 | 100 | 110 | 120 | 7615/64 |
| 64 | 1680 | 1848 | 2016 | 128415/64 |

At `k=16`, the rounded-up proposed bound is 119, while the exact cover
number is 120. See [the proof](PROOF.md) and [sources and scope](SOURCES.md).

## Reproduction

From this directory, with Python 3.11.2 or a compatible Python 3:

```sh
python3 check.py > /tmp/centered-cover-audit.json
cmp /tmp/centered-cover-audit.json AUDIT.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) uses only the standard library and exact integer and
`Fraction` arithmetic. It checks primal and dual certificates, independently
enumerates the gadget's actual packing and cover optima, and compares two
affine-line generators entry by entry. It checks every clique pair,
every generated centered triangle, edge capacities, a centered packing,
and the disjoint gadget decomposition for `d=1,2,3,4`. Five damaged
certificates must be rejected. The expected output is [AUDIT.json](AUDIT.json);
runtime and interpreter details are in [RUN.json](RUN.json).

Large graphs and triangle lists are regenerated and hashed, not stored.
The universal quantifier is established by the proof, not by four finite
examples. Floating-point search found the gadget but is not a dependency
of the proof or checker. The trust boundary is the unformalized proof,
the visible checker, and Python's exact arithmetic.

The fingerprint serializes, for each lexicographically ordered affine
line, all its centered triangles followed by the five packing triangles.
Records are ASCII `T u v w\n` and `P u v w\n`, in the local order in the
checker. Line hashes use compact JSON with no final newline.
