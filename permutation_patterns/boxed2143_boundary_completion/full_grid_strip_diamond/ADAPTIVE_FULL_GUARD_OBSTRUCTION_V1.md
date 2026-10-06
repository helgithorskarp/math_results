# Full guard order adaptation does not give universal completion

Lyra, literature-researcher-2, 2026-10-06. New author partial argument and
directed exact controls, pending Sage's separate check. Full target410
remains UNSOLVED. This rejects a specified construction mechanism within
that target; no problem, success criterion or source scope is replaced.

## Exact map and complete decoder

Use r old rows sigma_i and r old columns tau_j in S_r, and r-1 guard rows
alpha_i and r-1 guard columns beta_j in S_(r-1), r>=2. One old point in
each cell(i,j) has horizontal key(2i,position of j+1 in sigma_i) and vertical
key(2j,tau_j(i+1)). One guard in EVERY gap cell(i,j), i,j<r-1, has horizontal
key(2i+1,position of j+1 in alpha_i) and vertical key(2j+1,beta_j(i+1)).
Sort horizontal keys and replace vertical keys by ranks. The output length
is N_r=r^2+(r-1)^2. This now allows every independent guard ordering;
the earlier four monotone layouts were only special cases.

Every old horizontal/vertical band has the fixed size r. Every interleaved
guard band has fixed size r-1. The output identifies all these bands, both
their type and their index. Reading old vertical band indices in old row i
recovers sigma_i, and their within-band ranks recover tau_j(i+1). Reading
guard vertical band indices in guard row i recovers alpha_i; their ranks
recover beta_j(i+1). This gives an exact decoder for ALL4r-2 input
permutations, not merely the original old2r fields. Thus the entire map
is injective, uniformly, independent of avoidance.

## All monochrome boxes are excluded, including the two half layouts

For avoiding old components, no occurrence consisting solely of old points
survives either the full guard layout or either checkerboard half, for ANY
guard orders. If its selected points all lie in one old row, an empty
rectangle would already be a box in that row permutation; likewise for one
old column. Otherwise let i be the first selected old row, let ell be the
last, and let j,k be the old column bands of the selected minimum and
maximum. We have i<ell and j<k. Every occupied guard vertex(h,v) with
i<=h<ell and j<=v<k is an unselected interior shading point, independently
of its within-band ranks.

The full layout supplies such a vertex. In either half layout it exists
whenever (ell-i)*(k-j)>=2: a rectangle of vertices containing an adjacent
pair has both parities. The only remaining case is ell-i=k-j=1. Four
distinct old selected points then use all four cells of a2x2 grid. The
first two positions lie in the first row and the last two in the second.
For a>b, a must be in the higher column and b in the lower; for c>d,
c must be higher and d lower. But then a>d, contradicting a<d. Thus
this case cannot even have the classical order2143.

Likewise no guard-only box survives if every guard row/column order itself
avoids. This includes the fixed monotone orders in the original half-grid P,
and the avoiding-component application of the full adaptive map. A box in
one guard row/column would already be a component box. For a putative box
with first/last guard rows i<ell and minimum/maximum guard columns j<k,
the ALWAYS-present old point(i+1,j+1) is unselected and lies strictly
inside both intervals, regardless of all component ranks. These indices
are in range even at the boundary. Therefore every remaining grid box is
mixed: one, two or three selected guards. This is a uniform geometric
reduction of the old P obligation; it does not estimate those mixed boxes.

## A zero completion fiber, with only three cases

At r=3 take ALL old rows123, and old columns(123,123,132). Every component
avoids. In the full-band output the old values by row are

    row0: 1,6,11; row1: 2,7,13; row2: 3,8,12.

The guards g00,g10 occupy values4,5 in either order; g01,g11 occupy9,10
in either order. Each guard row has two entries in either order. There are
EXACTLY16 possible full guard profiles. Every one fails, as follows.

* Case A: guard row0 orders g00 before g01. Select
  (old01,g00,g01,old11). Values are(6,b,c,7), with b in{4,5},
  c in{9,10}. Thus b<6<7<c. The only unselected interior old points
  are old02=11>c and old10=2<b. There are no other interior guards.
* Case B: guard row0 orders g01 before g00, and guard column1 orders
  g01 below g11. Select(g01,old11,old12,g11). Values(9,7,13,10)
  have order2143. Every unselected interior point is g00, old10 or,
  depending on guard row1 order, g10. Their values are all below7.
* Case C: guard row0 orders g01 before g00, and guard column1 orders
  g01 above g11. Select(old02,g01,old12,old22). Values(11,10,13,12)
  have order2143. Every other interior entry is below10: g00/g10
  have values4/5, g11=9, old10=2, old11=7, old20=3, old21=8.

Each listed positional quadruple is increasing. Each rectangle is empty
under the exact strict/unselected definition. These three cases cover all
guard profiles, independently of guard row1 and guard column0 orders.

## Uniform obstruction at every r>=3

For any r>=3 choose all sigma_i=12...r, all tau_j=12...r except

    tau_2=1324...r.

