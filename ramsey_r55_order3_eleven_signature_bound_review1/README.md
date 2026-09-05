# Independent review: sharp eleven-cycle signature bound

## Verdict

**Accepted, with the stated scope.** The submitted three-triangle lemma is
correct: among vertices uniformly attached to three disjoint red triangles in
a red/blue complete graph without a monochromatic `K5`, at most nine can have
a nonempty red signature. Equality has exactly two copies of each singleton,
one copy of each pair, and no triple signature.

In the order-three, three-versus-eight branch for a hypothetical Ramsey
`(5,5;43)` graph, the resulting SAT consequences exclude inherited core 8.
Together with the previously accepted fourteen-class core review, this leaves
exactly cores 11 and 13:

| class | red words on triangle pairs 01,02,12 | status |
|---:|:---|:---|
| 8 | `100,100,100` | independently refuted |
| 11 | `100,110,110` | open (`UNKNOWN` at 60 seconds) |
| 13 | `110,110,101` | open (`UNKNOWN` at 60 seconds) |

This is an intermediate reduction. It neither constructs a 43-vertex Ramsey
graph nor proves `R(5,5) >= 44`; the four-versus-seven branch is still open.
The reviewed Discovery Net contribution is
`bafkreicth5vr23eisyucxqelhjfggpgqmwvhdbazicbw25ehnisxai63pu`. Its public
source is unchanged from commit
`08fd1eeeb2680bc5ef488cda9104ca04956ec983`.

## Independent derivation

For triangle `Ci`, all uniformly red neighbors are pairwise blue, since a red
edge between two of them completes a red `K5` with `Ci`. Thus each incidence
count `a_i` is at most four and total incidence `I` is at most twelve.

Three vertices of singleton signature `{i}` are pairwise blue and are blue to
the other two red triangles. Those triangles have a blue cross-edge—otherwise
their six vertices form a red clique. That edge and the three singleton
vertices would be a blue `K5`, so every singleton count `x_i` is at most two
and `X=sum x_i <= 6`.

Writing `Y,Z` for the total pair- and triple-signature counts and `N` for the
nonempty count gives

```text
I = X + 2Y + 3Z,
2N = I + X - Z <= 18.
```

Hence `N<=9`. Equality forces `Z=0`, `I=12`, and `X=6`; all individual bounds
saturate. The three equations for the pair incidences then give one copy of
each pair. Similarly, four vertices with signatures `{i}` or `{i,j}` would be
a blue `K4` and are blue to the third triangle, proving
`x_i+y_ij<=3`.

Among the ten fixed vertices, at least one therefore has empty minority
signature. The already reviewed parent normalization sorts their eleven-bit
incidence vectors lexicographically with minority bits first, so vertex 33 has
minority bits `000`. This justifies units `-211,-212,-213`; it does not fix any
edge among fixed vertices.

## Clean-room checks

[independent_check.py](independent_check.py) imports no submitted module. It
uses a stars-and-bars enumeration rather than the submitted recursive
composition generator and obtains:

- 19,448 ten-vertex signature profiles;
- 928 satisfying `a_i<=4` and `x_i<=2`;
- 778 also satisfying every `x_i+y_ij<=3` cut;
- histogram `[1,7,28,81,189,257,226,110,28,1,0]` by nonempty count;
- the unique equality vector `(1,2,2,1,2,1,1,0)` in mask order `0,...,7`.

All 11,628 five-sets in each public 19-vertex fixture were checked directly.
The three graphs have respectively 81, 87, and 90 red edges, no monochromatic
`K5`, the claimed core words, the common fixed-signature list
`0,1,1,2,2,3,4,4,5,6`, and the full order-three symmetry.

The checker independently reconstructs all 320 primary edge orbits. Each full
formula is byte-for-byte the accepted 615,572-clause parent after the changed
DIMACS header, followed by exactly nine core units, three forced-signature
units, 360 singleton cuts, and 1,260 four-vertex cuts. All 1,536 singleton and
24,576 four-vertex truth-table assignments confirm the clause semantics. The
formula hashes are:

| core | variables | clauses | SHA-256 |
|---:|---:|---:|:---|
| 8 | 34,268 | 617,204 | `057a61e851efe4bc213dbbf17017d3c13716cc0db3b9099c28f397cfdbb301ef` |
| 11 | 34,268 | 617,204 | `edcb237d03e46805495c5151f4589d44543f0450c30564108bbefb7dea2905e1` |
| 13 | 34,268 | 617,204 | `3e795444d8ce43c10c52f20f382b0f981605f47223fc24204a22e8553c132236` |

Finally, drat-trim independently replayed the 49,868,240-byte class-8 proof
with SHA-256
`fb650c6e0f945a9987b21591d2447f59a67625a15136f19995c65e75d67047b4`.
It returned `s VERIFIED` and reported 821 RAT core lemmas. The successful run
is summarized in [report.json](report.json).

## Reproduction

Regenerate or retain the submitted external proof workspace, then run from the
repository root with one checker process:

```sh
python3 -B ramsey_r55_order3_eleven_signature_bound_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_signature_bound \
  --proof-work /scratch/team-r55-1-k11-signatures/full \
  --drat-trim /path/to/drat-trim \
  --work /scratch/r55-k11-signature-review1 \
  --report /scratch/r55-k11-signature-review1/report.json
python3 -c 'import json,sys; assert json.load(open(sys.argv[1])) == json.load(open(sys.argv[2]))' \
  ramsey_r55_order3_eleven_signature_bound_review1/report.json \
  /scratch/r55-k11-signature-review1/report.json
cd ramsey_r55_order3_eleven_signature_bound_review1
sha256sum -c SHA256SUMS
```

The replay used drat-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` and binary SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
Kissat is needed to regenerate the proof, not to check this review.

## Trust boundary

The standalone lemma and equality case are ordinary solver-free mathematics.
The two-core conclusion additionally imports the previously accepted parent
formula and fourteen-class core-cover reviews; in particular it imports the
parent normalization, formula reduction, and external `R(4,5)=25` input. This
review independently checks every newly appended clause and the class-8 trace,
but still trusts CPython/runtime/hardware, SHA-256, and the external drat-trim
implementation. It is not a proof-assistant formalization.

The approximately 25 MB formulas and 50 MB proof remain outside Git in the
read-only source workspace. Hashes alone are not refutations. Compact reviewer
state and the replay log are under
`/scratch/research-team-v2/tmp/reviewer-1/r55_k11_signature_review1_full`;
no reviewer-owned proof process remains active.
