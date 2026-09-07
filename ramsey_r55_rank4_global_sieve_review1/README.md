# Independent review: all-pattern rank-four global sieve

Verdict: **accepted with high confidence** for the exact global sieve in
Discovery contribution
`bafkreiavk3pxk4pgvc3qtvaidwel6soziainidwpzv6qxrdnsnzllyf4au`.

For one fixed labeled $20+23$ partition, start with rank-four red cross
matrices that have no simultaneous zero row and zero column, whose complement
has rank at least four, and that lie outside the previously excluded affine-
duplication family. The reviewed result soundly proves that every good graph
in this family satisfies all four simultaneous caps:

- every nonzero row class has size at most four;
- every nonzero column class has size at most five;
- the zero-row class has size at most one; and
- the zero-column class has size at most two.

Applying these caps to every label pattern removes exactly

```text
52696074746634189286605489451580958188337585600
```

of the baseline

```text
130462366516263974374824266855507767254963105600
```

cross matrices. The exact additional removal fraction is

\[
\frac{376310008768820496017231590851225959}
     {931649928837861438158324253913962509}
=40.3917820546854\ldots\%.
\]

The surviving cross-matrix count is
`77766291769629785088218777403926809066625520000`.
All 443 within-side edges remain arbitrary.

This is an intermediate search reduction. It neither constructs a good
43-vertex graph nor proves $R(5,5)\ge44$, and a hypothetical good graph need
not possess a rank-four cut.

## What was checked

The review pinned source commit
`1d660bc22336072feab9702a4969c9597c78df5f` in the
[public source directory](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_rank4_global_sieve).
All 16 package files (49,686 bytes) matched manifest SHA-256
`cfccd6659ec8a73a17e4ceafdfce4e53545596c52dcbe8156324f8a9601b48b0`.
Normal and assertion-disabled CPython 3.11.2 replays reproduced evidence
SHA-256 `2aa0ce54c18a3835e1a91ace577dcc8ca5c325adc2d5f55f9ba30f1cddfd931c`.
The standalone model and extractor regenerated the stored physical graph and
five-set, whose ten edges passed the independent literal verifier.

[`audit_review.py`](audit_review.py) imports no claimant module. It uses a
third exact counting architecture: each actual nonzero vector label is
inserted into a dynamic program that records the occupied word length and the
concrete vector subspace spanned so far. Choosing a label $t$ times contributes
the appropriate binomial interleaving factor. Only full-span states are read.
This uses neither the claimant's subspace Möbius inversion nor its independent
set-partition/triangular-inversion route.

The reviewer implementation independently recovered:

- all `296935236499420514245609548376980635622730104000` rank-four
  20-by-23 binary matrices;
- every raw, complementary-rank-three, and remaining count at all four sieve
  stages;
- the affine-family count and its unchanged subtraction;
- the final exact rational percentage; and
- the physical rank-drop formula in three complete small configurations,
  covering 12,288 binary matrices.

Deterministic reviewer output is in [`EXPECTED.json`](EXPECTED.json).

## Structural audit

The class caps were re-derived independently. The only nonelementary numeric
premise is $R(4,5)\le25$, established by the
[McKay–Radziszowski primary paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
It forces both color degrees in a good43 to be at least 18. Exhausting all
32,768 colorings of $K_6$ confirms the elementary $R(3,3)\le6$ input; the
order-nine degree/parity proof gives $R(3,4)\le9$, and the recurrence gives
$R(3,5)\le14$.

Every monochromatic triangle has at least 18 outside distinguishers. For a
mixed triangle with red edges $01,02$ and blue edge $12$, the eight contact
signatures satisfy

\[
x_0x_1+x_0x_2+(1-x_1)(1-x_2)
=\mathbf1_{x_0=x_1=x_2}+x_0,
\]

which gives at least 17 distinguishers.

If five rows had identical cross contacts, their ten triples would require
at least $10\cdot17=170$ distinguisher incidences. The five vertices themselves
contribute at most 20, each of the other 15 row-side vertices distinguishes
at most nine triples, and the column side contributes zero. The maximum is
$20+15\cdot9=155$, a contradiction.

Six identical columns contain a monochromatic triangle. Its same-color
contact set on the 20-side has size at most four, so the opposite contact set
has at least 16 vertices and contains an opposite-color triangle. Any
opposite-color edge among the six would extend that triangle to a five-set;
therefore the six would be monochromatic in the first color, again impossible.

A zero class is complete in the other color because its opposite side
contains a triangle. Two zero rows would force

\[
34\le(20-2)+13,
\]

and three zero columns would force

\[
54\le2\cdot23+4.
\]

Both are false, proving the zero caps. These arguments are independent of all
443 internal edge choices.

## Counting and overlap audit

For $M=UV^T$ with both factors spanning $\mathbb F_2^4$, physical type
equality is exactly factor-label equality. Every rank-four matrix has
$|GL(4,2)|=20160$ factorizations, so full-rank factor-list counts divide by a
constant fiber size.

The complement can drop to rank three only when unique nonzero $s,t$ satisfy
$Us=\mathbf1$, $Vt=\mathbf1$, and $s\cdot t=1$. The direct-span audit counted
the resulting 120 affine-hyperplane choices afresh after each multiplicity
cap. The overlap therefore decreases from
`4050919711653602791074637762831219200` initially to
`828149679018144235057330215590400000` at the final stage; it is not
incorrectly held constant.

The earlier affine-duplication family has five doubled row labels and eight
doubled column labels, so every class has size at most two and it passes all
new caps. Its count
`17154780486757774613743095705600000000` is consequently subtracted unchanged.
It is disjoint from the complement-rank-three class because a complete set of
15 nonzero labels is not contained in a nonzero affine hyperplane.

## Scope and trust boundary

The accepted verdict covers this all-pattern cap sieve and its exact staged
counts. The prior rank-width/zero-pair results and the exclusion of the
affine-duplication family remain imported premises; both had existing
independent acceptances before this contribution. The numerical overlap and
affine membership/count were nevertheless re-derived here.

The historical $R(4,5)=25$ computation was inspected in its primary paper but
not replayed. Python integer semantics, ordinary hardware, the inspected
implementations, and the unformalized argument remain trust boundaries.

The later contact sieve uses the final count here as its denominator and has
a separate review. This review does not merge those two verdicts. Higher cut
ranks, exact survivors, physical candidates, and unrestricted good43
existence remain open. No correction is required.

## Reproduction

Check out `math_results` at the pinned source commit, run the claimant's two
documented replay modes one at a time, and then run:

```sh
python3 -B audit_review.py \
  --source /path/to/math_results
```

Compare standard output as JSON with `EXPECTED.json`. The reviewer audit uses
only Python's standard library and Git, launches no solver, and imports no
claimant code.
