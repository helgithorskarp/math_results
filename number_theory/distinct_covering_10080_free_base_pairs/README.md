# Two period10080 prefixes and an exact pair separator

Actual author: **six-covering-1**, role **researcher**. Same-author exact
checks; independent review and formalization are pending.

A nonnegative integer weight excludes a specified23-class prefix with
all42 unused distinct divisors at least8 free or omitted. In particular,
seven non-7 base moduli retain arbitrary phases. A binary weight excludes
a related24-class prefix and forces at least ten physical holes. A
separate206-point base residual admits no strict single-point addition or
subtraction, but a two-point addition gives a strict gap6 certificate.

These are conditional statements. No complete period10080 exclusion,
new covering or improved unrestricted L_min(8) bound is claimed. The
method instantiates the existing residual-weight bound; no method-priority
claim is made. See [proof.md](proof.md) for hypotheses and exact values.

From the repository root, Python>=3.10, standard library only:

```text
python3 -B number_theory/distinct_covering_10080_free_base_pairs/check.py
python3 -B -O number_theory/distinct_covering_10080_free_base_pairs/check.py
python3 -B number_theory/distinct_covering_10080_free_base_pairs/controls.py
```

Expected: prefix gaps10 and18, pair gap6, all412 single-point moves
nonstrict, and nine invalid fixtures rejected. [expected.json](expected.json)
contains every exact field and an event hash. The compact
[certificate.json](certificate.json) and checker suffice: no solver,
random search, private weight pool or proof corpus is required.
