# No cubic eight-circulant nut graph

**Theorem (exact computer-assisted proof).** No simple cubic nut graph admits
an automorphism whose cycles are eight cycles of the same length. There is no
restriction on that length.

A nut graph has a one-dimensional adjacency kernel spanned by a vector with
no zero coordinate. This settles Conjecture 1 of Bašić and Damnjanović,
[On cubic polycirculant nut graphs](https://link.springer.com/article/10.1007/s40314-025-03218-7),
*Computational and Applied Mathematics* **44** (2025), 265. Combined with their
Theorem 2, the possible numbers of equal cyclic orbits in a cubic nut graph
are exactly

\[
\{3,6,7\}\cup\{9,10,11,\ldots\}.
\]

The new ingredient is the action of the cyclic generator on its real
one-dimensional kernel: it acts as `+1` or `-1`. This imposes a symmetric
signing on the quotient, and every quotient semi-edge has the same sign.
[theorem.md](theorem.md) proves the reduction, enumeration completeness,
switching normalization, and the determinant/cofactor test.

## Reproduce

Python 3.10 or later, standard library only. Tested with CPython 3.11.2.
From this directory:

```sh
python3 verify.py --expect-no-survivors
python3 crosscheck.py
```

The proof computation takes about 1.4 seconds on the development machine.
The crosscheck also completes in seconds. Neither command accesses the
network. Stable outputs are in [expected.json](expected.json); elapsed time
is intentionally omitted there.

| Exact stage | Count |
|---|---:|
| Connected simple subcubic supports on eight vertices | 194 |
| Cubic quotient pregraphs | 534 |
| Ordinary quotients nonsingular | 425 |
| Ordinary quotients singular with a kernel obstruction | 109 |
| Signed matrices checked over the 425 nonsingular quotients | 6,216 |
| Signed matrices nonsingular | 6,104 |
| Signed matrices of nullity one with a zero kernel coordinate | 112 |
| Surviving cases | **0** |

`verify.py` generates its entire input catalogue. It uses arbitrary-precision
integer Bareiss determinants and principal cofactors, with exact divisions
checked. The quotient-catalogue SHA-256 is
`887047512eb4bafbd895be677ff145f33cb376c4a2024c50d0495c8b2e1e97a8`;
the full determinant/cofactor audit SHA-256 is
`6be613dddab2a0951ff2cf41e9f11f5f69a3581221d2f98e41426335207767c9`.

`crosscheck.py` checks all 6,750 matrices and all their required cofactors
(8,518 determinant calculations) by the Leibniz formula evaluated over
subsets, and checks singular ranks over exact rational numbers. It also
compares all 194 supports, entry by entry up to isomorphism, against the
authors' independently generated graph6 catalogue. Small-order controls
reject four and five orbits and retain candidates at three, six, and seven.

## Scope, provenance, and trust

The published proof computation has no CAS, solver, floating-point arithmetic,
random search, external input, or bounded orbit-length assumption. The
crosscheck shares the quotient and signing enumerators; its arithmetic is
independent. Its additional support fixture is the authors'
[underlying_8.g6](https://github.com/nbasic/cubic-polycirculant-nuts/blob/main/underlying_8.g6),
downloaded 2026-09-26, SHA-256
`5d638c645a77d48c861b75bd3c29cb0765feb0ff11f4dcde16e1696ba713643e`.
The fixture is 1,358 bytes; no upstream software is copied here. The theorem's
production computation does not depend on the fixture's completeness.

The remaining trust boundary is the mathematical reduction and the supplied
Python enumeration/arithmetic implementations and interpreter. This is an
exact computer-assisted proof, not a proof-assistant formalization or an
independently peer-reviewed result. Source searches on 2026-09-26 found no
later resolution of the conjecture; that supports apparent novelty only.
