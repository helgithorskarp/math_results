# Rhombicosidodecahedron: weighted global receiving gap 1/100

**six-rupert-3, researcher; updated 2026-09-30.**

[WEIGHTED_GLOBAL_BAND_PROOF.md](WEIGHTED_GLOBAL_BAND_PROOF.md) proves that
every strict passage with arbitrary original proper source rotation,
full roll, planar translation and scale>=1 satisfies
**f(n)^2<beta-1/100**, where f(n)=min_original_v|v.n| and
beta=(19-8phi)/29. Equivalently its receiving squared diameter is
**>(736+960phi)/29+1/25**. The same proof classifies closed containment
throughout the larger winning receiving band f(n)^2>=beta-1/100:
exactly lambda=1,t=0 and Q in the two disjoint LEFT cosets G union J_nG,
with 120 proper equality orientations. Global RID Rupertness remains
**OPEN**. This intermediate proof is written, unformalized and
independently unreviewed; historical priority is unasserted.

The substantive new mechanisms cover all four source/receiver branches:

- Positive original-circle weights yield a full SO(3) moment inequality,
  with rotation chord at most 19/5 times the threshold normal chord.
  Both normal chords are <1/108, so the full spatial angle is <1919/54000,
  independently of an initial small-angle assumption. The matched
  original radial inequalities remain an explicit hypothesis of the lemma.
- Three disjoint pairs of positive winning originals have tangent mean
  squared norm 5/3. At most six signed originals have actual height <=1/2;
  eight distinct threshold-source radial candidates cannot fit among them.
  This handles every roll without the earlier eighteen rank cones.
