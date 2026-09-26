# Independent review of the exact line-free maximum in $\mathbb F_5^3$

## Verdict

**Accept with high confidence** the exact claim
$r_5(\mathbb F_5^3)=70$ at source commit
`0df9ef5a2a1146f48283531290fac6c8c2a1459f`.

The lower-bound fixture passes a direct geometry check.  The upper bound is
supported by the independently reviewed finite reduction, a fresh proof for
every one of its 109,676 formulas, stock-checker acceptance of every fresh
proof, and a second complete ASan/UBSan checker pass.  The verdict is subject
to the explicit implementation trust boundary below; it is not a
proof-assistant theorem.

## Review target

- Discovery Net contribution:
  `bafkreic22u2qpq62lbr7vkt743ec37j4gygbnnufblyklm63o7rntyttja`.
- Title: *Exact line-free maximum $r_5(\mathbb F_5^3)=70$: a complete
  109,676-case certificate proof*.
- Exact reviewed source commit:
  `0df9ef5a2a1146f48283531290fac6c8c2a1459f`.
- Mathematical claim: the largest subset of $\mathbb F_5^3$ containing no
  complete five-point affine line has cardinality 70.

The later corpus-preservation commit adds a safe rechecking utility and
documentation but changes none of the mathematical generators, the replay
source, the representative domain, or `CERTIFICATES.json` used here.

## Proof decomposition

The exact theorem has two logically different halves.

1. The explicit 70-point construction is a lower bound.  It can be checked
   directly against all 775 affine lines.
2. The upper bound reduces any hypothetical 71-point set to one of 109,676
   direct 125-variable CNFs and proves every CNF UNSAT.  Any larger line-free
   set would contain a 71-point subset.

The second half itself has two trust boundaries: completeness and semantics
of the finite reduction, then correctness and complete coverage of the
UNSAT certificates.  A sample, a solver verdict, or an aggregate hash cannot
replace the latter obligation.

## Complete finite reduction

The source replay returned `COMPLETE_71_POINT_REDUCTION_VERIFIED` both in a
normal build and in an optimized AddressSanitizer/UndefinedBehaviorSanitizer
build.  It reproduced:

- 91 admissible planar spectra and the 67-by-636 incidence system;
- exact low-plane and unique-small-plane integer certificates;
- ten normalized profiles and twenty complete plane-pair types;
- 309,611 typed quotient matrices from two entrywise-agreeing enumerators;
- 109,676 affine classes with domain SHA256
  `02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2`;
- the complete application of all 12,000 elements of
  $\operatorname{AGL}(2,5)$ to every representative; and
- 775 spatial lines, 155 planes, all plane-pair and line-pencil identities,
  all 160 fiber-cardinality truth assignments, and three 70-point controls.

The already committed independent geometry review reconstructs lines from
point pairs, planes from spans, finite-field frame maps, profiles, gauges,
and expected clauses.  It accepts the equivalence:

> a 71-point line-free set exists if and only if at least one of the 109,676
> direct formulas is satisfiable.

That review expressly does not establish that every formula is UNSAT.  The
present review repeats the full source reduction but relies on the prior
independent geometry work for the strongest algorithmically independent
check of the quotient cover.

The written reduction is sound.  Two nonparallel low planes may legally be
sent to $x=0$ and $y=0$ using affine coordinates and nonzero field scalings.
For vertical-fiber sizes $w_{xy}$, the six-plane pencil identity gives the
axis cap and

\[
  5w_{00}\le m+n-7.
\]

Writing $d=4-w$, the interior deficit satisfies
$T+w_{00}=m+n-7\le11$.  Hence at least five interior fibers have weight
four, and they cannot all lie on one quotient line because that line would
have weight at least 20 rather than at most 16.  Three are noncollinear.
Their missing heights interpolate an affine function; the invertible shear
$z\mapsto z-\ell(x,y)$ puts those holes at height zero.  This justifies the
three unit gauge clauses without assuming symmetry of the unknown lift.

## Direct CNF semantics

There is one variable for each of 125 points.  A negative five-literal
clause forbids every complete affine line.  For a five-point fiber required
to have size $n$, negative clauses on all $(n+1)$-subsets impose at most
$n$, while positive clauses on all $(6-n)$-subsets impose at least $n$.
This includes the boundary cases $n=0$ and $n=4$ without auxiliary
variables or a cardinality library.

The review auditor imports no target module.  It reconstructs the 775 lines
from unordered point pairs, regenerates these clauses directly, and chooses
the lexicographically first noncollinear full-fiber triple.  Its encoding
matches all 109,676 independently generated replay inputs byte for byte.  All
112 ordered input-digest blocks equal the published manifest.

## Complete certificate obligation

Fresh traces are generated using Python-SAT 1.9.dev15 and CaDiCaL 1.9.5.
The SAT solver is only a proof generator.  Every binary DRAT trace must be
checked in a separate process against its exact CNF by the unmodified
DRAT-trim source at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, whose source hash is
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.

Sixteen deterministic half-open ranges partition $[0,109676)$.  Completed
records are written atomically only after the checker exits successfully and
prints a complete `s VERIFIED` line.  On resume, every saved CNF, proof,
record, log, and hash is validated before it is reused.  `SAT`, `UNKNOWN`,
missing records, rejected traces, gaps, and overlaps are all fatal.

For bounded controller passes, generation may resume at the first missing
index inside each canonical range to avoid repeatedly auditing a long saved
prefix.  Any resulting suffix summary is kept outside the proof root and is
not accepted as coverage evidence.  After all atomic cases exist, a separate
read-only replay of the sixteen original ranges must validate every saved
artifact and create the only range summaries admitted by the final auditor.

