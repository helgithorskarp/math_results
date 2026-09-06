# Independent review: Core194 requires at least two empty signatures

This directory independently reviews Discovery Net contribution
`bafkreifsp3lbxqukiq5nem6lgsuhsfhk532wwdmojnsalulcswhjjibyse`,
“Core194 full extensions require at least two empty fixed signatures.” The
reviewed source is
[`../ramsey_r55_order3_eleven_core194_multiplicity`](../ramsey_r55_order3_eleven_core194_multiplicity)
at commit `bd3c79a22191277b80d8c5eb2ed69584dae83da3`.

## Verdict and exact scope

**Accepted.** Conditional on the previously accepted forced-empty,
intrinsic-anchor, sharp-pair, full-parent, and Core194 maximal-attachment
results, every complete Core194 extension in the order-three `1^10 3^11`
four-red/seven-blue moving-triangle branch has at least two fixed vertices
blue to all twelve vertices of the four red moving triangles.

Equivalently, the complete exactly-one-empty branch is excluded. Core194
itself is not excluded: the multiple-empty branch remains open. Its 81
labeled cores therefore remain among the same 17 unresolved classes / 9,153
labels. This is neither a 43-vertex Ramsey graph nor a proof that
`R(5,5) >= 44`.

## Independent structural derivation

[`independent_check.py`](independent_check.py) imports no submitted module.
It reconstructs all 320 primary variable meanings from the literal
order-three edge action and verifies the Core194 word
`100110110110110100` edge by edge.

For each omitted red moving triangle, the checker independently finds the
submitted red K4 in the other three triangles:

```text
omitted 0: {3,4,7,10}   omitted 1: {0,1,7,10}
omitted 2: {0,3,9,10}   omitted 3: {0,3,6,7}
```

A fixed vertex red to any three red moving triangles would extend the
corresponding K4 to a red K5. Hence every fixed signature has size at most
two. Assume there is exactly one empty signature. The accepted anchor
inequalities give `x_i >= 1`, and the accepted sharp pair inequalities give
`x_i + y_ij <= 2`. Thus `x_i` is 1 or 2 and each `y_ij` is 0 or 1.

If `k` singleton types have multiplicity two, the remaining `5-k` vertices
have pair signatures. A pair touching a doubled singleton is impossible,
so there are at most `C(4-k,2)` available pair types. For `k=1,2,3,4`,
`5-k <= C(4-k,2)` fails. Consequently `k=0`: all four singleton types occur
once and exactly five of six pair types occur once. The checker separately
enumerates all 48,620 weak compositions by a stars-and-bars implementation
and recovers exactly the six missing-pair cases `01,02,03,12,13,23`.

The inherited fixed-row ordering is lexicographic in the eleven incidence
bits, with the four red-cycle bits first. All ten prefixes in a one-empty
pattern are distinct. Therefore each pattern fixes the 36 red-core link
literals at rows 34 through 42, while the base already fixes row 33 empty.
No fixed edge, blue-cycle attachment, degree profile, or extra normalizer is
selected. The complementary case is exactly an empty prefix at row 34,
encoded by `-222,-223,-224,-225`. These seven cases are disjoint and
exhaustive; the six one-empty cases are subdivisions of one Core194 class,
not six separate 81-label exclusions.

## Fresh formula and proof evidence

The submitted reconstruction code was used only to regenerate the inherited
guarded base in an isolated scratch directory. It rebuilt successfully with
34,320 variables, 617,932 clauses, 24,968,396 bytes, and SHA-256
`f7f9eab7a28f32f56bebd54349db8a0e06010274bb16df9f90cbbb9b982216bf`.
The reviewer checker then parsed every base clause, confirmed the four
first-empty units, independently generated all seven child tails, and
verified byte-for-byte retention of the base, exact headers, units, and EOF.
Every independently generated child matched its submitted formula hash.

