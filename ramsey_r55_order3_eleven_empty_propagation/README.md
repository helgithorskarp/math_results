# Full four-versus-seven extensions with an empty fixed signature

**Core123 has no complete Ramsey(5,5;43) extension in the eleven-cycle
four-versus-seven branch.** Its full refutation passed DRAT replay twice,
after fresh complete reconstruction. This excludes 648 labeled cores and
leaves **25 classes / 15,957 labeled cores open**. The cumulative exclusions
are **172 of 197 classes / 99,586 of 115,543 labels**, importing the earlier
full-core exclusions. No target graph or Ramsey lower-bound improvement
is claimed.

The complete bounded test covered all 26 previously open cores after
propagating two proved consequences: the first fixed four-bit signature
is `0000`, and each singleton-or-pair signature class has size at most two.
The other 25 cases returned explicit UNKNOWN at their 20-second caps.
Every case retained the complete 43-vertex extension formula. The
three-versus-eight branch and other moving-cycle counts are unchanged.

| Evidence | Result |
|---|---|
| Newly excluded full core | 123, words 000,110,110,011,101,011 on 01,02,03,12,13,23 |
| Complete bases / final formulas rebuilt twice | 26 / 26 |
| Literal blue cross-edge applications | 312 |
| Cut truth assignments checked | 49,152 |
| Malformed cases / formulas rejected | 4 / 8, normal and optimized Python agree |
| Core123 formula | 34,290 variables / 617,432 clauses |
| Core123 solve / first replay | 19.640767 / 28.762592 seconds |
| Core123 proof | 19,801,958 bytes; 673 RAT core lemmas |
| Production / fresh verification elapsed | 381.525480 / 83.734201 seconds |
| Largest child maximum RSS in production | 261,568 KiB |

The complete [case list](cases.json), [controls](controls.json),
[result](result.json), [fresh verification](verification.json), and
[exact boundary](boundary.json) record the result entry by entry.
Core123's full formula SHA-256 is
`d103da79b90dbb5d3f8bb9822a90d3b387823eee866af0c3f991f2d7f3db25f1`;
its proof SHA-256 is
`e7f7293e5a6de165c219f34af9284051a626d6877d6b1a50aca417c44933a700`.
The full proof, rather than a solver status or a hash, establishes the
finite refutation; its large trace is regenerated outside Git.

The mathematical reduction is in [PROOF.md](PROOF.md). For distinct red
triangles i,j, three fixed vertices whose signatures are {i} or {i,j}
would form a blue triangle. A blue cross-edge between the other two red
triangles would complete a blue K5. Hence `x_i+y_ij<=2`. The previous
[no-empty rigidity theorem](../ramsey_r55_order3_eleven_noempty_rigidity)
forces the first fixed prefix `0000` under the existing lexicographic
ordering. Both are necessary conditions for the whole extension, with
no fixed graph, degree profile, blue attachment, or new normalization.

Each formula retains its entire inherited strengthened base and adds four
primary units and 1,440 nine-literal clauses, with no new auxiliary variable.
The seven one-anchor cases have 34,290 variables / 617,432 clauses; the
eighteen two-anchor cases have 34,300 / 617,482; core194 has 34,320 / 617,582.
An UNSAT outcome excludes the whole selected core conditional on these
proved consequences. UNKNOWN is inconclusive and never means feasibility.

## Reproduction

From the repository root, use CPython 3.11.2, GCC 12.2.0 (Debian
12.2.0-14+deb12u1), and these pinned tools on Linux x86-64:

* Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
  binary SHA-256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`;
  binary SHA-256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to their executable paths. Keep generated
formulas, proofs, and logs outside the repository:

```bash
python3 -B ramsey_r55_order3_eleven_empty_propagation/run.py \
  --work /scratch/r55-empty-propagation/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_empty_propagation/verify.py \
  --source-work /scratch/r55-empty-propagation/full \
  --work /scratch/r55-empty-propagation/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_empty_propagation/summarize.py \
  --source-work /scratch/r55-empty-propagation/full \
  --verification-work /scratch/r55-empty-propagation/verification \
  --output /scratch/r55-empty-propagation/boundary.json
