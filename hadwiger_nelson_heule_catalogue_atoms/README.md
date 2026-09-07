# Exact exclusion of target-sized Heule catalogue block selections

Every selection of the 21 blocks defined below with at most 508 vertices is
four-colourable. There are **1,648,500 such selections**, including **3,840 of
order exactly 508**. All vertex- and edge-deleted subgraphs of these selections
are also four-colourable. Fifty explicit positive colourings certify the entire
family. This is a finite construction-family exclusion, not a record improvement.

The host is the union of `510.vtx`, `517.vtx`, `529.vtx`, and `553.vtx` from
[Heule's CNP-SAT coordinate archive](https://github.com/marijnheule/CNP-SAT/tree/master/vtx),
in their supplied placements. Its strict unit-distance graph has **711 vertices
and 3,844 edges**. This host differs from the campaign's earlier H517, which
adjoined seven completion points to H510. The present source `517.vtx` is the
original archived graph.

## Complete candidate space

Write the four coordinate sets, in this order, as P510, P517, P529, P553.
Their coordinates lie in K = Q(sqrt(3),sqrt(5),sqrt(11)). Let sigma be the
field automorphism changing the sign of sqrt(5) and fixing sqrt(3), sqrt(11).
For a point p in their union define

- m(p) = the four-bit membership mask of the source sets containing p;
- s(p) = 0 if both coordinates are fixed by sigma, and 1 otherwise.

A block consists of all points with the same pair (s,m). The blocks are
nonempty and disjoint. Order them lexicographically by (s,m). A candidate
includes or omits each whole block independently, with total order at most 508.
The table specifies every block; membership bits 1,2,4,8 mean 510,517,529,553.

| s | Membership masks, in order | Block orders, in the same order |
|---|---|---|
| 0 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 | 27,3,4,14,2,14,77,125,1,1,7,9,1,20,256 |
| 1 | 4,7,8,11,12,15 | 2,15,11,3,2,117 |

Thus this is a complete decision on **all 2^21 = 2,097,152 assignments** under
the order predicate, rather than a sampled sequence of exchanges. Exactly
4,396 admissible assignments are maximal under containment.

The initial concrete crossover takes the 375 sigma-fixed vertices of P510
and the 133 nonfixed vertices of P553. It has exactly 508 vertices and 2,497
unit edges, and is four-colourable. Its colouring is the first certificate
word. The full block decision includes all other admissible recombinations.

Arbitrary subsets that split blocks are not all classified. Nor does this
classify other archive files, other relative placements, or all subgraphs of
the entire 711-point host. The selected coordinate sets and partition are
part of the theorem's hypotheses.

## Certificate and proof

[certificate.json](certificate.json) has 50 entries. Each entry gives a
21-bit support mask and a 711-character word. A selected vertex has one of
`0,1,2,3`; every absent vertex has `-`. Vertices are labelled by lexicographic
order of their 16 integer coordinate coefficients. Each coordinate has scale
288 in the ordered radical basis

```
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The checker verifies support membership and every edge of every word, totaling
**165,644 checked edge incidences**. The coloured supports have orders from
455 through 705. Larger coloured supports legitimately certify their smaller
subgraphs by restriction.

For completeness, set C[mask]=1 for each certified support, then propagate
C[M] |= C[M union {i}] for every bit i absent from M. The elementary induction
after each processed bit shows that the final value is one exactly when M is
contained in a certified support. The checker inspects every assignment in
Gray-code order, updating its vertex count by its single changed block, and
requires C[M]=1 whenever its order is at most 508. Every admissible candidate
therefore inherits a proper four-colouring. No solver UNSAT claim is needed.

[verify.py](verify.py) imports no producer module. Its mathematical and
computational checks are independent in the following ways:

- The producer evaluates the coordinate syntax as eight-component field
  vectors, using successive conjugate norms for inversion. The checker keeps
  rational-expression numerators and denominators separate, multiplies
  squarefree radical dictionaries using gcd, and verifies that the expanded
  denominators in this pinned corpus are monomials. It then rationalizes those
  monomials exactly. Both parsers restrict the AST; neither executes source text.
- The producer uses bit-indexed products and optimized squaring to enumerate
  unit edges. The checker expands both squared coordinate differences using
  its separate radical arithmetic on **all 252,405 unordered point pairs**.
  Nonunit pairs are excluded by exact coefficient comparison, not a numerical
  threshold or modular acceptance.
- Discovery explicitly enumerates maximal admissible masks and removes them
  by support containment. Verification uses the downward Boolean transform
  and a separate Gray-code scan of every assignment, including the empty set.

Independence of the square classes of 3,5,11 makes coefficient equality exact.
All square roots in the source expressions are positive. No floating-point
proposal, guessed contact, native SAT verdict, or previous chromatic-number
certificate is a premise of the proof. This is author-run independent
checking, not an independent-author review or formal proof-assistant result.

## Reproduction

Python 3.11 or later, with the standard library, suffices to verify. The four
original text coordinate files total 107,377 bytes and are downloaded into
an external working directory, not redistributed here. [inputs.json](inputs.json)
pins their exact sizes and SHA-256 hashes. The archive head inspected was
`bb414955a6ef5f49f7df2b245b1e778aa67c068a`; hashes, rather than the mutable branch
name, determine the mathematical inputs. A changed download is rejected.

From this directory in a full checkout:

```bash
python3 -B native.py --inputs /scratch/heule-catalogue-inputs --download
python3 -B verify.py --inputs /scratch/heule-catalogue-inputs --check-expected
python3 -B controls.py --inputs /scratch/heule-catalogue-inputs
python3 -O -B controls.py --inputs /scratch/heule-catalogue-inputs
sha256sum -c SHA256SUMS
```

[expected.json](expected.json) contains the deterministic verifier report.
The 36,963-byte certificate has SHA-256
`5733907c26804d6502fa8943d13071ee977d5e04d6c91027b5964adf4386291a`.
The canonical coordinate-stream hash is
`917b08b63f709d25513d1853ed246e4124acfeafdde8a01e72cfc0bdd3e57f2c`;
the sorted `u v` edge-stream hash is
`bb69cb043383192f717abcfbc91bf87861a87790eee66fb6f562fb3f9cc9881e`.
Both streams end every row with a newline.

Optional discovery needs `python-sat==1.9.dev15` and its bundled CaDiCaL195:

```bash
python -B generate.py --inputs /scratch/heule-catalogue-inputs --out /scratch/heule-catalogue-regeneration
```

The output directory must not already exist. This regenerated the committed
certificate byte for byte in 71.75 seconds in the recorded Python 3.11.2
environment. Besides the initial crossover, 49 primary candidates were all
SAT within 200,000 conflicts per query. The 529 optional whole-block growth
queries used 2,000 conflicts each: 305 returned checked colourings and 224
were UNKNOWN. The latter are unused extension attempts; none is an exclusion
or a remaining candidate. No budget was raised, and the final family has no
unresolved member. Different solver builds can produce different valid words;
the positive checker remains the authority.

The controls exhaust 11,542 small weighted-coverage cases over all cover
families on up to three blocks, weights in {1,2}, and all cardinality thresholds.
Their reference implementation uses direct subset tests and containment,
including incomplete covers. They also check 64 basis products, six parser
fixtures, equality of the two full geometry reconstructions, and rejection of
14 corrupt inputs. Removing an essential final word tests actual incomplete
family coverage. Normal and optimized verifier and control reports agree.
[controls_expected.json](controls_expected.json) records these results.

## Scope, provenance, and disposition

Heule's [primary paper](https://arxiv.org/abs/1805.12181) explains the earlier
SAT-based graph minimization work; the exact inputs here are the separately
pinned archive files. This package does not claim that the original graphs,
coordinate field, or block-exchange heuristic are new. It supplies a compact
complete positive certificate for this specified candidate space.

The scoped Discovery Net refresh through height 3646 found no overlapping new
work. The accepted [Parts planar-realization review](../hadwiger_nelson_parts509_plane_realizations_review1/README.md),
the completed [Haugland metric-ball family](../hadwiger_nelson_haugland2131_target_balls/README.md),
and the teammate's [EI17 common-pair assembly exclusion](../hadwiger_nelson_ei17_common_pair/README.md)
were read as coordination context. None is a proof premise. The retired H560,
capped H632, Parts-map and teammate construction routes were not resumed.

This 21-block candidate gate is complete and retired. The overall <=508
five-chromatic unit-distance graph target remains open. No finer-block ladder,
additional catalogue source, or subsequent major phase is started here.
