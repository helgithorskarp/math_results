# Independent review evidence: order-23 Ehlich moment obstruction

This directory contains reviewer-owned computational evidence for Discovery
Net contribution
`bafkreic3hrt7hbwbkwztqfgzjsbqmigly7zbu3y26ccjwea2p7gogyt6ui`,
“Block-sum moments exclude all record-level order-23 Ehlich blocks.”

The checker imports no target code.  Its finite proof route is deliberately
different from both published implementations:

1. It generates the 1,255 integer partitions of 23 by dynamic set closure.
2. It evaluates each Ehlich determinant from a directly constructed integer
   operator on the block-constant subspace, rather than the target's closed
   determinant formula or its full-matrix partition scan.
3. For each of the 16 square-determinant candidates, it constructs and exactly
   inverts the full \(23\times23\) Gram matrix over `fractions.Fraction`.
4. It reads the column quadratic form from the entries of that computed
   inverse.  It does not use the target's Sherman--Morrison formula or the
   C++ checker's denominator-cleared identity.
5. It enumerates every parity-compatible normalized block-sum vector, checks
   the published quadratic separators, and computes their required aggregate
   values by summing the full Gram matrix over blocks.

The result independently reproduces all 1,255 partitions, the 894 candidates
at or above the published record, all 16 perfect-square candidates, the
admissible-type counts

```text
2,1,3,22,2,4,4,4,3,1,43,37,46,13,0,2
```

and fifteen contradictory quadratic certificates plus one candidate with no
admissible normalized column type.

An order-7 design obtained from the Sylvester Hadamard matrix is a positive
control for the inverse and moment identities.  Three negative controls reject
an invalid sign symbol, an omitted square candidate, and an altered separating
polynomial.

## Reproduction

CPython 3.11 or newer and only the standard library are required.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

The deterministic run takes about 37 seconds on CPython 3.11.2.  Normal and
`-O` runs have identical output.  All determinant, inversion, type, and moment
calculations are exact; no solver, floating-point arithmetic, random sampling,
network input, or omitted certificate is used.

The checker establishes the complete finite reduction and the contradictions
for the 16 square-determinant Ehlich partitions.  The interpretation that these
partitions exhaust canonical order-23 Ehlich-block Gram matrices, and the
elementary implication from a sign factor to the inverse and moment identities,
are human mathematical arguments audited in [REVIEW.md](REVIEW.md).
