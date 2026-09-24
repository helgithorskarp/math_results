# Independent review of the upper-six square-saturation construction

This directory reviews Discovery Net contribution
`bafkreib2coyqjuo45hvsv3heeftor2rwcrrcigflsodh42lmi43npznqt4`,
*Finite syndrome certificates give asymptotic upper constant six for square
saturation*, at source commit
`e30f5a692b7c727e738784ffe073d62c77a3fb51`.

The verdict is acceptance with high confidence.  The construction proves, for
every integer `n >= 14`,

\[
  \operatorname{sat}(Q_n,Q_2)
  < \left(6+\frac{49}{n+2}\right)2^n,
  \qquad
  \limsup_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le 6.
\]

It does not determine an exact value or a limit and does not improve the
previous `11/2` subsequence bound.  The complete proof audit, novelty boundary,
and strengthening directions are in [REVIEW.md](REVIEW.md).

## Independent reproduction

Python 3.11 or later, standard library only:

```bash
python3 independent_audit.py \
  ../hypercube_square_saturation_shortened_templates/templates.json \
  > /tmp/upper6-review.json
diff -u EXPECTED_OUTPUT.json /tmp/upper6-review.json
sha256sum -c SHA256SUMS
```

The checker imports no reviewed module.  It reconstructs all three finite
templates from the proof, enumerates their affine planes by a different
method, and rebuilds each replicated quotient at the previously untested scale
32.  It independently checks the exact interval arithmetic through dimension
100,000.

It also constructs the theorem-selected dimension-19 case `H(2), S(4)`—one
dimension beyond the submitted expansion cap—and enumerates all 22,413,312
two-faces before and after greedy completion.  The final 1,935,771-edge graph
is square-free and every one of its 3,044,965 missing cube edges has a
three-edge witness.  This finite computation corroborates rather than proves
the universal construction.
