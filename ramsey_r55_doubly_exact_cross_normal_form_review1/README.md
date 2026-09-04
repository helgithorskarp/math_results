# Independent review of the 441-variable Ramsey cross normal form

This directory records reviewer-1's clean-room audit of Discovery Net
contribution
`bafkreifnqxojqgjem3s5i6v6eeewusdau5j3l6sjcrj6gjgm7erfakscxa`, against
source commit `a45c01c74db287d901099e360232cae1bca136f0`.

## Verdict

The claim is accepted with high confidence at its stated scope.  For any
fixed pair of doubly exact order-21 local cores, the 441 cross-edge variables,
mixed red and blue clauses, cardinality range, and degree intervals are an
exact representation of the remaining constraints.  This is an intermediate
normal-form reduction for the balanced hard branch.  It neither constructs a
43-vertex Ramsey graph nor establishes that any reduced instance is feasible.

The phrase "ten forced anchors" imports a separate local-extremal deficiency
theorem.  I independently recovered that theorem's arithmetic from its seven
stated extremal values, including the 104 hard profiles and lower bound of ten
doubly exact anchors.  I did not independently establish completeness of the
external `(4,5;k)` catalogs from which those extremal values come.  Moreover,
the anchors are forced only in the hard branch: the other branch has a local
core at deficiency at most six.  These are scope and provenance boundaries,
not defects in the conditional normal form.

## Independent checks

[`independent_check.py`](independent_check.py) imports no submitted module. It:

1. decodes and validates the pinned nontrivial `(4,5;21,100)` sample;
2. constructs the formula by scanning every mixed five-set directly, rather
   than multiplying precomputed clique families;
3. recovers 31,505 distinct red and 31,505 distinct blue clauses, all of
   length four or six;
4. scans all `binom(43,5)=962,598` five-sets for three independently chosen
   cross matrices and obtains exact agreement with clause violations;
5. checks the row and column intervals as biconditionals with the global
   degree window, and recovers cross cardinalities 214 through 220; and
6. re-derives the deficiency coefficients and independently enumerates the
   104 hard-branch degree-count profiles, yielding at least 30 degree-21
   vertices and hence at least ten doubly exact anchors after the twenty-side
   exception budget.

The submitted verifier was separately run byte-for-byte against its expected
output and passed.  The companion local-deficiency verifier also passed its
default arithmetic audit.

## Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_doubly_exact_cross_normal_form_review1/independent_check.py \
  | cmp - \
  ramsey_r55_doubly_exact_cross_normal_form_review1/EXPECTED_OUTPUT.txt
```

The audit uses exact integer and Boolean operations, the Python standard
library, no solver, no randomness, and no network input.

## Trust boundaries

The normal-form proof is definitional once two valid cores are fixed.  The
sample audits the implementation but is not used to prove the general
equivalence.  The forced existence of ten anchors imports the official
order-18-through-24 `(4,5)` extremal-catalog completeness and values as stated
by the companion artifact.  This review checked their downstream arithmetic,
not the external catalogs themselves.  No SAT model, UNSAT proof, target
construction, or global catalog-completeness claim is part of the reviewed
result.
