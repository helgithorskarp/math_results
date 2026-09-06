# All 328 catalog switching classes fail arbitrary one-vertex extension

**No Ramsey(5,5) graph lies in the following complete 43-vertex family:**
choose any of the 328 literal graph6 records in `r55_42some.g6`, arbitrarily
Seidel switch its 42-vertex core, and attach one new vertex with all 42
incident edge colors free. All 328 cases have checked physical UNSAT
certificates. The whole-union gate is complete, not just a checked prefix.

Consequently, every vertex deletion of a hypothetical Ramsey(5,5;43)
graph must lie outside all these catalog switching classes, including
after relabeling and global color reversal. This is a restricted-family
computer-assisted exclusion, **not a general 43-vertex exclusion or a
new Ramsey bound**. No target graph or priority claim is made.

[report.json](report.json) and [cases.tsv](cases.tsv) give the complete
coverage and certificate identities: 1,437,080 necessary physical clauses,
699,541 checked additions (631,970 RUP and 67,571 RAT), 66,248 RAT-side
checks and 2,128,834 deletions. There are no unresolved parents. The
canonical table SHA-256 is
`e3262023b7883a5706650d5bd79b4bb4a9e4da8f4c25b3618faf37a69c4733dd`.

For each parent, variables1..41 are switch bits s_1..s_41 with s_0=0.
Variables42+v,0<=v<=41, are the physical colors of edges {v,42}. A core
edge has color G_uv XOR s_u XOR s_v. Complementing all switch bits changes
no core edge, and comparison of edges {0,v} proves injectivity after
normalization. Each parent therefore gives exactly2^83 distinct labeled
graphs. We do not assume the parent switching classes are disjoint and do
not multiply this count by328. Global color reversal covers complementary
parent orientations; arbitrary relabelings preserve the exclusion property.

There is no degree, automorphism, radius, or neighborhood assumption. A
nonempty/nonfull switch changes |S|(42-|S|)>=41 old-old pairs, so this is
not a replay of the old radius-six enumeration. The old catalog's extension
and radius-closure theorems are not proof premises. Neither the H92/H93
route nor the excluded Paley41 switching class is reopened. Teammate
Core186 switching candidates have a different literal seed and are separate.

## Exact encoding and certificate interpretation

Every five-set consists of either five core vertices or four core vertices
and the added vertex. For each desired monochromatic color c, set the first
core switch to0 and force each other one to G_av XOR c. Test every core
pair. A successful candidate and its complement are exactly the possible
patterns. For a five-set using vertex42, also require all four added-edge
colors to equal c. Negating each event gives a clause. Events requiring
s_0=1 are impossible and skipped; the s_0=0 literal is otherwise removed.
The resulting CNF is exact for the full43family, not a local relaxation.

`generate.cpp` implements this anchored construction. `audit.py` independently
enumerates all switches of every4-/5-vertex graph to reconstruct the full
formula by physical five-sets. The checked parent0 formula has83variables,
102776clauses and SHA256
6b9364ccc144e22db2fddebde67531c79202b83ab36c9e8d185d4f24aa016864.

For UNSAT, `check.py` validates an extracted set of necessary physical
clauses and then checks the entire trimmed DRAT proof. No completeness of
the extracted set is required. For clauses touching new-edge variables,
those four variables determine the four physical core vertices. Their
falsifying colors must agree, and precisely the nonzero core vertices must
have switch literals. Other clauses name five core vertices, adjoining
vertex0 when the width is4. `physical.py` checks every underlying pair.

The forward multiset-based RUP/RAT checker is reused by a pinned import
from `../ramsey_r55_paley41_switch_family/check_certificate.py`, SHA256
c11cb9ced4987bdb8384cc57a87c455c9d59c33f28df56da53918351c0516e2c.
Only its generic proof-checking functions are used, not its Paley graph
interpreter or theorem. The present graph decoder and physical mapping are
new. The theorem depends on this unformalized physical bridge,
checker implementation, compiler/Python semantics and execution platform, not on a SAT verdict,
catalog completeness, nauty, or full-formula coverage. There is no external
independent review of the new adaptation.

