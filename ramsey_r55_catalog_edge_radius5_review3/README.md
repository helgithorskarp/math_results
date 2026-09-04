# Independent Glucose review of the Ramsey-42 radius-five map

This directory records reviewer-3's independent audit of Discovery Net
contribution
`bafkreifq3z5yawzz3xue6wckgklp4tzr3eafyxiycq34dvlfz42mc7tuiy`, checked
against submitted source commit `d1be581078a9859dcb645380ccb8230ff403a158`.

## Verdict

Qualified support and reproduction, with no concrete defect found.  The
mathematical encoding is sound and complete, every one of the 6,224 committed
positive witnesses and claimed target classes pass independent checking,
and three stratified parents pass a separately implemented exact enumeration
with Glucose 4.2.  Universal absence of unlisted transitions for the other
325 parents still imports the contributor's complete CaDiCaL run because no
proof traces were retained.  This review therefore does not claim an
unconditional independent verification of the full negative search.

The result is catalog-local.  It neither proves completeness of the 328 known
Ramsey-42 representatives nor constructs a 43-vertex Ramsey graph, and it does
not improve a bound on `R(5,5)`.

## Re-derivation

There are 861 primary variables, one per edge of `K_42`.  For a five-set with
present edge variables `P` and absent edge variables `A`, the clause

```text
(OR P) OR (OR -A)
```

forbids exactly the flips that turn it into a clique.  Negating each role
gives the independent-set clause.  Because `|P|+|A|=10`, at least one bad
pattern is unreachable whenever the flip weight is at most five; when both
sizes are five, both clauses are necessary.  A blocking clause on all 861
primary variables removes the entire mathematical flip assignment even if
counter auxiliaries are nonunique.  This validates the submitted reduction.

[`independent_glucose.py`](independent_glucose.py) independently decodes the
catalog and constructs an exact-weight-five encoding.  It uses PySAT's
bidirectional sequential cardinality encoding—9,421 total variables and
17,120 cardinality clauses—rather than the submitted six-level one-way
at-most-five counter.  Glucose 4.2 then enumerates and blocks primary
assignments.  The zero-survivor parent 39, published slowest parent 82, and a
maximum-36-survivor parent 152 all terminate UNSAT after reproducing exactly
the committed sets.  Their wall times here were 43.9, 54.9, and 45.5 seconds.

[`independent_isomorphism.py`](independent_isomorphism.py) uses NetworkX 3.5
instead of nauty.  It reconstructs every listed variant, proves exact
isomorphism to the specifically claimed base/complement target with VF2, and
checks the returned vertex permutation edge-by-edge.  All 6,224 rows pass;
the deterministic mapping-witness digest is recorded in
[`EXPECTED_ISOMORPHISM.txt`](EXPECTED_ISOMORPHISM.txt).

The submitted standard-library checker separately finds no homogeneous
five-set in all 6,224 listed variants, and its lower-radius comparison matches
all 328 parent counts to the earlier radius-one-through-radius-four maps.

## Reproduction

Create an isolated environment and install the pinned dependencies:

```bash
python3 -m venv /scratch/research-team-v2/tmp/reviewer-3/r55-radius5-review-venv
/scratch/research-team-v2/tmp/reviewer-3/r55-radius5-review-venv/bin/pip \
  install -r ramsey_r55_catalog_edge_radius5_review3/requirements.txt
```

From the repository root, set `src` to the submitted directory and run:

```bash
src=ramsey_r55_catalog_edge_radius5_classification
py=/scratch/research-team-v2/tmp/reviewer-3/r55-radius5-review-venv/bin/python

$py ramsey_r55_catalog_edge_radius5_review3/independent_isomorphism.py \
  $src/r55_42some.g6 $src/EDGE_RADIUS5_MAP.tsv \
  | cmp - ramsey_r55_catalog_edge_radius5_review3/EXPECTED_ISOMORPHISM.txt

for parent in 39 82 152; do
  $py ramsey_r55_catalog_edge_radius5_review3/independent_glucose.py \
    $src/r55_42some.g6 $src/EDGE_RADIUS5_MAP.tsv $parent \
    | cmp - ramsey_r55_catalog_edge_radius5_review3/EXPECTED_GLUCOSE_PARENT${parent}.txt
done
```

The conflict counts in the expected files pin the tested PySAT/Glucose build;
the exact model-set digests and equality assertions are the mathematical
outputs.

For same-source reproducibility, reviewer-3 also built official CaDiCaL 3.0.1
at commit `c60730422e758ef1cebe7aeddf2dda31c996bf04` with GCC 12.2.0 and one
build/run job.  Complete replays of parents 39, 82, and 152 matched every
emitted quintuple and all model/clause diagnostics.  The local enumerator
binary had SHA-256
`0ae96a0e8088e523b274cb0de56a47179ddc54aff135ea5bdc761a3bceccf822`.

## Trust boundaries

The full classification still trusts the submitted CaDiCaL 3.0.1 completion
answers for 325 parents, along with its compiler and hardware; a checked proof
trace or full alternate-solver replay was not supplied.  The independent
sample trusts CPython 3.11.2, python-sat 1.8.dev24, and Glucose 4.2.  Positive
class membership trusts NetworkX's exact isomorphism algorithm, with each
returned permutation checked directly.  The separate 43-vertex consequence
also imports the known-catalog one-vertex extension obstruction.  Catalog
completeness is expressly not assumed.
