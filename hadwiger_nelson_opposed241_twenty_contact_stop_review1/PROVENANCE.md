# Provenance and trust boundary

## Reviewed source

- Mathematical source commit:
  `3d0415fe410c7a0fa5b18aaacf71a7049014d382`.
- Later non-mathematical publication-metadata tip used for pinned public
  bytes: `e5deefabadbf4956986be5e6437d3248199e2838`.
- Target directory:
  <https://github.com/helgithorskarp/math_results/tree/3d0415fe410c7a0fa5b18aaacf71a7049014d382/hadwiger_nelson_opposed241_twenty_contact_stop>.

The mathematical certificate, verifier, controls, source selection, and B214
fixture are pinned individually in `independent_check.py`. The current README
and publication metadata were added after the mathematical commit; this
review separates those packaging bytes from the theorem-bearing source.

## Dependency alignment

The review rebuilds the 241-point source from:

- `hadwiger_nelson_nonmono159_214_lowden2/points214.tsv`;
- `hadwiger_nelson_opposed241_conditional_core/certificate.json`.

It then matches the point and edge hashes from the already published
independent review
`hadwiger_nelson_opposed241_conditional_core_review1`. No theorem about the
source's conditional colour relation is imported into the present chromatic
argument.

## Method independence

The target checker represents `x` and normalized `y` separately over the
quadratic tower `K+Kt`. The review instead performs ordinary physical
rotation and distance arithmetic in one flat eight-coordinate field. It does
not import or execute any target module.

The target's four-word is checked, but the upper bound is corroborated by a
fresh graph-colouring search which does not consume that word. The lower
bound is a direct enumeration on the reconstructed Golomb subgraph; it does
not trust a SAT or UNSAT report.

## Residual trust

The result trusts the pinned repository bytes, the short field-degree and
colour-normalization arguments, Python 3.11 exact integer and `Fraction`
arithmetic, the review programs, SHA-256 collision resistance, CPython, the
operating system, hardware, and the human interpretation of the output. No
floating-point comparison, omitted edge list, solver verdict, external proof
log, or target executable lies on the proof path. This is independently
reproducible computer-assisted evidence, not formal verification.