```

Each run uses at most two workers. Solver caps are 20 seconds per case;
full proof replay caps are 300 seconds. Exact resource/source/tool contracts
are recorded in `result.json`. `--resume` requires the same contract and
checks saved formula/proof identities. A `STOP` file in the production
work directory prevents unstarted cases while active solve/replay units
finish. Fresh verification requires a new directory.

Preparation regenerates the complete parent and audits it with the separate
C++ clause checker, rebuilds and matches all 26 inherited strengthened bases,
and checks the preceding no-empty arithmetic and local certificates. The
new auditor recovers primary edge orbits independently, checks all 312
literal blue cross-edge witnesses, and examines all 49,152 ordered
three-signature truth assignments, including both values of each free
coordinate. It compares every line of each complete base and new tail.
Four malformed case records and eight malformed formulas are rejected;
normal and optimized-Python control reports agree. Production sources are
frozen before the complete solver run. An earlier preproduction mutation
accidentally preserved a zero bit; its control correctly failed, the
mutation was changed to an actual bit flip, and a fresh production directory
was used. No solver case ran before that correction.

The fresh verifier repeats complete reconstruction and all controls, then
replays each full refutation again against the rebuilt formula. Replays
permit general RAT steps; solver status alone is never accepted as a proof.
No old UNKNOWN trace is used as a refutation or resumable solver state.
A SAT candidate must be decoded as an explicit 43-vertex edge list and
checked over all five-sets before it is reported as a target graph.

## Dependencies and trust

The starting 26-core boundary and complete strengthened bases come from
[anchor propagation](../ramsey_r55_order3_eleven_anchor_propagation), source
`f89bbeb410f38354705654fe1742fb05c2acbbdc`, Discovery Net
`bafkreibl3i6mlluc4giwc2l2tut2c5lccxj2675b4kssftp4qdwrtnslgi`.
Its eight whole-core exclusions and complete clause bridge now have an
[accepted independent review](../ramsey_r55_order3_eleven_anchor_propagation_review1),
source `1e3a7785c7f54235d4725d6b8af6085df6722abd`, Discovery Net
`bafkreicpjjb27sgmgpec4bfsecmu4nxoahrnt6mqhknhh65lb3pkaepzei` at height 3005.
That review accepts the eight exclusions individually; the cumulative
171/26 starting count additionally imports older empty-signature-specific
closures that were not re-reviewed there.

The empty-prefix and sharp pair bound are proved in
[no-empty rigidity](../ramsey_r55_order3_eleven_noempty_rigidity), source
`9a03389107f03306cf491ea1684a016a2ca72801`, Discovery Net
`bafkreibfkg7phtivnfvv3iyinp4lzgr24ca7j4ybxjjhrrn24tm3icttoi`. That new
hand reduction and its use here await independent review. The accepted
full parent, 197-core cover, abstract signature lemma and universal
anchor theorem remain inherited dependencies. The parent's external
R(4,5)=25 degree theorem is not recomputed here.

Only source and compact case/hash/control/result manifests are public.
Large CNFs, traces, binaries, and logs remain external and are regenerated
by the commands above. Hashes and compact reports alone are not refutations.
Trust remains in the ordinary unformalized reductions, exact source and
runtime/compiler/hardware, SHA-256 identity, and the full DRAT checker.
Internal independent reconstruction and second replay are not independent
peer review or formalization. The teammate's marked-H20 footprint work is
a distinct non-symmetric frontier and supplies no premise to this test.


The bounded milestone is complete, and no job remains running. All 25
remaining cores retain the forced empty signature and sharp pair cuts.
A useful next direction is to derive stronger restrictions on the empty
vertex and its attachments to the seven blue moving triangles, then test
a complete, justified split. This pass does not open that phase or repeat
an unchanged timeout. The new full exclusion and its inherited no-empty
reduction await independent review.
