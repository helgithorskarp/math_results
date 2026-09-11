# Line-free sets in F_5^3 have at most 72 points

**Theorem: 70 <= r_5(F_5^3) <= 72.** Here r_5(F_5^3) is the largest
cardinality of a subset of the 125 affine points containing no complete
five-point affine line, in any direction. Equivalently, a set meeting every
affine line in AG(3,5) has at least 53 points.

The [complete upper-bound proof](upper_bound72.md) excludes every 73-point
candidate. It combines incidence counting with published classifications of
strong (3 mod 5)-arcs and a support theorem for strong (2 mod 5)-arcs. No
solver verdict or symmetry restriction is a premise. The exact value and
existence at 71 or 72 remain unresolved in this work.

The prior published interval was 70–73, from Elsholtz et al. (2025). The
70-point construction is theirs; it is reproduced here only as a control.
The improvement to 72 is the result established by this contribution. The
searched primary literature contained no earlier statement of this bound;
this is not an assertion of exhaustive priority verification.

## Mathematical route

The [first-pass reduction](proof.md) bounds the dual cardinality by 173 and
leaves full-plane support, lifted duals, or the unique exceptional dual of
size 128. It also provides four globally exhaustive coordinate cases.

The new argument closes the complete dual cover:

* The exceptional 128 dual would require seventeen 9-point planes. Each
  of its forty possible marked points permits only six corresponding lines.
* Every lifted case is excluded by exact spectrum and incidence equations,
  or already has full-plane support.
* Full-plane support forces a sparse direction. Adjoining its point at
  infinity gives a strong (2 mod 5) dual. Its supported plane forces a new
  affine point, creating a 74-point line-free set and contradicting the
  published upper bound 73.

The proof explicitly includes the lifted and full-support alternatives.
Every use of a classification or extension result states its hypotheses.

## Reproduce

Requires Python 3.10+ and a C++20 compiler. No third-party Python package,
solver, downloaded catalogue or network connection is required for replay.
From this directory:

```sh
python3 verify_upper72.py --out build/upper72
```

Expected output is [upper72_expected.json](upper72_expected.json), beginning
`FINITE_CHECKS_FOR_UPPER_BOUND_72_PASSED`. The complete replay took about
2.3 seconds with Python 3.11.2 and GCC 12.2 on the research host.

The replay checks:

* every one of the 5,200,300 labelled planar 12-subsets for the three-points-
  per-line bound, and every one of the 1,081,575 planar 17-subsets for
  line-freeness; both survivor counts are zero;
* affine incidences and the known 70-point witness;
* all 156 projective points, 806 lines, 156 planes and every pencil identity,
  comparing lines generated from point spans with plane intersections;
* the exceptional 128 arc from its published matrix, including all forty
  marked multiplicity-one points individually;
* every relevant lifted spectrum and all displayed integer obstructions.

The imported classification and support theorem are **external mathematical
premises**. The replay does not re-prove them or formally verify the written
bridges. This is an exact computer-supported proof using published theorems,
not a proof-assistant formalization. No independently checked SAT exclusion
is claimed or needed.

## Primary sources and inputs

1. C. Elsholtz, J. Führer, E. Füredi, B. Kovács, P. P. Pach, D. G. Simon,
   and N. Velich, *Maximal line-free sets in F_p^n*, Periodica Mathematica
   Hungarica 90 (2025), 7–21,
   [DOI](https://doi.org/10.1007/s10998-024-00617-x),
   [arXiv:2310.03382v2](https://arxiv.org/abs/2310.03382v2).
   Theorem 1.5 supplies r_5(F_5^3)<=73; Figure 4 supplies `known70.json`.
2. S. Kurz, I. Landjev and A. Rousseva, *Classification of (3 mod 5) arcs in
   PG(3,5)*, Advances in Mathematics of Communications 17 (2023), 172–206,
   [DOI](https://doi.org/10.3934/amc.2021066),
   [arXiv:2108.04871v2](https://arxiv.org/abs/2108.04871v2).
   Theorem 5.2 supplies the low-cardinality exceptional classification;
   Tables 4–7 supply the planar spectra; Theorem 3.9 supplies full-plane
   support for strong (2 mod 5)-arcs. Numbering refers to that arXiv version.

`exceptional128.json` contains the displayed 4-by-128 matrix, and
`lifted_catalogue.json` records precisely the table entries used. The
checker verifies that the matrix itself defines a nonlifted strong arc
without full-plane support, so the cited uniqueness theorem applies.
The small explicit inputs are included in the repository. Source and
compact-output hashes are recorded in `manifest.json`.

## Preserved earlier formulation

`proof.md`, `generate.py`, `check_reduction.py`, `expected_reduction.json`
and `runs.json` preserve the first-pass four-case coordinate reduction.
Its four 300-second Kissat probes returned UNKNOWN; those solver verdicts
remain UNKNOWN. The cases are now excluded by the global mathematical
proof in `upper_bound72.md`.

Reproducing the old CNFs additionally requires `python-sat==1.9.dev15`:

```sh
python3 generate.py --case 0 --out build/case0.cnf
```

Cases 1, 2 and 3 are generated identically; `--many-full` adds the proved
74-full-plane cut. These historical probes are not needed by the upper-bound
proof. Later sparse-fiber probes were stopped when the analytic argument
made them unnecessary. Large instances and incomplete traces remain outside
Git; they supply no proof premise. Both earlier research programs remain
separate from this contribution.

## Structure at 72 points

A subsequent [certified theorem](sparse_directions/README.md) shows that every
possible 72-point line-free set has a four-point line in each of the 31
directions. At least 50 planes have 16 points, and their projective
completions cover every point of PG(3,5) at least twice. The proof excludes the complete sparse-direction
family using exact reconstruction checks and five independently verified
SAT certificates. The numerical bounds remain 70–72.

## Global low-plane reduction at 72

The [low-plane theorem](low_planes72/README.md) proves that every possible
72-point set has at least five planes of size at most nine, with three
independent normals. It reduces the entire 72-point problem to the four
coordinate profiles AAA, AAB, ABB and BBB, where A=(8,16,16,16,16) and
B=(9,15,16,16,16). The optimizer-free replay checks complete planar spectra
and 128 exact rational certificates. These four cases remain open; the
numerical interval is still 70–72.
