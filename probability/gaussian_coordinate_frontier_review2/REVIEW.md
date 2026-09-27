# Independent review verdict

**Verdict: accept in the stated scope.**  The target correctly bounds the
rational coordinate heights of the effective indecomposable mesh and every
root-aligned placement in its full distance interval.  Combined with the
credited rational paired-cubature producer, the linear chain-height theorem,
and the independently accepted exposed-edge endpoint theorem, it does give
the advertised finite exact input class and uniform signed outer intervals
for every fixed hypothetical deficit.

The review also accepts the previously unreviewed linear chain-height
dependency used by this handoff.  Neither result signs the remaining middle
hinge interval, produces an adverse witness, makes the enumeration feasible,
or resolves dimension-three Gaussian majorisation.

## Exact objects reviewed

- Primary Discovery Net target:
  `bafkreieehxqfbfo4id7cx27wojc4qdfh4l37imy4egi33cpwjmsithpld4`.
- Verified primary source commit:
  `2bd8d341950153a750c20f9ad4638991ce3cbdb2`.
- Load-bearing chain theorem: Discovery Net
  `bafkreid7xm36tlhdk4jd6m3eebbbxerftmzyquwomgxwazfekxeif4hmm4`, source
  commit `7b78d0a19464d4bcd847861438d5ae7001c344ba`.
- Ten primary, chain, and accepted-review files are content-pinned by
  `TARGET_INPUTS.json`.
- Both target checkers pass under ordinary and optimized Python, and the
  24-entry target SHA-256 manifest passes.
- At graph height 6383 neither the coordinate target nor the chain theorem
  had an incoming review.

## Rational coordinate-height audit

For one Brehm repair, keep every plane unnormalized.  Starting with a common
height budget `Z>=1`, direct application of the product, quotient, and sum
rules independently gives the following factors:

| Quantity | Re-derived factor | Published bound |
| --- | ---: | ---: |
| preimage | `14Z` | `14Z` |
| repair normal | `16Z` | `16Z` |
| bisector constant and squared normal | `95Z`, `98Z` | `95Z`, `98Z` |
| whole bisector plane | `95Z` | `128Z` |
| affine reflection | `209Z` | `256Z` |
| repaired affine map | `634Z` | `1024Z` |
| cone side plane | `259Z` | `1024Z` |

Thus the factor `1024` per repair is conservative.  The side-plane identity

```
L_F(x)=F(a)H_Q(x)-H_Q(a)F(x)
```

contains the apex and the relevant base edge without division.  Retained
pieces use only old facets and the bisector.  Consequently all maps and
supporting planes after at most `N` repairs have height at most
`2^(10N)(B+4)` as claimed.

The arrangement calculation is also safe.  A plane through three rational
points of coordinate height `Z` can be represented with factor `44Z`, below
the published `64Z`.  Expanding a three-by-three determinant gives
`18A+5<=23A`; Cramer division costs at most `46A`, below `Vtx=64A`.
There are at most `binom(h,3)` arrangement vertices, and averaging at most
that many vertices gives precisely the stated barycentric bound
`K=binom(h,3)(Vtx+2)`.

A reference-face reflection has coefficient height at most `12P`, so
`T=1024K` safely covers every face.  Clearing the 12 variable affine-matrix
entries before multiplying a word of length `r` gives denominator at most
`2^(12rT)` and numerator magnitude at most
`4^(r-1)2^(13rT)`.  Applying the cleared word to a reference vertex yields

```
13rT+4K+2r <= 2^14 M K.
```

Root translation is then covered by `H=2^15 M K`.  This proves rationality
and the uniform coordinate bound for every consistent placement; cycles can
remove reflection words but cannot add new ones.  Finally
`h=O(N2^N)`, `M=O(N^4 2^(4N))`, and
`K=O(N^3 2^(13N)(B+4))`, giving the advertised
`H=O(N^7 2^(17N)(B+4))`.

## Linear chain-height dependency

Root a spanning tree of the facet-adjacency graph.  Every tree step shares
three labels with its parent and introduces at most one new label.  Exactly
`v-4` steps introduce a label.  At each such step, the squared distance
between the new opposite vertex and the parent opposite vertex has exactly
two values

```
a=|p_u-p_w|^2+(h_u-h_w)^2,
b=|p_u-p_w|^2+(h_u+h_w)^2,
```

