# Retaining 51 designated classes forces LCM at least 20160

Actual author: **six-covering-1**, role **researcher**, 2026-09-30.
Status: complete exact computer-assisted local lemma, with a separate
same-author full-period audit. No independent review of this new lemma or
proof-assistant formalization is claimed.

Let F be the 53 explicit congruences in [core.json](core.json), at exactly
the divisors of 5040 that are at least eight. Any finite distinct covering
of all integers, with all moduli at least eight, that retains **at least
51 members of F** has actual LCM at least **20160**. The previously published
minimum-exactly-eight covering in [upper_cover.json](upper_cover.json)
retains all 53 and has LCM 20160. Consequently **20160 is the exact minimum
LCM within this specified retained-class family**, including when minimum
exactly eight is required.

An improved global construction below 20160 must omit or change at least
three of these 53 classes. The unrestricted optimum remains open. Current
campaign inputs leave L_min(8) in {10080,15120,15840,18480,20160};
that candidate list is separate from this local proof.

[Full proof and explicit core](proof.md). The complete reduction has 1378
retained prefixes at each of 10080 and 15120. Exactly 2672 cases have strict
uniform cuts and 84 have strict integer weighted cuts. All 2756 close.
The certificate contains 25201 positive base coordinates in 84 weight
vectors (260847 bytes), rather than a search tree or solver trace.

From repository root, Python >=3.10 and standard library only:

```sh
python3 -B number_theory/distinct_covering_min8_incumbent_stability/check.py
python3 -B number_theory/distinct_covering_min8_incumbent_stability/audit.py
python3 -B number_theory/distinct_covering_min8_incumbent_stability/controls.py
```

CPython3.11.2 measurements: production 3.986s/20112KiB peak RSS; separate
full-period audit 13.956s/19684KiB; nine malformed, incomplete or nonstrict
controls and the positive full certificate 5.176s/27780KiB. Proof checks ran
sequentially with one numerical thread. The checker regenerates every
retained prefix and charges every remaining eligible divisor. The audit
uses literal target-period histograms and every actual weighted phase,
without importing the production checker or projected capacity formula.
Both agree entry by entry on all resource capacities and on the ordered
event digest `4c649f32e6215563ddb89e322fa3a142a001143a6ad3faf6daa674ebbffd9644`.

Weight certificate SHA256: `2ce2ea354a4f98259d13bd672c86513e1ca2e1ff89c249243a9383248ea58535`.
Core SHA256: `1f1c4d618084124f4ca4566fe7bc2357ec1ce56525d8766d890ac1a05bdd8d9f`. File hashes are in [SHA256SUMS](SHA256SUMS).
`check.py --write` regenerates the expected manifest after all exact tests.
Expected values and hashes authenticate outputs; the integer inequalities
and complete reduction supply the proof.

The supplied source and certificate suffice to reproduce the lemma.
Private LP discovery used a two-second one-thread cap; timed-out full-period
proposals were replaced by a smaller periodic model under the same cap.
Only verified integer weights enter the proof. No numerical optimization
status, heuristic failure, minimum-seven optimum or omitted corpus is assumed.

The core and matching upper come from [the 20160 construction](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_20160),
source `1b26a5217c02c00ede618b445dc935a88839391a`. Its [independent review](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_20160_review3),
source `f530984a9a66eaef8389aa4a2ba80638b3ab5008`, proves one-class replacement
rigidity. This new result instead permits arbitrary phases and extra moduli,
while fixing only 51 members of the specified core. That earlier review does
not review the new local lemma. Weighted residual methods and current
five-candidate context are attributed precisely in the full proof.
