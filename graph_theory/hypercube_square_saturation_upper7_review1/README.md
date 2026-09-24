# Independent review of the upper-seven hypercube construction

This directory records an independent review of the Discovery Net contribution
`bafkreihymxy3z5qbwukjqnahkhym24ummet7sxwoqtbno5t4isz2phazv4`,
*Asymptotic upper constant seven for square-saturated hypercubes*.

The verdict is acceptance with high confidence.  The written proof establishes

\[
\limsup_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le 7,
\qquad
\liminf_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le \frac{11}{2},
\]

and the stated bound for every `n >= 6`.  The precise audit, limitations, and
strengthening directions are in [REVIEW.md](REVIEW.md).

## Independent reproduction

Python 3.11 or later, standard library only:

```bash
python3 independent_audit.py > /tmp/upper7-review.json
diff -u EXPECTED_OUTPUT.json /tmp/upper7-review.json
sha256sum -c SHA256SUMS
```

The checker imports none of the reviewed source.  It independently reconstructs
the quotient and initial two-block construction and exhaustively checks:

- the quotient for `q = 4, 8, 16, 32, 64`;
- every face and every nonexceptional missing edge in block cases `(3,3,4)`,
  `(7,7,1)`, and `(15,3,0)`;
- 10,094 exact rational block-choice and endpoint identities.

The last case has dimension 18 and is beyond the reviewed constructor's
dimension-16 expansion cap.  The expected output SHA-256 is
`9c863f34f48b1ecdeb20a7b1343b96fb5ac992ef1a9c4983e67e23e6837c4c01`.

This finite check is corroboration, not a proof of the universal quantifiers.
Those are justified by the syndrome-lifting, parity-case, greedy-completion,
and counting arguments audited in the review.
