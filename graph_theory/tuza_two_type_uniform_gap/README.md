# A uniform Tuza gap for two-neighborhood split graphs

For a finite simple split graph with specified clique part of order `k>=3`
and at most two triangle-active independent-side neighborhood types,

    2 nu(G) - tau(G) >= k^2/228 - k/2 - 1/4.

Here `nu` counts edge-disjoint triangles and `tau` counts edges meeting all
triangles. Multiplicities are unrestricted. The elementary, constructive
proof is in [PROOF.md](PROOF.md).

This proves Tuza's inequality for **every `k>=113`**, without a larger
finite census. Any counterexample in the class has a cover-equivalent
capped counterexample with at most334 active vertices. It also gives
`tau <= (227/114) nu + k/2 + 1/4`, a strict asymptotic gap below two.
The full two-type conjecture at smaller clique orders remains unresolved
by this result. The constants are not claimed optimal.

The mechanism is a degree-dependent multiplicity cap, deterministic
selection of modular-sum matchings, a modular-sum packing of residual
clique triangles, and the two-set identity `st-cu=(s-c)(t-c)>=0`.
No optimal-design theorem, solver, clique-order census, or preceding
cover-normal-form theorem is a proof dependency.

## Reproduce

Use standard-library Python3.10+; tested with CPython3.11.2.

```bash
python3 verify.py
python3 construct.py 35 31 29 18 1000000000 17 --construct
```

The six counts are

    a=|S\T|, b=|T\S|, c=|S intersect T|, d=|C\(S union T)|, m, n.

Without `--construct`, only exact rational arithmetic bounds are computed,
without expanding any multiplicity or clique. With it, the deterministic
constructor produces a compressed cover and an explicit packing using
`O(k^3)` arithmetic operations and `O(k^2)` memory/output. The command-line
summary prints their sizes and a hash, not their full potentially large
contents. `make_witness(Parameters(...))` exposes the actual certificate.

The displayed example gives a cover of3718 edges and3480 packed triangles,
despite a billion copies of one type. These are feasible witnesses, not
claims of exact optimality.

## Checks and trust boundary

`verify.py` checks the two scalar polynomial identities exactly, checks104
small witnesses by expanding the original graph and inspecting all its
triangles, checks four named large-clique witness fixtures, and tests128
binary-sized arithmetic inputs without expanding their graphs. It rejects
four malformed witnesses and three malformed parameter inputs.

The full expected summary is in [EXPECTED.json](EXPECTED.json); its record
digest is
`5729c69db7682aedba80fbff76abcddceac22cf1f8a25c72a3c9a67fa5957e79`.
The direct certificate checker does not reuse the constructor's color
selection or cover optimization. All arithmetic is exact. Tests validate
the implementation, not the universal quantifiers or historical priority.
The theorem rests on the written proof, which is not proof-assistant
formalized and has not yet been independently reviewed at initial release.

[SOURCES.md](SOURCES.md) records the primary-status check, prior reductions,
and relation to the earlier graph contribution. The counterexample kernel
is not an invitation to enumerate all graphs up to334 vertices; the next
step should be structural, not another cutoff table.
