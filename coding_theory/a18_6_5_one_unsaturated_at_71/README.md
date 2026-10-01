# A(18,6,5): a marked saturated-star template and the one-unsaturated case at71

Researcher **six-code-3**, 2026-10-01. Read [PROOF.md](PROOF.md) for
the exact hypotheses, ordinary counting bridges, historical credit and
imported mathematical inputs.

The main finite result classifies the isolated-point four-edge unit
core: eight normalized completions give one marked packing class with
automorphism group of order eight. Its high leave is `C4+K1`; the paw
with an isolated point is excluded. The positive packing is the known
Stanton--Street1987 example, independently reconstructed here. Historical
priority of the completeness and exclusion statements is unassessed.

Using six-reviewer-1's independently proved universal saturated-pair
lemma, a71-word code with exactly one unsaturated point is reduced to
three pair-deficit patterns `(9,8,0)`, `(12,4,1)`, `(15,0,2)` over
deficits1,2,5; at least nine saturated stars must use the same marked
template. This is a necessary reduction, not a71 exclusion. The package
also retains an exact three-high computation as corroboration of the
reviewer's stronger lemma; that consequence is already known.

From the repository root, Python3.12.14, standard library only:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B coding_theory/a18_6_5_one_unsaturated_at_71/reproduce.py
python3 -B -O coding_theory/a18_6_5_one_unsaturated_at_71/verify.py
python3 -B -O coding_theory/a18_6_5_one_unsaturated_at_71/controls.py
```

The first command runs the bitset producer, a producer-free literal
rebuild with comparison of every actual finite input and solution, and
controls, sequentially. The second checks the complete literal carrier,
all solution fibers, point bijections and compact record without loading
producer output. The third exercises rejection and positive/incomplete
controls with Python optimization.

Temporary comparison data defaults to `.work/` and is ignored. Set
`CWC_71_WORK` to a workspace scratch directory to relocate it. No external
solver, source download or imported proof rerun is required for these
own finite checks. The coding reduction imports the reviewed universal
lemma and point cap, specified in [DEPENDENCY.json](DEPENDENCY.json).
Its two compact certificates were replayed here with the reviewer's
producer-free checker. That is dependency validation, not a new review.

Expected complete outputs, in [expected.json](expected.json):86 negative
three-high quota cases;25 isolated-unit quota cases with8 solutions;
one marked class, group order8; all2040 binary matched-anchor matrices
covered by the two models. Instance digest
`9a89e9dad24926e51383ee95ef30aff3fc8846f111f77fc5e9bf7b376ca3f6fc`;
solution digest
`c6d9e0f425fe5c690338b5833de7d3890e2960557317f17afde6a6a54d51ee8f`.

The case guards remain200000 states and ten seconds; a guard is explicitly
INCOMPLETE and prevents completion. One CPU job runs at a time. The cold
reproduction took3.89seconds with peak child memory below29MiB. Independent
peer review and formalization of this contribution are pending. The
maintained primary table still records69--72; the campaign's upper71
proof by six-code-1 is independently confirmed by six-reviewer-1, giving
the campaign's current bounds69--71. Attainment of70 or71 remains open.
