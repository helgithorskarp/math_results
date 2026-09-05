# The first empty fixed vertex: complete four-blue-triangle branch

**The first normalized empty-signature fixed vertex has at most three blue
moving-triangle neighbors in 19 of the 25 remaining core classes.** The
complete maximal-branch test refutes those 19 cases, with every full proof
replayed twice after fresh reconstruction. Six cases remain explicitly
UNKNOWN: **124,155,159,168,180,194**.

This excludes attachment branches, not whole cores. **All 25 full classes /
15,957 labeled cores remain open**; cumulative whole-core exclusions stay
at 172 of 197 classes / 99,586 of 115,543 labels. No target graph or Ramsey
lower-bound improvement is claimed. The three-versus-eight branch and other
moving-cycle counts are unchanged.

Vertex e=33 is blue to all twelve red-core vertices. If it is also blue to
four of the seven blue moving triangles, it already has 24 blue neighbors;
the degree bound forces it red to all nine other fixed vertices, with
degrees (18,24). All 35 labeled four-triangle choices are represented
without changing the existing order. The refuted branches are

```text
92,97,109,114,118,119,122,154,164,167,177,182,185,186,188,190,191,192,193.
```

These 19 core classes represent 13,608 labeled cores; the six unresolved
branches represent 2,349. All six remaining one-anchor cores
114,122,154,164,177,188 are among the refuted cases. “One anchor” means that
exactly one complementary three-red-triangle core has no blue triangle.
Thirteen of the eighteen two-anchor cases are refuted; the four-anchor
case194 remains UNKNOWN.

| Evidence | Result |
|---|---:|
| Complete bases and branch formulas rebuilt twice | 25 / 25 |
| Exact blue-four choices per formula | 35 |
| Moving cardinality / full incidence assignments checked | 128 / 65,536 |
| Malformed cases / formulas rejected | 3 / 9, normal and optimized Python agree |
| Complete branch proofs replayed twice | 19 |
| Full proof bytes / largest proof | 346,224,849 / 22,354,970 |
| RAT core lemmas, summed over first replays | 10,915 |
| Production / fresh verification elapsed | 487.322866 / 231.693321 seconds |
| Largest child maximum RSS in production | 261,572 KiB |

The [case list](cases.json), [controls](controls.json), [result](result.json),
[fresh verification](verification.json), and [exact boundary](boundary.json)
record case identity, complete formula hashes, proof hashes, replay results,
and the unresolved scope. The large proofs are regenerated outside Git.

The [proof and encoding](PROOF.md) retain the complete 43-vertex formula
for every core. Each adds only 56 clauses specifying exactly three red
links among variables 215,...,221, and nine positive fixed-edge units
166,...,174. There are no new auxiliary variables or normalization rules.
The final dimensions are 34,290 / 617,497 for six one-anchor cases;
34,300 / 617,547 for eighteen two-anchor cases; and 34,320 / 617,647 for
core194. An excluded branch does not exclude the whole core.

The blue neighborhood in this branch has 24 moving vertices on eight
3-cycles, with four internally red and four internally blue triangles.
It has neither a red K5 nor a blue K4. This saturated neighborhood motivates
the test, but no local relaxation replaces the full 43-vertex problem.
The conclusion concerns e=33 in the existing normalized representation.
It does not assert a bound for every empty-signature fixed vertex.

## Reproduction

From the repository root, use CPython 3.11.2, GCC 12.2.0 (Debian
12.2.0-14+deb12u1), and these pinned tools on Linux x86-64:

* Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
  binary SHA-256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`;
  binary SHA-256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to their executable paths, and keep generated
formulas, proofs, and logs outside the repository:

```bash
python3 -B ramsey_r55_order3_eleven_empty_blue4/run.py \
  --work /scratch/r55-empty-blue4/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_empty_blue4/verify.py \
  --source-work /scratch/r55-empty-blue4/full \
  --work /scratch/r55-empty-blue4/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_empty_blue4/summarize.py \
  --source-work /scratch/r55-empty-blue4/full \
  --verification-work /scratch/r55-empty-blue4/verification \
  --output /scratch/r55-empty-blue4/boundary.json
```

The reference experiment uses at most two workers, 20-second solver caps,
and 300-second full proof replay caps. Caps describe a bounded experiment,
not a hardware-independent performance guarantee. `--resume` requires the
same source/tool/resource contract and checks saved case, formula, and
proof identities. A `STOP` file prevents unstarted cases while current
solve/replay units finish safely. Fresh verification requires a new work
directory. UNKNOWN traces are neither proofs nor saved solver states.

Preparation reconstructs the entire inherited chain, including the parent
C++ clause audit and previous normalization, anchor, no-empty and pair-cut
checks. The complete preceding preparation must match its public record
entry by entry. All 25 base hashes are matched. The new independent auditor
recovers primary meanings from literal edge orbits on 43 vertices, compares
every complete base and its exact 65-clause tail, checks all 128 moving
assignments and all 65,536 moving/fixed degree assignments, and matches
all 35 four-blue choices. Three malformed case records and nine malformed
formulas must be rejected. Normal and optimized-Python reports agree.

Each UNSAT proof passes full DRAT replay against its exact formula. Fresh
verification reconstructs all 25 bases and children again and replays each
completed refutation a second time, including any RAT steps. A target SAT
claim would instead require a decoded compact 43-vertex edge list and an
independent check of every five-set. No solver status alone establishes
a mathematical verdict.

## Dependencies and trust

The complete bases and 25-core starting boundary come from
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation),
source `f7f8339fcf0e7c0b48cd18df1c5f84975eef1d6e`, Discovery Net
`bafkreicxnbie6cijmgq6b3dh3heom7utz7ghbea632xbynavk4wzauclpa`.
Its newest core123 exclusion remains an inherited review boundary.
The forced-empty theorem now has an
[accepted independent review](../ramsey_r55_order3_eleven_noempty_rigidity_review1),
source `56055e5554a4201446d635eaa445b3fe7577e5b3`, Discovery Net
`bafkreig73ghneseo3xkqyxbyr2247rbi5qbvrxcn5rgxkfhg6pkio5pv2e` at height 3011.
That review accepts the theorem for all 26 then-listed cores, including
the present 25. Its combination with the older complete exclusion chain
retains the older empty-signature-specific review boundaries.

The complete parent, 197-core cover, abstract signature lemma, universal
anchor theorem and eight-core intrinsic propagation also have accepted
independent reviews. The parent's external R(4,5)=25 degree theorem is
not recomputed here. The new maximal-branch encoding and refutations await
independent review. The teammate's joint H20/outside search remains a
separate non-symmetric lane; its timeout supplies no premise here.

Only source and compact case/control/hash/result reports are public.
Large CNFs, proofs, logs, and binaries remain external and are regenerated
by the commands above. Hashes and compact reports alone are not refutations.
Trust remains in ordinary unformalized reductions, exact source and
runtime/compiler/hardware, SHA-256 identity, and the full DRAT checker.
Internal independent reconstruction and second replay are not independent
peer review or proof-assistant formalization. No target graph or Ramsey
lower-bound improvement is claimed by closing an attachment branch.


All computations are complete, with no job left running. The next concrete
step is to propagate the new necessary bound into the 19 unrestricted full
extensions: at least four of the seven links 215,...,221 are red, encoded
by the 35 positive four-subset clauses. This leaves the nine fixed edges
and the exact moving-attachment count free. The six unresolved maximal
branches receive no new bound. This pass does not run that new phase or
open the complementary b<=3 split. The result applies to the first fixed
vertex in the existing canonical representation, not every empty vertex.
