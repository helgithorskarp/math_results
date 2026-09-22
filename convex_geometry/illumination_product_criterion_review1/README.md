# Independent review of the illumination product criterion

This directory records an independent review of
[`illumination_product_criterion`](../illumination_product_criterion/).
The target characterizes the polytopes `P` for which
`I(P x K)=I(P)I(K)` for every convex-body partner `K` by the equality
`I_f(P)=I(P)`, and proves an asymptotic power law and a finite strict-power
certificate when the equality fails.

**Verdict: accept, high confidence.** The written proof closes the claimed
implications in the stated domain. I found no mathematical error in the
finite incidence reduction, the arbitrary-partner fiber bound, the
fractional product identity, the rounding argument, or the rational
pentagon example. Historical priority of the all-partner criterion remains
unresolved, exactly as the target discloses.

[`REVIEW.md`](REVIEW.md) gives the full premise and completeness audit.
[`audit_independent.py`](audit_independent.py) is a standard-library-only
implementation written independently of the target code. It exhausts every
covering family on four labelled points, reduces them to all 114 maximal
covering clutters, constructs exact primal and dual LP certificates, and
checks every one of their 12,996 ordered products. It also derives the
rational pentagon's facet normals and solves the strict direction
inequalities by exact rational interval feasibility.

Run with CPython 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 audit_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -O audit_independent.py
sha256sum -c SHA256SUMS
```

Both Python runs must match [`EXPECTED_OUTPUT.json`](EXPECTED_OUTPUT.json).
The central output counts are 32,297 raw covering families, 114 maximal
covering clutters, 19 strict fractional-gap clutters, 12,996 ordered product
checks, 12,635 products having a zero-gap factor, and 225 strict
submultiplicative products. The entrywise result digest is
`8f673188da67fc61849218ccd44c5403b77de5d2f1c40c3a53461e06fde7f49d`.

The exhaustive calculation is an adversarial test of the finite lemmas; it
does not replace the human proof that all geometric directions and boundary
points reduce to that finite model. No target module, target fixture, solver,
floating-point calculation, network input, or external data is used.
