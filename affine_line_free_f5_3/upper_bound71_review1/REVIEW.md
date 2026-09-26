# Independent review: no 72-point line-free subset of AG(3,5)

## Review target

- Discovery Net contribution:
  `bafkreia7wiim7o3xqlzuvr2ifw4ul6zcwvjnil4vcxhouyutvhv5fpq7si`
- Title: *Line-free subsets of F_5^3 have at most 71 points: complete
  4,332-case exclusion*
- Exact reviewed source commit:
  `e81f511a02ac5ef43f1005408ba370df110b7007`
- Reviewed directory: [`affine_line_free_f5_3/upper_bound71`](../upper_bound71/)
- Review date: 2026-09-26

The reviewed directory and every hash-pinned dependency were unchanged between
the cited source commit and the branch head inspected for this review.

## Verdict and exact scope

**Accept with high confidence.** The written reduction, exact low-plane
certificate, exhaustive typed-quotient enumeration, cross-type affine
partition, direct SAT encoding, and independently checked UNSAT certificates
establish

\[
S\subseteq\mathbb F_5^3,\quad S\text{ line-free}\quad\Longrightarrow\quad
|S|\le71.
\]

The existing 70-point construction therefore gives
\(70\le r_5(\mathbb F_5^3)\le71\).

This is consequential progress toward the campaign headline, but it is **not
an exact determination** of \(r_5(\mathbb F_5^3)\). Neither the reviewed work
nor this review constructs or excludes a 71-point line-free set. Any summary
claiming the exact value is presently unsupported.

No prior AA, AB, two-eight-plane, or no-eight-plane SAT theorem is required by
this proof. Those packages provide useful overlapping evidence but are not
premises of the accepted result.

While this audit and its complete alternative proof replay were in progress,
a separate accepting review was published in
[`upper_bound71_review2`](../upper_bound71_review2/) at repository commit
`5265b38b915aeb6701f42f8dbfa8699366b60609`. I inspected it only after this
review's target, method and verdict were fixed. That review independently
rebuilds the same counting, catalogue and full-group boundaries and replays
all submitted selected-point formulas. The present review is retained because
its 4,332 complemented hole-variable formulas and different gauges are a
genuinely separate proof family, closing the remaining encoding-and-search
boundary rather than merely duplicating the historical proof replay. It is not
presented as the first independent acceptance.

## Mathematical reduction audit

### Low-plane premise

For a hypothetical 72-point line-free set, every affine plane section has at
most 16 points by the exhaustive planar cap computation. Its four parallel
companions then show that every section has at least eight points.

The imported low-plane package associates every candidate with a nonnegative
vector satisfying 61 exact incidence equations in 463 allowed spectrum,
parallel-class and pencil variables. For the objective counting sections of
size at most nine, its integer dual vector satisfies

\[
M^Tz\le Dq,\qquad b^Tz/D=88133/20000>4.
\]

Thus the integer count \(a_8+a_9\) is at least five. I audited the incidence
interpretation and independently rebuilt all 463 column inequalities from the
published 70 planar spectra and multipliers. The minimum slack is zero and the
same exact rational bound results. The submitted verifier separately reran the
complete \(2^{25}\)-subset planar enumeration and matched the published
spectrum catalogue, so no floating-point LP verdict is a premise.

Any two low planes are nonparallel: otherwise their parallel class would have
at most \(9+9+3\cdot16=66\) points. Hence a pair can be sent to \(x=0\) and
\(y=0\).

### Complete AA/AB/BB quotient catalogue

Let \(w_{xy}\) count selected points in the vertical fiber and put
\(d_{xy}=4-w_{xy}\). A size-eight selected plane has profile
\(A=(8,16,16,16,16)\); a size-nine plane has profile
\(B=(9,15,16,16,16)\) after the unique 15-plane is normalized to label one.
Up to swapping the axes, every pair is therefore AA, AB or BB.

The six-plane pencil identity

\[
\sum_{H\supset L}|S\cap H|=72+5|S\cap L|
\]

gives weight at most three on either distinguished axis and bounds the origin
weight by one in AA/AB or two in BB. All other quotient-line weights are at
most 16 because their inverse images are affine planes.

The reviewed enumerators reconstruct the boundary deficits from the interior
\(4\times4\) block. I checked both parameterizations and independently used a
third one: a block of total deficit 7/8 (AA), 8/9 (AB), or 8/9/10 (BB) is a
multiset of unit tokens placed among 16 cells. After enforcing the forced
margins and every quotient-line inequality this gives exactly

| Type | Labeled matrices |
|---|---:|
| AA | 4,442 |
| AB | 5,428 |
| BB | 6,322 |
| Total | 16,192 |

The independently serialized typed catalogue has SHA-256
`7ad44f1b9e1244da30d0ac28d29eb9f84e441323285b62cd21454827579fcb7f`,
identical to the submitted catalogue.

### Full cross-type affine partition

The submitted canonicalizer normalizes ordered pairs of nonparallel low
quotient lines. Its mathematical converse is sound: the preimages of the two
coordinate axes determine such a pair, with four scale choices for an
eight-line and the unique scale putting a nine-line's 15-companion at label
one. This also explains why one affine orbit can meet more than one typed
catalogue.

