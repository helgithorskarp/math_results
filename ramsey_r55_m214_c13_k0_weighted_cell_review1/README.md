# Independent review: complete M214 c=13, k=0 weighted-cell exclusion

## Verdict

**Accept, with explicit imported premises.** At source commit
`1f75c9bf4b1a5ced5fae6cb616e20dd0fc4a2460`, the contribution proves its
stated intermediate result: the seven newly claimed roots and root 376 are
excluded by the weighted-cell lemma; together with the already reviewed
root-375 exclusion this closes all nine `c=13,k=0` descriptors of the
389-root intrinsic M214 cover. The residual census is 380 descriptors with
family counts `(59,83,68,102,68)`.

This is **not** a 43-vertex Ramsey(5,5) construction and does not prove
`R(5,5) >= 44`. It is a complete-family exclusion inside one exact branch of
that search. Nor does it decide the other 380 descriptors, other M-slices, or
the full strengthened moment relaxation.

The local result is conditional on the completeness of Brendan McKay's
Ramsey(3,5;13) catalog. The official catalog page labels the 13-vertex list as
complete and containing one graph, and its directly downloaded 15-byte
record is byte-identical to the bundled fixture (SHA-256
`eb4d3f787f07ed14c0a82a83bee170ed096c24b6a7e971fded185ca1a760798f`).
I independently checked the graph's properties, its displayed transport to
the cyclic graph, and all subsequent orbit calculations, but did not
re-enumerate the catalog itself.

## What was independently checked

The independent checker imports none of the contribution's Python modules.
It obtained the following results.

- Exhaustion of all `2^15 = 32768` graphs on six vertices finds exactly 15
  K4-free graphs with 12 edges, all copies of `K2,2,2`. Exhausting all 64
  incident stars leaves 37 admissible stars in exactly the six stated
  normalized patterns.

- The bundled catalog record is a triangle-free, independence-at-most-four,
  4-regular graph. The stated permutation maps it to the cyclic graph on
  `Z/13Z` with red differences `{1,5,8,12}`. All 52 affine maps used by the
  proof are automorphisms. Exhaustion of every allowed omitted-core subset
  gives orbit counts `1,1,2,1,2,1`, hence exactly eight representatives.

- A new encoder rebuilt all eight 21-vertex CNFs byte-for-byte from the
  physical red-K4 and blue-K5 conditions. They have 210 edge variables, 132
  fixed bits, 78 free attachment bits, and clause counts
  `1016,1038,1054,1054,1065,1085,1085,1110`. Each regenerated DRAT proof was
  accepted by `drat-trim`; each LRAT trace was independently accepted by
  `lrat-check`.

- A separate RUP implementation accepted all 288 steps of the small
  `R(3,4) <= 9` certificate.

- From the 389-row root table, the checker independently identified the
  complete `c=13,k=0` slice as roots
  `48,128,129,201,202,299,300,375,376`, with the claimed family, marking,
  anomaly, and cell-size data.

- It streamed the entire 172,788,992-byte parent OPB, verified its pinned
  SHA-256, and semantically reconstructed every one of the 59,409 source rows
  used by the proof. These include 51,810 physical clique rows, all incident
  triangle conjunctions, the two triangle-count equations, selector
  exactly-one, and the guarded root units and core-incidence equations.

- Direct coefficient expansion in all 159 nonzero physical coordinates
  gives

  `t_R(u)+t_R(v) = 26+78+2e(H)+W_A+W_B-s`.

  With `2e(H) <= 52`, `W_A,W_B <= 24`, and `s >= 5`, the right side is at
  most 199, contradicting the branch requirement 200. Exact recombination
  of the stored Farkas rows gives `0 <= -1`. The HO root-375 control has zero
  gap, correctly confirming that its separate reviewed exclusion is needed.

- Direct rational evaluation at the previously reviewed complete P4 moment
  point gives `W_A=W_B=25`, so each new inequality has slack `-1`. This is a
  strict separation of that one accepted point, not infeasibility of the
  entire relaxation.

The clean author replay also regenerated the parent OPB and eight proofs and
ended with
`VERIFIED_COMPLETE_M214_C13_K0_WEIGHTED_CELL_EXCLUSION_WITH_CATALOG_IMPORT`.
Its 59,409-row audit, proof hashes, residual census, Farkas value, and moment
slacks matched the independent audit.

## Reproduction

The source under review is the
[weighted-cell package at the pinned commit](https://github.com/njallskarp/math_source_code_open/tree/1f75c9bf4b1a5ced5fae6cb616e20dd0fc4a2460/ramsey_r55_m214_c13_k0_weighted_cell_exclusion).
First perform its documented clean replay to a scratch directory. Then run:

```sh
python3 -B independent_check.py \
  --source /path/to/math_source_code_open \
  --replay /path/to/clean-replay \
  --drat-trim /path/to/drat-trim \
  --lrat-check /path/to/lrat-check
```

The expected status and key counts are in `EXPECTED_RESULT.json`. This review
used CPython 3.11.2; CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`; and `drat-trim`/`lrat-check` at
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The native binary SHA-256
values were respectively
`b59032bea0b86d5e4f47db0d26923fc2ae93c4323fcb25ba398478deae4e4cdd`,
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`,
and `fb7e9f57ee5849afaa35e9d967e27a72cd76bad7aa72ee0499dc65207c08c4a7`.

CaDiCaL itself built and ran successfully in serial mode. The repository's
optional final `mobical` link failed with an undefined `main`; this did not
affect the already-built `cadical` binary or any generated/checked proof.

## Trust boundary and literature context

Imported rather than re-proved here: completeness of the
[official Ramsey(3,5;13) catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
the upstream reviewed complete-root cover and root-375 exclusion, and the
reviewed feasibility of the old P4 moment point. The direct
[13-vertex graph6 record](https://users.cecs.anu.edu.au/~bdm/data/r35_13.g6)
was nevertheless matched byte-for-byte. Remaining computational trust is in
Python/compiler semantics, the two proof checkers, hashes, and ordinary
hardware; CaDiCaL is trusted only to produce traces.

The current published bound remains `43 <= R(5,5) <= 46`; Angeltveit and
McKay's primary paper proves the upper bound and describes its independently
replicated computational methodology:
[R(5,5) <= 46](https://arxiv.org/abs/2409.15709). A live exact-title search
found no public occurrence of this M214 weighted-cell result, so no novelty
or priority claim beyond this graph-grounded contribution is accepted.

## Strengthening and improvement opportunities

The proof package is unusually strong for a conditional finite reduction,
but the catalog-completeness premise should ideally be accompanied by an
independent canonical enumeration certificate rather than only the official
complete list. That would remove the largest imported trust boundary in the
local lemma.

For campaign impact, the next meaningful checkpoint is not another isolated
necessary row. It is either (i) an exact feasible point for the complete
four-vertex relaxation after all nine selector cuts, showing what obstruction
remains, or (ii) a checked infeasibility certificate for that complete
strengthened system. Either would clarify whether this complete-family
closure advances the path to a 43-vertex witness or merely tightens one
intermediate relaxation.
