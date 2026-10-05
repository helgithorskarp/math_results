# Author control run, version 1

Atlas / `studio-researcher-1`, researcher, 2026-10-05. The unchanged
`check_structural.py` was run once with its deterministic entry point and
the resulting compact JSON is `EXPECTED.json`.

Environment: CPython 3.11.2, GCC 12.2.0 build, standard library only,
one process, native thread variables set to one. The child had an
address-space ceiling of 2 GiB and a 60-second CPU ceiling. Observed wall
time was 0.589 seconds, user CPU 0.563 seconds, system CPU 0.012 seconds,
and peak child RSS 13,452 KiB. It exited zero with no stderr. Timing and
memory are observations, not mathematical inputs to the deterministic
output.

The 594 input cases comprise all 144 labeled trees of orders 3--5,
18 boundary fixtures, and 432 branched-broom parameter controls. Some
fixtures and parameter choices repeat isomorphism types; this is not a
count of 594 distinct unlabeled trees. The checks cover:

* 16,106 directed deficit/full-degree identities;
* 2,243 nonstar edge decompositions and 1,933 explicit disjoint bottom
  edge pairs;
* 1,145 maximizing nonstar parent budgets, including 993 d=1 occurrences;
* 18 star-parent controls and 278 input cases with tied maximizing parents;
* six malformed graph rejections and the three negative controls described
  in the README and deterministic output.

The negative controls distinguish two genuinely necessary hypotheses:
maximality and the nonstar restriction on the stronger form. The known
order-22 example also guards the graph-leaf/core height distinction.
These are author implementation controls. They are not a reachability
census, an independent researcher's check, a proof of the inherited
classification, or an extrapolation to all trees. The ordinary universal
proof is `PROOF.md`; a new exact-version internal check is pending.
