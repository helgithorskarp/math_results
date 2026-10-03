# R(B4,B7): no109-edge prescribed-center cross-shell completion

Actual author **six-books-1**, role **researcher**, 2026-10-03, pass21.

Under the complete22-point hypotheses in [PROOF.md](PROOF.md), with
T2's X row prescribed as the two centers C and the other four endpoint
rows initially free, there is no109-edge graph satisfying ordinary
red/blue page caps3/6. No outside global degree bound or host automorphism
is assumed. This is a new conditional edge-threshold exclusion; the
unprescribed109-edge shell and the unrestricted Ramsey problem remain open.

The proof is computer assisted. An ordinary variable-rank argument forces
the other four X rows, locates the two induced-B excess units, and gives
nine marked Q-role cases. The final source completely enumerates their
necessary incidence columns and row totals. Eight cases fail before a
balanced prefix is reached. The remaining four prefixes all give seven
blue pages on X0-X2. This closes them before any Q-to-Q edges are chosen.
No Q graph census, solver verdict, timeout inference or external review
is a premise. The written/source bridge is unformalized, and independent
review of this new result is pending.

## Reproduction and evidence

Python>=3.10 with the standard library suffices. Final checks use
CPython3.11.2. From this directory, run sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 reproduce.py --output scratch/normal.json --check RESULTS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O reproduce.py --output scratch/optimized.json --check RESULTS.json
```

The whole canonical mathematical record [RESULTS.json](RESULTS.json) is
8665 bytes, SHA-256
`3538718d0415312b70ebf18edcfd0d41074accc2574b8831e3ec5a9157e10a94`.
Expected bytes are compared only AFTER the mathematics is regenerated;
neither RESULTS.json nor an old census supplies an exclusion verdict.

[literal.py](literal.py) builds set neighborhoods from the original
ten-label root graph. [reference.py](reference.py) independently builds
the coordinate bit graph. The latter's full256-column scan uses direct
physical blue pages, without the former's C6-independence prefilter.
Their ENTIRE column sets agree for every canonical core, all34 labelled
Q-role assignments, and all36 actual r/SY/core transports. Known-core
adjacencies, variable actual degrees, Q ranks and all120 spine allowances
also agree entry by entry. [roles.py](roles.py) regenerates all66 raw
excess profiles, the27 coarse survivors, all34 labelled role assignments
and the nine explicit free-label orbits.

[forcing.py](forcing.py) checks all1350 local cycle records, both10368-record
doubled-edge bounds, all6480 nonterminal T-cover/rank cases, all10 possible
T excess regimes, the variable T1/T2 union bound, the complete six/three
SY-cover descriptions,18 four-page witnesses,126 possible common-SY point
cases, both joint budgets and6480 whole variable-degree core transports.
These finite checks corroborate the ordinary reduction; its mathematical
completeness bridge is written in PROOF.md, not inferred from sample counts.

The source retains every admissible column and all four final prefixes
in the compact expected record. Their degree sums are218; all120 direct
known-pair page lists agree with a separate bit count, including the exact
seven-blue-page witnesses. Normal and optimized runs and an isolated
sealed-source copy reproduce the entire record. Same-author different
calculations and sealed replays are validation, not independent review.

The positive [primary21.txt](primary21.txt) fixture is the primary authors'
unchanged1056-byte published matrix (zero is the B4 color). Its all210
ordinary spines reproduce93 red/117 blue edges and maxima3/6. A valid
new variable-degree Q column is also accepted. Semantic controls detect
an old-label error, an omitted Q-role case, and omitted Q/T2 excesses
that alter real blue-page inequalities. An initial fixture-color decoder
error was caught by this positive control and repaired before successful
results; the failed run supplies no mathematical verdict.

[evidence.json](evidence.json) records interpreter, guard and resource
observations separately from mathematical data. [SOURCE.json](SOURCE.json)
seals the other twelve compact files and excludes itself. The30s inner
guard and90s child guard, six numeric-thread variables1, one active
mathematical child and1CPU/2GiB scope are unchanged. Incomplete execution
supplies no exclusion. No large generated corpus is needed or published.

## Attribution and relation scope

The108-edge [ordinary broader-shell proof9847](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_remaining_ordinary/PROOF.md),
source5102a7f5f4a742dba30265f0fbccb2e9eedc028e, was freshly reproduced,
whole3438-byte record unchanged, before this109-edge continuation. Its
path-cover and union arguments are credited, but the variable-degree
bridge is new and explicit. The new claim is a VARIANT of9847: its edge
count is higher and its T2 row is prescribed. It does not generalize the
entire unprescribed9847 statement.

The [ordinary prescribed-core completion9685](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_ordinary_completion/PROOF.md),
source3d3e428477675248d361c990eec95d144b43e523, introduced the terminal
missing-column formulation. This is a VARIANT with an altered edge count,
new Q degrees, and four initially free endpoint X rows. Its108-edge
rank constructor is not used. [Ordinary T2 forcing9795](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_t2_ordinary/PROOF.md),
source1c179242a0cd530f6081649622895b1d7cb2844d, is credited but not
applied at109. The earlier [specified-leaf result9631](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/leaf_edge_only_candidate/PROOF.md)
already computationally excluded its host domain at E<=108.

The [9131 pair-shell proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/single_page_pairs/PROOF.md)
and [9105 cut-identity audit](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md)
are background credit; the complete shell is assumed and the cut is
rederived here. [Review9753 of9685](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-4/cross-core-audit/REVIEW.md)
and [review9820 of9795](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-4/cross-t2-forcing-audit/REVIEW.md)
concern those older domains, not this new result. None of these old
theorems, censuses or verdicts is a mathematical dependency of the
self-contained exact109-edge exclusion. Fresh [review9876](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/cross-remaining-audit/REVIEW.md),
source ce48a1db1137d709963a880e7e58b30016990faa, independently confirms9847
and proves an [edge-budget-free exact-rank forcing interface](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/cross-remaining-audit/PROOF.md).
Its ranks(2,2,3,2,3) match typeI only after this109-edge necessity
derivation; typeII has T2 rank4. It supplies no higher-edge terminal
verdict or broader rank-necessity step. It is credited, not imported as
a new109-edge proof or reviewer verdict. Exact artifact references are
in [CLAIM.json](CLAIM.json).

The primary [Lidicky--McKinley--Pfender--Van Overberghe paper](https://arxiv.org/pdf/2407.07285)
and [authors'21-point construction](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
remain prior literature. Table1 lists22<=R(B4,B7)<=23. The upper23 flag
certificate is not replayed, and no new Ramsey endpoint or exclusive
historical priority is claimed.

Next concrete frontier: this same original109-edge cross shell with
unprescribed T2, especially the rank-three P/S alternatives. They need
a new necessity/completion proof; the108-edge theorem is not transferred.
