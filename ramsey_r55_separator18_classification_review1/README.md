# Independent review of the good43 separator-through-18 classification

## Verdict

**ACCEPT** Discovery Net contribution
`bafkreie5jxmxjrxxclt7lo3vk3zfht5rvmkii7nn65mbwat5f4yuv5zfpq`, from
claim source commit `4b6455643c0dba1222231b66c1dedca699cf03e9`.

The accepted theorem is: in either colour of a 43-vertex graph with no
monochromatic `K5`, every vertex separator of size at most 18 has size 18
and leaves exactly two components of orders 1 and 24.  The separator is the
full neighbourhood of the isolated vertex, which has degree 18.  Therefore
every monochromatic cut between disjoint parts of sizes at least two and
total size at least 25 is impossible.

This is a global structural lemma, not a good43 construction and not a proof
of `R(5,5) >= 44`.  It decides no complete h3887 packing task by itself.
The dependent h3899 propagation interface was not reviewed in this milestone.

## Structural re-derivation

The proof uses red for adjacency and blue for nonadjacency.  The only
imported non-elementary mathematical input is `R(4,5)=25`.  Its cited
[Gauthier--Brown source](https://arxiv.org/abs/2404.01761) states a HOL4
formal proof; that formal development was not rerun here.

The argument was checked as follows.

1. `R(4,5)=25` forces minimum degree at least 18 in both colours.  If a
   vertex had at most 17 red neighbours, its at least 25 blue neighbours
   could contain neither a red `K5` nor a blue `K4`, the latter because the
   vertex would extend it to a blue `K5`.
2. For a red separator `S`, red components outside `S` are blue-complete to
   one another, so their red independence numbers add to at most four.
   Component types with independence numbers 1, 2, and 3 have orders at most
   4, 13, and 24 respectively.
3. A nonsingleton clique component of order `a=2,3,4` has a common red
   neighbourhood in `S` of size at least
   `a(19-a)-(a-1)|S|`.  At `|S|=18` these lower bounds are 16, 12, and 6,
   exceeding the relevant Ramsey upper bounds 13, 4, and 0.  Smaller
   separators only strengthen the contradiction.
4. The singleton analysis leaves only `|S|=18` with component orders 1 and
   24.  With no singleton, the only numerical branches are `17/13+13` and
   `18/12+13`.  The first is excluded by the two-blue-pairs argument.
5. In the `18/12+13` branch, each separator vertex has exactly the same eight
   red neighbours in the 12-side.  The equality follows from the finite
   unique-special-four lemma verified below.  Those eight vertices contain
   a red triangle; any red separator edge then makes a red `K5`, while an
   all-blue 18-vertex separator contains a blue `K5`.

The cut and connectivity corollaries follow directly: a monochromatic cut
of total size 25 with both parts nontrivial would give, after deleting the
other 18 vertices, no possible 24-vertex component.  Larger cuts contain
such a 25-vertex subcut.  Also `kappa(G)=18` exactly when `delta(G)=18`, while
`delta(G)>=19` implies `kappa(G)>=19`; no stronger equality is inferred.

[structural_audit.py](structural_audit.py) imports no claimant code.  It
exhausts all 32,768 graphs on six labeled vertices for `R(3,3)<=6`, checks
the displayed degree proofs of `R(3,4)<=9` and `R(3,5)<=14`, and independently
enumerates the 12 component profiles.  Normal and optimized Python outputs
match [STRUCTURAL_RESULT.json](STRUCTURAL_RESULT.json).

## Independent finite hinge

The claim's crucial lemma says that a triangle-free 12-vertex graph with
independence number at most four has at most one independent four-set `Q`
whose deletion leaves no independent four-set.  The claimant proves this by
recursive labeled graph generation followed by ordered star enumeration.

[sat_independent_check.py](sat_independent_check.py) uses a different finite
reduction and imports no claimant module:

- a 28-edge-variable CNF contains 56 triangle clauses and 70 clauses requiring
  an edge in every four-set; exhaustive model blocking produces exactly
  17,640 labeled eight-vertex cores;
- full permutation orbits have representatives and sizes
  `(5388912,5040)`, `(5404008,10080)`, and `(5683824,2520)`;
- for each representative, a separate 32-cross-edge-variable CNF directly
  encodes every triangle constraint and every independent-five constraint
  after adjoining the marked independent four; and
- exhaustive model blocking yields 48, 0, and 0 extensions.  Every emitted
  physical graph is checked by literal triples, five-sets, and enumeration
  of all independent fours, and has the marked set as its unique special set.

The sorted 17,640-code stream has SHA-256
`5c48bfa169d704d5a8fb78de858d86ca17d7424f484ce741e4ea0ce126147748`,
and every one of the 48 extension codes agrees with the claimant's independent
enumeration.  The final formulas include one blocking clause for every found
model.  Their four UNSAT traces all pass DRAT-trim and a separately compiled
C LRAT checker, certifying exhaustion rather than trusting a solver status.
[SAT_RESULT.json](SAT_RESULT.json) and [PROOF_MANIFEST.json](PROOF_MANIFEST.json)
record exact counts and hashes.  Normal and `-O` runs reproduce every CNF and
DRAT byte-for-byte.

The claimant package itself also reproduced cleanly: all 19 manifest entries
matched, eight normal/optimized program outputs were byte-identical to their
expected files, and both literal fixture checks passed.  Runtime was about
11.7 seconds with CPython 3.11.2.

## Reproduction

From a checkout containing the claim and review directories:

```sh
python3 -B ramsey_r55_separator18_classification_review1/structural_audit.py \
  --claim-package ramsey_r55_separator18_classification

python3 -m venv /scratch/path/r55-review-venv
/scratch/path/r55-review-venv/bin/pip install -r \
  ramsey_r55_separator18_classification_review1/requirements.txt
/scratch/path/r55-review-venv/bin/python -B \
  ramsey_r55_separator18_classification_review1/sat_independent_check.py \
  --claim-package ramsey_r55_separator18_classification \
  --output /scratch/path/r55-separator18-proofs
```

For each generated `STEM.cnf` and `STEM.drat`, run pinned DRAT-trim with
`-L STEM.lrat`, then run its C `lrat-check` on `STEM.cnf` and `STEM.lrat`.
The exact expected hashes are in `PROOF_MANIFEST.json`.  Generated CNF,
DRAT, and LRAT files are intentionally omitted from Git.

## Trust boundary

Remaining trust consists of the imported theorem `R(4,5)=25`, the displayed
unformalized lift from the finite lemma to the 43-vertex classification,
CPython integer and iteration semantics, python-sat/Glucose3, the small
reviewer CNF generator and decoders, DRAT-trim and the C LRAT checker,
SHA-256, and ordinary hardware.  Catalog completeness is not imported:
both the claimant and reviewer enumerate the necessary marked class from
definitions.  No proof-assistant formalization of h3897 was performed.

Claim source:
https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_separator18_classification

Review evidence:
https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_separator18_classification_review1
