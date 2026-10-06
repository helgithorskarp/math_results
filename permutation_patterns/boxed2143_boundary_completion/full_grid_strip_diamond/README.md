# Full-grid boxed2143 strip and diamond reduction

This is a checked partial research result by Lyra (`literature-researcher-2`),
with an entire internal check by Sage (`literature-researcher-1`). The full
growth problem remains unsolved. These are internal team checks, not
external peer review or novelty certification.

Let a_n count permutations with no i1<i2<i3<i4 satisfying
p(i2)<p(i1)<p(i4)<p(i3) and with no unselected point in the strict open
rectangle between positions i1/i4 and values p(i2)/p(i3). The agreed
target is to decide whether one finite positive C satisfies a_n<=C^n
for every n>=1, or limsup a_n^(1/n)=infinity. This directory establishes
neither alternative.

The construction uses r^2 old points and(r-1)^2 guard points, with all
4r-2 row/column component permutations independently recoverable from
fixed bands. Every component lies in its boxed2143 avoidance class.
`FULL_GRID_STRIP_AND_DIAMOND_REDUCTION_V1.md` proves, uniformly in r,
that its COMPLETE output occurrence set is exactly the union of adjacent
old/guard strip occurrences and two precisely indexed orthogonal diamond
families. The diamond clauses depend on comparisons of successive label
positions. Vertical inputs use inverse column permutations.

Consequently the exact compatible input count K_r is a weighted partition
over TWO independently sampled WHOLE strip-safe chains. It retains every
actual permutation multiplicity and all correlations within a chain.
It is not an unweighted attained-state count or independent-bit model.
The proof also records the r2 boundary and an obstruction to substituting
arbitrary positive chain weights for the actual uniform population.

The missing estimate is fixed r0>=2 and delta>0 with
K_r>=2^(delta*(r^2+(r-1)^2))*a_r^(2r) for EVERY r>=r0. If established,
the decoder would give an iterated growth gain and solve the negative
alternative. Finite K3=88456 proves no such estimate. There is no fitted
delta or starting size. The separate later projected-weight work is outside
this publication.

`ADAPTIVE_FULL_GUARD_OBSTRUCTION_V1.md` includes the prior uniform decoder,
monochrome exclusion and an explicit dead old-core repair fiber at every
r>=3. That dead fiber does not refute an aggregate K inequality.
`GRID_MIXED_BOX_LOCALIZATION_V1.md` and its review preserve the related
earlier geometric dependency. Its historical half-grid P status was
later superseded: the original every-r half-grid premise was disproved
at8 and is not adopted here. Original proof/review status text is preserved;
current accepted scope is recorded in `PUBLICATION_PROVENANCE.json`.

Use CPython3.11.2 or later with the standard library, one native thread,
from this directory. Both output paths must be fresh:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B full_grid_strip_diamond_probe_v1.py --output /tmp/boxed2143-full-grid-author.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B review/check_lyra_full_grid_strip_diamond_v1.py --author-dir . --author-report /tmp/boxed2143-full-grid-author.json --output /tmp/boxed2143-full-grid-review.json
```

These regenerate the bulky reports locally. They are deliberately omitted
from Git; `COMPACT_CHECKED_EVIDENCE.json` records their original hashes,
complete-domain sizes, exact counts and mathematical stream hashes.
Expected results include:

* Every avoiding old/guard pair through size5 in BOTH strip directions:
  domains2/12/138/2438 and safe counts2/11/103/1423 per direction.
* All1694 prescribed FULL literal grid sets:1536 at3,48 diamond truth
  controls at4 and110 directed profiles at5. Complete set stream
  `1e0a9c6c7f74d2526bbfff06643d97fe68aed0b451a1a510f8642511facd06d0`.
* All864 raw chains at3,616 strip-safe chains,256 full comparison-word
  states with every multiplicity, and all65536 weighted state pairs:
  K3=88456. Chain stream
  `2857b46eeba38c0fe33db1785314d32fff494f468463d9ab0364bab7ce6b1f5b`;
  weighted partition stream
  `39f385e8e6adc4be5f2e852802be448349760dd091da86b64b3d8d0cfba2b292`.
* The independent checker additionally evaluates ALL379456 actual pairs
  of the616 safe chains in the SAME execution, obtaining88456. It also
  checks all16 literal r2 grids and the identity-chain incompatible pair.

There is no complete746496 literal r3 grid census, larger input census,
uniform density result or second independent checker execution. Source
publication does not prove the theorem. The written all-size argument and
the exact finite reconstruction have distinct roles.

The author source/encoder/literal checker/proofs are unchanged. The portable
reviewer changes only source pinning and input/output paths. Every other
function is AST-identical to Sage's checked source; the two helper files
retain exactly the used original function bodies. The reviewer uses its
own literal oracle, arithmetic encoder/decoder, actual-band strip extraction
and actual-point diamond checks, importing no author executable. The
portability replay is an author publication check, not another independent
review. `PORTABILITY_VERIFICATION.json` records all deterministic field
alignments. `MANIFEST.json` pins runnable sources and their compact evidence;
`SOURCE_MANIFEST.json` covers the entire publication except itself.
Original review manifests in `review/` retain historical LOCAL closure
identities and list omitted generated files for provenance; they are not
claims that all those bulky files are present here.

Primary context is Kitaev--Qiu--Xu,
[Coincidences and Growth of Boxed Mesh Patterns](https://arxiv.org/html/2609.13764v1),
Theorem3.2 and Section7. No graph entry supplied the target. Downloaded
papers, campaign checkpoints, chat/private notes, credentials and verbose
generated data are excluded from this directory.
