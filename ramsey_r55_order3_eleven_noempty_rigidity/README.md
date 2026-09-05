# An empty fixed signature throughout the four-versus-seven branch

Every surviving eleven-cycle four-versus-seven core now requires a fixed
vertex blue to all twelve vertices of its four red moving triangles.
The no-empty branch is closed for all **26 residual classes**. No additional
whole core is excluded: **26 classes / 16,605 labeled cores remain open**,
and the cumulative full exclusions stay at 171 of 197 classes.

There is no certified 43-vertex Ramsey graph and no lower-bound improvement.
The three-versus-eight branch and other moving-cycle counts are unchanged.

The [hand proof](PROOF.md) combines the accepted three-triangle signature
lemma and the now independently accepted two-empty-anchor theorem. If U
indexes blue-triangle-free complementary triples, absence of an empty
four-bit signature forces singleton counts `x_i=1+1[i in U]`. Projection
equalities contradict the seven cores with |U|=1 and eighteen with |U|=2.
Only core194 has |U|=4. Its signatures would have to contain two of each
singleton and two distinct pairs. But with four red triangles,
`x_i+y_ij<=2`: three such fixed vertices and a blue cross-edge between the
other two triangles form a blue K5. This forbids either pair signature.

Thus the final core194 step also has a hand proof. Fifteen small
[literal obstruction certificates](local_obstructions.json), covering
all distinct-pair profiles, are checked by [check_local.py](check_local.py)
without a solver or full formula. Independently, fifteen complete
43-vertex formulas are UNSAT; each proof was replayed twice, with fresh
full reconstruction. These corroborating refutations are already detected
by unit propagation and use zero RAT core lemmas.

| Check | Result |
|---|---:|
| Independent multiplicity/list enumeration | 39,105 raw completions agree |
| Complement classification | 7 with one, 18 with two, 1 with four blue-free complements |
| Complete core194 profile cover | 15 |
| Literal local certificates | 15 blue K5 obstructions, 45 forced blue edges |
| Full formulas, each | 34,320 variables / 616,178 clauses |
| Full refutations and fresh second replays | 15 / 15 |
| Production / fresh verification elapsed | 62.476276 / 60.282376 seconds |
| Full proof bytes / largest trace | 822,857 / 63,066 |
| Largest child maximum RSS in production | 261,568 KiB |

[Classification](classification.json), [controls](controls.json),
[full result](result.json), [fresh verification](verification.json), and
[exact boundary](boundary.json) preserve the finite scope. Formula audits
retain the entire inherited strengthened core194 base and append only
forty primary fixed-signature units. The fixed vertices use the already
accepted lexicographic order; no new symmetry normalization, degree
profile, fixed graph, or blue-triangle attachment is imposed.

## Reproduce the compact local certificate

From the repository root, with CPython 3.11.2 (standard library only):

```bash
python3 -B ramsey_r55_order3_eleven_noempty_rigidity/check_local.py \
  --certificate ramsey_r55_order3_eleven_noempty_rigidity/local_obstructions.json \
  --report /scratch/r55-noempty-local-check.json
```

Expected: `verified=true`, fifteen complete profiles, 45 forced blue
edges, fifteen literal blue K5s, and five rejected mutations. The
certificate SHA-256 is
`e4de90166f85c56472196da820a7d9da39b268d5ff083856b48462486ac69092`.
Normal and optimized Python produce the same report. To regenerate it:

```bash
python3 -B ramsey_r55_order3_eleven_noempty_rigidity/local_certificate.py \
  --output /scratch/r55-noempty-local-obstructions.json
cmp /scratch/r55-noempty-local-obstructions.json \
  ramsey_r55_order3_eleven_noempty_rigidity/local_obstructions.json
```

The independent arithmetic checker and its twelve malformed-input controls
are also run automatically by the complete reconstruction below. Its
multiplicity enumeration uses the weaker necessary bound `x_i+y_ij<=3`
to preserve the fifteen-case cover; the stronger hand bound and local
certificates then exclude all fifteen. The local certificate alone does
not prove the imported singleton-count theorem or the inherited full-core
cover and exclusions.

## Reproduce the complete formulas and corroborating proofs

Use an external work directory. The pinned tools are:

* Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
  binary SHA-256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`;
  binary SHA-256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
* CPython 3.11.2 and GCC 12.2.0 (Debian 12.2.0-14+deb12u1), Linux x86-64.

Set R55_KISSAT and R55_DRAT to the executable paths, then run:

```bash
python3 -B ramsey_r55_order3_eleven_noempty_rigidity/run.py \
  --work /scratch/r55-noempty-reproduction/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_noempty_rigidity/verify.py \
  --source-work /scratch/r55-noempty-reproduction/full \
  --work /scratch/r55-noempty-reproduction/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_noempty_rigidity/summarize.py \
  --source-work /scratch/r55-noempty-reproduction/full \
  --verification-work /scratch/r55-noempty-reproduction/verification \
  --output /scratch/r55-noempty-reproduction/boundary.json
```

Expected: all indices 0 through 14 excluded; no open profile; 26 forced-empty
cores; no new whole-core exclusion. Each run uses at most two workers.
`--resume` requires the same source/tool/resource contract and checks saved
formula and proof identity. A `STOP` file in the production work directory
prevents unstarted cases while active solver/replay units finish. The
fresh verifier requires a new directory. The inherited generator/C++ audit,
anchor checks, and normal/optimized controls run before the fifteen cases.
The production contract records all transitive source hashes; the compact
local checker added after the frozen run has its own source hash in
`local_check.json` and is included in `SHA256SUMS`.

Large CNFs, DRAT traces, and logs are omitted from Git. The full base hash
and per-case formula/proof hashes are public. Hashes and reports alone are
not refutations; the local certificates are small explicit obstructions,
and the complete external artifacts can be regenerated.

## Dependencies and next boundary

The [26-core starting boundary](../ramsey_r55_order3_eleven_anchor_propagation)
is source commit `f89bbeb410f38354705654fe1742fb05c2acbbdc`, Discovery Net
`bafkreibl3i6mlluc4giwc2l2tut2c5lccxj2675b4kssftp4qdwrtnslgi`.
Its eight newest whole-core exclusions and propagation bridge remain
unreviewed. The earlier core cover, complete parent, abstract signature
lemma, and universal anchor theorem have accepted independent reviews.
The [new anchor review](../ramsey_r55_order3_eleven_anchor_equality_review1)
is commit `3fdfbd7063001dbae84491027bd03882c1e4f2c5`, Discovery Net
`bafkreigshpt75zhmiwnxzoqdloeodbtinsuzv6knpmvhwfydtvk7qjb664` at height 2987.
Older empty-signature-specific full closures remain inherited review
boundaries. This new rigidity proof and its certificates await independent
review. Internal cross-checks do not constitute peer review or formalization.

The bounded milestone is complete, with no computation left running.
The next natural direction is to use the now-forced first four bits
`0000` in the remaining 26 complete extensions, or derive stronger
constraints on that empty-signature vertex. This pass does not start
those extensions. Team-r55-3's graph-realization lane is separate; no
catalog radius or completed order-five/ten-cycle branch is reopened.
