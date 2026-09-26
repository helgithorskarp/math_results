# Review of the complete formula and certificate boundary

**Verdict:** accept the independent reconstruction and integrity audit of
all 109,676 published lift inputs. **Independent acceptance of the exact
value 70 is still pending.** The separate native proof replay has checked
13,675 cases, leaving 96,001. No numerical extremal bound is established
by treating the input audit or that partial replay as a full exclusion.

The target is the [complete author proof](../decision71/THEOREM.md),
Discovery Net `bafkreic22u2qpq62lbr7vkt743ec37j4gygbnnufblyklm63o7rntyttja`
(height 6076). Our [earlier geometry review](../decision71_geometry_audit/REVIEW.md)
accepts its complete finite reduction. The author has now supplied all
UNSAT traces, so the remaining decisive obligation is their complete
independent checking against the correct inputs.

## Complete input reconstruction

The new code imports no author point-model, geometry, or evidence module.
It constructs the 775 spatial lines directly from all pairs of points of
\(\mathbb F_5^3\). Points are ordered lexicographically, with Boolean
variable \(1+25x+5y+z\) selecting \((x,y,z)\). A negative clause on each
five-point line forbids that complete line.

For a fiber of required weight \(n\), the program generates Boolean
words of length five. Each word with \(n+1\) ones gives the corresponding
negative clause; each with \(6-n\) ones gives a positive clause. These
enforce at most and at least \(n\) selected points. The empty lower family
at \(n=0\) is correct: the upper clauses already forbid every selection.
This generation differs from the author's subset-combination routine.

The gauge is obtained using separate Gaussian elimination over
\(\mathbb F_5\). A full fiber has four selected points and one hole.
Three noncollinear full fibers determine an affine height function whose
subtraction moves their holes to zero. The earlier review proves that
every quotient in this complete domain has such a triple and that this
shear loses no candidate. The new reconstruction chooses the ordered
triple directly and emits the three negative height-zero unit clauses.

For **every** ordered quotient representative, the resulting complete
DIMACS byte string equals the actual stored CNF, including its header,
clause order, signs, point numbering, cardinalities and gauge. The source
also checks the original record's index, type, weight word, gauge, variable
and clause counts, domain hash, input hash, proof hash and proof length.
Every ordered digest block agrees with the public manifest.

[INPUT_AUDIT.json](INPUT_AUDIT.json) records:

- 109,676 independently reconstructed formulas and exact stored-byte matches;
- all twenty type counts, matching the complete domain;
- all 112 ordered input/proof digest blocks;
- 19,782,097,200 original proof bytes hashed;
- **zero native proof checks performed by the input-audit program**.

The serial reference and the eight-thread version both completed, agreeing
in every mathematical output. Threading changes independent I/O scheduling;
ordered collection and all case and block checks remain the same. A separate
31-case comparison also agreed entry by entry across all twenty types.
These are execution regression checks, not independent mathematical
enumerations. The formula construction is independent of the author's
implementation; completeness of the quotient domain remains the already
reviewed geometric/enumerative premise.

## Native proof replay so far