These old components avoid even classical2143: the exceptional permutation
has only one inversion, whereas2143 requires two disjoint inversion pairs.
Allow ALL guard components in S_(r-1), whether or not they themselves avoid.

Delete the positional suffix beginning with guard row2, leaving old rows
0,1,2 and guard rows0,1. Next delete the remaining highest-value suffix of
vertical bands, beginning with guard column2, leaving old columns0,1,2
and guard columns0,1. Neither operation can remove an unselected interior
point of a retained rectangle: the first deletes only positions beyond
every retained endpoint, and the second only values beyond every retained
maximum. Standardization therefore preserves boxed avoidance.

The geometric cut is exactly the r3 grid above. Old rows restrict to123;
old columns to123,123,132. Each retained guard row restricts to its labels
1,2, giving one of12/21. Each retained guard column restricts to its first
two entries and standardizes, again giving12/21. The r3 proof rules out
avoidance. Hence NO full adaptive guard ordering completes this valid old
tuple at ANY r>=3. This includes the subset of avoiding guard components.
The full arbitrary-guard fiber has ((r-1)!)^(2(r-1)) profiles; its rejection
is the uniform projection and three-case proof, not an infinite enumeration.

The statement concerns fixed full occupancy and variation of guard ORDERS.
It does not reject varying guard locations, deleting guards, another
completion layout, or a weighted aggregate compatible population.

## The actual entropy obligation if the aggregate route is retained

Let K_r count compatible ordered tuples from
(Av_r)^(2r) x (Av_(r-1))^(2(r-1)) for this exact full map. Its complete
decoder gives a_(N_r)>=K_r. A sufficient all-size aggregate bound is:
there are r0>=2 and delta>0 such that, for EVERY r>=r0,

    K_r >= 2^(delta*N_r) * a_r^(2r).

Indeed t_r=(log_2 a_r)/r is nonnegative, and N_r<=2r^2. Therefore

    t_(N_r) >= (2r^2/N_r)*t_r + delta >= t_r + delta.

Iterating r_(k+1)=N_(r_k)>r_k yields unbounded nth roots and solves the
full negative alternative of410. This is a CONDITIONAL proposition;
the aggregate bound is unproved. Pointwise zero guard fibers do not refute
it. A single compatible guard choice for every old tuple, even if it were
true, would provide no delta term. Guard entropy and all multiplicities
must be counted. No finite fitted constant is used as a premise.

## Directed exact controls and precise exclusions

`adaptive_full_guard_probe_v1.py` stopped after the first TWO lexicographic
old cores at r3, testing all16 guard profiles for each. The second is the
zero core above; its complete16 output words and FULL literal occurrence
sets are retained. This is not a complete6^6 old-input census. Original
stream7938e97832cf66963d3c284c3668d2002fd4858d3d56c82e4791f201bac2383a.

`adaptive_full_guard_lift_controls_v1.py` checks the exact full-component
decoder, extreme-band projection and prescribed literal selected box on
EVERY guard profile for this fixed core at r3 and r4, respectively16 and
46656 profiles. Case counts are(8,4,4) and(23328,11664,11664).
The r4 scan does not compute every unrelated box set; only its three
prescribed representatives have complete sets. The report also includes
three complete r3 representative sets, and64 specified monotone/nonmonotone
lifted controls at r5..8, which are not full guard populations.
All these fields and guards are explicitly recorded or streamed with SHA256.
The complete selected-control streams are

    r3 b04e5ecb9a6953d2b038ecd8cc97941fd0e459c2476f4e6a6bfa9d2ee5a8aa4a
    r4 0cb25c147213364fdb0988f461cdfff763e402949e43b177539dbfa1fd2d2933
    lifted64 6f440f56df7ac8f6ed135b2d8e3adebaf8f1cd700868e17d635e2503ad2657e2

Separately, `grid_monochrome_shading_controls_v1.py` checks EVERY old-only
selected quadruple for EVERY one of46656 old-component tuples at r3 under
EACH half layout. Both domains have5,878,656 quadruples and zero old-only
boxes. At r3 each occupied guard band has one point, so this includes every
guard ordering for those layouts. It is not a mixed-box classification or
an all-guard census. The two full streams are

    parity0 ab0147fe27d9bec86e67d637e61e2cc80521d3d8b234fc049ed473e188f7520f
    parity1 36de87d1f5e9c0edacfe5d469dc6ba7a66e6497127e3fc32a6f34955c4d00bac

This directed check takes10.804907s/16552KiB. The guard-only statement is
the uniform old-point shading/component proof above; the r3 half layouts
have fewer than four guards and provide no nonvacuous all-guard census.

The finite controls use our exact literal strict-rectangle checker and
take9.519853s/18064KiB on the recorded interpreter. They are same-author
controls; a different researcher's full argument and certificate check
is requested under the existing pairing. No prior review is extended.
Neither original half-grid P, new K_r's aggregate bound, full410 nor any
novelty/publication claim follows. No standalone publication or graph
original is planned for this failed universal recipe and conditional bridge.
