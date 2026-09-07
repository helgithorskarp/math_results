# Review of the full-support rank-four physical completion exclusion

## Verdict

**Accepted with high confidence at the stated structured-family scope.** I
found no error in the orbit coverage, physical SAT reduction, regenerated
formula identities, or 1,348 independently checked UNSAT proofs of h3791
(`bafkreiclmkonai5ugjizxvswct3adsype7gnlsncoy3sri232rjke2dgsy`). The
reviewed source is commit `f3ca3be5e96bde79f807192d985b0c63c38d3506`.

The new computation proves the non-affine portion. The statement that the
*entire* full-support profile is closed also imports the affine-column
exclusion h3757 and its independent acceptance h3761; I did not reopen that
already reviewed dependency in this milestone.

## Family and orbit coverage

For a fixed labeled 20+23 cut, write its red cross matrix as `M=UV^T` over
`F_2`, with rank four. In the reviewed profile each factor list contains all
15 nonzero vectors, while five distinct row labels and eight distinct column
labels occur a second time. Permuting physical vertices inside either side
removes the ordering of those repeated labels. A factor-basis change acts on
the row and column sets by `L` and `L^{-T}`, preserving every dot product and
hence physical completion.

There are `binom(15,5)=3003` row sets and `binom(15,8)=6435` column sets. The
15 affine hyperplanes are the imported family, leaving 6,420 non-affine
column sets and

```text
3003 * 6420 = 19,279,260
```

new doubled-set pairs.

The reviewer checker uses neither the target's generator BFS nor its
ordered-basis/stabilizer audit. It enumerates all `2^16` binary 4-by-4
matrices, retains the 20,160 invertible ones, constructs the dual action, and
uses Burnside's lemma. This independently gives four row-set orbits and 1,348
pair orbits. Their row-orbit sizes are `168,315,840,1680`.

As a separate completeness check, every manifest pair is lexicographically
canonicalized under all maps taking its row set to the canonical row. The
1,348 canonical pairs are distinct, split `201,661,394,92` among the four row
types. Since Burnside gives exactly 1,348 orbits, these representatives cover
the entire non-affine family without omission or duplication.

## Physical formula equivalence

The 460 cross edges are fixed dot products. The other
`binom(20,2)+binom(23,2)=443` physical edges are Boolean variables, with true
meaning red. For each physical five-set whose fixed cross edges permit an
all-red `K_5`, the CNF includes the negative clause requiring an internal blue
edge; analogously, a positive clause rules out an all-blue `K_5`. A satisfying
assignment is therefore exactly a completion with no monochromatic five-set.

I checked the target's four split cases (`1+4`, `2+3`, `3+2`, `4+1`) against
this definition. The independent checker reconstructs all 962,598 physical
five-sets and separately reconstructs the same clauses through the cut
decomposition. It compares clause **multisets**, because different physical
five-sets can reduce to duplicate internal clause lines after fixed cross
edges disappear. The target correctly retains that multiplicity.

Six complete formulas were audited at definition level: one from every row
orbit, both row-block boundaries, and the global minimum and maximum clause
cases. Their indices are `0,201,862,1255,1256,1275`, with 139,963 to 143,680
clauses. In every case the two clause multisets agree and their total equals
the committed manifest entry. Source inspection confirms the same split
construction is applied uniformly to all representatives.

## Full independent certificate replay

I rebuilt the claimed toolchain exactly:

- CaDiCaL 3.0.1, commit `c60730422e758ef1cebe7aeddf2dda31c996bf04`;
- `drat-trim`, commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA-256
  `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

A single-process replay regenerated every one of the 1,348 CNFs, required its
hash to match the exploration record, obtained a fresh UNSAT proof, and passed
that proof to `drat-trim`. CNFs and proofs were deleted after each check; the
manifest was fsynced after each case. The run completed in 1,907.629 seconds.

```text
verified cases       1,348
clauses              190,848,992
streamed CNF bytes   7,481,258,038
streamed proof bytes 1,124,629,092
solver seconds       444.421272119
checker seconds      608.764170140
maximum solve/check  1.147696 / 1.297959 seconds
```

Every regenerated stable per-case field matches the four public manifests:
orbit index, repeated-label sets, variable and clause counts, CNF size/hash,
proof size/hash, and verified status. Their canonical stable-record digest is
`744c2ced26ee6794f7a81d65f1f5250842c0230b40e96ce4dd89438ac658020a`.
Only timing fields were excluded from entrywise equality. The fresh raw
manifest SHA-256 is
`1cbfada67af75801e280d6f257170843e361ea5e52cac78902407db68221544b`.

## Scope and trust boundaries

The result excludes the fixed-partition rank-four profile in which every
nonzero label occurs and precisely five row labels and eight column labels are
doubled. The new 1,348-case computation covers non-affine column doubled sets;
the 15 affine choices are supplied by h3757/h3761. All 443 internal edges are
quantified, so the conclusion is a physical completion exclusion rather than
a cross-matrix filter.

This does not exclude rank-four profiles with missing or zero labels or other
multiplicity patterns. It does not prove a rank-four normal form for good43,
decide unrestricted good43 existence, construct a Ramsey graph, or improve
`R(5,5) >= 43` to the campaign target `R(5,5) >= 44`.

Remaining computational trust includes CPython and exact file semantics,
SHA-256 collision resistance, CaDiCaL as proof producer, the C implementation
and standard soundness of `drat-trim`, and ordinary hardware. Since every
solver conclusion was certificate-checked, CaDiCaL's search correctness is
not independently trusted. The orbit and reduction arguments are not
proof-assistant formalized. The six definition-level formula comparisons do
not enumerate every clause independently for all 1,348 cases; uniform source
inspection, exact hashes, the all-case count audit, and the full proof replay
cover the remaining interface.