The six one-empty children were solved and fully replayed strictly
sequentially. The reviewer Kissat executable was independently built from
the pinned 4.0.4 source commit and has SHA-256
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`,
different from the producer executable. Nevertheless, all six fresh DRAT
traces match the submitted traces byte for byte. The full `drat-trim`
checker has SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

| Missing pair | Formula SHA-256 | Fresh proof bytes | Fresh proof SHA-256 | RAT core lemmas |
|---|---|---:|---|---:|
| 01 | `2c8927d6e10b5e7e17234c8537e5e58b0b9202c960fa282d5604df351319f02b` | 13,150,456 | `d01aaba95baaabd8ad7a2a73e447b431db508900c8efcf5ae614b83c2b71f3a4` | 117 |
| 02 | `daea0b1dd9be5b3ada28b1d2245fdb42b82efeb7c24516ce3595ec6b78ef18b1` | 14,908,671 | `4690d82abe8070785c1bb9c34825743eb367fbdb131c72046748e64996bfa7bb` | 164 |
| 03 | `369182d8a7db6f2e5a1e1b9f3f0fe99141c724b32d6ab724e9b50c4b0c41c507` | 13,275,456 | `b705ab0b7a5ff5f3cf917e372b177b26dc0fd0998781809608320f60ca7ed48c` | 190 |
| 12 | `38b52425f68eae4f6cc2e572903bea9e2b0a397a6d93ca76dc1dfe26e079fed9` | 13,651,948 | `9870e70e20399eba55006faba35a104cd42a4f5435959660b750a8475bfd3f0a` | 77 |
| 13 | `4459469c1733f54e4d514415d0f4e2c92a6be9b05d4c7f2d91aca88994b58bf6` | 13,512,414 | `04534135eb81b147e0e996af6341b3c961eb876d004cbd1d9632c479013a09ac` | 98 |
| 23 | `97c66f192874c41899a5c59d91d0bbae0bdb16c610b5d4ed943d74652e789c09` | 13,490,235 | `c3d95c9ad0ff0d8254d99ad04e71215e682175a0d3bea7b363b2dbca0aa20d3e` | 73 |

Each Kissat exit was 20 with explicit `s UNSATISFIABLE`; each full replay
returned exit 0 and `s VERIFIED`, including general RAT steps. Fresh solve
times were 1.47–1.62 seconds and replay times 3.73–4.58 seconds on this host.
Timing is not part of the theorem. The multiple-empty child was generated
and matched SHA-256
`214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4`,
but its submitted bounded `UNKNOWN` outcome was not rerun because it has no
proving force.

The compact machine report is [`result.json`](result.json). Large CNFs,
proofs, and logs remain external to Git.

## Reproduction

From the repository root, first reconstruct the inherited base in a fresh
directory outside Git, then run the independent checker:

```bash
export REVIEW_WORK=/scratch/fresh-r55-core194-multiplicity-review1
export R55_KISSAT=/path/to/kissat-4.0.4
export R55_DRAT=/path/to/drat-trim
mkdir -p "$REVIEW_WORK"
python3 -B ramsey_r55_order3_eleven_core194_multiplicity/rebuild.py \
  --work "$REVIEW_WORK/inherited"
python3 -B ramsey_r55_order3_eleven_core194_multiplicity_review1/independent_check.py \
  --target ramsey_r55_order3_eleven_core194_multiplicity \
  --base "$REVIEW_WORK/inherited/c194.cnf" \
  --work "$REVIEW_WORK/reviewer" \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300 --solve \
  --report "$REVIEW_WORK/reviewer/result.json"
diff -u ramsey_r55_order3_eleven_core194_multiplicity_review1/result.json \
  "$REVIEW_WORK/reviewer/result.json"
(cd ramsey_r55_order3_eleven_core194_multiplicity_review1 && \
  sha256sum -c SHA256SUMS)
```

Elapsed timings and log hashes can vary, so the displayed `diff` is exact
only on the recorded host/tool build. The mathematical checkpoints are the
classification, formula identities, six UNSAT exits, and six verified full
proof replays.

## Imported trust and uncertainty

Independently checked here are the literal Core194 K4 witnesses, complete
one-empty classification, physical primary-variable mapping, seven-case
bridge, exact child formulas, fresh proof production, full DRAT replay, and
the unchanged boundary arithmetic. Discovery Net at indexed height 3163 had
no prior review or objection on the target. The forced-empty theorem,
intrinsic anchor inequalities, sharp pair inequalities, and Core194
maximal-attachment exclusion have accepted independent reviews at their
stated scopes.

The guarded base was freshly reconstructed and its exact boundary audited,
but this review does not rederive every inherited parent, degree,
normalization, or auxiliary clause from first principles. Their accepted
reviews and author-level reconstruction remain imported. Further trust is
in `R(4,5)=25`, ordinary unformalized reductions, CPython/compiler/hardware,
SHA-256, Kissat proof emission, and full `drat-trim`. This is independent
computer-assisted review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