The reviewer compiled the official, **unmodified** DRAT-trim source at
upstream commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` using
`gcc -std=gnu99 -O2`. Its exact source and executable hashes are recorded
in [VALIDATION.json](VALIDATION.json). No author allocation patch is used.

Each proof check first regenerates and compares the whole CNF, validates
the corresponding input and proof identities, then starts a new native
checker process. Acceptance requires a zero exit status and an entire
output line equal to `s VERIFIED`. Source CNF/proof sizes and modification
times must remain unchanged across that invocation. Timeouts, crashes,
missing evidence and rejected proofs are failures, never exclusions.

The bounded four-worker run completed **13,675** checks and stopped
cleanly. The durable, checked prefixes are:

| Required range | Checked prefix | Cases |
|---|---|---:|
| [0,27419) | [0,3525) | 3525 |
| [27419,54838) | [27419,30994) | 3575 |
| [54838,82257) | [54838,58038) | 3200 |
| [82257,109676) | [82257,85632) | 3375 |

Twelve complete manifest blocks contain 12,000 cases; validated partial
checkpoints contain another 1,675. These checks cover 2,239,656,093 proof
bytes. [PROOF_PROGRESS.json](PROOF_PROGRESS.json) pins their ordered input
and proof digests and the frozen source and checker identities. The pilot
and separate controls are not added to this production count.

The source now saves atomic groups of 25 cases, as well as full manifest
blocks. On resumption it checks code/checker/domain/manifest identities,
case order and type, and reconstructs and hashes partial checkpoint inputs
again. A real two-process stop/resume test preserved old checkpoint bytes
and counted only newly executed checks as fresh. Completed review state is
trusted local execution evidence; a new independent reviewer must begin
with an empty output directory and run the proof checks.

The earlier uncheckpointed process did not survive an agent turn boundary.
Its unsaved progress is not included here. The current bounded run has
finished, and its durable prefixes can be resumed without relying on
background-process survival across controller rests.

## Regenerated traces and rejection controls

Fresh generation of case 20750 produced a proof with different bytes from
the original, despite the same input and solver conflict count. The
original has 3,482,287 bytes; the new proof has 3,482,192 bytes. Both were
checked here with unmodified DRAT-trim against the same independently
reconstructed CNF. This is permitted by the author's documentation and is
not an error in the exact-value proof.

Accordingly, `check_saved.py` deliberately binds the original archive and
its historical block hashes. `check_regenerated.py` independently rebuilds
the formulas and freshly verifies new traces without imposing historical
proof hashes. Its positive changed-trace test passed. A false empty-clause
trace was rejected even after its record was changed to match its hash
and size. This prevents confusing fresh-proof validity with archive identity.
The new-trace driver has not completed an entire-family run.

The ordinary and Python-optimized pilots agreed on 31 cases spanning all
twenty types, boundaries and the hardest author case. They directly checked
a genuine 70-point line-free set and its normalized satisfying assignment.
Three native rejection controls, four damaged-block controls, eight
damaged-partial-checkpoint controls, an incomplete-summary rejection and
the bounded-dispatch control all passed. These controls exercise the
acceptance boundary; they do not replace the unperformed proof cases.

## Provenance, independence and remaining obligation

[SOURCE_BRIDGE.json](SOURCE_BRIDGE.json) confirms that 27 files from the earlier
review are unchanged, including every mathematical program and input.
The six changed pre-existing files concern documentation or evidence.
The final author preservation supplement adds a separate read-only replay
procedure and [corpus guide](../decision71/CORPUS.md), leaving the frozen
manifest and mathematical implementation unchanged. The new author replay
modules are not used by this independent formula checker.

The [two-low-plane theorem](../low_pair71/THEOREM.md) and its independent
review remain the nontrivial structural premise in our preferred reduction.
The latest one-six-plane classification and nonzero cubic-moment theorem
were inspected as team context, not added as filters or assumptions.
There is no new census or local marginal variant in this result.

No mathematical defect was found in the checked parts. The unresolved
requirement is the **96,001 remaining fresh native proof checks**. The
whole-family summary must validate all 112 blocks and exact coverage of
109,676 cases before this replay can support accepting the global exclusion.
The known 70-point construction and subset monotonicity then supply the
other parts of the exact-value conclusion, together with the accepted
geometric reduction. That conclusion is not asserted as independently
accepted in this review, and the campaign handoff remains unauthorized.

The ordinary trust boundary includes the written argument, earlier exact
enumeration/certificate replay, Python and compiled C execution, SHA256
identification, unmodified DRAT-trim, and runtime/hardware. This is not a
proof-assistant formalization. The SAT solver supplies proof traces; its
reported verdict alone is not used to accept a case.

## Strengthening and improvement opportunities

The highest-value next step is to finish the same global replay, using
the durable checkpoints already validated. No additional local subcase,
classification, or marginal relaxation is needed for this acceptance
route. Further reducing trust through a formally checked proof format
would require a separate conversion/checking bridge; this review makes
no claim that such a bridge has been supplied.

The bounded primary-source refresh found the published 70-point lower
bound and upper bound 73 and no external exact determination among the
inspected sources. We make no priority claim. A completed, independently
accepted exclusion of 71 points would close that exact finite-geometry
parameter; the present contribution supplies its complete input audit
and a reproducible path through the remaining proof-checking obligation.
