# Complete low cut-rank exclusion for Ramsey(5,5;43)

Every 43-vertex graph with neither a clique nor an independent five-set
has binary cut rank at least three across **every partition with at least
four vertices on each side**, in each color separately. Thus the complete
global family admitting any such cut of rank at most two is excluded.
All internal edges and all low-rank cross matrices are covered.

The [proof](PROOF.md) gives the stronger cut-size profile

| smaller side | 1 | 2–3 | 4–7 | 8–9 | 10–14 | 15–19 | 20–21 |
|---|---:|---:|---:|---:|---:|---:|---:|
| rank at least | 1 | 2 | 3 | 4 | 3 | 4 | 3 |

Consequently both color graphs have rank-width at least three and linear
rank-width at least four. No claim of sharpness or historical priority is
made. The local pair/triple identities come from the earlier accepted
[module-resilience result](../ramsey_r55_module_resilience/README.md);
this package applies them to all cuts and gives a complete global-family
decision. The proof imports R(4,5)<=25 and derives its other small Ramsey
inputs elementarily. It is not proof-assistant formalized.

## Physical search branch

In the earlier [F27 pentagon normal form](../ramsey_r55_pentagon_normal_form/README.md),
take A=7..26 and B={0..6,27..42}. The 460 cross pairs are all initially
free, while the 61 pins leave 382 other free pairs inside the two sides.
The entire branch with a rank<=2 cross matrix in either chosen color is
excluded. For each rank color separately it contains exactly

    12,895,167,237,427,691,649,324,376 * 2^382

distinct labeled physical assignments. The color branches overlap and are
not added. `model.family` covers the whole branch by a 20x2 times 2x23
binary factorization and all 382 internal bits. Its factor map is not
injective; distinct matrix counts are independently checked by a Gaussian
binomial recurrence and exhaustive small cases.

This closes the stated branch, not the remaining 842-variable normal
form. There is no new Ramsey graph, improvement in the Ramsey bound,
measured solver speedup or decision of rank-width-three graphs. No solver,
graph catalog, fixed-neighborhood gluing or full adjacency-rank threshold
is used. The normal form's external universal-coverage premise is not
needed to exclude these explicitly specified physical graphs.

## Reproduction and certificates

Python 3.11, standard library only; tested with CPython 3.11.2. From this
directory run:

```sh
python3 -B reproduce.py
python3 -B extract.py fixture.json
python3 -B verify.py fixture.json fixture_certificate.json
```

The full replay checks every manifest hash and compares expected outputs
byte for byte in normal and assertion-disabled Python. Expected status:
`REPRODUCED_CUT_RANK_OBSTRUCTION`, with the selected global family excluded,
`ramsey_graph_found=false`, and `ramsey_bound_improved=false`.

The finite audit checks:

* 126 cut-capacity cells and all 231 possible ordered centroid-component
  leaf-count triples. The centroid existence argument itself is in the proof.
* All 74,954 binary matrices of dimensions 1..4 by 1..4 with independent
  dense and bitset elimination, exact matrix counts and row-space counts.
* All 65,536 factor words for 4x2 times 2x4: exactly 7,576 distinct matrices
  of rank<=2. Rank-zero, rank-one and rank-two fiber sizes are 1,186,90,6;
  only the full-rank fiber is divided by six in the rank-two formula.
* Pair and triple contact identities; all 33,867 labeled graphs through
  order six, with 135,468 literal clique comparisons and all 32,768
  six-vertex checks of R(3,3)<=6.
* 96 F27 parameter graphs with all 86,688 physical pairs checked, also
  tested under relabeling and taking the complementary cut side, yielding
  192 controls in both rank colors. Another 42 controls cover every entry
  of the cut-size profile in both colors. All 234 give verified physical
  five-set obstructions.
* Two high-rank controls that correctly return outside this gate, eleven
  malformed-input rejections in each parser, and eleven corrupt-certificate
  rejections.

These controls are not an enumeration of the full 43-vertex family. The
guarantee for every admitted graph rests on the universal proof. The
extractor uses complete bitset clique search after gate recognition; its
failure to find a bad five is a hard theorem/implementation error, never a
feasibility verdict. The standalone verifier imports no producer, solver,
catalog or Ramsey theorem: it reconstructs dense adjacency, computes rank,
checks the supplied row-space basis, and inspects the witness's ten pairs.
Its profile arithmetic validates the stated gate relative to the proof.
The physical five-set check itself needs no Ramsey premise.

Input is a JSON object with exactly `n:43`, `red_hex`, `cut`, `rank_color`.
`red_hex` has exactly 226 lowercase hex digits and encodes 903 bits in
lexicographic pair order (0,1),(0,2),...,(41,42), first pair at the least
significant bit. Its value must be less than 2^903. Omitted red bits denote
blue pairs; there are no loops. `cut` is a sorted nonempty proper vertex
list using labels 0..42; the smaller side is selected automatically.
`rank_color` is `red` or `blue`. The interface accepts every profile
violation, including the rank-three exclusions at the stated cut sizes.

`EXCLUDED_WITH_PHYSICAL_WITNESS` includes five sorted vertices and their
color. `OUTSIDE_CUT_RANK_GATE` says only that this cut in this color meets
the necessary rank bound; it says nothing about Ramsey feasibility. The
saved fixture is expressly non-Ramsey and supplies no candidate. The
certificate binds to the canonical JSON input by SHA-256. All reproduction
inputs are included here; there are no network or repository-relative
runtime dependencies. Independent external review remains pending.
