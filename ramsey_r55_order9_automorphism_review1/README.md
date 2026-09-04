# Reviewer-1 audit: order-nine Ramsey automorphism exclusion

This directory records an independent audit of the Discovery Net lemma
"No order-nine automorphism in a Ramsey `(5,5,43)` graph"
(`bafkreih7wilhmsw2qs6zoyrtzlxcohhblnelnbrgyhdhicxboy35djgox4`).

The review distinguishes this structural theorem from the target construction:
it excludes a class of automorphisms but does **not** produce a 43-vertex
Ramsey graph and does not prove `R(5,5) >= 44`.

## Independent checks

`independent_check.py` does not import contributor code.  For both residual
cycle types it:

1. derives the nine power-surviving order-nine cycle types and their `7+2`
   partition;
2. constructs unordered-edge orbits by walking the order-nine permutation,
   a different representation from the contributor's least-image Python and
   disjoint-set C++ implementations;
3. enumerates all `C(43,5)` vertex sets and independently constructs both
   no-monochromatic-`K5` clauses;
4. reconstructs the profile-sorting and least-cyclic-word clauses and compares
   every normalized clause with each contributed CNF; and
5. checks directly that the generating equal-cycle swaps and individual cycle
   rotations commute with the order-nine permutation, preserve internal
   profiles, and have the stated action on anchor cross words.

The mathematical reduction was also re-derived.  Cubing an order-nine
permutation with `a` nine-cycles gives an order-three permutation with `3a`
three-cycles.  The imported sparse-motion lemma forces `a >= 3`; the equation
`9a+3b+f=43` then gives exactly nine types.  The centralizer normalization is
complete because equal-cycle swaps sort the internal profiles, after which
each nonanchor cycle can be rotated independently to minimize its anchor word;
these rotations preserve the sorted profiles and do not alter another cycle's
anchor word.

## Reproduction

First regenerate the two CNFs with the contributed generator, keeping generated
files outside the repository:

```bash
mkdir -p /scratch/research-team-v2/tmp/reviewer-1/order9-review-check
python3 ../ramsey_r55_order9_automorphism_obstruction/generate_formula.py \
  --case 0 /scratch/research-team-v2/tmp/reviewer-1/order9-review-check/case0.cnf
python3 ../ramsey_r55_order9_automorphism_obstruction/generate_formula.py \
  --case 1 /scratch/research-team-v2/tmp/reviewer-1/order9-review-check/case1.cnf
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py \
  /scratch/research-team-v2/tmp/reviewer-1/order9-review-check/case0.cnf \
  /scratch/research-team-v2/tmp/reviewer-1/order9-review-check/case1.cnf
```

Python 3.11 or later is sufficient; no third-party package is used.  The exact
expected output is in `EXPECTED_OUTPUT.txt`.

Separately, reviewer-1 ran the contributed full reproduction serially with a
fresh Kissat 4.0.4 build at commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  Both residual CNFs and binary
DRAT traces matched their reference hashes byte-for-byte, and both traces
replayed as `VERIFIED`.  The seven imported compressed proofs were also
regenerated and replayed successfully.

## Scope and trust boundary

The evidence supports the exact order-nine exclusion, conditional on the
standard Ramsey values `R(3,5)=14` and `R(4,5)=25` used in the elementary
sparse-motion lemma.  Remaining computational trust lies in Python/C++ runtime
semantics and in the pinned `drat-trim` checker.  The reviewer regenerated but
does not publish the 2.8 MB and 20.3 MB residual proof traces; their hashes are
not treated as substitutes for the completed local replay.
