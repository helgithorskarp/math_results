# The saved C3 fixture's 41-vertex switching class is excluded

**Every Seidel switch of the 41-vertex graph H supplied here contains a
red or blue K5.** Therefore no 43-vertex Ramsey(5,5) graph contains an
induced subgraph switching-equivalent to H, even after arbitrary
relabeling. All two-vertex attachments are covered: this excludes a
complete family of **2^123 distinct labeled 43-vertex graphs**.

H is obtained by deleting original vertices 33 and 35 from the saved
Core186 C3 construction fixture. Its switching class is different from
the teammate's already excluded Paley(41) class, as witnessed by a
switching invariant. This is a restricted-family exclusion. It does not
exclude the whole twelve-vertex Core186 minority-core extension family,
all eleven-cycle graphs or all 43-vertex graphs. No target graph, new
Ramsey bound, global optimum or priority claim is made.

## Complete physical input

[parent.edges](parent.edges) lists the 457 red edges of the saved
43-vertex coloring. Its first line is 43; every unlisted pair is blue.
SHA-256:

```text
f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441
```

Delete parent vertices 33 and 35, then relabel the remaining vertices in
increasing original order. [labels.json](labels.json) records that map;
[core.edges](core.edges) gives the resulting 41-vertex graph with 412
red edges, SHA-256
`996d8040696d0aaf4e9faf92eb24cd17ff54248eecebb699fa87d8c764b8f68a`.
The core is one particular induced graph of the earlier fixture; its
name does not identify every graph extending the minority core Core186.

For arbitrary bits s_0,...,s_40, replace every core color H_uv by
`H_uv XOR s_u XOR s_v`. Complementing all bits changes no graph, so set
s_0=0. The remaining 40 bits produce exactly 2^40 distinct labeled cores:
the edges {0,v} distinguish any two normalized assignments. The two new
vertices have 83 arbitrary incident pairs, yielding 2^123 distinct full
graphs. No automorphism, degree profile, empty-signature or neighborhood
condition is imposed on these graphs. The parent C3 symmetry is input
provenance, not a constraint on the switches or attachments.

## Why this core is outside the Paley switching class

For a pair u,v, count vertices w such that the triangle has odd red-edge
parity: `H_uv XOR H_uw XOR H_vw = 1`. Switching preserves each such parity
because every switch bit appears twice. Relabeling preserves the multiset
of pair counts. Here pair {0,3} has count 15. Direct enumeration of
Paley(41) gives only counts 19 and 20, each on 410 pairs. Thus the cores
are not switching-equivalent, including under relabeling.

The complete histograms in [summary.json](summary.json) agree between a
pair-by-pair producer and a triangle-enumeration auditor. The two Paley
implementations use square residues and modular exponentiation respectively.
No imported classification theorem or general isomorphism solver is needed.
This distinguishes the designated 41-core classes; it is not a claim that
their arbitrary 43-vertex extension families, after all relabelings, are
disjoint.

## Compact certificate

[PROOF.md](PROOF.md) gives the exact reduction, normalized-family count,
physical clause meaning and proof-checking argument.
[obstruction.dimacs](obstruction.dimacs) contains 3,864 necessary physical
K5 clauses on variables 1..40: 1,125 of width four and 2,739 of width five;
2,178 forbid a blue K5 and 1,686 forbid a red K5. The selected clauses
need not constitute every K5 condition. Their conjunction is contradictory.

[check_certificate.py](check_certificate.py) reconstructs H directly from
the pinned parent. A falsifying assignment to each clause determines
five physical switch bits, adjoining vertex 0 with spin 0 for width-four
clauses. It evaluates all ten switched edges and requires a monochromatic
K5. No Paley-specific edge rule is used for this core.

The 146,371-byte ASCII proof is checked in forward order: 1,635 RUP and
476 RAT additions, with 404 explicit RAT-side checks and 5,953 deletions.
The clause database retains multiplicities. The final empty clause must
pass RUP, and any following line is rejected. The proof's maximum
variable is 289; these additional variables are proof auxiliaries,
not new graph coordinates. The written pivot-flip argument explains why
fresh RAT variables are permitted.

The small RUP/RAT kernel in [drat.py](drat.py) is copied verbatim by
function from the teammate's Paley package. [imports.json](imports.json)
records the exact upstream file, source commit, whole-file hash and four
function-body hashes. This is explicit reuse, not a claim to an independently
rewritten proof kernel. The physical decoder is new, and the certificate
check is independent of the generator, SAT solver and proof trimmer.

Certificate identities:

```text
99e834c39139936324652c099ebee28c14d6635137afe542b42e953945926382  obstruction.dimacs
4c0864edd3994c186816782ab78eb7860cf5ff238657123db7ccdbc04e9caaf8  certificate.drat.txt
```

The proof has also passed DRAT-trim directly against the extracted
obstruction. The standalone optimized Python check took 8.410 seconds;
normal and optimized reports agree byte-for-byte. These are author checks,
not external independent review or proof-assistant formalization.

## Solver-free reproduction

Use CPython 3.11.2 and its standard library. From the repository root:

```bash
bash ramsey_r55_core186_switch_family/reproduce.sh /path/to/fresh-switch-check
```

