# Review of the four-set lemma and rank-five global sieve

## Verdict

**Accepted with high confidence, at the scope actually claimed.** I found no
mathematical, counting, or reproducibility defect in the target contribution
at commit `6ef98a6c00632951be13c661898437576fc6615b`.

The accepted mathematical result is a universal four-set distinguisher lemma
and its exact counting consequence for a selected rank-five cross-matrix
branch. It is an intermediate reduction, not a 43-vertex Ramsey graph, a
nonexistence proof for all good43 graphs, or an improvement of `R(5,5)`.

## Independent proof audit

Write a good43 for a two-coloring of `K_43` without a monochromatic `K_5`.
The imported bound `R(4,5) <= 25` gives color degrees in `[18,24]`. The
elementary bounds `R(3,5) <= 14` and `R(4,4) <= 18` give an own-color
common-neighbor cap of 13 for an edge and 4 for a monochromatic triangle.

For a monochromatic triple with `D` distinguishers and `a` common
own-color neighbors, the incidence inequality

```text
54 <= 6 + 3a + 2D <= 18 + 2D
```

gives `D >= 18`. For a mixed triple whose red edges are `01,02`, the eight
contact signatures satisfy

```text
x0*x1 + x0*x2 + (1-x1)*(1-x2) = 1_uniform + x0.
```

Summing yields `C01+C02+C12 = 38-D+d_red(0) <= 39`, hence `D >= 17`.
Equality forces `D=17`, the majority-color center to have degree 18 in that
color, and all three relevant common-neighbor counts to equal 13.

If a four-set `Q` had at most 16 outside distinguishers, all four triples in
`Q` would attain that equality. Exactly 16 outside vertices would distinguish
every triple, so their four-contact signatures would all have weight two and
would contribute 32 red incidences. The other 23 vertices would be uniform;
if `t` are uniformly red, the edge common-neighbor bounds force `10 <= t <=
13`. Each vertex of `Q` has internal red degree one or two. If `a` vertices
have degree one, then `a` is in `{0,2,4}`, and equality gives total red degree
`72+6a`. Counting incidences another way gives

```text
72+6a = (8-a) + 32 + 4t,
4t = 32+7a.
```

The three possible values of `a` force `t=8, 23/2, 15`, respectively, all
impossible. Thus every four-set has at least 17 outside distinguishers. Four
identical rows on the 20-side could be distinguished only by the other 16
same-side vertices, so their multiplicity is at most three.

I independently enumerated all 64 labeled colorings of `K_4`, all 16
four-contact signatures, all 20,349 distributions of 16 distinguishers among
the six weight-two signatures, and `t=10,11,12,13` for each of the 18
nonmonochromatic `K_4` colorings. All 1,465,128 degree-feasibility cases give
the same contradiction. This computation is an audit of, not a substitute
for, the incidence proof.

## Independent exact-count audit

For the fixed 20+23 cut, the target counts all red cross matrices `M` of rank
five for which `M+J` has rank at least five. Both factor matrices span
`F_2^5`, and every matrix has exactly

```text
|GL(5,2)| = 9,999,360
```

factor pairs. The zero-pair exclusion and zero/nonzero row and column
multiplicity caps are invariant under this change of basis.

My checker does not import the target implementation. It generates every
concrete linear subspace of `F_2^5` (374) and every affine subspace of a
fixed 16-point affine hyperplane (307). It computes capped word counts as
exact exponential-generating-function coefficients and recovers exact spans
by recursively subtracting proper concrete subspaces. This differs from both
the target's Gaussian-coefficient Möbius formulas and its label-insertion
positive dynamic program. All 212 spanning-word entries and every raw,
complement-rank-four, and remaining count at all six stages agree.

The rank-four complement overlap was recomputed at every cap stage. The final
values are

```text
baseline  = 5265776463769286448156565145344760253473964876758764876800
removed   = 2066365377174402749659084812993090655368806390234845516800
remaining = 3199411086594883698497480332351669598105158486523919360000
```

The removed fraction reduces exactly to

```text
72250993667250533318774539803589602314409997
------------------------------------------------
184119220220965173622650664548131290651799397
```

or `39.241418457313%`. Relative to the branch remaining after the older caps,
the new row cap alone removes
`319639601769240155564925006980617339728513107340597120000`, or
`9.083120138796%`. These percentages have different denominators and are not
combined.

The audit also reconstructs all 903 bits of the target's physical fixture
from factor labels plus 443 internal bits. It verifies red cross rank five,
blue cross rank six, satisfaction of every earlier predicate, failure first
at row multiplicity four, and all ten red edges of the certificate on
vertices `[0,4,11,29,30]`.

## Reproducibility and trust boundaries

Normal and assertion-disabled CPython both match `EXPECTED.json`. The target
manifest independently verifies 16 entries covering the other 16 files in
the 17-file, 63,311-byte package. The reviewer checker uses exact integers and
rationals, one process, the Python standard library, and no solver or network.

The proof still imports the historical result `R(4,5)=25`; that computation
was not independently rerun. The earlier zero-class and multiplicity
predicates are restated in the target and their short arguments were checked,
but their antecedent review artifacts were not treated as new objects of this
review. Ordinary CPython execution, SHA-256, and the supplied fixture bytes
remain computational trust boundaries. The theorem is not proof-assistant
formalized.

Finally, the 39.2414% denominator is the explicitly defined rank-five,
blue-rank-at-least-five family for one fixed partition with arbitrary internal
edges. It is not the set of good43 graphs, not a union over partitions, and
not an isomorphism count. A good43 need not lie in this branch, and the
positive remaining count does not assert that any survivor is good.
