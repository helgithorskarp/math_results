# Independent review boundary

This is an author-supplied guide, not an independent review or acceptance.
The claimed exact value is 70; its new proof obligation is the complete
exclusion of 71 points. The earlier accepting reviews do not cover that
obligation.

The written proof and reproducible checks have three separate parts:

1. **Complete mathematical cover.** Audit the plane cap, line-pencil and
   plane-pair identities, exact integer certificates, and legal coordinate
   normalizations. Either the self-contained twenty-type argument or the
   independently reviewed fifteen-type theorem supplies a complete cover.
   `verify.py` checks both routes. No prior SAT exclusion is required.
2. **Complete finite domain and exact formulas.** Reproduce the two
   entrywise quotient enumerations and the complete 12,000-map affine
   audit. Check that the 109,676 representatives cover every candidate.
   Audit the 125 point variables, all 775 affine-line clauses, direct
   fiber-cardinality clauses, and lossless three-hole affine shear. A
   different independent encoding may complement the variables or choose
   another noncollinear triple; it must preserve the same complete domain.
3. **Every remaining lift.** Run all proof cases and check every trace.
   An unmodified DRAT-trim build removes the production allocation patch
   from the review's trusted code. Fresh traces need not match historical
   proof hashes. `audit.py --compare-inputs CERTIFICATES.json` verifies the
   original exact input family when using the supplied generator. The
   resulting full audit must have 109,676 cases, complete coverage and no
   unknown or rejected cases. A partial range or sample is not a complete
   review of this claim.

For existing proofs, use `recheck.py` to write every fresh checker result
into a new directory while preserving all four original case files. The
[corpus guide](CORPUS.md) specifies the command, block hashes and complete
success condition. The original large corpus is preserved privately;
readers with only the repository can instead generate fresh proofs.
The older `replay.py --recheck-existing` replaces saved checker logs and
identities and is appropriate only for disposable copies. The separate `audit.py`
regenerates formulas and checks evidence integrity but does not infer
DRAT validity from logs or hashes alone. Missing and overlapping range
audits are rejected by `merge_audits.py`.

Independence should be reported by actual method: source replay, different
enumeration algorithm, independent mathematical reduction, alternate
formula encoding, or different proof checker. Reusing a generator while
changing only the solver does not independently validate its semantics.
The plain-language argument remains outside proof-assistant verification.

For the lower bound, the 70-point input is explicitly listed and checked
directly. Once every 71-point candidate is excluded, larger sets are
excluded by taking a 71-point subset. A durable independent acceptance
of this complete argument, identifying reviewed source and replay scope,
is the remaining campaign handoff requirement.

The earlier geometry review pins its entire source snapshot, including
documentation, at `0bd139b2d32f58fcb080b6f90aa42387931d54b6`. Its
`--check-expected` command targets that snapshot. This final publication
changes documentation and adds complete evidence, so that old whole-file
manifest is intentionally no longer the current directory manifest.
The mathematical implementation and inputs are unchanged. The geometry
checker can also run on the current source without `--check-expected`;
compare the mathematical output separately from `reviewed_files` and
`seconds`. This does not extend the earlier review to the global proofs.

## Later independent input audit

The [independent formula review](../decision71_independent_proofs/REVIEW.md)
at source commit `c72217b52bd58ac0e4ee3d7c099be7fa6e644e48` reconstructs
all 109,676 formulas without importing the author's point-model or evidence
modules. Its [input audit](../decision71_independent_proofs/INPUT_AUDIT.json)
matches every stored CNF byte and all 112 input/proof digest blocks.
Its [source comparison](../decision71_independent_proofs/SOURCE_BRIDGE.json)
identifies the unchanged mathematical files from the accepted geometry
review. This completes the reported all-formula audit; that audit invokes
no native proof checker. The separately recorded proof replay is partial,
and the review explicitly leaves exact-value acceptance pending.

## Recording a completed review

A useful final review can record the following distinctions. This is an
author handoff guide, not an accepting verdict or a request to duplicate
an ongoing computation.

| Review record | Evidence to identify |
|---|---|
| Target and source | Exact theorem and graph artifact; reviewed source commit, domain hash, input manifest, and any source changes |
| Mathematical coverage | Accepted or newly checked finite reduction, coordinate normalizations, and formula semantics; cite reused reviews with their actual scope |
| Proof coverage | Exact case identities covering `[0,109676)`, checked inputs, proof hashes, and successful checker results; account for missing, rejected, SAT or UNKNOWN cases |
| Checker and execution | Checker source/build/flags, patches, fresh versus resumed checks, and the actual scope of any sanitizer or alternative-checker run |
| Exact-value conclusion | Directly checked 70-point construction, complete exclusion of 71 points, and the subset argument excluding larger sets |
| Verdict and durable evidence | Explicitly identify what is accepted, pending or rejected; link the published source and compact results and the committed review artifact |

For split runs, reconcile exact coverage and overlap before reporting a
complete family. Progress totals from separate reviewers, repeated checks,
pilot cases and resumed checkpoints cannot simply be added. Fresh valid
traces may differ from historical proof hashes; the review must say whether
it checks the original archive or regenerated evidence. A progress snapshot,
complete input audit, or successful sample does not replace the remaining
proof checks. Mathematical acceptance and campaign handoff authorization
are separate: this guide authorizes neither.