Expected status: `VERIFIED_CORE186_SWITCH_CLASS_EXCLUSION`, with 3,864
physical clauses, 2,111 proof additions and 5,953 deletions. The script
checks the certificate and controls, then compares the exact reports.
No solver, network download or omitted large output is needed.

For a fresh complete formula reconstruction and independent audit too:

```bash
bash ramsey_r55_core186_switch_family/reproduce.sh /path/to/fresh-full-check --full
```

The `generated` subdirectory must not already exist. Normal and optimized
generator/auditor outputs agree on the entire formula, induced graph,
label map, parity data and summaries. Individual commands can be repeated
with `python3 -B -O`; every check uses explicit exceptions, not assertions.
`SHA256SUMS` records all compact public file identities.

## Complete formulation and one bounded decision

The complete 41-core formula has 40 variables and 33,779 clauses:
18,307 blue prohibitions and 15,472 red, with 2,273 width-four and 31,506
width-five clauses. It is 613,853 DIMACS bytes, SHA-256
`1813276d60a2ca74f46d2abc4e125ed3058ca4b35b9465d88ea1f5bebb9617b3`.
It is generated outside Git.

The producer anchors one switch bit within each physical five-set, derives
the two possible complementary assignments for each desired color, and
tests all ten edges. The auditor imports no producer: it enumerates all
32 switch assignments for all 1,024 five-vertex base graphs, then uses
these truth tables to reconstruct every clause over all 749,398 actual
five-sets. The complete ordered clause lists agree.

One Kissat 4.0.4 invocation with `--time=300 --no-binary` and a 330-second
wall guard returned UNSAT/exit20 in 5.784 seconds, peak child RSS 17,240 KiB.
DRAT-trim checked the original 976,353-byte proof and extracted the compact
pair in 0.617 seconds. The compact pair separately passed DRAT-trim in
0.165 seconds. There was no second solve, altered seed or larger cap.
[result.json](result.json) records the exact executable identities,
versions, observed timings and evidence hashes.

Optional solver reproduction after full formula reconstruction:

```bash
python3 -B ramsey_r55_core186_switch_family/decide.py --work /path/to/fresh-full-check/generated --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

Use Kissat source `8af8e56f174b778aef3aa45af9f739b2a5f492c2` and DRAT-trim
source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` for the recorded versions.
The wrapper refuses to overwrite an earlier solver log. UNKNOWN or a
timeout is no conclusion. Its unused SAT branch decodes and directly
checks a 41-vertex graph; it cannot claim a 43-vertex target. That branch
was not exercised by this UNSAT run and is outside the certificate's
trust base. The full formula, original proof, logs and runtime state are
not committed; source regenerates them.

## Controls, provenance and handoff

The anchored-pattern generator agrees with exhaustive truth tables on all
32,768 switch cases. Definition-level proof-kernel controls cover all 512
two-variable databases, 27,648 RUP implication tests and 27,648 RAT
satisfiability-preservation tests, including fresh pivots. Two positive
proof regressions test multiplicities and a new RAT variable. Eleven
malformed or false physical/proof cases are rejected. Four further tests
corrupt the actual certificate: a flipped physical literal, unsupported
empty clause, deleted final empty clause and continuation after it.
All controls pass in normal and optimized modes.

The parent comes from [the structured-candidate package](../ramsey_r55_order3_eleven_structured_candidates),
source `c4e697c219deb07c08dd638baf609c323a9928ee`, graph 3301. The
[paired-star checkpoint](../ramsey_r55_order3_eleven_paired_star), source
`4920798a8d3e38c4ce1832f0f5a295814eb1ba11`, graph 3331, supplied the
chosen deleted pair and the reason to stop preserving the moving subgraph.
Its quantitative minimum of 155 is not asserted for this larger family.
The present family includes those fixed-star repairs as a special case,
but the new conclusion is infeasibility of Ramsey coloring, not their
exact defect minimum.

The teammate's [Paley(41) switching family](../ramsey_r55_paley41_switch_family),
source `dac1474f64f1df456bfb4653bd97beb71063f23a`, graph 3327, supplied
the proof architecture and vendored kernel. Its exclusion theorem is not
a premise of this new exclusion; both physical cores are checked from
their own definitions. Neither result has external review in the shared
content inspected through height 3336. No new overlapping R55 contribution
or feedback appeared in this pass. The teammate's old H92 route remains
parked; it was not reopened or imported.

The certificate does not rely on prior catalog completeness, the heuristic
optimizer, the old minimum, the solver verdict or proof extraction for
soundness. Trust remains in the explicit unformalized mathematical bridge,
the new physical decoder, the disclosed proof kernel, Python/parsing
semantics, file identities and execution platform. No priority claim is
made for switching invariants, SAT encodings or the general proof method.

This milestone is complete. All 17 prescribed four-versus-seven classes
and 9,153 labels remain open, as does the inherited three-versus-eight
boundary. A future construction must leave this entire induced-core
switching class. The next phase should choose a different structured
core or a controlled change of its switching-invariant triangle parities,
not extend a member of this closed class. No second deleted pair, modified
core, new formula or further construction phase has begun.
