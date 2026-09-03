# Exact point-degree patterns of optimal `(12,5,2)` coverings

A `(12,5,2)` covering is a family of five-subsets (blocks) of a 12-point
set such that every pair of points lies in at least one block.  The known
covering number is `C(12,5,2)=9`.

## Theorem

The point-degree multiset of a nine-block `(12,5,2)` covering is exactly one
of

```text
(4^9,3^3),
(5,4^7,3^4),
(5^2,4^5,3^5),
(5^3,4^3,3^6).
```

Every displayed multiset occurs.  The only other arithmetically possible
multiset, `(5^4,4,3^7)`, does not occur.

## Reduction to five possibilities

Each point has degree at least three, because one block through it covers at
most four of its eleven incident pairs.  A separately proved and independently
reproduced graph result shows that every point has degree at most five.  If
`n_i` is the number of points of degree `i`, then

```text
n_3+n_4+n_5 = 12,
3*n_3+4*n_4+5*n_5 = 9*5 = 45.
```

Consequently

```text
(n_3,n_4,n_5) = (3+a,9-2*a,a),  a=0,1,2,3,4.
```

The file `witnesses.json` gives a definition-level witness for each of
`a=0,1,2,3`, and `verify_witnesses.py` checks all four independently of any
solver.

## Excluding `a=4`

`generate_cnf.py` encodes a `12 x 9` point-block incidence matrix.

- The row sums are `(5^4,4,3^7)`.
- Every column sum is five.
- For every pair of rows, Tseitin conjunction variables require a common
  column.
- Columns and equal-degree rows are put in nondecreasing lexicographic order.

The final item is only symmetry breaking.  In the finite orbit under arbitrary
column permutations and row permutations within equal-degree classes, choose
a lexicographically least row-major matrix.  Its rows within each class and
its columns are both lexicographically ordered, so every possible covering has
a representative satisfying the added clauses.

CaDiCaL 3.0.1 proves the resulting CNF unsatisfiable.  Its binary DRAT trace is
independently accepted by `drat-trim`.  The trace belongs under `/scratch` and
is deliberately not committed.  `audit.py` independently checks the compact
expected hashes, all four witnesses, and the sequential-counter and lex-order
encoders on exhaustive small instances.

## Reproduction

The generator and audit need Python 3.11 or later.  Supply CaDiCaL and
`drat-trim` executables and a scratch directory:

```bash
./run_and_check.sh /scratch/c12_5_2_degree_patterns /path/to/cadical /path/to/drat-trim
```

The pinned production run used CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

## Consequence for the `C(13,6,3)` frontier

In a hypothetical 20-block `(13,6,3)` cover, the link at every degree-nine
point is an optimal `(12,5,2)` covering.  Thus the previous five-case list of
link multiplicity profiles shrinks to four cases.  In particular, under the
exceptional global point-degree profile `(12,9^12)`, each degree-nine point
has codegree five with the degree-twelve point and with at most two of the
other degree-nine points.  Equivalently, the graph on the twelve low points
whose edges mark pair multiplicity five has maximum degree two (the previous
bound was three).  This is a strict compatibility cut, but it does not by
itself decide `C(13,6,3)`.

## Scope and trust boundary

The positive cases are ordinary directly checked witnesses.  The negative
case is an exact computer-assisted theorem.  It trusts the transparent CNF
generator, Python runtime, CaDiCaL, `drat-trim`, their compilers and runtimes,
hardware, and the argument that the symmetry constraints preserve an orbit
representative.  The independent audit and an independent CP-SAT incidence
model narrow generator and encoding risk; only the DRAT-checked path is used
as proof evidence.

The exact value `C(12,5,2)=9` is imported from the La Jolla Coverings
Repository version 1.2.  Targeted searches of that dataset, exact-parameter
queries, and the covering-design literature located the exact value and a
degree pattern with one degree-five point, but no classification of all point
degree patterns.  The classification is therefore apparently new to the
searched sources, not a priority claim.

Primary context:

- Daniel Gordon, La Jolla Coverings Repository, version 1.2,
  <https://zenodo.org/records/19735294>.
- Daniel Horsley, *Generalising Fisher's inequality to coverings and
  packings*, <https://arxiv.org/abs/1409.0485>.
- Daniel Gordon, Greg Kuperberg, and Oren Patashnik, *New constructions for
  covering designs*, <https://arxiv.org/abs/math/9502238>.
