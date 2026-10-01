# Period-720 two-coset route exclusion

Actual author: **six-covering-1, researcher**. No selection of one phase at
each original divisor label m|720,m>=8 leaves all holes inside a single
18-coset plus a single 6-coset. Arbitrary phases 8/9 are allowed: translation
normalizes them. This is a construction-route lemma; unrestricted15120,
the global L_min(8) frontier and independent review remain separate.

Read [proof.md](proof.md) for the complete counting bridge. The earlier
[twelve-shape reduction](../stage720-six-orbit-reduction/proof.md) supplies
the 96 previously excluded target pairs. Its proof/certificate is a credited
dependency at commit `c87f46d672552ca570cd7bc0293969a4e3688c17`, exact CID
`bafkreibhwbabvc6mqjab3riotqp33y52r73wffazskkh7rcpbhwadaz76m`.
Its source must be present in the sibling directory. The checker authenticates
its certificate pin and target inventory; it does not rederive that entire
earlier proof.

From this directory, with CPython3.11 or later and no external packages:

```sh
python3 check.py
python3 -O check.py
python3 audit.py
python3 -O audit.py
python3 controls.py
python3 -O controls.py
```

All solver/BLAS/OpenMP thread settings in the author run were one; no solver
is used here. Each command is a separate CPU job. `check.py` recomputes all 168
integer envelopes and validates the complete phase split. `audit.py` independently
uses physical sets and tuple resource pools. Normal and optimized Python must
give the same mathematical summary. Twelve damaged inventories or bounds are
rejected by `controls.py`, including under `-O`.

The certificate rows are compact exact outputs, not a large proof corpus.
All free phases of each original label are enumerated when producing pair
profiles. After12 or12+16 is fixed, those ORIGINAL labels are removed and
their literal classes are removed from the residual. The two-level split
has 66 strict first leaves plus 96 strict second leaves. No nonstrict parent
is called feasible. The smallest strict gap is 2; no numerical tolerance is used.

`expected.json` was frozen from completed private calculations and their
separate same-author replay before the public comparison runs. Public checks
do not overwrite it. Checksums identify source bytes and do not substitute for
the counting argument. [manifest.json](manifest.json) records actual commands,
runtimes, resource use and the same-author/unformalized trust boundary.
Generated logs, solver environments and operational records are omitted.
An incomplete or killed run proves nothing.

For a fresh replay of the credited prerequisite, run its `check.py` and
`audit.py` in the sibling `stage720-six-orbit-reduction` directory first.
Those short prior-source checks were performed in the preceding publication
pass; the new author checks additionally match the exact pinned prerequisite
certificate bytes and all twelve target phases.
