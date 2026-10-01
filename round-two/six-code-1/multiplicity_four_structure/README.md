# Multiplicity four: no low-low v leave and no saturated internal excess

Actual author: **six-code-1, researcher**, 2026-10-01.

For a71-word constant-weight `(18,6,5)` code with replication profile
`(16,19,20^16)`, let u,v be its replication16 and19 points. **If
`lambda_uv=4`, the nineteen-word v-link has no uncovered pair between
replication-five points, and every pair of the sixteen saturated points
has multiplicity four or five.**

The [proof](PROOF.md) excludes the complete low-low branch: every one
of388 replication-four marks in the46-representative imported census
is decoded, and32578 charge inventories reduce to three carriers.
Six exact [integer LP duals](INTEGER_DUALS.json) certify an upper strictly
below52 added words in every remaining carrier/exception case. A separate
ordinary argument handles all120 placements of the only possible internal
heavy edge, using the existing shared-hub lemmas and a direct row-sum
contradiction. [ERRATUM.md](ERRATUM.md) corrects the old remaining-placement
paragraph and removes the paired2111 dependency; the named independent
reviewer six-reviewer-5 identified and proved this repair in
[audit8989](../../six-reviewer-5/multiplicity-four-audit/REVIEW.md).

This is a conditional structural theorem. The subsequent
[multiplicity-four exclusion](../multiplicity_four_exclusion/PROOF.md)
uses it. Independent [audit8989](../../six-reviewer-5/multiplicity-four-audit/REVIEW.md)
confirms both conclusions with the repaired bridge and its explicit
reviewed classification premises. It gives no verdict on the older
zero-through-three chain or uniform tail theorem8947. The campaign interval
remains **69--71**, and the external table69--72. Ordinary bridges remain
unformalized. This erratum supplies no new numerical bound or census.

## Check the published certificates

From this directory, with Python3.11.2 standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B verify.py
python3 -B -O verify.py
```

The checker independently decodes the two anchor models by row/column
injections and literal mask ownership, compares every result with the
producer's subset decoder, and compares both complete62/40 cohort streams.
For each dual it independently generates all1219 compatible words using
literal intersections, reconstructs every signed constraint from its
mathematical descriptor, and checks every column and integer objective.
Twelve malformed certificate controls reject negative/noninteger weights,
uncovered columns, non-strict bounds, wrong cases/rows/domains and missing
cases. All checks remain active with `-O`.

[expected.json](expected.json) records exact replay data, including the
six bounds. Their worst upper is `5194350/100000 <52`. The certificate
does not require SciPy, HiGHS, a private corpus, or a numerical tolerance.
The checker does import the local producer's **non-solver** decoder for
the full comparison; certificate semantics and candidate generation are
separate implementations. Both are by the stated author.

## Optionally regenerate integer duals

Discovery used Python3.11.2, NumPy2.4.6, SciPy1.17.1 and HiGHS through
`scipy.optimize.linprog(method="highs-ds")`. Install these libraries into
a disposable local directory, then generate a certificate there:

```sh
python3 -m pip install --only-binary=:all: --target /tmp/m4-libs numpy==2.4.6 scipy==1.17.1
PYTHONPATH=/tmp/m4-libs python3 -B produce.py --out /tmp/m4-duals.json
python3 -B verify.py --certificate /tmp/m4-duals.json
```

The producer specifies one solver thread and a40-second time limit for
each of the six LPs. The calls run sequentially. It requires a successful
exploratory solve, rounds the duals to integer weights, repairs coverage
through the positive point rows and **checks the resulting exact inequalities**.
A failure or insufficient strict margin gives no certificate. Different
valid duals need not have identical bytes. Only the later exact check
establishes the bound; the exploratory floating optimum is not a theorem.

All generated libraries, matrices and logs stay in workspace scratch or
the specified temporary directory. [VALIDATION.json](VALIDATION.json)
records measured runs and [DEPENDENCIES.json](DEPENDENCIES.json) pins the
imported graph/source premises. The copied compact
[nineteen-star manifest](NINETEEN_STARS.json) is unchanged credited source
by six-code-3. The included [ACL69 fixture](acl69.txt) is classical and
directly checked for exact bytes,69 distinct weight-five words and all
pair distances; baseline reproduction is validation.

The original m4,mu0,X0 frontier has since been excluded in the linked
subsequent proof. Current uniform two-unsaturated research is in the
[tail-structure contribution](../two_unsaturated_tail_structure/PROOF.md);
its independent review and whole-family coverage remain separate.
[ERRATUM_VALIDATION.json](ERRATUM_VALIDATION.json) records the corrected
checker's fresh replay; original VALIDATION.json is historical evidence
at source4983b8eca2f526f445be39cce7de0a41ef66836e.
