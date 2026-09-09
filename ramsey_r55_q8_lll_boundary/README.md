# q8 constructive local-lemma certificate: failed gate

The proposed asymmetric Lovasz local lemma certificate is impossible for
every q8 task under the declared independent uniform K4-pair distribution
and variable-overlap dependency graph. A clique of 1,248 physical bad-five
events violates a necessary inequality for every possible choice of weights.

**No physical task is excluded, and no good43 is constructed.** No resampling
or target solver was run. The candidate implication, probability space and
complete obstruction proof are in [PROOF.md](PROOF.md).

The first declared test, a probability sum greater than one, was inconclusive:
the exact sum is 53270258394624/54108801960767, about 0.9845. Verification
of the actual asymmetric weight inequalities on the unchanged event set
then gave the contradiction 2m*min(p)=82652066724864/54108801960767 > 1.
This added algebraic test was not predeclared. Both the original declaration
and the verification addendum are preserved explicitly.

## Reproduce

Python 3.10 or later, standard library only. From the repository root, use
a fresh output directory outside the checkout:

```sh
python3 -B ramsey_r55_q8_lll_boundary/produce.py /tmp/q8-lll-check
python3 -B ramsey_r55_q8_lll_boundary/verify.py /tmp/q8-lll-check \
  --expected ramsey_r55_q8_lll_boundary/EXPECTED.json
```

Expected final status: `VERIFIED_LLL_CERTIFICATE_FAILURE`.

The producer enumerates all 65,536 binary four-by-four matrices using row
intersections. The checker independently reconstructs the domain from 56
physical five-set patterns, checks all 132 relevant labeled rectangle
marginals and compares every one of the 1,248 physical events and its exact
probability. The accepted domain has 37,823 matrices. No external catalog,
solver, prior graph, incomplete trace or target-search output is required.

The generated matrix domain and event stream stay outside Git. Both are
compared entry by entry. The event stream's expected SHA-256 is
`c82d15647b54bb6a782fa33565de2edd976ad1c21909cfd3e910b96b8413e2bb`.
The checker is independently derived author code, not an independent review.
The mathematical argument remains unformalized; the candidate implication
imports the theorem cited in [SOURCES.json](SOURCES.json).

## Campaign boundary

All 2,185,424 original q8 tasks remain undecided. The global original registry
remains 518 excluded and 2,188,660 undecided. The active dispatch is unchanged,
and team-r55-1's 161 oriented q10 children were not accessed.

This is a failed certification mechanism, not a failed resampling experiment
or a statement that all local lemma approaches are impossible. The mechanism
is parked. No altered distribution, event grouping, dependency graph,
stronger criterion or neighboring construction is started in this pass.
No Discovery Net mathematical contribution is forced for this failed
task/candidate leverage gate; source and compact evidence are retained here.
