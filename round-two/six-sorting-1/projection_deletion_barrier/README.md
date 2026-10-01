# Deletion barrier for projected thirteen-input construction seeds

Author and executing agent: **six-sorting-1, researcher**, 2026-10-01.

None of the **868 distinct 46-comparator seeds** defined below remains a sorter
when one or two of its comparators are deleted. A compact **487-input Boolean
certificate** excludes all **39,928 size-45** and **898,380 size-44** labelled
deletion choices. We also reproduce the already-known 45 single deletions of
the 45-comparator incumbent, giving **898,425** checked size-44 choices in total.
A separate recursive circuit evaluator checks the certificate and independently
replays every candidate on all **8,192 Boolean inputs**. The fewest failures
among the size-44 candidates is **11**.

This is a barrier for one concrete construction family. The thirteen-input
minimum-size interval remains **44..45**; arbitrary 44-comparator networks,
rewiring, comparator insertion, and deletion from longer projections are not
excluded. The experiment says that these shortest projected seeds need a
substantive modification to reach the target. No priority claim is made for
extreme deletion, comparator normalization, or the general method.

## The exact seed family

`parents.json` pins the flat comparator lists for the eight 13..16-input
networks currently listed in
[Dobbelaere's maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
fetched 2026-10-01. For each parent on n inputs, choose n-13 distinct original
input positions and independently fix each to a minimum or maximum. Delete
comparators touching a fixed value, bypass its other input along that value's
route, and then normalize the surviving oriented comparator word to standard
comparators by the explicit wire-frame rule in [PROOF.md](PROOF.md). Keep only
words of length at most 46 and deduplicate their **complete ordered comparator
lists**, with no isomorphism reduction. No additional redundant gates are removed.

| Parent | Size45 projections | Size46 | Size47 | Size48 | Size49 |
| --- | ---: | ---: | ---: | ---: | ---: |
| N13L45D10 | 1 | 0 | 0 | 0 | 0 |
| N13L46D9 | 0 | 1 | 0 | 0 | 0 |
| N14L51D10 | 0 | 0 | 24 | 4 | 0 |
| N14L52D9 | 0 | 0 | 0 | 28 | 0 |
| N15L56D10 | 0 | 105 | 270 | 45 | 0 |
| N15L57D9 | 0 | 0 | 105 | 270 | 45 |
| N16L60D10 | 0 | 1120 | 2880 | 480 | 0 |
| N16L61D9 | 0 | 0 | 1120 | 2880 | 480 |

There are 9,858 marked assignments, including the two thirteen-input controls.
The 1,227 qualifying assignments yield one size-45 word and 868 distinct
size-46 words. The latter consist of the size-46 thirteen-input table network,
91 new words first encountered from N15L56D10, and 776 first encountered from
N16L60D10. These are literal-word counts, not counts of inequivalent networks.

**Operation order matters:** normalize the complete projected word first,
then delete the selected comparators. Deleting before normalization is a
different family and is not covered. Retained gates keep their per-wire order;
any topological schedule with that order has the same outputs, so a depth
limit is unnecessary for this particular family.

The incumbent single-deletion part is a control and reproduction of a subset
of the [published local barriers](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_local_barriers),
graph `bafkreiek6vqrtic367qt5zaefknx7sk6k7ui5ltfl576y54c366l5qhpcm`.
The projected-seed deletion family is different from those incumbent repairs.
The present proof does not import their exclusion certificate.

## Reproduce

Run from the repository root with Python **3.11+**, GCC **12.2.0**, C++20,
one process doing CPU-intensive work, and one thread:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 round-two/six-sorting-1/projection_deletion_barrier/generate.py
python3 round-two/six-sorting-1/projection_deletion_barrier/verify.py --full
python3 round-two/six-sorting-1/projection_deletion_barrier/verify.py --sanitize
```

Generated seed lists, binaries and outputs go under
`scratch/projection-deletion-barrier`, or a supplied `--work-dir PATH`.
No downloads, solver, third-party package, private input, cutoff or large proof
corpus are needed. The first command regenerates the certificate byte for byte.
The independent checker checks the eight parents by scalar compare-exchange on
245,760 original Boolean inputs and regenerates the normalized seed set using
a different enumeration and normalization implementation.

Expected principal output:

```text
COMPLETE seeds=869 candidates44=898425 sorters44=0 sorters45=0 minimum_failed_inputs=11 witnesses=487
ALL_DELETIONS_EXCLUDED seeds=869 size44=898425 size45=39928 witnesses=487 minimum44_failures=1 positive_control=PASS
ALL_DELETIONS_EXCLUDED seeds=869 size44=898425 size45=39928 witnesses=8192 minimum44_failures=11 positive_control=PASS
PARENTS_SCALAR_CHECKED 245760 PROJECTED_SEEDS_ENTRY_MATCH 869
```

The certificate subset guarantees at least one failure for each candidate;
the minimum of eleven uses the optional complete Boolean replay. The native
full-input generation took about 2.7 seconds; both independent circuit checks
together took about 10.7 seconds. Measurements vary by host. Ordinary
reproduction, including compilation, stayed below 160 MiB peak child RSS;
the sanitizer run stayed below 200 MiB.

Certificate SHA256:

```text
1071ff1667264044d10a9db347b1b09e904fdaa4ca834fc3842779562793b8f7
```

Canonical projected-seed text SHA256:

```text
8eaf44524362295a699d0a9aacb13368f0ec9d5a8c7ce4d14bbecf2ad6bf4cd9
```

Both algorithms were written and executed by this researcher. Their different
representations and evaluation paths supply an algorithmic independent check;
this is not an external reviewer verdict or a proof-assistant formalization.
The trust boundary is the pinned parent data, the finite-family definition,
the code and ordinary Python/C++ execution. All arithmetic is exact. Full
sorting-network size lower bounds are not premises of the deletion exclusion.

Construction searches with multiple rewires remain heuristic and are separate
from this certificate. A useful next construction step is to change the
comparator structure, or use independently justified prefix filters before
trying expensive completions. An unsuccessful stochastic run does not prove
that an untested construction family is empty.

## Construction handoff examples

`construction-examples.json` additionally records two invalid 44-comparator
words from whole-sequence stochastic search. They are outside the deletion
certificate and are not sorting witnesses. Scalar replay gives ten and thirty
Boolean failures. Applying six-sorting-2's published
[redundancy-aware prefix filter](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-sorting-2/semantic-pruning),
source `97bd126fa1aa3756008e6dc7c1e04a4f9542bffe`, graph
`bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4`,
gives these concrete rejections at budget44:

| Candidate | First rejected prefix length | Family | Semantic mass | Necessary total size |
| --- | ---: | --- | ---: | ---: |
| Unweighted fitness | 26 | Two minima | 576 | 45 |
| Extrema-weighted fitness | 34 | Two maxima | 640 | 45 |

These are applications of the teammate's lemma. They identify impossible
construction prefixes earlier than terminal sorting verification. Replay the
exact fixtures and filter interface with:

```sh
python3 round-two/six-sorting-1/projection_deletion_barrier/check_examples.py
```

That optional command requires the published teammate source at its ordinary
repository path (or `--profile PATH`) and checks its pinned file SHA256 before
execution. The deletion barrier's reproduction needs no teammate code.
The candidate failures and the filter rejections are kept separate; passing a
prefix bound would still give no construction certificate.
