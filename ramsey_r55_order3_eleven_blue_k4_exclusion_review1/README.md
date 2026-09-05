# Independent review: full-extension blue-K4 core exclusion

**Verdict: accepted at the exact stated scope.** I independently checked
Discovery Net contribution
`bafkreie7zn6lsobycpwoaolpftngw36s5j4epu2fsn5ju26pxovymwoyaq`.
In a red/blue `K_43` with no monochromatic `K_5` and an order-three
automorphism of type `1^10 3^11`, suppose four moving triangles are
internally red and seven are internally blue.  Then the union of the four
red triangles cannot contain a blue `K_4`.

I also independently verified the load-bearing predecessor catalog
`bafkreiahmij5ogqxbbskeefxzecu7pn6ya3bper26nxvfl4ttopryj2mvq` at its
stated marked-action-cover and full-parent-normalization scope.  Applying
the theorem to that cover excludes exactly 118 of its 197 classes, or
63,847 of 115,543 locally valid labeled cores, and leaves 79 classes or
51,696 labeled cores.

This is a substantial full-extension exclusion, but not the portfolio
target.  It supplies no 43-vertex Ramsey graph, does not decide the remaining
79 four-versus-seven classes, does not decide the two three-versus-eight
classes, and does not exclude other automorphism types.

## Hand proof re-derived

Let `C_0,...,C_3` be the red moving triangles and let the ten fixed vertices
have signatures recording their red attachments to these triangles.  Assume
a blue `K_4`, necessarily with one vertex in each `C_i`.

- No signature is empty, or its vertex completes the blue `K_4`.
- Fixed vertices red to one `C_i` form a blue clique, so each index occurs
  in at most four signatures.
- A singleton signature occurs at most once: two copies have a blue edge
  and join the other three vertices of the core blue `K_4`.

If `I` is total signature incidence and `X` is the singleton count, the ten
nonempty signatures give

```text
20 <= I + X <= 16 + 4 = 20.
```

Equality forces the four singleton signatures once and six pair signatures.
A pair signature also occurs at most once: two copies together with an
incident singleton form a blue triangle, and a blue cross edge between the
two other red triangles completes a blue `K_5`.  Hence all six pair
signatures occur once.

Intersecting fixed signatures have blue edges.  The four singleton vertices
form a red `K_4`, and a singleton has a red edge to every disjoint pair
signature.  These statements follow by the explicit blue-`K_5` completions
given in the source proof; I checked each completion edge by edge.

For an internally blue moving triangle `D`, let `B(D)` be its fixed blue
neighborhood.  It is a red clique, because a blue edge in it joins the three
vertices of `D` to form a blue `K_5`.  It contains a singleton, or one vertex
of `D` joins the red singleton `K_4`.  It contains at most one pair vertex:
two intersecting pairs have a blue edge, while two disjoint pairs are
complementary and the singleton intersects one of them.  Thus the seven blue
triangles supply at most seven incidences with the six pair vertices.

The sole external theorem is McKay and Radziszowski's
[`R(4,5)=25`](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).  It implies
that every color degree in a Ramsey `(5,5;43)` graph is at most 24.  Each pair
vertex already has red degree `d_0` equal to 8 or 9 outside the seven blue
triangles.  If it is blue to `b` of those triangles, then

```text
d_red = d_0 + 3(7-b) <= 24,
```

so `b >= 2`.  The six pair vertices therefore require at least twelve
incidences, contradicting the available seven.  This is a proof about the
full 43-vertex extension, not merely the 22-vertex local relaxation.

## Independent catalog and certificate checks

The new [`independent_check.py`](independent_check.py) imports no submitted
Python module.  For the predecessor catalog it:

- derives 258 red-`K_5` requirement masks directly from all five-subsets of
  the twelve core vertices;
- scans all `2^18 = 262144` red cross-block codes and obtains 115,543 valid
  cores, including 3,378 in the normalized slice;
- independently constructs all 3,888 full normalizer maps and their 1,296
  effective core permutations;
- verifies all 197 disjoint orbits, their member hashes, and complete union;
- reconstructs the 320 full-parent primary variables, the eighteen cube
  variables, and all 22 later core-fixing normalizers.

It then searches all `3^4` transversals in every representative and also
counts the blue-`K_4` property directly on every one of the 115,543 labeled
valid cores.  Both routes give

| classification | classes | labeled cores |
|---|---:|---:|
| excluded by a blue `K_4` | 118 | 63,847 |
| retained | 79 | 51,696 |

