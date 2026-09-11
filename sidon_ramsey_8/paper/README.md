# A complete proof package for 81 ≤ SR(8) ≤ 83

The [manuscript](manuscript.tex) consolidates the complete P83 profile reduction
and final exclusion into a proof covering **every partition of `[83]` into eight
Sidon classes**. The Sidon convention includes repeated summands. The lower bound
uses the partition of `[80]` from Xiu, Fan and Liang, *On Disjoint Golomb Rulers*,
[Table I, case I=8](https://arxiv.org/abs/1405.4535).

This is a draft for human mathematical review and authorship assignment.
It packages the existing numerical result; it does not improve the bound further
or decide P81 or P82. The P84 theorem and the quantified P82 residual remain in
their original directories.

## Complete reproduction

On Linux, from the repository root, with Python 3.11+ and GNU g++ supporting C++20 and
`__uint128_t`:

```sh
python3 sidon_ramsey_8/paper/verify.py --work /tmp/sr8-full-proof
```

Use a **new directory outside the repository**. The default starts both stages
concurrently, with four profile workers and six completion workers. It includes
AddressSanitizer and UndefinedBehaviorSanitizer on the controls. Allow about
25 GB of free disk space. Timings and compiler versions for the current full
replay are recorded in [validation.json](validation.json), with full compact
stage records in [profile_replay.json](profile_replay.json) and
[completion_replay.json](completion_replay.json). Counts are exact;
elapsed times depend on hardware and concurrent load.

The entry point:

1. Checks the [source and input manifest](source_manifest.json), the explicit
   weights, and the lower-bound partition directly by unordered sums. It also
   checks the manuscript's printed weights, witness, and case-ledger digests.
2. Runs the [full profile driver](../p83_profiles/reproduce.py), regenerating
   catalogs, excluding all six nonbalanced profiles, and recording the complete
   cover for `11^3 10^5`.
3. Runs the [full balanced completion driver](../p83_exclusion/reproduce.py),
   regenerating its own catalogs and completing both full traversals.
4. Compares the two stages' eleven catalogs and full and heavy ten catalogs byte
   for byte. It compares all 5,364 anchor rows and all 65,073,232 triple counts,
   then checks the compact ledgers and terminal artifact identities.

Success writes `paper_verification.json` containing `verified: true`,
`numerical_conclusion: "81 <= SR(8) <= 83"`, and
`mode: "fresh_full_replay"`. Python `-O`/`PYTHONOPTIMIZE` is rejected because the
stage drivers use assertions as proof checks. Any mismatch aborts the run. Progress is written to `profiles.log` and
`exclusion.log` under the work directory.

Two narrower modes are explicit:

```sh
python3 sidon_ramsey_8/paper/verify.py --check-inputs
python3 sidon_ramsey_8/paper/verify.py --check-existing --work /tmp/sr8-full-proof
```

The first verifies only the source manifest, weight data and known partition.
The second aggregates completed runs in `profiles/` and `exclusion/`; it does
not rerun the exhaustive searches or turn untrusted output files into a proof.
Its report says `aggregate_existing_completed_runs`. In the accompanying fresh
replay, the two complete stage drivers were launched directly; the wrapper was
then run in this aggregation mode. No execution of
the wrapper's fresh-launch mode is claimed for that record.

## Proof map

| Claim | Exhaustive scope | Source |
|---|---|---|
| Every Sidon class has at most 11 points and weight at most 4,000,000 | All size-10, size-11, size-12 sets; direct bound for smaller sets | [Profile stage](../p83_profiles/) |
| Five or more elevens are impossible | 2,142 weighted five-tuples and all five residual size profiles | [Profile stage](../p83_profiles/) |
| Four elevens are impossible | 2,701 anchors, 7,805,097 quadruples, all mixed completions | [Profile stage](../p83_profiles/) |
| Three elevens are impossible | 5,364 anchors, 65,073,232 triples, every five-ten completion | [Completion stage](../p83_exclusion/) |
| The proof stages cover the same cases | Byte comparisons and all 5,364 case records | [Aggregation entry point](verify.py) |
| `[80]` has eight Sidon classes | Explicit previously published witness | [Witness](../p80_extension_barrier/partition80.txt) |

The seven profiles arise by distributing the deficit `8*11 - 83 = 5`; balance
is a proved consequence of the first stage, not an assumption. Reflection gives
a proved complete anchor cover, possibly with multiplicities. Integer weights
justify every catalog cutoff and every heaviest-class recursion. The final
nine-class in the mixed profile is bounded separately from the ordered tens.

No earlier P84 or P85 exclusion is a mathematical premise. The manifest includes
an earlier weight vector for a checked provenance identity and a general catalog
generator stored under a historical P84 directory. Both stages independently
regenerate their P83 catalogs and validate the explicit P83 inequalities.

## Review and trust boundary

The [separate P83 computational review](https://github.com/njallskarp/math_source_code_open/tree/main/sidon_ramsey_8_p83_independent_review)
accepted both stages with stated limitations. Its evidence commit is
`e9c0d9f9ddf88ab2c74277153635003d19815438`; reviewed source is
`d198c6081c400f4096b53bb7737ca014442fd160`. It replayed both stages and added an
unordered-sum checker for the small residual domains. It did not implement a
third global search. This is a separate automated research review, not journal
peer review or a proof-assistant formalization.

The coverage arguments, integer programs, compiler, runtime and hardware remain
trusted. The two global implementations originated in the same campaign. Their
complete recorded **nonempty** query streams agree; empty queries appear in the
state counts but are not individually recorded. The sanitizer runs cover controls,
not the full production search. Hashes identify artifacts; they do not establish
mathematical completeness.

The compact validation records and source are committed. Full catalogs, binary
query traces, executables, typesetting dependencies and compiled PDFs remain
outside the repository and can be regenerated.

## Typesetting

Build from this directory using a standard LaTeX/BibTeX toolchain, or from the
repository root with Tectonic:

```sh
tectonic --outdir /tmp/sr8-paper sidon_ramsey_8/paper/manuscript.tex
```

Create the output directory first. The local validation used Tectonic 0.15.0.
The [bibliography](references.bib) distinguishes the primary literature, source,
and separate computational review. The published comparison bound of 86 is
Theorem 4.1 of [Espinosa-García and Pellicer's open preprint](https://arxiv.org/abs/2309.08553);
the journal publication is *Discrete Applied Mathematics* 378 (2026), 120–124,
[doi:10.1016/j.dam.2025.07.002](https://doi.org/10.1016/j.dam.2025.07.002).
