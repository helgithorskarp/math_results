# Structural and checker handoff for independent acceptance

This is a source-level handoff, not an accepting review of the exact value.
The structural lane has parked its native replay while the independent
reviewers check the complete corpus. Its frozen core and 13,675 saved
ordinary-checker records remain unchanged. No native proof check was run
for this handoff.

## The mathematical boundary already supplied

The [geometry review](../decision71_geometry_audit/REVIEW.md) checks the
lossless cover by 109,676 quotient representatives and the affine gauge.
The preferred structural input is the independently reviewed
[two-low-plane theorem](../low_pair71/THEOREM.md). No one-six-plane
classification, cubic-moment exclusion, or further local marginal condition
is needed by this cover. The separate [input audit](INPUT_AUDIT.json)
reconstructed every full CNF and matched all 112 published digest blocks.
It performed zero native proof checks.

The input-audit contribution is committed at Discovery Net height 6092,
reference `bafkreibzukiugw4pdgcpp4xvdgzysosq7icuwyso5l7v6kgu45nu7rjcqi`.
Its full body and seven relations were read back and matched. The original
source commit is `c72217b52bd58ac0e4ee3d7c099be7fa6e644e48`.

Independent acceptance still requires complete proof coverage for those
formulas and an explicit checker trust account. Combining a complete
accepted exclusion with the directly checked 70-point example and subset
monotonicity would determine the value. Neither this note nor the partial
ordinary replay supplies that acceptance.

## A qualification to warning suppression

The active reviewer reported an ASan/UBSan finding in the optional warning
printer for case 20750. Inspection here independently confirms the source
mechanism: `ID` is -1; `printClause` reads `clause[ID]`; two parser warning
sites pass the unshifted allocated `buffer`. The official `-w` option skips
those calls. This inspection did not rerun the native checker or sanitizer.

There is also a necessary qualification: **`-w` is not globally a
printing-only change on arbitrary input.** In the malformed-binary-prefix
branch, `break` is inside the `warning != NOWARNING` guard. An invalid
command byte therefore stops parsing with ordinary warnings but does not
take that break with `-w`. This is a directly inspectable control-flow
difference, not a demonstrated false acceptance of a theorem or trace.

All locations below refer to the byte-identical pinned upstream
`drat-trim.c`, SHA256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`:

| Source location | Fact to inspect |
|---|---|
| lines 36, 78–80 | negative metadata index in `printClause` |
| lines 983–994 | signed-int base-128 literal decoder |
| lines 1069–1070 | raw parser buffer allocation |
| lines 1106–1115 | binary-prefix branch and warning-guarded `break` |
| lines 1168–1173, 1177–1185 | raw-buffer warning calls; deletion handling follows outside printing |
| line 1415 | `-w` sets `NOWARNING` |

Primary source: [upstream DRAT-trim](https://github.com/marijnheule/drat-trim).
Pinned upstream commit: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The [author generator](../decision71/replay.py) deliberately copies the
native **binary** proof stream. Forcing ASCII mode is not a remedy for
this corpus.

The final team refresh reports that the reviewer has already moved from
the provisional `-w` plan to a narrower two-call diagnostic patch. We
inspected that proposed change: a raw-buffer printer omits the negative
metadata read, and only the two raw-buffer call sites use it. Ordinary
warning guards and the malformed-prefix `break` remain. The candidate
source hash reported by the reviewer is
`12173598973df1d7d374cfedea977451c10d5a7aea7c90dc77f41c8cf2fad1b0`.
This is progress context, not an adopted or completed independent review:
its final source and complete execution evidence still need publication.
The guard below is an optional input check, not a request to replace that
route or rerun an ongoing corpus audit.

## A small input guard for reviewers

[`binary_drat_framing.py`](binary_drat_framing.py) provides an independent
streaming syntax guard. It accepts canonical binary a/d commands and
zero-terminated clauses, rejects incomplete or overflowing literal codes,
and hashes the exact bytes it processes. The accepted literal-code bound
keeps the pinned decoder's bit shifts within a 32-bit signed integer.
This is a deliberately restricted subformat, not a claim to recognize
every encoding tolerated by DRAT-trim.

For an accepted stream, induction over command and literal boundaries
shows that the malformed-prefix branch cannot be reached: every command
starts with a/d, both decoders consume the same canonical literal bytes,
and each zero ends a clause. Thus that particular non-printing difference
of `-w` is irrelevant to such a stream. This does not prove the rest of
DRAT-trim correct or replace complete instrumented proof checking.

The guard can consume chunks from an existing hash loop, avoiding a second
corpus read. Its digest must be bound to the same bytes passed to the
native checker. Standalone invocation is:

```sh
python3 binary_drat_framing.py /path/to/case_020750.drat
python3 framing_controls.py
```

It reports `BINARY_DRAT_FRAMING_VALID`, `syntax_only=true`, and
`global_unsat_accepted=false`. Empty streams and a false empty-clause proof
can pass syntax checking. No derivation, RAT condition, deletion validity,
or UNSAT claim is checked. The small controls and two archived-case samples
are recorded in [FRAMING_VALIDATION.json](FRAMING_VALIDATION.json).
**The full corpus has not been checked by this guard.** Reviewers may
instead establish the same format condition by their own parser audit;
this handoff does not require duplicating an ongoing full replay.

## Preserve the evidence distinctions

The completed all-formula audit is unaffected by the native warning issue.
The saved 13,675 ordinary native checks remain historical execution
evidence; they are not sanitizer coverage or a substitute for the current
independent acceptance runs. Their source is frozen so earlier checkpoint
identities remain reproducible.

Archived proof identity and regenerated proof validity are different
obligations. Case 20750 already has two different saved traces for the
same CNF. New valid traces need not have historical proof hashes. Every
fresh input must still represent the correct quotient, and every fresh
trace must actually be checked with the reviewer's stated options.

No new mathematical counterexample or gap is claimed. The newly recorded
issue is an overly broad interpretation of warning suppression and its
precise binary-format condition. Exact-value acceptance and the campaign
handoff remain pending.
