# Independent review: eleven-cycle minority cores

## Verdict

**Accepted, with the stated scope.** In the three-versus-eight branch of an
order-three action of type `1^10 3^11` on a hypothetical Ramsey `(5,5;43)`
graph, the nine vertices in the three internally red moving triangles have,
up to the proved full-action normalizer, one of exactly three surviving core
types:

| class | red offset words on 01,02,12 | weights | phase sum |
|---:|:---|:---|:---|
| 8 | `100,100,100` | 1,1,1 | zero |
| 11 | `100,110,110` | 1,2,2 | zero |
| 13 | `110,110,101` | 2,2,2 | nonzero |

These are necessary local cores, not 43-vertex realizations. Classes 8, 11,
and 13 remain open. This result does not settle the four-versus-seven split,
construct a Ramsey graph, or improve the lower bound for `R(5,5)`.

Reviewed Discovery Net contribution:
`bafkreifis3am5nzzwbkfyffwms43tlyidpobstal7utqkziyl7oinptg2q`.
The source directory is unchanged from commit
`e5b88c054f96354007df003068c369ed273c65a5`.

## Core classification

Each pair of internally red triangles has a three-bit circulant red word. A
word `111` creates a red `K6`. Conversely, if all three words are noncomplete,
a blue clique uses at most one vertex from each red triangle. A red `K5` would
have occupancy 3+2, 3+1+1, or 2+2+1 across the triangles: the first two force
a complete block, while the last needs a red `K2,2`, which occurs in neither
an empty block, a matching, nor a six-cycle. Thus all `7^3=343` remaining
labeled cores and only those cores avoid a monochromatic `K5` locally.

The permitted relabelings permute the three red cycles, rotate them
independently, and optionally invert coordinates on **all eleven** moving
cycles. The 324 resulting vertex maps normalize the order-three action. Their
orbits are classified by the unordered block-weight triple and, when all
weights are nonzero, whether

```text
h = p_01 + p_12 - p_02 mod 3
```

vanishes. If a block has weight zero, the nonzero blocks form a forest and
rotations remove all phases, giving six weight classes. The four nonzero
weight triples each split into `h=0` and `h!=0`, giving eight more classes and
fourteen total.

The clean-room checker in [independent_check.py](independent_check.py) imports
no submitted module. It checks all 512 binary cores literally, reconstructs
all 343 valid cores, all fourteen orbits, all 42 parent-normalized
representatives, and all `343*324=111,132` literal transports. It verifies all
324 maps on the full 43-vertex action and 24 generators for the later blue
cycle and fixed-vertex normalizations; those later maps fix the minority core.
It also reproduces the local fixed-signature facts: class 8 permits all eight
signatures, whereas classes 11 and 13 forbid only `111`.

## Formula and certificate audit

The parent `r=3` formula has already received accepted independent review at
Discovery Net artifact
`bafkreidkjevnpnqbwqiewmrbf7ksnxgtlad3tc54jyqppytjcykr4b36n4`. This review
imports that audited formula rather than relitigating its 615,572 clauses. Its
SHA-256 is
`82f27b524e893d237f7a478c43bc9d49ff559faaa28e260d688d1591bdfaad20`.

I independently reconstructed the moving-pair orbit order and obtained core
variables `1,2,3; 4,5,6; 31,32,33`. Every one of the fourteen cube files is
byte-for-byte the accepted parent formula after its changed DIMACS header,
followed by exactly the nine units specified by the representative. Each has
34,268 variables and 615,581 clauses.

The eleven claims for classes `0,1,2,3,4,5,6,7,9,10,12` were then replayed
serially with drat-trim. All returned `s VERIFIED`; ten proofs exercised RAT
checking. The successful proof traces total 399,325,866 bytes. The remaining
classes `8,11,13` have only explicit `UNKNOWN` solver logs, which are neither
certificates nor evidence of feasibility.

[report.json](report.json) records every representative, formula digest,
successful proof digest and RAT count, along with the independently obtained
cover totals.

## Reproduction

First generate or recover the source proof workspace with one worker:

```sh
python3 ramsey_r55_order3_eleven_minority_core/run.py \
  --work /scratch/r55-k11-core/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --workers 1 --solve-seconds 60 --replay-seconds 300
```

Then run this serial independent checker from the repository root:

```sh
python3 -B ramsey_r55_order3_eleven_minority_core_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_minority_core \
  --parent-formula /scratch/r55-k11-core/full/parent.cnf \
  --proof-work /scratch/r55-k11-core/full \
  --drat-trim /path/to/drat-trim \
  --work /scratch/r55-k11-core/reviewer-replay \
  --report /scratch/r55-k11-core/reviewer-report.json
cmp ramsey_r55_order3_eleven_minority_core_review1/report.json \
  /scratch/r55-k11-core/reviewer-report.json
cd ramsey_r55_order3_eleven_minority_core_review1
sha256sum -c SHA256SUMS
```

The review used drat-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The solver is needed only to regenerate traces; the review replay does not
trust its verdict.

## Trust boundary

The direct parent reduction imports `R(4,5)=25`; this review imports the
previously accepted parent-formula review and rechecks every new core,
normalizer, cube unit, and DRAT proof. Remaining trust lies in the ordinary
unformalized relabeling argument, CPython/runtime/hardware, SHA-256, and the
external drat-trim checker. Large formulas and proofs remain outside Git in
the read-only source workspace `/scratch/team-r55-1-order3-k11-r3/full`;
compact hashes alone are not refutations. Reviewer logs and reports occupy
about 112 KiB under
`/scratch/research-team-v2/tmp/reviewer-1/r55_k11_minority_core_review1`.
No reviewer-owned proof process remains active. This is not a proof-assistant
formalization or external peer-review verdict.
