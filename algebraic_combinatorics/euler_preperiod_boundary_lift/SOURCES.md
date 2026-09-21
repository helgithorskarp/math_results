# Sources and literature-status check

Checked 2026-09-21 UTC.

## Primary problem source

Berke Guelec, *Modular periodicity of the Euler up/down numbers at odd prime
powers*, arXiv:2608.27058v2 (2026).
<https://arxiv.org/abs/2608.27058>

The paper proves the exact preperiod criterion used in (7) and formulates
`s(p^r)>=r-2`.  It does not state the uniform valuation formula (1) or the
order-three Wieferich consequence for `r=1 mod (p-1)`.

## Classical ingredients

- NIST Digital Library of Mathematical Functions, Section 24.15(ii),
  especially equation 24.15.4, records the tangent--Bernoulli identity used
  in (3): <https://dlmf.nist.gov/24.15#ii>.
- The von Staudt--Clausen theorem gives the exact reduced denominator of
  every even Bernoulli number.  A reference with the original sources and
  later extensions is:
  <https://encyclopediaofmath.org/wiki/Von_Staudt-Clausen_theorem>.
- The remaining input is the standard lifting-the-exponent lemma for odd
  primes.

## Graph dependency

The existing Discovery Net lemma **Exact diagonal Euler preperiod
classification via higher Wieferich valuation**
(`bafkreifeajdiiqrfvux5w7xowmagwzcw2uync75vp5cdyct6hgo7cm33s4`) proves
the `q=1` case and its `r=p` preperiod consequence.  The present theorem
generalizes it to every `q>=1`; it does not claim the endpoint identity as a
new base case.

The later local four-class theorem and its independent review are published
in the same repository at:

- <https://github.com/helgithorskarp/math_results/tree/main/algebraic_combinatorics/euler_preperiod_local_irregularity>
- <https://github.com/helgithorskarp/math_results/tree/main/algebraic_combinatorics/euler_preperiod_local_irregularity_review1>

They classify consecutive zeros modulo `p` and explicitly identify coupling
the classes to the `p^2,p^3` lift conditions as the highest-value remaining
bridge.

## Search boundary

Targeted searches covered the exact valuation phrase, tangent numbers with
Wieferich primes, Euler up/down numbers with higher Wieferich conditions, and
later works citing the 2026 preperiod paper.  Apart from the already-known
`q=1` graph lemma, no source stating the all-`q` formula (1) or its full
congruence-class preperiod consequence was found.  The generalization is a
short consequence of classical ingredients, so this report claims an
independently derived graph bridge and bounded-search novelty, not historical
priority.
