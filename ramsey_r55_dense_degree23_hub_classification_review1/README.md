# Independent review: dense degree-23 hub classification

Verdict: **accept, with the imported completeness boundaries stated below**.
The reviewed contribution is
`bafkreib32yjgeg6rdrmz7y5wo3csmanuuy234kr3aakm2363pqd3hn7oke`, from
source commit `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb` in
[`njallskarp/math_source_code_open`](https://github.com/njallskarp/math_source_code_open/tree/590bcae0fe01e88e0a8fcf8030fbb2524973e4cb/ramsey_r55_dense_degree23_hub_classification).

The result has two accepted parts:

1. For the two specified degree-five hub-neighborhood types over the displayed
   Paley-17 core, the sharp edge maxima are 115 and 116.  Their complete
   equality families contain 24 and 29 isomorphism classes, respectively;
   every one of the 53 graphs has a unique degree-five hub and is rigid.
2. All 144 marked type-62 density-115 extensions of original interfaces 6, 7
   and 8 are UNSAT with every remaining physical edge free.  This strengthens
   the red-deficiency lower bound from seven to eight in precisely those
   degree-23 branches.

This is an intermediate reduction.  It does not exclude an entire degree-23
interface, the 3,132 type-126 equality templates, any whole M-slice, or the
order-43 Ramsey problem.

## Independent checks

[`independent_check.py`](independent_check.py) imports no reviewed module.  It
performs a third complete local enumeration, with no affine normalization and
the different variable order `X2,X4,X3,X0,X1`.  It obtains exactly 6,528 and
47,328 labeled tuples, hashes their full sorted streams, reconstructs all
certificate orbits, and confirms 24 and 29 rigid classes.  It also:

- derives the full 5,593-column domain and its size histogram directly;
- checks every representative as a physical 23-vertex graph;
- derives all 136 Paley-core automorphisms through the eight-neighbor
  stabilizer rather than assuming a group order;
- decodes and validates the thirteen imported interfaces, retains every
  relative marking, and reconstructs all 144 plus 3,132 boundary keys;
- reconstructs every type-62 physical fixed/free matrix and confirms exactly
  389 remaining variables in each case;
- checks every regenerated CNF against both author encoders and the committed
  manifest, then independently reruns `drat-trim` on all 144 proofs; and
- uses a third literal enumeration of all 962,598 physical five-sets to rebuild
  one complete CNF for each of original interfaces 6, 7 and 8.

The reviewed full reproduction was run in one sequential process.  It
regenerated the certificate, independently enumerated both full tuple streams,
ran definition-level controls, regenerated and byte-compared all 144 formulas,
and checked every fresh solver proof.  The replay used Kissat 4.0.4 at commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

## Mathematical audit

Let `S` be the five red neighbors of the degree-five hub and `T` its seventeen
blue neighbors.  Once `T` is the displayed Paley graph, the four column
conditions are necessary and sufficient.  A red `K4` meeting `S` uses one or
two vertices of `S`; a blue `K5` meeting `S` uses two or three.  The stated two
graphs on `S` are triangle-free, have no independent four-set, and have the
unique independent triple `{2,3,4}`.  These facts account for every possible
forbidden clique and justify the finite five-column enumeration.

For each marked global case, the fixed data contain exactly the original
22-vertex interface, the root star, the degree-23 hub star, the Paley core,
and 85 classified `S`-to-core edges.  Exactly 389 physical edges remain free.
The CNF contains both color prohibitions for every physical five-set after
substitution, with no degree, quota, symmetry, or auxiliary-variable
constraint.  Verified UNSAT therefore has the asserted complete-extension
meaning.

## Imported trust and scope

The checker verifies the literal Paley computation and every supplied
interface graph.  It does **not** reprove the classical uniqueness of the
order-17 `(4,4)` Ramsey graph, nor the upstream completeness of the thirteen
interfaces and their separator bridge.  Those are explicit imported facts.
The global verdict also trusts the small `drat-trim` checking kernel, the
published source identity, compiler/runtime semantics, and ordinary hardware.

The 3,132 type-126 marked templates remain open, as do lower-density cases,
lower global hub degrees, and all other structural families.  Local existence
of one of the 53 neighborhoods does not imply a compatible order-43 graph.

## Reproduce

First run the reviewed package from its repository root into a fresh external
directory:

```sh
python3 -B ramsey_r55_dense_degree23_hub_classification/reproduce.py \
  /scratch/dense-hub-full --cxx c++ \
  --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim
```

Then, from this repository root, run the independent audit against that source
and replay directory:

```sh
python3 -B ramsey_r55_dense_degree23_hub_classification_review1/independent_check.py \
  /path/to/math_source_code_open/ramsey_r55_dense_degree23_hub_classification \
  --replay /scratch/dense-hub-full \
  --drat-trim /absolute/path/to/drat-trim \
  > ramsey_r55_dense_degree23_hub_classification_review1/verification.json
sha256sum -c ramsey_r55_dense_degree23_hub_classification_review1/SHA256SUMS
```

The independent enumeration is intentionally compute-bearing.  Use a fresh
scratch location outside the repositories and run only one such process at a
time.  The complete command was also repeated with `python3 -O -B`; it produced
the byte-identical report, so no semantic check depends on Python assertions.
