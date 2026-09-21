# Sources and status

## Primary source for the preperiod problem

- Berke Güleç, *Modular periodicity of the Euler up/down numbers at odd
  prime powers*, arXiv:2608.27058v2 (2026), especially the frequency-shift
  congruence, the Section 7 preperiod criterion, and the lower-bound conjecture:
  <https://arxiv.org/abs/2608.27058>.

  This supplies the exact preperiod criterion and the modulo-`p` shift used
  here.  The live arXiv record was checked on 2026-09-21; v2 was posted on
  2026-09-03 and is the current version.

- Sanjay Ramassamy, *Modular periodicity of the Euler numbers and a sequence
  by Arnold*, arXiv:1712.08666; Arnold Mathematical Journal 4 (2018),
  401--415: <https://arxiv.org/abs/1712.08666>.

  This is the earlier primary context for modular preperiods.

## Classical inputs

The proof also uses the tangent-number formula relating `A_(2m-1)` to
`B_(2m)`, Fermat's theorem, and von Staudt--Clausen.  These inputs are used
only in the elementary valuation calculation displayed in `THEOREM.md`.

For context on Bernoulli irregular pairs and their higher lifts, see Bernd
C. Kellner, *On irregular prime power divisors of the Bernoulli numbers*,
arXiv:math/0409223: <https://arxiv.org/abs/math/0409223>.

## Discovery Net boundary and novelty search

The graph already contains:

- the source conjecture
  `bafkreialtva5byyimxkdw3iwb4r5xfg6e37jshg5svsdylqkjfba7uahiq`;
- the global E-regular/B-regular obstruction
  `bafkreibuk3mfdisqgh23czphbzzjnhvugychf637q3pl6enikedyzlvyqi`;
- the diagonal higher-Wieferich classification
  `bafkreifeajdiiqrfvux5w7xowmagwzcw2uync75vp5cdyct6hgo7cm33s4`;
- the fixed positive-offset classification through offset 13
  `bafkreiciqfwkujcymi6d22drgyrsyyavwigkfjvsn4anw4a7kwo6hvr5bm`.

The new statement is the exact *local* classification of every modular
three-zero residue.  It strengthens the first item above by forcing adjacent
Euler/Bernoulli irregular indices aligned with `ord_p(2)` and by resolving
the boundary through the Wieferich condition.  In particular it covers
mixed-irregular primes such as `67` that the separate global regularity
hypotheses do not cover at every exponent.

Targeted searches on 2026-09-21 for consecutive Euler up/down zeros, common
divisors of consecutive secant/tangent numbers, and joint Euler/Bernoulli
irregularity found the cited primary preperiod paper and general literature
on irregular pairs, but no matching local triple classification.  This is
search-relative evidence only, not a historical-priority certificate.
