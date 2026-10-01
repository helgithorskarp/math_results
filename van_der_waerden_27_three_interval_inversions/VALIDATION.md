# Exact coverage and measured resources

Author: six-vdw-1, researcher, 2026-10-01.

The fresh source-only replay completed24 serial stages in27.863s. Longest
child8.970s, largest bounded case count186998, maximum child RSS74280KiB.
It used only this compact package and installed Python-SAT: no private
CNF or proof input. Canonical CNF, DRAT and positive-hint trace hashes all
match `expected.json`. It imports the preceding two-run mathematical lemma
for normalization, explicitly without rerunning that earlier proof.

The24 stages are construction; six independent semantic literal audits
(three complete row parts in each interpreter mode); untrusted native proof
proposal; compilation and proof transformation; strict Python RUP verification
and small proof controls in each mode; and ten encoding rejection checks.

Each proof-control mode accepts two valid small certificates and rejects15
targeted false/malformed certificates, including an empty clause without
hints, a false empty clause over a satisfiable input, missing final conflict,
RAT hints, unavailable/deleted/reused identifiers, satisfied/nonunit hints,
out-of-range variables, repeated or tautological literals, incomplete input
and content after the empty clause. Each encoding-control mode rejects five
defects after updating hashes: wrong first-edit unit, wrong counter overflow,
wrong AP sign, an extra axiom and a Boolean-valued AP coordinate. This totals
40 corruption rejections and four accepted small proof checks.

The final native proposal used9127 conflicts and3.096s in the original
search. Proof transformation reported zero RAT lemmas. The strict checker
verifies34289 added RUP clauses and75318 deletions, with4305587 hint reads
and10763662 literal inspections. Its151143 case count is input clauses plus
proof obligations plus deleted identifiers; the separately reported hint
work is not asserted to be151143 primitive operations.

Before the actual construction search, all512 edit masks of a nine-position
fixture were tested against direct actual-run and all actual-AP definitions
in both interpreter modes. Per mode239 masks satisfy the canonical three-run
definition and273 fail it. All six literal section audits also passed.
These native small-model checks are regression evidence; the written complete
counter extension proof, not small negative answers, proves projection
completeness at3704.

Seven bounded native queries were made, with six SAT words independently
decoded and checked on all1141450 actual positive APs each. All six fail:
their respective monochromatic counts are14235,327,1223,8861,13358,692.
At most128 newly verified bad APs from each word enlarge the1485-AP seed
to2253. The full word checks use seven serial AP-rank chunks, each at most
190000 APs. Literal assignment checking covers every actual clause in
separate bounded row slices; direct run/selected-AP checks use no encoder or
native solver. The search's150 compute children finish in53.237s, longest
3.232s and peak75904KiB. No failed word or native UNSAT alone establishes
the family theorem.

Limits stay30s per child,20s native proof transformation,200000 generation/
audit or logical proof-obligation cases,9500 requested and10000 reported
native conflicts, one thread, one CPU-intensive job at a time, existing
1CPU/2GiB scope. Every construction/audit/query stage is preflighted, even
at the prospective2893-AP feedback cap, with no limit increase. A combined
parse/model-check stage would exceed a stored budget; independently complete
checking is partitioned instead. UNKNOWN, timeout, kill or incomplete
enumeration supplies no exclusion. No such limit event occurred here.

The first small pilot harness expected a `source_sha256` field where the
independent audit writes `checker_sha256`. The failed source/cohort is
preserved privately. A corrected new harness and fresh cohort supplied the
successful pilot; no mathematical source or resource limit changed.

Generated proof traces, CNFs, binaries, detailed journals and checkpoints
remain in scratch and are omitted from the repository. There are no keys,
credentials, private ledger data, archives or environment copies here.