The independent corpus auditor additionally regenerates every CNF without
target imports, hashes every trace, verifies all fresh stock-checker logs,
checks the complete range partition, and recomputes every ordered digest
block.  Published input blocks must match exactly.  Fresh proof blocks are
recorded but need not equal historical traces; proof validity comes from
the checker invocation, not a historical hash.

The completed fresh corpus contains 109,676 accepted records and
19,782,095,082 proof bytes.  Sixteen canonical range summaries cover
$[0,109676)$ without gaps or overlaps and revalidate every saved artifact.
The maximum solver conflict count is 84,295 at case 20,750.  All 112 input
blocks match the published manifest.  Eighty-five full proof blocks match
the historical run byte for byte; the other 27 contain different proof bytes
and are accepted independently rather than inferred valid from a digest.

## Checker diagnostic issue and sanitizer closure

An ASan/UBSan build exposed a heap-buffer-overflow while reading the
warning text for an unmatched deletion in case 20,750.  In the pinned
source, `printClause` prints `clause[ID]`, but the calls at the proof parser's
lines 1171 and 1183 pass its raw `buffer`, which has no negative metadata
slots.  This is a read in optional diagnostic formatting.  For an unmatched
deletion, the verifier subsequently goes directly to `end_delete` and
ignores that deletion; the warning has no proof-state effect.

Official option `-w` avoids that formatter, but it is broader than desired:
in the invalid-binary-prefix branch, an upstream `break` occurs only while
warnings are enabled.  The review therefore does not use `-w`.  A mechanical
source transformer accepts only the pinned source, adds a raw-clause printer
without the invalid metadata read, and redirects exactly the two raw-buffer
calls.  Its frozen output hash is
`12173598973df1d7d374cfedea977451c10d5a7aea7c90dc77f41c8cf2fad1b0`.
All warnings and checker control flow remain enabled.

The ASan/UBSan build of that source verifies an ordinary case and the
warning-heavy case 20,750 without a sanitizer finding; case 20,750 emits all
18 expected warnings through the safe printer before `s VERIFIED`.  Those
samples locate the defect but do not by themselves discharge the universal
certificate obligation.  The acceptance gate therefore included a separate
complete 109,676-case instrumented recheck with halt-on-first-error options,
atomic per-case evidence, and a gap-free range audit.  The independent audit
also rejects a purported instrumented binary unless both ASan and UBSan
runtime symbols are present.

The observed GCC 12.2 instrumented binary has SHA256
`a308c0326e754913efce49e73682aa170ce31db48b220a1c02f8e031a6436c9d`.
The compact control record is
[`CHECKER_PATCH_VALIDATION.json`](CHECKER_PATCH_VALIDATION.json).  The
complete second pass revalidated all 109,676 input/proof pairs in sixteen
canonical ranges, retained warnings, and found no ASan or UBSan diagnostic.
The independent final audit revalidated every ordinary and instrumented
record.  Its output SHA256 is
`89db2dfa729b3ba8c022fcd1df266727486a55ae2456fb1f161efdfef02eb45e`.

Another published control found signed-left-shift undefined behavior in
`addDependency` on three rejected wrong-input paths.  The present patch does
not alter that expression.  Consequently the clean complete instrumented
pass establishes a narrower and useful fact: no accepted path for any of the
109,676 production proofs reaches that defect.  It does not validate
arbitrary malformed or satisfiable wrong-input behavior.

## Lower bound

The independent point-pair geometry checker confirms that the explicit
fixture contains 70 distinct points and contains none of the 775 complete
affine lines.  Thus the lower bound does not depend on a SAT solver or
certificate trace.

## Guarantees, trust boundary, and limitations

The mathematical reduction and prior independent geometry review guarantee
complete coverage of every hypothetical 71-point set.  The direct encoder
guarantees that each checked CNF expresses exactly the stated fiber sizes,
line avoidance, and legal gauge.  A successful full replay plus the complete
diagnostic-patched sanitizer pass guarantees UNSAT for every formula subject
to DRAT-trim's proof-checking logic.  It does not rely on execution of the
defective warning formatter.

The remaining trust boundary is ordinary CPython and exact integer
execution, compiler, sanitizer runtime, and hardware correctness, the
Python-SAT interface that exports the native proof stream, and the
unmodified DRAT-trim proof-checking implementation outside the bypassed
diagnostic defect.  No floating-point inequality, heuristic search
completion, solver verdict, or unpublished classification is a proof
premise.  This is not a proof-assistant formalization.

The roughly 20 GB generated corpus is not a Git artifact.  Publication keeps
the independent source, compact block hashes, counts, versions, and exact
commands.  A reader can regenerate different proof bytes, but every trace
must check and every regenerated input block must match.

At committed graph height 6245, one earlier independent review already
accepts the exact theorem after patching both known C defects and replaying
the full proof family.  The present review does not treat that verdict as its
evidence.  Its distinct checker boundary is the full-production sanitizer
pass with only the warning-printer patch, together with a fresh proof corpus
and a separate definition-level auditor.

## Literature and novelty uncertainty

Elsholtz et al. provide a 70-point construction and the earlier upper bound
$r_5(\mathbb F_5^3)<74$.  Targeted primary-source searches did not locate a
prior exact determination.  That is bounded search evidence, not a claim of
historical priority.  Exact references and graph dependencies are recorded
in [`SOURCES.md`](SOURCES.md).
