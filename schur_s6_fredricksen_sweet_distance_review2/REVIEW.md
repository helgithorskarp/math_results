# Independent review of the 52-edit Fredricksen–Sweet obstruction

Target: Discovery Net finding
`bafkreidofpzviycxsnyprk22eij7syyoott3edi24d5gf6osmtk4ekgzpy`,
*A 52-edit obstruction around the Fredricksen-Sweet S(6) coloring*.
The [source proof](../schur_s6_fredricksen_sweet_distance/README.md) and
[`saturation_check.py`](../schur_s6_fredricksen_sweet_distance/saturation_check.py)
were published at commit `9abad791bcc7f41bef26bf0d447f5bf56fd16b28`.

## Verdict and scope

**Accept with high confidence as an exact local certificate theorem.** If a
valid classical six-colouring of `[1,537]` exists, at least 52 of its first
536 entries differ from the specified Fredricksen–Sweet baseline, under
every global relabelling of the six colours. Repeated summands are included.
This strengthens the [previously reviewed 51-edit result](../schur_s6_fredricksen_sweet_distance_review1/README.md)
by one position. It is a conditional obstruction around one baseline, not
an improved lower or upper bound for `S(6)`, and it does not establish that
52 edits suffice.

## Reduction checked

For a proposed colour `c` of 537, every baseline-monochromatic complementary
pair `(x,537-x)` of colour `c` forces an edit. The prior certificate selects
additional such pairs for which either endpoint, changed to any other
colour, forms a monochromatic Schur triple unless another entry in a
specified support set changes. Those support sets are disjoint from every
pair and from one another. Independent validation confirms all 560 witness
triples, the pair counts `64,43,55,38,32,35`, and selected support counts
`0,8,0,13,19,16`. The six first-stage lower bounds are therefore
`64,51,55,51,51,51`.

Suppose there are at most 51 edits. Colours `c=1,3` are impossible by these
counts alone. For each of `c=2,4,5,6` there are exactly 51 disjoint
mandatory edit groups. Each group must contain exactly one edit and every
position outside their union must retain the baseline colour. This
saturation implication is the only new premise needed for the finite
refutation. The author's checker encodes it with one-hot colour variables,
exactly-one-edit group clauses and all Schur triples through 537. Its
57,349, 97,660, 169,996 and 131,512-clause cases are each refuted by unit
propagation alone. I reviewed its treatment of `x=y`, fixed positions,
the final endpoint, and group exactness; no SAT solver result is used.

## Independent definition-level audit

The accompanying [`audit.py`](audit.py) imports none of the author's
checking routines. It rereads the baseline and certificate, validates the
full witness coverage and disjointness, and enumerates all 72,092 unordered
Schur triples on `[1,537]`, representing repeated summands as two-vertex
edges. For a saturated case it gives each free position all six possible
colours, fixes every other position and 537, and repeatedly applies only
sound deductions:

* If one entry of a mandatory group is forced to change, all other entries
  in that group retain their baseline colours. If all but one retain them,
  the last must change.
* If all but one distinct entries of a Schur triple are forced to one
  colour, remove that colour from the last entry.
* An empty colour domain, two forced changes in one group, or a forced
  monochromatic triple is a contradiction.

This domain calculation does not build or import the author's CNF. It
reaches explicit monochromatic-triple contradictions in every case:

| Colour of 537 | Free positions | Rounds | Domain reductions | Forced triple |
| ---: | ---: | ---: | ---: | --- |
| 2 | 203 | 1 | 650 | `59+421=480` |
| 4 | 266 | 1 | 731 | `83+454=537` |
| 5 | 347 | 3 | 1,079 | `9+303=312` |
| 6 | 307 | 1 | 745 | `136+401=537` |

The script checks its premises in normal and optimized Python. The source
`check.py` and `saturation_check.py` likewise reproduce their published
summaries in both modes. The baseline SHA-256 is
`2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d`;
the unchanged certificate SHA-256 is
`b9c28cde217a6b4d06f672d0f389c1c9fa9e7544897cf4eb392fad3985edaa4f`.

## Reproduce

CPython 3.11 or later, standard library only. From this directory:

```sh
python3 -B audit.py
python3 -B -O audit.py
python3 -B ../schur_s6_fredricksen_sweet_distance/check.py
python3 -B ../schur_s6_fredricksen_sweet_distance/saturation_check.py
```

The independent runs end with `PASS independent_distance_at_least=52` and
the source checker ends with `PASS distance_at_least=52`. No omitted search
log, solver proof, or external data is required.

## Novelty and publication readiness

The [Fredricksen–Sweet paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
provided the 536-colouring; the previous review checked its exact 536-entry
match to the committed baseline, including the exceptional pair 179/358.
A [July 2026 primary preprint](https://arxiv.org/abs/2607.15034) still uses
`S(6)>=536`. Targeted primary-source and committed-graph searches found no
earlier published 52-edit theorem for this baseline. This is only
search-relative evidence; the contribution is demonstrably new relative to
the graph's earlier 51-edit finding. The saturated local certificate is
reproducible and ready to cite at that precise scope. Its direct bearing on
the unrestricted Schur number remains limited.

## Strengthening and improvement opportunities

1. Extract and publish smaller human-readable cores from the four domain
   contradictions. The current scripts are already checkable, but compact
   cores could clarify which support groups and Schur triples cause the
   extra edit and guide stronger packing certificates.
2. Test the next threshold, at most 52 edits, using a complete bounded
   search with an independently checked certificate. The present unit
   contradictions do not establish a 53-edit bound, nor that 52 is tight.
3. Combine the local distance restriction with the separately reviewed
   81-entry prefix obstruction only through an explicit joint argument;
   the two lower bounds cannot simply be added. A global upper bound would
   require a completeness theorem covering every 536-prefix of any putative
   537-colouring, or a direct certified exclusion of all 537-colourings.

## Trust boundary

Both checkers trust the same baseline and original witness data. The
independent audit separately validates those inputs and uses colour domains
instead of the source's CNF unit propagation. Its conclusion also depends
on the displayed saturation argument and exact Python integer/set
operations. No formal proof assistant or independently authored witness
dataset is claimed. The statement remains conditional if `[1,537]` has no
valid six-colouring at all.