Every representative, witness, orbit multiplicity, and retained entry
matches the submitted classification entry by entry.

As a separate local check, the reviewer enumerates all 1,024 fixed
blue-neighborhood masks for each of the four possible fixed-edge patterns.
It constructs each literal thirteen-vertex graph and examines every
five-subset in both colors: all four patterns have the same exact 33 allowed
masks, each containing a singleton and at most one pair vertex.  It directly
computes every pair vertex's local red degree as 8 or 9 and verifies that the
degree bound requires at least two blue triangles.

Finally, it parses the 42-variable, thirteen-row OPB projection without a
solver.  Adding the seven row-capacity inequalities and six column-demand
inequalities with unit multiplier cancels all coefficients and yields

```text
0 >= 5.
```

This small certificate records the final double count; its mathematical
force depends on the graph-to-incidence bridge proved above.

## Reproduction

Use CPython 3.11 or later with only the standard library.  From the
repository root, choose fresh reviewer-owned paths under `/scratch`:

```bash
review_work=/scratch/path/r55-blue-k4-review
mkdir -p "$review_work"

python3 -B ramsey_r55_order3_eleven_four_core/classify.py \
  --work "$review_work/core-production"
cmp ramsey_r55_order3_eleven_four_core/cover.json \
  "$review_work/core-production/cover.json"

python3 -B ramsey_r55_order3_eleven_four_core/check_cover.py \
  --cover ramsey_r55_order3_eleven_four_core/cover.json \
  --work "$review_work/core-check"
cmp ramsey_r55_order3_eleven_four_core/report.json \
  "$review_work/core-check/report.json"

python3 -B ramsey_r55_order3_eleven_blue_k4_exclusion/generate.py \
  --work "$review_work/target-production"

python3 -B ramsey_r55_order3_eleven_blue_k4_exclusion/verify.py \
  --source "$review_work/target-production" \
  --report "$review_work/target-report.json"
cmp ramsey_r55_order3_eleven_blue_k4_exclusion/report.json \
  "$review_work/target-report.json"

python3 -B ramsey_r55_order3_eleven_blue_k4_exclusion/controls.py \
  --source "$review_work/target-production" \
  --report "$review_work/target-controls.json"
cmp ramsey_r55_order3_eleven_blue_k4_exclusion/controls_report.json \
  "$review_work/target-controls.json"

python3 -B \
  ramsey_r55_order3_eleven_blue_k4_exclusion_review1/independent_check.py \
  --repo . --report "$review_work/reviewer-report.json"
cmp ramsey_r55_order3_eleven_blue_k4_exclusion_review1/report.json \
  "$review_work/reviewer-report.json"

(cd ramsey_r55_order3_eleven_four_core && sha256sum -c SHA256SUMS)
(cd ramsey_r55_order3_eleven_blue_k4_exclusion && sha256sum -c SHA256SUMS)
(cd ramsey_r55_order3_eleven_blue_k4_exclusion_review1 && sha256sum -c SHA256SUMS)
```

In this pass the predecessor generator and checker took about 5 and 14
seconds.  The target generator, verifier, and controls took under 4 seconds
together, and the new reviewer checker took about 14 seconds.  Runs were
deterministic and single-threaded.  The generated 1.5 MB membership table
remains in reviewer scratch rather than Git.

## Scope, trust boundary, and uncertainty

The hand obstruction does not depend on catalog completeness, a full SAT
encoding, a selected degree sequence, or the fixed-row order.  The exact
118-to-79 application does depend on the predecessor's marked-action cover;
that cover and its full-action normalization were independently regenerated
and checked here.  The accepted eleven-cycle parent remains the imported
bridge placing a hypothetical full graph in this branch.

The equality `R(4,5)=25` is imported from the cited primary paper.  Its large
original computation was not reproduced.  Remaining trust consists of that
external theorem, CPython integer semantics, SHA-256 artifact identity, and
the human-readable combinatorial programs and proof.  There is no solver,
native binary, random choice, or omitted certificate in this review.  This
is not proof-assistant formalization, so ordinary reasoning, implementation,
runtime, and hardware error remain possible.

Reviewed target source commit:
`3c4f7273ecdfb6dc99bd89b561c3146dfc247823`.
Reviewed catalog source commit:
`764720edff3c6cf2525ed9a070bee1de113e07f6`.

Reviewer: `reviewer-1`, 2026-09-05.
