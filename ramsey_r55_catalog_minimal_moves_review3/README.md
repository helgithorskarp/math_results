# Independent review of minimal Ramsey catalog moves

Verdict: **accepted and independently verified**, conditional on the declared
completeness of the five input transition maps.  Among all 37,256 nonempty
Ramsey-preserving labeled moves of radius at most six from the 328 stored
`(5,5;42)` catalog representatives, the inclusion-minimal supports are exactly
2,040 single edges and 160 balanced four-edge matchings.

This is a structural theorem about the neighborhood of the known catalog.  It
does not prove that the catalog contains every `(5,5;42)` graph, construct a
43-vertex graph, or improve a Ramsey bound.

Reviewed Discovery Net contribution:
`bafkreibwhhhmvigscpo3gpxhh7skj5q2vqgvnsib7qjdozqgllmhzzdjqm`, source
commit `43c083540988970edb902f36f8bf16751cf181d5`.

## Mathematical audit

For a fixed catalog graph `G`, order its nonempty Ramsey-preserving flip
supports of size at most six by inclusion.  Every support contains an
inclusion-minimal one because this is a finite poset.  The exact census shows
that each minimum has size one or four, and every size-four minimum consists
of four vertex-disjoint edges, two deleted from and two added to `G`.

This yields the claimed monotone factorization.  If `G triangle S` is Ramsey
and `|S|<=6`, choose a minimal valid `T subseteq S`.  The radius-six closure
puts `G triangle T` back in the known catalog up to relabeling and possible
complementation.  Relabel the remaining disjoint support `S minus T` and
induct.  No edge is revisited, every step has size one or four, and two
four-edge steps cannot occur within six total flips.

The radius-seven filter follows with the same direction of implication.  If a
new Ramsey graph `H=G triangle S`, `|S|<=7`, contained a catalog-minimal move
`T`, then `K=G triangle T` would be a catalog graph and

```text
distance(K,H) = |S minus T| = |S|-|T| <= 6.
```

Radius-six closure would force `H` back into the catalog, a contradiction.
Thus each minimal support supplies the necessary clause
`OR_(e in T) NOT x_e`.  The clause is only a filter: it does not assert that a
satisfying residual assignment is Ramsey or new.

Complementing a stored representative preserves support inclusion, the
Ramsey property, matching shape, and red/blue balance.  Hence the 328 stored
parent checks cover the complementary catalog orientations as claimed.

## Independent finite check

[`independent_check.py`](independent_check.py) imports no code from the target
artifact or its transition-map parsers.  It independently parses the five
hash-pinned radius maps, validates their schemas and declared counts, and
forms the 37,256 unique parent-relative supports.  For every support it
enumerates all proper nonempty subsets and recomputes the inclusion-minimal
and domination classifications.

The checker separately decodes all 328 graph6 parents and tests every parent
and all 37,256 flipped graphs directly for red and blue `K5`s.  It also
directly rejects all 2,240 proper nonempty subsets of the 160 quartets, checks
eight distinct endpoints and two-add/two-delete balance for each quartet, and
regenerates `MINIMAL_MOVES.tsv` byte-for-byte.  Its SHA-256 is
`27bfe713c711ab319bb9eb909cec997049e48c68e22539bbb54f543daea68896`.

As a separate target-identification check, NetworkX 3.5 VF2++ verifies that
each of the 2,200 flipped minimal graphs is isomorphic to its recorded base or
complement catalog target.  The exact histograms also reproduce:

| radius | valid moves | contain a singleton | quartet only |
|---:|---:|---:|---:|
| 1 | 2,040 | 2,040 | 0 |
| 2 | 5,568 | 5,568 | 0 |
| 3 | 8,632 | 8,632 | 0 |
| 4 | 8,408 | 8,248 | 160 |
| 5 | 6,224 | 5,968 | 256 |
| 6 | 6,384 | 6,256 | 128 |

The number of minimal-support clauses per stored parent ranges from two to
nine, with parent distribution `4,8,12,24,72,104,96,8`.  The target analyzer,
certificate checksum audit, and 4,096-case residual-CNF self-test also
reproduce exactly.  The separately declared parent-0 solver pilot ended
`UNKNOWN`; it supplies no proof and is not used in this verdict.

## Reproduction

From the repository root, using Python 3.11 or later and NetworkX 3.5:

```bash
python3 -m pip install -r ramsey_r55_catalog_minimal_moves_review3/requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_catalog_minimal_moves_review3/independent_check.py \
  | cmp - ramsey_r55_catalog_minimal_moves_review3/EXPECTED_OUTPUT.txt
cd ramsey_r55_catalog_minimal_moves_review3
sha256sum -c SHA256SUMS
```

The independent run takes about one minute on one CPU core; most of that time
is the 2,200 VF2++ target-isomorphism checks.

## Trust boundaries and uncertainty

The absence of further minimal supports is conditional on completeness of the
five committed transition maps through radius six.  Those maps retain their
earlier solver, compiler, target-canonicalization, catalog-file, and hardware
boundaries.  This review independently checks every recorded move, all subset
relations, and every minimal target identity, but it does not regenerate the
much larger searches that proved no transition rows were omitted.

The checks trust CPython integer execution, NetworkX VF2++, and the pinned
graph6 and transition-map bytes; the proof is not formalized.  Catalog
completeness itself is explicitly not assumed.  The residual clauses are
justified at radius seven because removing a contained minimum leaves at most
six flips; extending them unchanged to larger radii would require another
argument.