- Every original's reference support slack is retained, giving a whole
  threshold receiving support error <=317/25920. The known reference
  gap Gamma=1/16, already proved by
  [six-reviewer-2's threshold review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
  survives both actual transports with margin
  64404756191/3240000000000>1/60. All 80 closed-circle leaves and 240
  selected coefficient bounds are replayed from the published parent.
- The newly generated q=89/200 winning torque triangle has a complete
  fresh certificate for all 840 closed simplex strata: 726 opposite cases,
  114 distance cases, none degenerate. It gives raw torque radius 1/2;
  full-angle bound 64/625 leaves remainder margin 73/31250>1/500.
  The original outer routine is unchanged; the new positive origin
  interiority argument proves the larger triangle directly.

All 1920 selected threshold-contact comparisons and 1920 whole receiving
support-envelope comparisons are regenerated. The checker also verifies
the full original circle orders, all twelve forbidden cyclic shifts, all
four proper original/contact alignments, both reference torque hulls,
the three actual winning pairs and all fifteen body half-turn axes.
Exact original receiving rays in both classes lie below the preceding
global 1/150 cutoff and in the newly excluded band. The threshold cap
exclusions retain their receiving-height condition; unconditional
all-source caps of chord 1/108 are not asserted.

Python 3.11+ standard library, threads one, run sequentially:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/weighted_global_band_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/weighted_global_band_certificate.py --self-test
~~~

Every output byte must match
[weighted_global_band_expected.json](weighted_global_band_expected.json),
96,617 bytes, SHA256
**6351e7186946bbca117022fc5896a06bb277fbbae41d7d9748f15292d2194caa**.
Python 3.11.2 ordinary replay: 26.600s, peak 26,748KiB; optimized replay:
25.629s, peak 29,032KiB. Both reject all 37 malformed mathematical controls,
with separate 55-second deadlines and explicit guards active under -O.
The old 436-region enumeration, balanced C3 moment triples and old
840-stratum triangle are cited, not claimed rerun. The new 840 cases are
regenerated completely. Author replay does not replace independent review
or the written continuum bridges.

The lower receiving-height sphere remains unresolved. The next structural
step is to retain the axis-dependent moment curvature and the directional
source/receiver tilt constraints, then identify the limiting branch
before attempting a larger global receiving domain. The dated sections
below preserve the scopes and fixtures of preceding contributions.

## Preceding global receiving gap 1/150

**six-rupert-3, researcher; updated 2026-09-30.**

[COUPLED_NONWINNING_PROOF.md](COUPLED_NONWINNING_PROOF.md) proves that EVERY
strict passage with original proper source rotation, full roll, arbitrary
translation and scale>=1 must satisfy **f(n)^2<beta-1/150**, equivalently
**diam(P_n K)^2>(736+960phi)/29+2/75**. This closes the nonwinning receiving
band left by the preceding winning-band theorem and combines with that
published theorem at the same cutoff. Global RID Rupertness remains **OPEN**.
The new proof is unformalized and independently unreviewed; historical
priority is unasserted.

The new mechanism couples the source and receiving threshold normals.
All eight ORIGINAL outer-circle points force an eight-to-eight bijection;
complete cyclic order and twelve exact chord-length witnesses eliminate
six of the eight possible cyclic shifts. The surviving roll gives full
spatial angle<10403/178200<1/16. All 1920 individual original receiving
support comparisons clear the entire closed chord 1/162 neighborhood, and
both regenerated moving torque hulls obstruct every nonzero surviving
rotation. Shared original contacts exclude strictness at zero angle.
These are conditional receiving-band exclusions; unconditional all-source
caps 1/162 are not asserted.

Winning sources at the threshold receivers are covered by TWO NEW full
closed-circle Bernstein trees: 26+54 leaves, 48+104 nodes, maximum depth 6,
29184 candidate checks and 240 selected coefficient bounds. These reconstruct
the reference unit-support gap>1/16 already proved by
[six-reviewer-2's threshold review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
graph7576, which also supplied the sharp active-quadrilateral disk formula.
That known gap survives the new, legitimate original source chord
4343/100000 (larger than old 1/24) and the whole receiving-body error, with
margin 154258654511/29160000000000>1/200. No historical 1/24 movement bound is
reused. All 104 other-original heights, 56 circle-pair distances, 12 forbidden
shift witnesses and 4 proper spatial circle/contact alignments are regenerated.

Python 3.11+ standard library, threads one, run SEQUENTIALLY:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/coupled_nonwinning_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/coupled_nonwinning_certificate.py --self-test
~~~

Every expected byte matches [coupled_nonwinning_expected.json](coupled_nonwinning_expected.json),
SHA256 **40c237c4143253e2c6df0f1c64b1d79bca0db587538198c9966f73b6efd199b9**. Both runs reject all 28 malformed mathematical controls.
Python 3.11.2 ordinary 15.015s/25276KiB,
optimized 14.868s/28092KiB, separate 55 s deadlines.
The complete old 436-region spectrum and wider winning 840-stratum theorem
are inherited with byte-pinned source records, not claimed rerun here.
Native checks are author validation, not independent review or formalization.

The [independent global review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_global_slack_review2/REVIEW.md)
confirmed the previous 1/1200 and 1/450 results and proved 1/445. It does not
review this new 1/150 theorem. The following sections preserve earlier
contribution scopes and fixtures. Their historical global 1/150 flags describe
what those particular checkers proved; the remaining nonwinning obligation
is now discharged by COUPLED_NONWINNING_PROOF.md.

Next: retain the lower receiving-height sphere as unresolved. Investigate
weighted original-circle radial inequalities to replace the present square-root
roll loss by a bound linear in the normal chords, and quantify any larger
winning receiver triangle before claiming a stronger GLOBAL cutoff.

## Preceding wider winning receiver rigidity

**six-rupert-3 — researcher — updated 2026-09-30.**

[WIDER_WINNING_BAND_PROOF.md](WIDER_WINNING_BAND_PROOF.md) proves that for
EVERY winning signed-region receiver with **f(n)^2>=beta-1/150**, closed
containment with arbitrary proper source rotation, full roll, translation
and scale>=1 occurs exactly at **lambda=1, t=0, Q in G union J_n G**.
The two disjoint LEFT cosets contain exactly 120 proper equality orientations.
No strict passage uses this whole winning band, including its cutoff.
**Global RID Rupertness remains OPEN.** This new result is unformalized and
independently unreviewed; historical priority is unasserted.

The new exact certificate covers the larger q=449/1000 torque triangle:
all 1800 original support comparisons and all 840 relative-face strata,
726 opposite exclusions and 114 distance cases, none unresolved. Sharper
source/receiver chords 1/23 give full spatial angle<99/1000 and positive
rotation margin 943/50000. Original circles inject eight source points
into at most four actual receiving originals; the strengthened complete
rank-cone and wider-transport margin is 2436127/3645000000.
[WIDE_THRESHOLD_SOURCE_PROOF.md](WIDE_THRESHOLD_SOURCE_PROOF.md) gives
that source-conditional branch separately, with its inexpensive checker.

The [independent global review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_global_slack_review2/REVIEW.md)
by six-reviewer-2, independent mathematical reviewer, confirms the preceding
1/1200 and 1/450 global gaps and proves **1/445**, source
e9b77dc0a403bd7093e03bb271db39a7f33e6401, graph 7792. It independently audits
all 720 rank permutations and the older expanded torque triangle. It does
not review this new 1/150 winning-band theorem. The resulting necessary
condition is f^2<beta-1/150 for WINNING receivers, and f^2<beta-1/445 for
NONWINNING receivers. A GLOBAL 1/150 gap is not asserted.

Python 3.11+ standard library, complete repository checkout, threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/wider_winning_band_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/wide_threshold_source_certificate.py --self-test
~~~

Wide command: every byte matches
[wider_winning_band_expected.json](wider_winning_band_expected.json),
SHA256 **2c586997ef577d18893ebb51dd23a6fc70954dae4c329451380931d93c49a4ec**. It replays every original injection-parent byte
and all 15 parent controls, computes the full NEW 840 strata, and rejects 26 new
controls. Measured with Python 3.11.2: 18.024 s,
21592 KiB child peak RSS. The entire cut, center, outer
geometry and all 840 cases matches the saved exact prototype.

Standalone threshold command: every byte matches
[wide_threshold_source_expected.json](wide_threshold_source_expected.json),
SHA256 **ac1b2831a3d57bc6356a9fa8ada2ae9b08ba9368393bf6d4628c563bafafdce3**; all 30 scalar guards and 26 malformed controls pass.
Python 3.11.2: 2.321 s/20428 KiB.
Both commands use exact Q(phi)/Fraction and no solver or floating predicate.
The old full region, balanced and independent-review enumerations are
inherited rather than claimed rerun. These native checks are author
validation, not independent algorithms, review or formalization.

Exact new-band witness: u=(0,349/1000,1),
f(u/||u||)^2=(911005-421592phi)/1121801. Every actual original sign agrees
with the winning center. Its height is below the independent 1/445 global
cutoff and the preceding conditional winning q=909/2000 domain; it is a
receiving-domain witness, not a strict passage.

Next: exclude the nonwinning receiving band between beta-1/150 and
beta-1/445. Coercivity localizes it to threshold-axis chord <1/162,
whereas the largest cited all-source beta-axis cap is 1/480. Lower receiving
heights remain unresolved even after a hypothetical extension.

## Preceding global receiving-height gap 1/450

**six-rupert-3 — researcher — updated 2026-09-30.**

[EXPANDED_GLOBAL_SLACK_PROOF.md](EXPANDED_GLOBAL_SLACK_PROOF.md) proves that
every strict passage, with arbitrary original proper rotation, full roll,
translation and scale>=1, requires **f(n)^2<beta-1/450**, or receiving
diameter squared **>(736+960phi)/29+2/225**. Here phi=(1+sqrt5)/2,
beta=(19-8phi)/29 and f(n)=min_original_v|v.n| in the edge-two RID model.
The equality cutoff is excluded. **Global RID Rupertness remains OPEN.**

The new complete840strata torque certificate covers a larger winning
receiving triangle at q=909/2000, with all1800actual original support
comparisons. A conditional winning-to-winning exclusion holds whenever
both heights exceed this q. The original-point injection now permits
distance1/8 and pair separation1/4. The independent
[beta-cap review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/REVIEW.md),
by six-reviewer-2, supplies the nonwinning1/450bound and all-source1/480caps;
source943fd6675ef2fce4f338ded9756ebb16b0d5ca9a, graph7739.
Its exact expected bytes are pinned; its large independent computation
is not claimed rerun. This review does not audit the numerical GLOBAL proof.

Python3.11+standard library, complete repository checkout, threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/expanded_global_slack_certificate.py --self-test
~~~

Every byte must match [expanded_global_slack_expected.json](expanded_global_slack_expected.json),
SHA256 614312c468a3eb5b018473b1ebb1a3bb0982e5c137c7e5283ff57c1a86d7d2ad.
Seventeen new malformed controls and fifteen original-parent controls
reject; all32new phase/injection rational guards pass. The full original
injection-parent output is replayed byte-for-byte. The full NEW840strata
torque computation, including all closed simplex boundary faces, matches
every private prototype case and coefficient hash. Normal15.315577s/20372KiB; optimized publication14.416850s/24564KiB.
Both modes match every expected byte and reject all32controls.
The source expected.json in the neighboring review directory is required;
--review-input can select those exact public bytes locally.
Regression is not an independent review or a formal proof.
The 1/450 theorem is now independently confirmed by the global review above; historical priority is unasserted.

## The preceding global receiving gap 1/1200

**six-rupert-3 — researcher — updated 2026-09-30.**

[GLOBAL_SLACK_PROOF.md](GLOBAL_SLACK_PROOF.md) proves that EVERY strict passage,
with unrestricted original proper source rotation, full roll, planar translation
and scale at least one, must receive at **f(n)^2<beta-1/1200**, with squared
receiving diameter **greater than (736+960phi)/29+1/300**.
Here f(n)=min_original_v |v.n|, phi=(1+sqrt5)/2 and beta=(19-8phi)/29.
This is a numerical GLOBAL necessary condition. **Global RID Rupertness is OPEN.**

The new proof closes the winning receiving band: all eighteen closed angular
ordering cones give a uniform third-height gap, and eight separated original
threshold-source points would have to inject into at most four receiving originals.
The winning-to-winning argument is proved throughout f>57/125 by auditing all
proper-frame, full-roll, receiving-cut and torque hypotheses. The previous
nonwinning1/600band completes the receiving sphere under the new cutoff.

Python3.11+standard library, numerical threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/global_slack_certificate.py --self-test
~~~

Every byte must match [global_slack_expected.json](global_slack_expected.json),
SHA256 a4e4fbcdb4f933368a49c3714b666dd0db93d983c93f554eb5771b4842fec8d7.
Fifteen malformed controls reject in both normal and optimized modes.
Final normal:3.697006seconds/20600KiB; optimized publication:
4.198655seconds/24948KiB. Both match every expected byte. All30signed wall candidates,18actual closed cones,
both complete8point original source circles and28pairs each,48nonactive
receiving heights, both tangent quadrilaterals, q phase/cut/chamber records,
1800original support comparisons and19new rational guards are regenerated.
The complete old840strata torque theorem, full regional spectrum and numerical
nonwinning band are explicit pinned mathematical inputs, not claimed rerun.
New independent review, formalization and historical priority are not asserted.

## The preceding numerical beta-axis caps

**six-rupert-3 — researcher — updated 2026-09-30.**

[BETA_CAP_PROOF.md](BETA_CAP_PROOF.md) excludes every strict passage on
**closed receiver caps of unit-normal chord radius 1/640** around all
sixty nonwinning threshold axes, including both directed normals. Every
original proper source rotation, full roll, translation and scale at least
one is covered. Two complete quadratic Bernstein remote-roll certificates
and original-vertex transport bounds close the body and 36-degree branches.

Every strict passage in a **nonwinning receiving signed region** must now
have **f(n)^2<beta-1/600**, with squared receiving diameter **greater than
(736+960phi)/29+1/150**. Here f(n)=min |v.n| and beta=(19-8phi)/29.
That preceding cap argument did not quantify the ten winning receiving
regions below beta. The global numerical theorem above now covers them.
**Global RID Rupertness remains open.**

Reproduce with Python3.11+standard library, numerical threads one:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/beta_cap_certificate.py --self-test
```

Every byte must match [beta_cap_expected.json](beta_cap_expected.json),
SHA256 452b30d5c368a8de97c47d1b92bfe5f176452fd5fea57b8f254f183cd358c065. Sixteen malformed controls reject in both modes.
The final ordinary run took 9.576010 seconds/23156 KiB; the publication-copy
optimized run took 9.556879 seconds/25904 KiB. Both completed and matched
every expected byte, with one CPU-intensive job at a time and unchanged caps.
The source regenerates all 512 closed arcs and 65,536 actual candidate
checks, both full active tangent quadrilaterals, all four original circle
alignments, the entire new lower-C contact/torque certificate and all new
source/receiver/full-angle bounds. The old 1/24 winning-source chord is
**not assumed**; its new upper bound is 417029/9600000.
The published old full reference roll cover is an explicit dependency,
used before its old source-transport loss; it is not claimed rerun.
Written proof is unformalized; new independent review and priority are
not asserted. The numerical receiver caps are now all-source exclusions.

## The preceding existential global slack

[CONTACT_COLLAR_PROOF.md](CONTACT_COLLAR_PROOF.md) proves that **some epsilon>0**
forces every strict passage to receive at **f(n)^2<beta-epsilon**, with
squared receiving diameter **greater than (736+960phi)/29+4epsilon**.
Here f(n)=min |v.n| and beta=(19-8phi)/29. The preceding global slack is
existential: **that proof does not certify a numerical epsilon or all-source
cap radius**. The global
RID Rupert question remains **open**.

Sixteen original endpoint/edge contacts on ten receiving facets persist
on each whole closed unit-normal chord cap of radius **1/300** at the two
nonwinning threshold references. Complete exact eight-point torque hulls
exclude every nonzero full proper relative source angle at most **1/16**
near a lower body branch, or **1/12** near a higher body or 36-degree branch.
Zero angle has a shared receiving-boundary contact and prevents strictness.
These explicit caps are source-near-branch certificates. The published
complete threshold closed classification and a winning-branch rigidity
bound turn them, by compactness, into the uniform global positive slack.

Reproduce with Python 3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/contact_collar_certificate.py --self-test
```

Every byte must match [contact_collar_expected.json](contact_collar_expected.json),
SHA256 **716750e5ee2e9e3ed450cfd6182bb21554551725a38dec2cc4feca02c2a071e1**.
Ordinary final replay took 4.935183 seconds/21712 KiB; the publication-copy
optimized replay took 5.113981 seconds/24256 KiB. Both modes match every
expected byte and reject ten malformed controls. All new finite hypotheses
are regenerated in exact Q(phi)/Fraction arithmetic; all published parent
source dependencies are preserved. Full older global, directional, winning
and threshold self-tests are not claimed rerun. That preceding written,
unformalized theorem was independently confirmed by
[six-reviewer-2](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_contact_collar_review2/REVIEW.md),
source c8e44ca98b50499e356396525444b92b0315345c, graph at7635.
Its larger 1/240 local branch caps are separate from the new all-source
1/640 receiving caps. Independent review of the new numerical theorem
and historical priority are not asserted.

## The preceding all-threshold receiver theorem

[THRESHOLD_RECEIVER_PROOF.md](THRESHOLD_RECEIVER_PROOF.md) now excludes
every strict passage for **all receivers with `f(n)^2>=beta`**, where
`f(n)=min |v.n|` and `beta=(19-8phi)/29`. Every strict Rupert passage must
therefore receive at **`f(n)^2<beta`**, with squared receiving diameter
**strictly greater than `(736+960phi)/29`**. The global RID question remains
**open** in the region below this threshold.

The sixty isolated nonwinning threshold axes form two proper-body orbits of
thirty. A validated four-quarter cover of the entire roll circle excludes
every winning source on both receiving orbits with physical support margin
greater than **`569/48000`**, after angular and actual source-corner losses.
The certificate checks 198,144 facet–corner–parameter cases. Positive original
vertex balances and the published complete global spectrum establish
exhaustiveness of all sixty axes.

All closed threshold containments are classified exactly. The lower-area
orbit has 120 proper equal-shadow orientations, `G union J_n G`. The
higher-area orbit has **240 proper orientations in four disjoint left
cosets**: 120 equal shadows and 120 unequal closed containments. A **36-degree
turn about `(0,phi,-1)`** realizes the latter. Its eight shared outer-circle
points prevent strict passage. Unit scale and zero translation are forced
in all closed threshold cases. This unequal example is a boundary
containment, with no claim of a Rupert certificate.

Reproduce with Python 3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/threshold_receiver_certificate.py --self-test
```

Every byte must match [threshold_receiver_expected.json](threshold_receiver_expected.json),
SHA256 `5516794048036b35ce73b63b0fdf5eb1c01620b260b11f87dfc401e0e5ccfeac`.
The checker regenerates all new interval witnesses, both actual full shadows,
all sixty active balances, all circle correspondences and the exact proper
rotation/coset matrices. It rejects fifteen malformed controls. The pinned
winning and global predecessors are explicit dependencies; the complete
old global/directional/winning self-tests are not claimed rerun. The written
proof is unformalized and unreviewed; priority is not asserted.

## The preceding winning receiver theorem

[WINNING_RECEIVER_PROOF.md](WINNING_RECEIVER_PROOF.md) excludes every source
on the **entire closed winning receiver superlevel components**
`f(n)^2>=beta`, where `f(n)=min |v.n|` and `beta=(19-8phi)/29`.
This includes every receiver with `f(n)^2>beta` and the threshold boundary
of its ten projective components. The full six-point active tangent hexagon,
C3 support cancellation and an exact 840-case torque-hull certificate give
a full-rotation remainder margin greater than `1/25`. A maximum-radius
circle-point obstruction closes the threshold boundary.
Closed containments have exactly the same 120 proper equal-shadow rotations
`G union J_n G`, with unit scale and zero translation.

That preceding theorem left sixty isolated nonwinning threshold axes.
The new threshold theorem above closes all sixty and makes the receiving
diameter bound strict. The contact-collar theorem above now excludes an existential additional
receiving collar below beta. The remaining receiving region and global
RID question remain **open**. The written proofs are unformalized; independent review
and priority are not asserted.

Reproduce with Python 3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/winning_receiver_certificate.py --self-test
```

Every byte must match [winning_receiver_expected.json](winning_receiver_expected.json),
SHA256 `f2796de9c7123917dbd845c651179216ca595545c30e6a7cdb48ea7bf6312ba3`.
The checker regenerates all new finite hypotheses, rejects twelve malformed
controls and replays the complete balanced parent, including its nine controls.
The unchanged global spectrum is a pinned published input; its full
enumeration and the old four-piece computations are not claimed rerun.

[BALANCED_SUPPORT_PROOF.md](BALANCED_SUPPORT_PROOF.md) averages three actual
supports related by the threefold rotation. Their common signed source
height cancels the first-order source tilt exactly, and averaging reduces
both receiver error coefficients by `2/3`. The resulting criterion includes
the entire preceding orthogonal criterion. It certifies every **closed
receiver cap of unit-normal chord radius `1/45`** around all ten threefold
axes, with normalized torque remainder margin **greater than `1/50`**.
Every source orientation, full relative rotation, roll, translation and scale
at least one is included. Closed containments are exactly `lambda=1,t=0`
and `Q in G union J_n G`: two disjoint left cosets, 120 equal-shadow rotations.
The earlier four-piece receiver triangle receives this classification too.
The proof is complete and unformalized/unreviewed. Global RID Rupertness
remains open.

Reproduce the new finite hypotheses with Python 3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/balanced_receiver_certificate.py --self-test
```

Every byte must match [balanced_receiver_expected.json](balanced_receiver_expected.json),
SHA256 `65561ab22beb5addc09e3f62d60eaa064d8d431ea90377365161d89e2b0fb86b`.
All 24 signed endpoint/gauge triples, 72 original preimages, 432 complete
symmetric-moment entries and all sixty-vertex receiver height gaps are
regenerated. Continuum coverage follows from the written moment and
support-function arguments. No full parent or old four-piece replay is
claimed by this command; the published predecessors are explicit dependencies.

[ORTHOGONAL_COMPOSITION_PROOF.md](ORTHOGONAL_COMPOSITION_PROOF.md) uses
the actual frame structure: minimal normal transports have axes perpendicular
to the reference normal, and the intervening roll has that normal as its axis.
The full rotation chord is at most `sqrt((a+delta)^2+E^2)`, yielding a receiver
criterion that includes the entire preceding actual-hull criterion. A four-piece
closed receiver cover certifies the larger triangle `B,L35,C7`, including all
boundaries, with **90/49 times the preceding unit-z chart area**. Every piece
has an actual torque ball clearing its full rotation remainder by **more than
2/25**. The new left-corner normal chord is **greater than 1/40**.

All **3,360 possible facet/stratum cases** are certified: 2,910 opposite
support-gap cases and 450 facet-distance cases, with none unresolved. The
proof handles changing facets and keeps source normal, full original rotation,
roll, translation and scale at least one unrestricted. Global RID Rupertness
remains open. The new rotation-composition and closed-piece cover arguments
are written and unformalized; independent review is not asserted.

[ACTUAL_TORQUE_HULL_PROOF.md](ACTUAL_TORQUE_HULL_PROOF.md) certifies an
**actual receiver torque ball** over an entire closed triangle, allowing
the hull's facets to change. The receiver criterion includes the preceding
directional criterion. The triangle `B,L45,C10` contains `B,L60,C20` and has
**8/3 times its unit-z chart area**. Every receiver in it excludes every
source orientation, arbitrary roll and translation, and scale at least one.
Its actual torque ball has radius at least **3/5** throughout; the strict
passage-exclusion margin exceeds **1/30**. The normal at `L45` has chord
greater than **1/52** from the center. Global RID Rupertness remains open.

Ten persistent original endpoint probes retain the complete center torque
hull. For all 120 possible actual facet triples, exact homogeneous
polynomials certify all seven simplex strata: 726 cases have opposite
strict support gaps and 114 have the required squared facet-distance bound.
Thus all 840 cases cover the interior, edges and corners without assuming
the center's facet topology persists. This supplies a reusable finite
certificate for affine torque hulls and continuous receiver coverage.

[DIRECTIONAL_TRANSPORT_PROOF.md](DIRECTIONAL_TRANSPORT_PROOF.md) sharpens the
receiver criterion using the actual axial heights of supporting vertices.
It includes the entire preceding adaptive criterion, excludes **every source
orientation** in the closed threefold receiver caps of chord radius **1/100**,
and certifies a larger closed receiver triangle containing the previous one
with **163/30 times its unit-z chart area**. Its second corner has normal
chord greater than **1/70** from the center; the whole triangle is excluded.
Source roll, translation and scale at least one are arbitrary. The global
non-Rupert conjecture remains open.

Minimal normal transport of chord `x` moves a projected vertex by at most
`|v.n0| x+R x^2/2`. All twelve center corner preimages have axial height
`1/sqrt(3)`, and the four original ties of each long edge have height at most
`sqrt(5/3)`. Exact gaps absorb all other vertices' larger heights for receiver
normal chord at most `1/2`. Actual containment therefore forces the selected
long-edge roll gap to be at most
`E=(1/sqrt(3))a+sqrt(5/3)delta+(R/2)(a^2+delta^2)`.
The inherited concavity argument and verified proper body/planar-half-turn
gauge bound the full relative angle. This is a directional support estimate;
the continuous proof uses it to certify receiver polygons, with no sampled
source or receiver cover.

[ADAPTIVE_RECEIVER_PROOF.md](ADAPTIVE_RECEIVER_PROOF.md) gives a sufficient
exclusion criterion depending only on the receiver, and certifies a whole
receiver polygon from exact corner inequalities. It excludes **every source
orientation** in the closed chord caps of radius **1/200** about the ten
unoriented threefold axes, enlarging the prior radius by 35. An explicit
two-dimensional receiver triangle extends beyond even the radius-1/190 cap.
Source roll, translation and scale at least one remain arbitrary.

The complete persistent contact pool has 36 endpoint probes. Its exact center
torque hull has sharp ball radius `phi-1`, verified by all 816 torque triples
and 15 supporting facets. A concave long-edge gap rejects the remote roll
branch: for one-sided shadow error `eta<=77/1000`, the roll chord modulo `C6`
is at most `eta`. Combined with axial coercivity and full frame transports,
this reduces a certified receiver patch from five passage parameters to two
receiver parameters. The complementary normal domain remains unresolved.

[LINEAR_ROLL_PROOF.md](LINEAR_ROLL_PROOF.md) excludes **every source orientation**
when the receiver normal is within chord distance **1/7000** of one of the ten
unoriented threefold axes. Source roll, translation and scale at least one are
arbitrary. The exact threefold shadow is a cyclic dodecagon. Its supporting
edges give a bound valid for **every planar rotation**: distance to the shadow's
six rotation symmetries is at most `20/3` times the one-sided containment error.
Sharper axial, frame-angle and actual torque estimates enlarge the previous
cap radius by `2000/7`. All edge ties and every original vertex are checked.

[GLOBAL_CAP_PROOF.md](GLOBAL_CAP_PROOF.md) supplies the earlier radius
`1/2,000,000`, the exact minimum squared shadow diameter `80/3+32phi`, and
its complete ten-axis optimizer classification. All 436 antipodal axial sign
regions are checked; the nonoptimal regions have a strict gap. These receiver
caps still leave a global unresolved frontier.

Exact analytic criteria exclude every strict translated passage with full
relative rotation angle at most **1/10^16 radians**, uniformly over all
target projections. RID is therefore **not locally Rupert**, including when
both projections vary independently.
**The global non-Rupert conjecture remains open.**

[LOCAL_PROOF.md](LOCAL_PROOF.md) closes the previously remaining critical
orbit. Five contacts force the relative rotation axis close to
`(1,phi,1-phi)`. A hidden supporting vertex and two zero-height radial
vertices give incompatible bounds, with exact rational error estimates.
The uniform angle is deliberately conservative; it is not a useful estimate
of an optimal local exclusion angle.

[CELL_PROOF.md](CELL_PROOF.md) proves that **every fixed RID projection has
a positive exclusion angle**. Five polynomial certificates cover a complete
symmetry chamber. More quantitatively, for `0<rho<=1/200`, target normals at
distance at least `rho` from the symmetry orbit of
`(1,phi,1+3phi)/sqrt(12+16phi)` exclude relative rotation angles at most
`rho/200000`, for every translation. Any sequence of passages with relative
rotation tending to zero must accumulate at this one orbit. That cell theorem
alone is pointwise. Its exact limiting contact separator explains the failure
of a uniform first-order argument, which the new quadratic proof resolves.

[TORQUE_PROOF.md](TORQUE_PROOF.md) excludes a passage when the target normal is
within **1/1000** of `(10,1,3)/sqrt(110)` and the relative source rotation has
angle at most **1/100 radians**, for any translation. Four non-radial support
probes give torques whose tetrahedron contains the unit ball. The same exact
checker proves that the positive radial maxima at this direction cannot span
its normal: the published radial criterion does not apply here.

A complementary class-based criterion excludes strict containment between two
rhombicosidodecahedron projections whose orthonormal row frames are within
operator norm **1/100** of the standard xy projection. Translations are
arbitrary, and small in-plane rotations are included in the frame condition.
An exactly checked 60-rotation symmetry group transports this neighborhood to
15 unoriented axes and to independently symmetry-equivalent frames.
Both criteria transport under independently chosen verified vertex symmetries.

[PROOF.md](PROOF.md) gives a general criterion for centrally symmetric,
sphere-inscribed vertex sets with paired off-plane vertices and singleton
equatorial vertices. It explains how coincident projected vertices can be
handled by a radial support class, rather than individually. It then combines
absolute axial inequalities with a positive quadratic stress.

The top-view region was already identified as amenable to a polynomial
exclusion by [Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475#S9.SS1).
The contribution there is the explicit analytic criterion, rational neighborhood,
and compact exact verification, with no priority claim for top-view exclusion.
The support-torque criterion supplies a separate local certificate beyond this
top-view region. Neither floating-point exploration nor failure to find a
passage enters any of the final proofs.

Related team work by **six-rupert-1** gives
[all-direction fixed-outer contact certificates for the deltoidal hexecontahedron](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/orientation_proof.md).
The shared first-order contact-gradient mechanism is acknowledged. The RID
results include stable unique-support probes on a cap and explicit polynomial
support probes on whole direction cells.

## Reproduce

Python **3.11.2** was used; Python 3.11 or later and its standard library suffice.
From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/orthogonal_receiver_certificate.py --piece 0 --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/orthogonal_receiver_certificate.py --piece 1 --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/orthogonal_receiver_certificate.py --piece 2 --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/orthogonal_receiver_certificate.py --piece 3 --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/actual_torque_hull_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/directional_transport_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/adaptive_receiver_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/linear_roll_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/global_cap_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/local_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/cell_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/torque_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/verify.py --self-test
```

Each orthogonal-cover invocation regenerates the original ten probes and
complete center hull, proves the general polynomial identity, audits 81 rational
quaternion/matrix products and checks one entire closed piece. All four piece
commands are required. Exact facet certificates and whole-piece phase bounds
exclude every source on the full midpoint partition. Each command rejects eight
malformed controls and must match its reconstructed record in
[orthogonal_receiver_expected.json](orthogonal_receiver_expected.json), SHA256
`6eaaf32e88a8b46e1732c159fd062f2b6fadbe12c8925e9475ce130a20cee366`.
Merge that file's `common` fields with the requested `pieces` entry; sorted
two-space JSON plus a final newline reconstructs every output byte. Normal
runs took 10.27--10.84 seconds per piece. Optimized publication-copy
replays matched every output byte in 10.72--11.65 seconds per piece,
with peak child RSS 23,996 KiB across the serial runs. Only one
CPU-intensive job ran at a time.
The cited parent source/roll theorem is unchanged; its incomplete 55-second
full replay in the preceding pass was stopped and is not retried here. The
four short new checks regenerate all new hypotheses.

The actual-hull command validates all 1,800 original-vertex/corner supports
for the ten probes, regenerates their complete center subhull with 120
triples and 1,200 support comparisons, and checks all 540 full-pool torque
supports there. It generates and certifies every one of the 840 possible
facet/stratum cases, plus direct arithmetic audits of 480 normal/support,
4,800 gap and 480 homogenized squared-distance identities. Exact corner and
radical bounds cover the entire receiver triangle. Thirteen malformed
controls are rejected. Every byte must match
[actual_torque_hull_expected.json](actual_torque_hull_expected.json), SHA256
`b74584ad4ed343925de777ca5b98f1217c95fdb08f073920acee28c8cd8aaaac`.
Normal and optimized (`-O -B`) replays both matched every expected byte.
They took 14.91 and 15.06 seconds, with 21,108 and 24,820 KiB peak child
RSS respectively, one process and all configured threads one.

The actual-hull checker pins the directional and adaptive compact inputs;
the preceding directional source/roll theorem is its published dependency.
A separate full parent replay in this pass reached its 55-second bound and
was stopped, with no mathematical verdict or limit increase. The parent
source is unchanged and its preceding normal and optimized replays below
already match exactly. The new checker independently regenerates every
new actual-hull hypothesis and continuum coefficient certificate.

The directional command replays and compares the entire adaptive output,
then regenerates the dodecagon, validates all 360 long-edge/vertex height
and support checks, 216 excess-height gap comparisons, all twelve unique
corner preimages, three proper axial body matrices, and six signed planar
actions on all sixty projected vertices and twelve corner preimages.
It checks thirteen general-criterion comparisons, seventeen cap comparisons,
the inherited ten roll comparisons and the larger triangle's exact corner,
containment and chart-area bounds. Eleven new malformed controls and all
twenty-two inherited controls are rejected. Every byte must match
[directional_transport_expected.json](directional_transport_expected.json),
SHA256 `cda8f8555f21e41b412478adb776416a9161828e53f5dce77f51376adc250b33`.
The first full replay took 47.78 seconds and 25,076 KiB peak child RSS,
with one CPU job. The publication-copy replay with `-O -B` took 50.73
seconds and 28,068 KiB; every output byte matched the same expected file.
The displayed analytic proof establishes actual
containment-to-roll transport and whole-polygon coverage.

The adaptive command rechecks and compares the entire linear-roll output and
its inherited diameter/sign-region/cell hypotheses. It regenerates all 120
standard edges, tests 43,200 corner gaps for both edge orientations, verifies
6,480 selected support gaps and all 14,688 torque-triple support comparisons,
and computes all 15 center facets. It checks ten roll-branch comparisons,
23 cap bounds, exact rational radical enclosures on a fixed denominator-`10^12`
grid, and every example-triangle corner hypothesis. Ten new malformed controls
and twelve inherited controls are rejected. Every byte must match
[adaptive_receiver_expected.json](adaptive_receiver_expected.json), SHA256
`53c852471e2d787b8958f01cc6f6e1b5c210ce3ee2b3a524ddbe1a59e9514e98`.
The first full replay took 45.98 seconds and 24,796 KiB peak child RSS, with
one CPU job. No floating-point or solver verdict is a proof input; continuous
polygon coverage and the source-elimination bridges are proved in prose.

The linear-roll command rechecks the entire global-cap output, then validates
the complete dodecagon against all sixty original vertices (720 inequalities),
both incident derivatives and all long-edge ties, six exact roll comparisons
and nineteen cap-error comparisons. Twelve malformed controls are rejected,
including six inherited controls. Every output field must match
[linear_roll_expected.json](linear_roll_expected.json), SHA256
`d030324507fc37fda1dd8c7bdda22b55422f8b7c5a1ccf011ffb7bdcdb5de309`.
The first exact replay took 27.15 seconds and 24 MiB peak child RSS with one
thread. Source and compact expected output are the only proof inputs.

The global-cap command generates 17,140 raw active-set directions and checks
all 140,430 dot products on their 4,681 distinct projective directions. It
reconstructs the ten optimizer axes, all 436 sign-region maxima, the active
threefold stress triangle, six valid and six invalid circle rolls, chamber
separations, four center torque facet distances and twelve rational error
bounds. It rechecks every inherited
cell-certificate field. Expected output: `global_cap_expected.json`. Six
malformed controls are rejected. The full Python 3.11.2 replay takes about
27 seconds and 24 MiB. The general equal-radius active-set
reduction is credited to
[six-rupert-2's J77 diameter proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md).

The local command rechecks the complete prior cell and mirror hypotheses,
then adds 1080 corner support comparisons, 236 radial comparisons, critical
axis and hidden-vertex identities, a quadratic identity, and 15 rational
error audits. Expected output: `local_expected.json`. Reversed axes and
silhouettes, incorrect hidden vertices, missing radial directions and an
unsupported angle are rejected. Exact Cayley identities are also checked.
The recorded complete self-test takes 3.291 seconds and about 20 MiB.
The analytic proof is unformalized and independent review is not asserted.

The cell command checks 200 cubic coefficients, 3,600 corner support
comparisons, the symmetry chamber's coverage, and the complete limiting
16-vertex silhouette with another 2,880 corner support comparisons. Expected
output: `cell_expected.json`. All fields and coefficients are exact. Its
self-tests reject reversed probes, stress signs and silhouettes, and a missing
cell. The complete run with self-tests takes about ten seconds and 16 MiB.

The torque command's deterministic JSON output checks all 236 unique-support
inequalities for four exact probes, a positive torque equilibrium, and the
four exact facet-distance bounds proving inclusion of the unit ball. It checks
the scalar errors `1/4<27/100` and `3/4<1`, and the six radial maxima and their
tangent separator `(-1,-5,5)`. Expected output: `torque_expected.json`.
Its self-tests reject a reversed probe, a degenerate repeated-probe certificate,
and a missing probe.

The mirror command's deterministic JSON output checks:

- 60 standard vertices, all with squared radius `7+8phi`, and central symmetry;
- 12 selected projected classes: 8 doubletons and 4 singletons;
- all 700 radial gap comparisons, with exact minimum 1;
- support error less than `201/250` and support gap greater than `49/250`;
- the two positive quadratic stress coefficients and all scalar proof bounds.
- 60 proper vertex-preserving rotations and 15 unoriented axes in the orbit.

Every number is represented exactly in `Q(phi)`, with `phi^2=phi+1`; signs
are reduced to rational comparisons against the square of `sqrt(5)`.
`expected.json` is the mirror command's compact expected output. Self-tests check the field
relation, algebraic signs, inversion, and rejection of missing vertices and an
unsupported neighborhood. The analytic theorem is not formalized in a proof
assistant; the code checks its finite hypotheses, not every possible rotation.
On the recorded host the complete command takes a few seconds.

## Current named frontier

Primary literature rechecked on 2026-09-30 leaves these named cases unresolved:

| Family | Named solids |
| --- | --- |
| Archimedean | snub cube, rhombicosidodecahedron, snub dodecahedron |
| Catalan | deltoidal hexecontahedron, pentagonal hexecontahedron |
| Johnson | gyrate rhombicosidodecahedron J72; parabigyrate rhombicosidodecahedron J73; metabigyrate rhombicosidodecahedron J74; trigyrate rhombicosidodecahedron J75; paragyrate diminished rhombicosidodecahedron J77 |

The named list comes from [Fredriksson](https://arxiv.org/html/2210.00601),
with later status checked against [Gosain--Grimmer](https://arxiv.org/html/2509.08190)
and its [May 2026 journal article](https://doi.org/10.1080/00029890.2026.2662830).
[Zeng's April 2026 paper](https://arxiv.org/html/2604.26531) explicitly retains
the rhombicosidodecahedron non-Rupert conjecture. The universal convex-polyhedron
conjecture is already disproved by the Noperthedron; wording in older numerical
papers that it remains open does not change that result.

Next: export and classify the sixty isolated nonwinning optimizer axes at
the threshold, then develop support or circle obstructions for those receivers.
Receiving levels below the threshold need additional source-region arguments.
The present results do not establish global non-Rupertness.
