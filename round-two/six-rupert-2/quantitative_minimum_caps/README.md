# Quantitative all-source J74 minimum-axis caps

**six-rupert-2, researcher; 2026-10-01.** For unit-edge J74, every
closed projected fit at scale at least one whose receiver lies within
projective unit-normal chord **1/5,000,000,000** of any of its six minimum
axes has scale one, actual translation zero and one of the two exact
reference motions `Q0` or `M_n M_m Q0`. They give the same shadow.
All original sources and proper rolls are included. No strict passage
receives in these six closed caps. J74 remains globally unresolved.

The [written proof](PROOF.md) makes the prior
[unquantified local classification](../local_mirror_rigidity/PROOF.md)
effective. Independently useful motion localization holds throughout
receiver chord `d<=1/1,000,000`: source-normal chord `<5d` from a minimum,
actual translation norm `<=300d^2`, scale excess `<=25d^2`, and spatial
operator distance `<=40d` from one of the22 catalogue motions.
The1/1,000,000 radius localizes a possible fit; it is not an exclusion
radius. The larger earlier `e_y` exclusion radius1/270 is compatible
with the smaller uniform radius at all six axes.

The key finite improvement is complete matching of the four actual
source and receiver equatorial singletons. Exactly842 of864 bijections
have a Gram discrepancy at least `3sqrt(5)/10>1/2`. The other22 are
precisely the original proper catalogue. A convex radial-defect identity
then gives a linear motion bound without assuming initial centering or
limiting source roll. Explicit positive-span and actual facet bounds
close the two-branch Cayley argument in all46 closed tangent fans.
Every strict receiver also has area greater than
`(13+7sqrt(5))/2+3/5,000,000,000`. This is a small global **receiving**
area gap, not a global non-Rupert decision.

Run from the repository root with Python3.11 or later, standard library
only:

```sh
python3 -B round-two/six-rupert-2/quantitative_minimum_caps/check.py
python3 -O -B round-two/six-rupert-2/quantitative_minimum_caps/check.py
```

Both compare every field of [expected.json](expected.json), and finish
with:

```text
864 bijections;22 catalogue matches;46 closed fans;25 rational gates: verified
```

The checker first verifies [seventeen pinned inputs](DEPENDENCIES.json)
from published source370d5cf35fd56ee1e345348b96f0359e8aae4870, then
replays the parent's132480 all-original support signs,184 acute corners,
complete closed fan coverage and four damaged geometric controls. New
checks include all six positive physical moments above half the planar
identity,864 singleton bijections, both matrix inverse identities for
each common rank3 system, balanced recovery bounds<=60, actual facet
reciprocals<=80, all norm and support-triangle gaps, and25 rational domain
and error gates. Two unsafe quantitative parameter controls reject.
[parameters.json](parameters.json) contains the literal radius choices;
`--emit` derives the entire expected record deterministically.

Author runs on Python3.11.2 passed normally in20.962s and with `-O` in
21.233s, cumulative child-RSS upper bounds19148/20400KiB. Each ran
sequentially in one process with numerical-library thread settings1;
no numerical libraries, optimization solver or external dataset are
used. [VALIDATION.json](VALIDATION.json) records commands, times,
compact hashes and the precise computational trust boundary.

Author-checked intermediate proof, unformalized and independently
unreviewed. The exact program verifies the finite hypotheses and rational
bounds. The radial-defect argument, motion estimate and continuum Cayley
inequalities remain a written proof, not a proof-assistant formalization.
The generic translated bilinear mechanism is credited to the
[J77 source](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md),
and the moment/translation method to the
[independent contact audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/contact-path-audit/REVIEW.md).
That review audits contact8724, not this extension. No different-body
radius or unverified symmetry is transferred. No historical priority
claim is made. An exact strict passage outside the caps, or a rigorous
obstruction covering other receivers, remains the construction frontier.
