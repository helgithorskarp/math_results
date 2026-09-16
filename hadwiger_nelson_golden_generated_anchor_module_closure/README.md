# Every sequential two-anchor golden reciprocal network is three-colourable

Start with the exact 16-point Parts `{1,phi}` plane carrier. Repeatedly add
whole copies of that same carrier at absolute scale `phi` or `1/phi`, allowing
reflections, with at least two distinct physical anchors already present at
each step. The anchors may come from any earlier generated copies.

**Every finite network obtained this way has chromatic number exactly three
on its complete collision-merged unit-distance graph.** Every subset is at
most three-colourable. Thus this construction mechanism cannot produce a
five-chromatic sub-509 graph, regardless of overlap or copy count.

This is a construction-side consequence of the fresh
[independent module-colouring theorem](https://github.com/helgithorskarp/math_results/blob/b3fc15ed9027348ad43b9121f3e0d4e457de197f/hadwiger_nelson_golden_generated_anchor_box_stop_review1/PROOF.md).
No second physical network, copy-placement sweep or new colouring search was
performed. The original 462-point, 1,532-edge graph is independently confirmed
as exactly three-chromatic; that review is banked in its source package.

## Why generated anchors cannot escape

Put `K=Q(zeta_5)`, `q=1/abs(1-zeta_5)`, and `A=Z_(3)[zeta_5]`, where
`Z_(3)` consists of rationals with denominator coprime to three. The reviewed
three-colouring covers the complete unit graph on qA.

The fifth cyclotomic polynomial is irreducible modulo three, so A/3A is a
field. Clearing a minimal power of three from the denominator proves:

```
u in K and u*conjugate(u) in A  =>  u in A.
```

Two existing anchors determine a new copy's multiplier inside K. Its squared
norm is `phi^2` or `phi^-2`, both in A, so the multiplier is in A; its
translation is then in A too. Induction keeps every new point inside qA.
The source's unit five-cycle supplies the lower bound three.

[PROOF.md](PROOF.md) states the hypotheses, denominator argument, reflection
case, full-edge colouring and limitations. The statement requires a valid
sequential two-anchor insertion order. Final contact cycles and incidental
edges are allowed. One-anchor placements and simultaneous assemblies lacking
such an order are outside the stated theorem, not suggested continuations.

## Check the finite algebra

Only Python 3.11+ and its standard library are required:

```bash
python3 -B check.py
python3 -O -B check.py
sha256sum -c SHA256SUMS
```

The checker verifies all three linear and nine monic-quadratic factor tests,
all 80 nonzero residue norms, conjugation on all 81 residues, the complete ten
unit-residue list, the golden scale identities and the exact source five-cycle.
Ten polarization evaluations certify every coefficient of the homogeneous
quadratic Gram identity. Seven malformed-input/certificate controls are
rejected; reducible-polynomial and forbidden-denominator controls also pass.
Normal and optimized reports agree.

The checker imports no reviewer or construction executable. It verifies the
finite algebra in the written proof; it is not a proof-assistant formalization
of the arbitrary-length induction. Trust rests on the explicit elementary
algebra, Python's exact integers/Fractions and the execution environment.

## Evidence status

- Independent prior review: `b3fc15ed9027348ad43b9121f3e0d4e457de197f`.
- Original physical network: `3beda50683c9d24e033e30e4b35e9d0d5927f0d7`.
- Fixed-base overlay theorem: committed Discovery h3833,
  `bafkreic3qhe4awwdjdvhsygo5oysaqaiceyfyrp6xqpv6sxcjouvpditua`.
- Present preservation corollary: author-side proof with compact exact checks;
  not independently reviewed and not a record improvement.

The review's broadcast remains pending/unindexed on the stale ledger. Public
source availability and independent review must not be confused with Discovery
commitment. The previous finite source files and all receipts are preserved.
