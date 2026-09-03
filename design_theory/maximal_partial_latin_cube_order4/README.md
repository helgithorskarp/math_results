# Maximal partial Latin cubes of order 4 with 28 and 30 entries

## Result

Let `ML(3,n)` be the set of sizes of maximal partial Latin cubes of order
`n`.  Britz, Cavenagh, and Sørensen proved

```text
ML(3,4) = {31,...,61,64} union S, where S is a subset of {28,29,30},
```

and left membership of 28, 29, and 30 as a challenging computational
problem.  The two explicit certificates in this directory prove

```text
28 in ML(3,4) and 30 in ML(3,4).
```

In particular, their exclusion of every smaller size together with the
28-entry certificate gives the exact minimum `f(3,4) = 28`.  This directory
does **not** decide whether `29 in ML(3,4)`.

The source problem is Theorem 11 and the paragraph following it in Thomas
Britz, Nicholas J. Cavenagh, and Henrik Kragh Sørensen, "Maximal partial
Latin cubes," *Electronic Journal of Combinatorics* 22(1) (2015), P1.81:

https://www.combinatorics.org/ojs/index.php/eljc/article/download/v22i1p81/pdf/

## Finite reduction

Represent a filled entry by a word `(layer,row,column,symbol)` in
`{0,1,2,3}^4`.  Two distinct entries are compatible exactly when they differ
in at least two coordinates.  A compatible set is maximal exactly when each
of the 256 words is at Hamming distance at most one from a selected word.
Thus a maximal partial Latin cube is exactly an independent dominating set
of the Hamming graph `H(4,4)`.

The two JSON files list 28 and 30 selected words.  `verify_certificate.py`
checks directly, with standard-library integer and tuple operations, that:

1. every word is distinct and lies in `{0,1,2,3}^4`;
2. every selected pair has Hamming distance at least two; and
3. all 256 words are in a selected closed radius-one neighborhood.

The last condition is precisely maximality, including all possible empty
cells and symbols.  The certificates are therefore proof witnesses; the SAT
solver used to discover them is outside the correctness trust boundary.

## Reproduction

Tested with CPython 3.11.2; no third-party Python package is required.

```bash
python3 verify_certificate.py order4_size28.json
python3 verify_certificate.py order4_size30.json
```

Expected headline fields are:

```text
order4_size28.json: status VERIFIED, selected_words 28,
  minimum_pairwise_hamming_distance 2,
  minimum_closed_neighborhood_coverage 1,
  canonical_selected_words_sha256
  5f377e8f313391a47c7a0748e88b0eed11ee1cf52b5fc1ddafc040ee87b86c7d

order4_size30.json: status VERIFIED, selected_words 30,
  minimum_pairwise_hamming_distance 2,
  minimum_closed_neighborhood_coverage 1,
  canonical_selected_words_sha256
  aaeef4b34fc12ef5fcebeac6f1b46c072ec6260dc57c254e18d3dfc3f6c7f073
```

`generate_cnf.py` emits the exact SAT reduction.  One primary variable is
used per lexicographically ordered word.  Binary clauses enforce
independence, 13-literal clauses enforce domination, and an exact unary or
Sinz sequential counter enforces cardinality.  Fixing `0000` is sound because
the Hamming graph is vertex-transitive.  For example:

```bash
python3 generate_cnf.py /scratch/order4-atmost30.cnf --bound 30
python3 generate_cnf.py /scratch/order4-atmost29-case-c.cnf \
  --bound 29 --fix-word 1,1,1,0
```

CaDiCaL 3.0.1 found the 30-entry certificate from the first instance and the
28-entry certificate from the second.  Solver models and logs are not needed
to check the result and are intentionally not committed.

## Continued size-29 search

`trade_search.py` exhausts bounded entry trades around either certificate.
`heuristic_search.py` is explicitly a non-proof, seeded witness finder.
They are included to make the unresolved middle case easy to resume.  In the
reported pass, no `+1` trade through three removals from the size-28
certificate and no `-1` trade through four removals from the size-30
certificate existed.  A seeded independent-only run reached a 29-word set
with three uncovered words, but no certificate.  Incomplete solver and
heuristic runs make no nonexistence claim.

## Novelty and trust boundary

Exact-phrase and concept searches through 2026-09-03 found the 2015 open
problem and later work on general lower bounds, but no resolution of these
three order-4 values.  The result is therefore described as apparently new to
the searched sources, not as a priority claim.

The positive theorem trusts only the short mathematical equivalence above,
the two JSON lists, CPython's exact finite operations, and inspection of the
small verifier.  The statement that 28 is minimum additionally imports the
published exclusion below 28 from Britz--Cavenagh--Sørensen.