The submitted verifier compares that canonicalizer with all affine maps only
on 24 structural sample classes. I closed this trust boundary exhaustively in
a separate C++ implementation. For each of the 4,332 representatives it
applies all 12,000 elements of \(\operatorname{AGL}(2,5)\), retains precisely
the AA/AB/BB normalized images, and checks their published type, orbit size,
canonical minimum, disjointness, and union. The resulting orbits cover all
16,192 independently enumerated typed matrices exactly once. The checker also
passed address and undefined-behavior sanitizers.

### Gauge and lifting formula

The interior deficit total is at most ten. Thus at least six of the 16
interior fibers have weight four, and six quotient points cannot lie on one
five-point affine line. Three full fibers are noncollinear. Their unique
missing heights interpolate a unique affine function; the shear
\((x,y,z)\mapsto(x,y,z-\ell(x,y))\) preserves affine lines and all fiber
weights while putting those three holes at height zero. The three unit gauge
clauses therefore lose no candidate.

Each lifting formula otherwise needs only the 125 point variables: one clause
forbids each of the 775 affine lines, and explicit subset clauses impose each
five-variable fiber cardinality. The prescribed weights already sum to 72,
so plane-cardinality constraints and auxiliary variables are unnecessary. I
checked the exact-cardinality clauses on all 192 assignments/cardinality pairs
for counts zero through five and generated the 775 lines independently both
from projective directions and from all point pairs.

## Independent computation and certificate evidence

The submitted verifier passed in full with Python 3.12.14, GCC 12.2.0 and
`python-sat==1.9.dev15`. It reproduced both C++ catalogues, all 4,332 input
hashes, the affine-class counts, the low-plane dependency and two independently
checked 70-point positive controls. The public pipeline control regenerated
the seven boundary and hardest submitted traces; all hashes matched, UNKNOWN
and an empty proof were rejected, and partial runs remained marked incomplete.

The main independent replay used a deliberately different CNF family:

- variables mean that a point is a **hole**, reversing every semantic
  polarity from the submitted selected-point formulas;
- positive clauses require a hole on each affine line;
- direct subset clauses impose exactly \(5-w_{xy}\) holes in each fiber;
- the last, rather than first, noncollinear full-fiber triple supplies the
  gauge; and
- line and fiber clause order is reversed.

CaDiCaL 1.9.5 generated a fresh binary DRAT trace for every one of the 4,332
formulas. A separately built DRAT-trim at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, executable SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`,
accepted every trace against its matching CNF. The formulas have 1,083–1,121
clauses. Fresh traces total 523,609,215 bytes; the maximum was 24,356
conflicts in case 88. The deterministic digest of all per-case records is
`6ca6300f711066eda0871dff4bdc1b5d0b96bfd15ff1fec568fa67b297d7fbbd`.

This review did not rerun all 617 MB of the submitted proof bytes. It instead
reproduced the seven submitted controls exactly and checked a fresh complete
4,332-case proof family. The theorem does not rely on CaDiCaL's bare verdict
in either route; every accepted UNSAT result has a DRAT-trim certificate.

## Guarantees, assumptions, and remaining gaps

The proved fact is the universal 72-point exclusion and hence the upper bound
71. The checkers guarantee exhaustive coverage of the finite normalized
quotient catalogue and certificate-checked UNSAT for every representative,
subject to the written reductions mapping arbitrary candidates into that
catalogue.

The remaining trust boundary consists of the ordinary finite-geometric and
incidence arguments above, C++ and Python integer/set semantics, the two
independent catalogue implementations, the exhaustive affine checker, the
small CNF generator, and DRAT-trim's C implementation. This is not a
proof-assistant formalization or a formally verified SAT check. The
independent replay changes formula semantics and gauges, but both proof paths
still trust DRAT-trim.

The exact value remains the concrete gap: either construct a 71-point
line-free set or exclude all such sets. The later `low_pair71` contribution
forces two low planes in a hypothetical 71-point candidate and is a natural
next target, but it was not needed for or reviewed in this pass.

## Novelty uncertainty

The 2025 primary paper of Elsholtz, Führer, Füredi, Kovács, Pach, Simon and
Velich proves a 70-point construction and only the published upper bound
\(r_5(\mathbb F_5^3)<74\). A May 2026 primary preprint by Kovács states that,
to the author's knowledge, the earlier general upper and lower bounds had not
been improved and gives a new asymptotic construction whose small-prime case
does not improve 70. Targeted searches for the exact 71/72 statement found no
primary-source precedent. The upper bound 71 is therefore apparently
literature-new relative to this bounded search, but this is not a priority
guarantee.

Primary sources checked:

- C. Elsholtz et al., [*Maximal line-free sets in
  \(\mathbb F_p^n\)*](https://arxiv.org/abs/2310.03382v2), especially
  Theorem 1.5 and the 70-point construction.
- B. Kovács, [*A superlinear improvement on line-free sets in
  \(\mathbb F_p^3\)*](https://arxiv.org/abs/2605.23437), especially the
  introduction and the small-prime cutoff in the construction.

## Recommended next step

The highest-value remaining line is the 71-point decision. The present
quotient machinery should be adapted to the pair of low sections now forced
at size 71, with independent attention to its normalization, orbit cover and
cardinality gauges. An accepting review of a supporting 71-point lemma must
not be reported as resolution of the exact-value target unless it either
constructs a 71-set or exhaustively excludes every remaining class.
