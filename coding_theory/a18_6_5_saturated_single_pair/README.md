# Two degree-20 points whose pair occurs once

Agent: **six-code-3**. Role: **researcher**. Date: 2026-09-30.

For a family `F` of five-subsets of an eighteen-point set, suppose distinct
words intersect in at most two points. Write `d_x` for the number of words
through a point and `lambda_xy` for the number through a pair.

**Exact computer-assisted theorem.** If distinct points `x,y` satisfy
`d_x=d_y=20` and `lambda_xy=1`, then `|F|<=56`. This maximum is attained.
There are unique further deficient neighbors `a` of `x` and `b` of `y`,
with `lambda_xa=lambda_yb=4`. More precisely, the maxima are **56 when
`a=b`** and **53 when `a!=b`**.

Combined with the
[absent-pair maximum 56](https://github.com/helgithorskarp/math_results/tree/main/coding_theory/a18_6_5_saturated_absent_pair),
any such packing of at least 57 words has `lambda_xy>=2` for every pair
of degree-20 points. Brouwer's established point-degree bound then implies
that every pair in a hypothetical **72-word** code occurs between two
and five times. Codes of size 70 or 71 have at least eight or thirteen
degree-20 points, respectively, and all pairs among them occur at least twice.

**Further corollary.** If `d_x=20`, `d_y=19` and `lambda_xy=0`, then
`|F|<=59`. Thus in any packing of at least 60 words, a degree-20 point
has no absent pair with a degree-19 point. This uses the just-proved
single-pair theorem to handle a completed line that fails to be an arc.

These are necessary conditions. The unrestricted interval remains
**69 <= A(18,6,5) <= 72**, as in the
[maintained table](https://aeb.win.tue.nl/codes/Andw.html), checked on
2026-09-30. The finite result does not resolve the global packing problem.

The complete reduction, symmetry coverage, exact search argument and
trust boundaries are in [PROOF.md](PROOF.md).

## Reproduce

Python standard library only. Checked with CPython **3.11.2**; the complete
generator also agrees entry by entry under CPython **3.12.14**, with `-O`.
All arithmetic and all comparisons are exact. No solver, floating point,
random sampling or external input file is used.

From this directory, run sequentially:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B audit.py
python3 -B generate.py --check expected.json
python3 -B verify.py
```

To regenerate both compact fixtures:

```bash
python3 -B generate.py --output replay.json --witness replay-witness.json
python3 -B verify.py --manifest replay.json --witness replay-witness.json
```

The deterministic `expected.json` SHA-256 is

```text
b6333aba3ac7c3370f0cfe12d566ac7ec3deed3b37a6e86528acdbf7cbe6efaf
```

Its 40,576 bytes record the full selected plane list, residual word lists,
attaining cliques and complete carrier-orbit coverage. It is a replay
manifest, not a standalone proof certificate: the exact algorithms must
finish and the mathematical reduction must be accepted. The classification
covers arbitrary relabelings; the 29 selected labelled planes are not asserted
to be inequivalent plane-pair isomorphism classes.

## Complete coverage

The two shortened stars merge to affine planes on the same sixteen old
points, with exactly one exceptional cross-line pair. A checked flag
stabilizer reduces the second split point to either the first split point
(`b=0`) or an outside point (`b=4`). The parallel class containing the
exceptional line is covered by the following complete enumeration.

| Second split point | Valid first classes | Class-orbit representatives | Selected second planes | Largest residual code | Largest full code |
|---|---:|---:|---:|---:|---:|
| `b=0` (`a=b`) | 600 | 14 | 3 | 17 | 56 |
| `b=4` (`a!=b`) | 537 | 92 | 26 | 14 | 53 |

The first plane has 840 four-arcs and 378 first-star-compatible five-words.
The generator exhausts **79,643** transverse second parallel classes across
the **106** representatives. It maps both normalized order-four grid planes
into every grid, checks that each accepted plane has all four required
completion occurrences, and directly validates every 39-word star union.
Residual maxima use complete inclusion/deletion clique recursion.

The checker imports no generator or geometry code. It generates a symmetry
closure from nine permutations, verifies all carrier orbits using point sets,
and completes each plane by enumerating all four-cliques of mutually
orthogonal transverse classes. It compares actual planes and actual residual
word sets entry by entry. Its complete residual scan uses all 4,368 old
five-subsets and its independent optimum calculation enumerates maximal
cliques by Bron--Kerbosch recursion. An explicit 56-word fixture is checked
directly; every manifest case also carries an attaining residual clique.

## Measurements and checks

One process, one CPU-intensive job at a time, single thread, below a 2 GiB
process limit:

| Job | CPython | Seconds | Maximum RSS |
|---|---|---:|---:|
| Complete generator | 3.11.2 | 13.9771 | 18,780 KiB |
| Separate complete checker | 3.11.2 | 55.9249 | 22,144 KiB |
| Engine and input audits | 3.11.2 | 0.6533 | not separately measured |

The audits exhaust all 1,100 simple graphs on at most five vertices under
two labelings, check 15,210 fixed-size clique queries, and compare 39,346
orthogonality tests for smaller parallel classes with direct intersections.
They also check all 35 four-block partitions of eight points, empty and
infeasible exact covers, four capped-search failures, and eleven malformed
inputs, including incomplete and overlapping carrier-orbit lists.
The degree-19 completion audit checks the complete reduced leave domain,
all 29 nonarc star-swap fixtures, all 20 missing-line additions in a fixed
orthogoval plane pair, and the complete small domain of removed-word
intersections with a four-point line.

Search caps raise an `INCOMPLETE` exception and produce no theorem verdict.
Optional `--progress PATH` outputs are explicitly incomplete checkpoints;
they are not published evidence. No cap was reached in the complete runs.
The checker used 101,054 maximal-clique recursion nodes in total. Independence
here means different algorithm and representation by the same researcher;
no independent peer review or proof-assistant formalization is claimed.

## Sources and provenance

Brouwer's
[1975 report, A(17,6,4)=20](https://ir.cwi.nl/pub/6883/6883D.pdf)
is imported only for the corollaries converting a code's size to degree-20
points. The restricted maxima 56 and 53 do not need that external theorem.
The classical lower bound 69 is from Aw--Chee--Ling,
[Six New Constant Weight Binary Codes](https://ymchee66.github.io/home/PDF/6cwc.pdf)
(2003); its Appendix A witness was exactly reproduced earlier in this campaign.

Order-four affine planes and orthogoval plane pairs are historical objects;
see Colbourn--Ingalls--Jedwab--Saaltink--Smith--Stevens,
[Sets of mutually orthogoval projective and affine planes](https://www.sfu.ca/~jed/Papers/Colbourn%20et%20al.%20Orthogoval.%202024.pdf)
(2024). The present enumeration permits one specified exceptional line pair,
so it does not assert a new existence theorem for orthogoval planes.
Targeted literature and committed-graph searches found no identical restricted
claim; this is not a priority guarantee.

The independent `(1,4)` split argument below is also a special case of
six-code-1's
[affine split lemma](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/AFFINE_SPLIT.md).
The earlier absent-pair theorem was independently confirmed by six-reviewer-1's
[review and equality classification](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_absent_pair_review1/REVIEW.md).
That review suggested the degree-19 completion frontier. Its completion
observation is used in the additional corollary proved here; the review
does not evaluate this new single-pair theorem or the bound 59.
`geometry.py` and the basic independent checker/audit helpers extend this
researcher's prior absent-pair implementation in the same repository. This
directory is self-contained and needs no other campaign directory at runtime.
