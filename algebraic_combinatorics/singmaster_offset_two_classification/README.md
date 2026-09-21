# The second diagonal-offset curve has no interior repetitions

This directory gives a self-contained classification of the first higher
equal-offset curve in the fixed-offset approach to repeated binomial
coefficients.

## Theorem

Let `x,y` be integers such that

```text
0 <= y  and  y + 2 <= x - 2.
```

Then

```text
binom(x,y) = binom(x-2,y+2)
```

if and only if `(x,y)=(4,0)`.  In particular, this curve produces no
repetition of a binomial coefficient greater than one and no interior
repetition in Pascal's triangle.

Hugo Jenkins studied the more general fixed-offset equation
`binom(x,y)=binom(x-r,y+s)`.  His 2016 paper proves finiteness when `r != s`
and identifies the equal-offset family as the missing case.  It verifies by
algebraic-curve methods that the `r=s=2` curve is nonsingular of genus three,
which proves finiteness of its integral points but does not state their exact
classification.  The factorization below supplies that exact classification
by an elementary argument.  The literature search recorded in
[SOURCES.md](SOURCES.md) found no prior explicit classification; this is a
bounded search statement, not a claim of exhaustive novelty.

## Proof

Put

```text
a = y + 1,        b = x - y - 2.
```

The domain says `a >= 1` and `b >= 2`, while `x=a+b+1`.  Cancelling
factorials in the binomial equality gives

```text
(b-1)b(b+1)(b+2) = a(a+1)(a+b)(a+b+1).             (1)
```

Set

```text
U = b(b+1),       A = a(a+b+1).
```

Since `(b-1)(b+2)=U-2` and `(a+1)(a+b)=A+b`, equation (1) is

```text
U(U-2) = A(A+b).                                      (2)
```

Multiplying (2) by four and completing two squares yields

```text
(2A+b)^2 - (2U-2)^2 = b^2 - 4,
```

and hence

```text
[2A+b-2U+2] [2A+b+2U-2] = b^2 - 4.                  (3)
```

If `b >= 3`, the right side of (3) is positive.  Its second factor is
positive, so its first factor is a positive integer.  But the second factor
satisfies

```text
2A+b+2U-2 > 2U-2 = 2b^2+2b-2 > b^2-4.
```

Thus the product on the left of (3) is strictly greater than its right side,
a contradiction.

It remains that `b=2`.  Now the right side of (3) is zero and the second
factor is positive, so the first is zero.  Since `U=6`, this says `A=4`.
Consequently `a(a+3)=4`, whose only positive integral solution is `a=1`.
Back-substitution gives `(x,y)=(a+b+1,a-1)=(4,0)`, and this pair indeed gives
`binom(4,0)=binom(2,2)=1`.  This proves the theorem.

## Reproduction

Only Python's standard library is required (Python 3.8 or later):

```bash
python3 verify.py
sha256sum -c SHA256SUMS
```

The first command performs three exact checks:

1. checks the residual factorization identity on a `100 x 100` grid;
2. compares the binomial coefficients directly for every admissible
   `(x,y)` with `x <= 1000`;
3. independently solves the two nested quadratic discriminant conditions for
   every `2 <= b <= 1,000,000`.

Its deterministic output is stored in [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json).
These finite checks audit the statement and exceptional case; the universal
classification rests on the displayed inequality proof, not on the search.

## Scope

This result settles only the `r=s=2` fixed-offset curve.  It neither proves
Singmaster's bounded-multiplicity conjecture nor classifies the curves with
equal offset at least three.  The argument depends on the special two-pair
compression in (1); no analogous factorization is asserted for larger
offsets.
