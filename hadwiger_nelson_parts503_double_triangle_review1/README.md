# Independent review of the Parts503 double-triangle family

Verdict: **accept and strengthen, with a strict finite-pool and fixture
limitation**.

An independent exact implementation confirms that every one of the 1,401
declared five-point double-triangle replacements produces a strict
**508-point plane unit-distance graph** with a proper four-colouring. The
review strengthens this to chromatic number **exactly four for every support**
by checking a retained seven-point, eleven-edge Moser spindle and exhausting
all `3^7` colourings.

The selected support on pool indices

```text
38, 54, 529, 561, 953
```

has 2,450 complete unit edges. It rejects 12 of the 22 supplied complete host
colourings; three of those failures disappear when the private new--new edges
are removed. Ten supplied host colourings still extend. This is the strongest
member only under the declared statistic—fewest surviving fixtures, then
lexicographic tie-break—not under the full host relation.

That distinction is decisive: the 22 words are genuine colourings of all 503
host vertices, but they do **not** enumerate every host colouring or every
replacement boundary state. The result proves a real partial input-colouring
obstruction inside this finite family, not a non-four-colourable graph.

## Independently recovered quantities

| Quantity | Result |
|---|---:|
| Ambient points / all unordered pairs | 1,667 / 1,388,611 |
| Complete ambient unit edges | 11,074 |
| Parent points / edges | 509 / 2,442 |
| Host points / edges after six deletions | 503 / 2,418 |
| Pool unit triangles | 625 |
| Distinct double-triangle five-sets | 1,401 |
| Points in every support | 508 |
| Complete support-edge range | 2,439--2,452 |
| Minimum surviving supplied fixtures | 10 |
| Selected old--new / new--new edges | 26 / 6 |
| Selected complete edges | 2,450 |
| Selected surviving / rejected fixtures | 10 / 12 |
| Rejections requiring new--new constraints | 3 |
| Chromatic number of every support | 4 |

The reviewer scans every ambient pair without the target's modular sieve. It
uses direct coefficient arithmetic in
`Q(sqrt(3),sqrt(5),sqrt(11))`, and its 11,074-edge stream agrees entry for
entry with the pinned ambient table. It independently enumerates the family
both by pairs of triangles meeting in one vertex and by two disjoint opposite
edges at a shared centre. Both routes give the same 1,401 five-sets.

For each support and each of the 22 host words, the review enumerates the
definition-level set of all `4^5` new-vertex colour words. The complete
support/fixture relation and first-positive-witness streams have SHA-256

```text
cases     3d6a2084e17d852dad98812b11ba1410fda1425283261278b46360e80811236c
witnesses f95e48873db8990a03ee7367a9ac48c616758a53e6e2ee67482aec9aeb756ba6
```

A fresh proper colouring uses host fixture 18 and differs from the target
word in 394 of 508 positions.

## Reproduction

CPython 3.11 or later and a full checkout of this repository are required;
the standard library suffices. From this review directory:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The controls compare the exact square formula with 6,561 generic radical
expansions, compare all 1,024 possible five-vertex edge masks with an
independent recursive colour enumerator, confirm the two family enumerators,
and reject input-hash and colour corruptions. See [PROOF.md](PROOF.md) and
[VALIDATION.json](VALIDATION.json).

The four public dependency files total about 744 KB and are not duplicated in
this review directory. Their paths and hashes are pinned in `verify.py` and
documented in [PROVENANCE.md](PROVENANCE.md). No private data, generated edge
dump, solver log, floating-point incidence predicate, or SAT result is needed.

## Exact scope and record status

The theorem closes only the host obtained by deleting Parts vertices
`310,313,316,319,322,325`, the published ordered 1,158-point pool, and the
five-point supports containing two unit triangles sharing exactly one vertex.
It does not cover points outside the pool, other deleted vertices, other
five-point shapes, more added points, or a complete host-colouring relation.

The selected graph is at the 508-point target cap but is four-colourable. It
is therefore not a record candidate. Parts's published 509-vertex,
2,442-edge five-chromatic construction remains the supported unrestricted
record in the bounded primary-source check, also identified as current by
Haugland's August 2026 paper.

## Sources

- Reviewed target (branch path):
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_parts503_double_triangle_stop>.
  Exact reviewed revision:
  `05f007b2fd745420c57b8e55d7f5a59609e01b6b`.
- Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- Haugland, [A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane](https://arxiv.org/abs/2608.04542).

The requested `math-review` skill was unavailable. Its independence,
exact-scope, geometric-realization, chromatic-certificate, hidden-assumption
and source-integrity criteria were applied directly with the available exact
computer-assisted and GitHub research skills.