The final production path uses [fast_check.py](fast_check.py) with the
straightforward C++ port [check_drat.cpp](check_drat.cpp). This is a
cross-language regression check, not an independent mathematical proof
kernel. The original Python checker remains available. The native checker
matches every certificate statistic on all 76 Python-checked prefix
cases, and all 328 final cases were subsequently replayed with their
physical clauses and every saved run-file hash checked by
[collect.py](collect.py). Its report does not merely trust `completed.json`.

The proof kernel's soundness argument is short. RUP means unit propagation
contradicts the negation of the proposed clause C, so C is implied.
Otherwise choose its first literal p. For every current clause D
containing -p, require RUP of C union (D minus {-p}). If a model falsifies
C, flip p to satisfy C. Any D that becomes false would have had all its
other literals false beforehand, contradicting the checked implication.
Thus a RAT addition preserves satisfiability, including with a fresh
pivot variable. Deletion removes one multiset copy and weakens the
formula. A final empty clause must pass RUP, and no subsequent line is
allowed. Induction proves the physical input clauses contradictory.

## Preflight and bounded batch

CPython3.11.2, standard library, GCC12.2.0:

```sh
g++ -std=c++17 -O3 -Wall -Wextra -Wpedantic -Wconversion -o generate generate.cpp
g++ -std=c++17 -O1 -g -Wall -Wextra -Wpedantic -fsanitize=address,undefined -fno-omit-frame-pointer -o generate-sanitize generate.cpp
python3 controls.py ./generate
python3 -O controls.py ./generate-sanitize
./generate r55_42some.g6 0 /path/to/family.cnf
python3 audit.py r55_42some.g6 0 /path/to/family.cnf
python3 batch.py /path/to/run --generator ./generate --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

Controls test74literal small graphs and19456complete global assignments,
including17986satisfying cases;5bad physical clauses and6bad graph6records
are rejected. Normal and optimized/sanitized results agree. Native production
was chosen because the previous Python million-five-set generation took
7.6seconds; repeating that328times would spend about42minutes on generation.
C++ uses bounded indices0..41, at most8literals per clause, and no bit shift
outside0..5 in graph6 parsing. Arithmetic and iteration are deterministic;
there are no floating-point operations or solver symmetry assumptions.

The retained reference `batch.py` is sequential, indices0..327, with one Kissat invocation per parent,
`--time=30 --no-binary`, and a45-second wall safeguard. At the first UNKNOWN,
invalid model, failed proof, or unresolved checkpoint it stops without an
equivalent retry. Completed case JSONfiles are written atomically; a resumed
batch rechecks completed certificates before skipping their solver calls.
For a graceful stop, create a file named `STOP` in the run directory or
send SIGTERM to the driver PID only. The driver finishes its current case,
writes its checkpoint, and stops before beginning another case. Do not
send the signal to its child solver or whole process group. Move the stop
file away before an explicitly requested resume. A pre-existing stop-file
control has been checked to exit before parent0 without invoking a solver.
Pending solver/proof cases deliberately require inspection rather than an
automatic new solve. A SATmodel is decoded and checked on every physical
five-set. The SAT branch was not exercised by this all-UNSAT run and is
not in the exclusion's trust base.

Keep runtime state outside Git. Each completed parent folder contains the
full formula, raw proof, extracted core, trimmed trace, logs and `result.json`.
`progress.json` is mutable operational state; `completed.json` is created only
after all 328 parent certificates pass. It is now present. The earlier
23-case and 76-case checkpoints remain historical, superseded prefixes.

## Final native and parallel reproduction

Run from this directory, keeping all generated files outside Git:

```sh
g++ -std=c++17 -O3 -Wall -Wextra -Wpedantic -Wconversion -o /path/to/check-drat check_drat.cpp
python3 -B proof_controls.py /path/to/check-drat
python3 -O -B runner_controls.py
python3 -B parallel_batch.py /path/to/run --generator /path/to/generate --kissat /path/to/kissat --drat-trim /path/to/drat-trim --checker /path/to/check-drat --jobs 4
python3 -O -B collect.py /path/to/run /path/to/audit --checker /path/to/check-drat --jobs 4
cmp /path/to/audit/report.json report.json
cmp /path/to/audit/cases.tsv cases.tsv
sha256sum -c SHA256SUMS
```

Use Kissat 4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`
and DRAT-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` for
the recorded identities. A different solver build may yield different
valid certificates: the physical and forward proof checks, rather than
matching a hash alone, are the mathematical test.

The original driver finished parents 0..75 and stopped cleanly. Only the
252 unfinished parents were then dispatched in increasing index order
to at most four workers, each owning a distinct directory. Every parent
still had one 30-CPU-second Kissat invocation with a 45-second wall guard.
No case reached its cap or was retried. The restarted driver replayed
the 76 saved certificates before dispatch, and finished in 497.763 seconds.
For a graceful parallel stop, create `STOP` in the run directory or send
SIGTERM to the controller PID only: no new parent is dispatched, and all
already dispatched proofs finish before the controller exits. An unresolved
case stops further dispatch; up to three other in-flight cases may finish.
Never launch two drivers on the same run directory simultaneously.

Native controls check all 512 two-variable clause databases using 27,648
RUP implication and 27,648 RAT satisfiability-preservation tests against
direct three-variable assignments, including fresh pivots. Five positive
trace regressions and 16 malformed/false-proof controls pass. Address and
undefined-behavior sanitizers pass these controls and parent 0's proof.
All native arithmetic is bounded: input/proof literal magnitude at most
1,000,000, signed values in {-1,0,1}, and 64-bit step/multiplicity counts.
No mathematical graph variable is omitted by this proof-parser bound.

The native physical-plus-proof replay took 36.904 seconds for the 76-case
reference prefix. Parent 0 took 0.510 seconds versus 12.293 for the simpler
Python implementation (about 24.1 times faster on that case). This is a
measured workload result, not a general speed claim. Runtime optimization
changed execution only, not the family, clauses or output schema.

The 328 cores total 25,354,724 bytes and trimmed proofs 53,829,561 bytes.
Those bulky generated artifacts, full formulas, raw traces, binaries and
logs are retained locally, **not committed**. The public source regenerates
them; `cases.tsv` pins every full formula, extracted core and trimmed proof.
Thus a public reader needs regeneration or the saved local certificates
for complete proof replay, not just the compact summary. There is no
claim that the hashes themselves certify contradiction.

## Concrete comparison with the Core186 family

The teammate's [separate 41-core result](../ramsey_r55_core186_switch_family)
uses source `5651aa9620f72b296fa6d6f7c889b5f440da821d`, Discovery Net
height 3347. Its fixed physical core has SHA-256
`996d8040696d0aaf4e9faf92eb24cd17ff54248eecebb699fa87d8c764b8f68a`.
Our designated cores have order 42, catalog indices 0..327 and the archive
hash below. Neither result is a premise of the other's exclusion.

There is also a reproducible non-subsumption certificate. Take our parent
0 without switching and add an isolated red-graph vertex 42. For each of
its 903 induced 41-vertex subgraphs, count odd-red-parity triangles through
each pair and form the histogram of these 820 counts. Switching preserves
triangle parity, and relabeling preserves this histogram. None equals
the teammate's core histogram or its complement histogram (counts t become
39-t). All 903 histograms agree between direct triangle enumeration and
subtracting the two removed vertices from full pair counts.

Thus this explicit member of our union lies outside the entire Core186
switch-extension family, even after relabeling and color reversal. It is
deliberately **not a target**: {0,1,2,3,42} is an independent five-set.
This proves non-subsumption, not disjointness of the two full families.
[deduplicate.py](deduplicate.py) and [deduplication.json](deduplication.json)
give the exact check; they use only the pinned physical core, not the
teammate's exclusion verdict or proof kernel:

```sh
python3 -B deduplicate.py --output /path/to/deduplication.json
cmp /path/to/deduplication.json deduplication.json
```

The earlier Paley(41) result has received independent acceptance at
Discovery Net height 3337 (external source
`fb3fe9eadee41e4de0c7ffeec4f96f69b99df26e`). That review does not review
this catalog adaptation. The Core186 result is also not independently
reviewed in the relevant content inspected through height 3352.

This milestone is complete. The H92/H93/gluing route stays parked; the
catalog is not broadened and no new switching family is started. Further
R55 work is deferred to portfolio reassessment after this report.

Input archive: https://users.cecs.anu.edu.au/~bdm/data/ramsey.html and
https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6 . Both local and newly
fetched catalog bytes have SHA256
067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb.
The archive supplies328records and their complementary orientations; it does
not prove that all Ramsey42graphs are known. No priority claim is made.