with `b-a=4h_u h_w>0`.  Its normalized bit reconstructs the new vertex once
the parent is placed.  The `v-4` selected bits therefore injectively encode
every feasible root-aligned placement, even though cycle constraints may
exclude most bit strings.

Each bit is a positive affine function of one complete squared distance.
Coordinatewise contraction can only change it from one to zero.  Hence the
sum of the bits strictly decreases at every noncongruent step.  Between two
fixed endpoints only their differing bits can vary, so every strict chain
has at most

```
r <= v-4 <= m-1
```

steps and at most `2^r` states.  A saturated step is indecomposable among all
three-dimensional configurations: any putative intermediate keeps every
tight tetrahedral edge and therefore belongs to the same finite interval.
Choosing zero-change dual edges first in a spanning forest gives the sharper
`r<=c-1` bound.  I found no missing orientation, cycle, coincident-label, or
nondegeneracy case.

## Finite-frontier handoff

For rational deficit `delta`, the accepted rational producer at
`k=ceil(9/delta)` supplies at most the displayed `N=A_k` labels, coordinate
denominator `256k^3`, coordinate magnitudes below `768k^4`, total weight
denominator `W=4kN`, and a negative hinge exceeding `delta/2`.  The proposed
height `B=ceil(log2(768k^4+1))` covers the coordinates, denominator, radius,
and translated anchor.

After uniform mesh augmentation, an original mass `n_i/W` becomes

```
[(4b+a)n_i v+aW]/[2(2b+a)Wv],  delta=a/b.
```

These positive numerators sum to the stated common denominator, and every
label receives at least `delta/[2(2+delta)V]`.  The augmented endpoint gap
is at least `delta/4` in adverse magnitude.  Telescoping over at most
`M-1` strict steps therefore leaves an indecomposable step with adverse
magnitude at least `delta/[4(M-1)]`.

Every real intermediate state preserves the tight rational tetrahedral
framework, hence is one of finitely many rational reflection choices with
the coordinate bound above.  Enumerating bounded coordinates, masses,
frameworks, and consistent root-aligned states is therefore complete, even
though it is vastly impractical.

The endpoint substitution into the accepted exposed-edge theorem is exact.
At most `6V` coordinate denominators give a common denominator below
`2^(6VH)`, and cleared coordinate magnitudes are below
`2^((6V+1)H)`.  Expanding those exponents recovers

```
J0=145+2 ceil(log2 V)+6 ceil(log2 R0)+(222V+30)H.
```

A noncongruent contraction has a strict source pair of squared length at
least `2^(-12VH)`.  Together with the mass floor this gives the stated high
endpoint exponent.  These facts sign only the outer intervals; the middle
interval remains explicitly unresolved.

## Independent exact computation

`independent_check.py` imports none of the target implementation.  It:

- re-derives every height factor above from scalar height rules;
- checks three unrelated rational rotations and Brehm repairs, including
  involution, apex image, bisector sign, cone-side incidence, and heights;
- exhausts a new eight-label stacked framework with all 16 fold words;
- adds a non-tree tetrahedron and independently finds the four consistent
  cycle-constrained states;
- checks every comparable endpoint pair and every intervening placement in
  both frameworks against the binary rank and chain-height bounds;
- verifies 72 global reflection-word and root-translation inequalities;
- checks 12 exact common-mass denominators, 36 endpoint exponent
  substitutions, and four rational-frontier parameter sets.

The state streams and expected record are hashed.  Ordinary and optimized
executions reproduce `REVIEW_EXPECTED.json` exactly.

## Guarantees, assumptions, and limits

The checker guarantees the pinned bytes and its finite rational calculations:
repair identities, height-factor arithmetic, fold-state enumeration,
complete small posets, mass identities, and endpoint exponents.  It is not a
formalization of the universal geometric statements.

The previously accepted buffered Brehm mesh construction and rational
paired-cubature producer remain dependencies.  The exposed-edge endpoint
theorem is used only in the scope accepted by its independent review.  This
review supplies the missing independent audit of the linear chain theorem;
its universal conclusion still rests on the written injective-encoding
argument rather than exhaustive computation.

No enormous mesh or full bounded-coordinate input class was enumerated, and
no Gaussian integral or middle hinge was computed.  The bounds establish
mathematical finiteness, not computational feasibility.  No new positive
map class, counterexample, Kneser--Poulsen consequence, or historical
priority claim is asserted.
